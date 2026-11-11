"""Exercise release gates in real temporary Git repositories with a fake gh."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
JOBS = ['Repository checks (ubuntu-24.04)', 'Repository checks (macos-15)',
        'External checks (Linux)']


class ReleaseTests(unittest.TestCase):
  def setUp(self):
    self.workspace = tempfile.TemporaryDirectory(prefix='repository-release-')
    self.addCleanup(self.workspace.cleanup)
    self.parent = Path(self.workspace.name).resolve()
    self.repo = self.parent / 'project with spaces'
    self.remote = self.parent / 'origin.git'
    self.bin = self.parent / 'bin'
    self.bin.mkdir()
    self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                    GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1',
                    PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                    GH_REPO='wrong/repository', RELEASE_TEST_STATE=str(self.parent / 'state.json'),
                    RELEASE_TEST_LOG=str(self.parent / 'calls.log'))
    subprocess.run(['git', 'init', '-q', '--bare', str(self.remote)],
                   env=self.env, check=True, capture_output=True)
    self.repo.mkdir()
    self.git('init', '-q', '-b', 'main')
    self.git('config', 'user.name', 'Release Tests')
    self.git('config', 'user.email', 'tests@example.invalid')
    shutil.copytree(ROOT / 'scripts/ops', self.repo / 'scripts/ops',
                    ignore=shutil.ignore_patterns('tests', '__pycache__'))
    suite = self.repo / 'scripts/ci/test.sh'
    suite.parent.mkdir(parents=True)
    suite.write_text('''#!/usr/bin/env bash
set -euo pipefail
echo suite >> "$RELEASE_TEST_LOG"
if [[ "${RELEASE_TEST_DIRTY:-0}" == 1 ]]; then touch unexpected.txt; fi
exit "${RELEASE_TEST_EXIT:-0}"
''')
    suite.chmod(0o755)
    self.git('add', '.')
    self.git('commit', '-qm', 'chore: initialize release fixture')
    self.sha = self.git('rev-parse', 'HEAD')
    self.git('remote', 'add', 'origin', 'https://github.com/example/project.git')
    self.git('config', f'url.{self.remote}.insteadOf', 'https://github.com/example/project.git')
    self.git('push', '-q', 'origin', 'main')
    # URL rewriting is used only by Git; the helper identifies the original URL.
    # Keep the local bare origin available while presenting the canonical target.
    original_git = shutil.which('git')
    git_proxy = self.bin / 'git'
    git_proxy.write_text(f'''#!/usr/bin/env python3
import os, sys
if sys.argv[1:4] == ['remote', 'get-url', 'origin']:
  print('https://github.com/example/project.git')
elif sys.argv[1:5] == ['remote', 'get-url', '--push', 'origin']:
  print(os.environ.get('RELEASE_TEST_PUSH_URL', 'https://github.com/example/project.git'))
else:
  os.execv({original_git!r}, [{original_git!r}, *sys.argv[1:]])
''')
    git_proxy.chmod(0o755)
    gh = self.bin / 'gh'
    gh.write_text('''#!/usr/bin/env python3
import json, os, sys
with open(os.environ['RELEASE_TEST_LOG'], 'a') as output:
  output.write(json.dumps(sys.argv[1:]) + '\\n')
if os.environ.get('RELEASE_TEST_GH_FAILURE'):
  sys.exit(1)
with open(os.environ['RELEASE_TEST_STATE']) as source:
  state = json.load(source)
print(json.dumps(state['runs'] if sys.argv[1:3] == ['run', 'list'] else state['detail']))
''')
    gh.chmod(0o755)
    self.state = {
      'runs': [{'databaseId': 100, 'headSha': self.sha, 'status': 'completed',
                'conclusion': 'success'}],
      'detail': {'headSha': self.sha, 'headBranch': 'main', 'event': 'push',
                 'status': 'completed', 'conclusion': 'success',
                 'jobs': [{'name': name, 'status': 'completed', 'conclusion': 'success'}
                          for name in JOBS]},
    }

  def git(self, *args):
    result = subprocess.run(['git', *args], cwd=self.repo, env=self.env,
                            text=True, capture_output=True, check=True)
    return result.stdout.strip()

  def run_verification(self, *args):
    (self.parent / 'state.json').write_text(json.dumps(self.state))
    return subprocess.run([str(self.repo / 'scripts/ops/verify-release.sh'), *args],
                          cwd=self.parent, env=self.env, text=True,
                          capture_output=True, timeout=20)

  def test_success_from_other_directory_preserves_repository_and_targets_origin(self):
    before = self.git('show-ref')
    result = self.run_verification('v1.2.3')
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn('No tag or release was created', result.stdout)
    self.assertEqual(self.git('show-ref'), before)
    self.assertEqual(self.git('status', '--porcelain'), '')
    calls = (self.parent / 'calls.log').read_text()
    self.assertIn('"--repo", "example/project"', calls)
    self.assertNotIn('wrong/repository', calls)
    self.assertIn('"--workflow", "repo-lint.yml"', calls)
    self.assertIn('"--event", "push"', calls)

  def test_invalid_arguments_and_tags_fail_without_running_suite(self):
    for args in [(), ('release-42', 'extra'), ('--help',), ('',), ('release name',),
                 ('release..42',), ('release@{1}',), ('release*',), ('release.lock',),
                 ('release/',), ('release//42',), ('release^',)]:
      with self.subTest(args=args):
        self.assertNotEqual(self.run_verification(*args).returncode, 0)
    self.assertFalse((self.parent / 'calls.log').exists())

  def test_valid_tag_formats_do_not_select_a_versioning_policy(self):
    for tag in ['v2.4.1', '2026.11.09', 'release-42', '3.7', 'snapshot-a1b2c3d',
                'v1.0.0-rc.1', 'v1.0.0+build.42', 'releases/2026.11']:
      with self.subTest(tag=tag):
        result = self.run_verification(tag)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git('tag', '--list'), '')

  def test_untracked_and_tracked_changes_are_rejected(self):
    for name in ['untracked.txt', 'scripts/ci/test.sh']:
      path = self.repo / name
      original = path.read_bytes() if path.exists() else None
      path.write_text('changed\n')
      self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)
      if original is None:
        path.unlink()
      else:
        path.write_bytes(original)

  def test_topic_and_detached_heads_are_rejected(self):
    self.git('switch', '-qc', 'topic')
    self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)
    self.git('checkout', '-q', '--detach')
    self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)

  def test_existing_local_and_remote_tags_are_rejected(self):
    self.git('tag', 'v1.0.0')
    self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)
    self.git('push', '-q', 'origin', 'refs/tags/v1.0.0')
    self.git('tag', '-d', 'v1.0.0')
    result = self.run_verification('v1.0.0')
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('exists on origin', result.stderr)

  def test_remote_main_must_equal_local_head(self):
    self.git('commit', '--allow-empty', '-qm', 'chore: advance local main')
    result = self.run_verification('v1.0.0')
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('HEAD must match main', result.stderr)

  def test_push_destination_must_match_fetch_repository(self):
    self.env['RELEASE_TEST_PUSH_URL'] = 'git@github.com:other/project.git'
    self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)

  def test_failed_suite_and_suite_mutation_stop_release(self):
    self.env['RELEASE_TEST_EXIT'] = '1'
    self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)
    self.env['RELEASE_TEST_EXIT'] = '0'
    self.env['RELEASE_TEST_DIRTY'] = '1'
    self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)

  def test_missing_or_malformed_ci_results_and_cli_failure_are_rejected(self):
    for runs in [[], {}, [{'databaseId': '100'}], [{'databaseId': 100, 'headSha': 'wrong'}]]:
      with self.subTest(runs=runs):
        self.state['runs'] = runs
        self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)
    self.env['RELEASE_TEST_GH_FAILURE'] = '1'
    self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)

  def test_newer_failure_or_pending_run_cannot_be_masked_by_older_success(self):
    original = copy.deepcopy(self.state['runs'][0])
    for status, conclusion in [('in_progress', ''), ('completed', 'failure'),
                               ('completed', 'cancelled')]:
      with self.subTest(status=status, conclusion=conclusion):
        newer = dict(original, databaseId=101, status=status, conclusion=conclusion)
        self.state['runs'] = [original, newer]
        self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)

  def test_wrong_commit_branch_event_or_conclusion_is_rejected(self):
    original = copy.deepcopy(self.state['detail'])
    for field, value in [('headSha', 'wrong'), ('headBranch', 'topic'),
                         ('event', 'pull_request'), ('conclusion', 'failure')]:
      with self.subTest(field=field):
        self.state['detail'] = dict(original, **{field: value})
        self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)

  def test_missing_skipped_failed_or_duplicate_required_jobs_are_rejected(self):
    original = copy.deepcopy(self.state['detail']['jobs'])
    variants = [original[:-1], original + [original[0]], None,
                [dict(job, conclusion='skipped') for job in original],
                [dict(job, conclusion='failure') for job in original]]
    for jobs in variants:
      with self.subTest(jobs=jobs):
        self.state['detail']['jobs'] = jobs
        self.assertNotEqual(self.run_verification('v1.0.0').returncode, 0)


if __name__ == '__main__':
  unittest.main()
