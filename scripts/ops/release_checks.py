"""Verify the release candidate against local state and exact-commit push CI."""
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit


REQUIRED_JOBS = {
  'Repository checks (ubuntu-24.04)',
  'Repository checks (macos-15)',
  'External checks (Linux)',
}


def command(root, *args):
  result = subprocess.run(args, cwd=root, text=True, capture_output=True)
  if result.returncode:
    raise ValueError(f'{args[0]} {args[1]} failed; check prerequisites, authentication, and access.')
  return result.stdout.strip()


def github_repository(url):
  """Derive an explicit API target; do not rely on GH_REPO or CLI defaults."""
  if url.startswith('git@github.com:'):
    path = url.removeprefix('git@github.com:')
  else:
    parsed = urlsplit(url)
    if (parsed.hostname != 'github.com' or parsed.scheme not in {'https', 'ssh'}
        or parsed.query or parsed.fragment):
      raise ValueError('Release verification requires a github.com origin.')
    path = parsed.path.lstrip('/')
  path = path.removesuffix('.git')
  if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', path):
    raise ValueError('Origin must identify one GitHub repository.')
  return path


def local_state(root, tag):
  if Path(command(root, 'git', 'rev-parse', '--show-toplevel')).resolve() != root.resolve():
    raise ValueError('The helper must be located in the repository root.')
  if command(root, 'git', 'status', '--porcelain', '--untracked-files=all'):
    raise ValueError('Commit or preserve tracked and untracked changes before verification.')
  if command(root, 'git', 'branch', '--show-current') != 'main':
    raise ValueError('Release verification must run on main.')
  if command(root, 'git', 'tag', '--list', tag):
    raise ValueError('The proposed tag already exists locally.')
  return command(root, 'git', 'rev-parse', 'HEAD')


def remote_state(root, tag, sha):
  repository = github_repository(command(root, 'git', 'remote', 'get-url', 'origin'))
  push_repository = github_repository(command(root, 'git', 'remote', 'get-url', '--push', 'origin'))
  if repository.lower() != push_repository.lower():
    raise ValueError('Origin fetch and push URLs must identify the same repository.')
  output = command(root, 'git', 'ls-remote', 'origin', 'refs/heads/main', f'refs/tags/{tag}')
  refs = {}
  for line in output.splitlines():
    commit, ref = line.split()
    refs[ref] = commit
  if refs.get('refs/heads/main') != sha:
    raise ValueError('HEAD must match main on origin; a local tracking ref is insufficient.')
  if f'refs/tags/{tag}' in refs:
    raise ValueError('The proposed tag already exists on origin.')
  return repository


def remote_ci(root, repository, sha):
  runs = json.loads(command(
    root, 'gh', 'run', 'list', '--repo', repository, '--workflow', 'repo-lint.yml',
    '--branch', 'main', '--commit', sha, '--event', 'push', '--limit', '100',
    '--json', 'databaseId,headSha,status,conclusion'))
  if (not isinstance(runs, list) or not runs
      or any(not isinstance(run, dict) or type(run.get('databaseId')) is not int
             or run.get('headSha') != sha for run in runs)):
    raise ValueError('No valid exact-commit push workflow results are available.')
  # A newer pending or failed run must not be masked by an older success.
  latest = max(runs, key=lambda run: run['databaseId'])
  if latest.get('status') != 'completed' or latest.get('conclusion') != 'success':
    raise ValueError('The latest Repository Checks push run must have completed successfully.')
  detail = json.loads(command(
    root, 'gh', 'run', 'view', str(latest['databaseId']), '--repo', repository,
    '--json', 'headSha,headBranch,event,status,conclusion,jobs'))
  if (not isinstance(detail, dict) or detail.get('headSha') != sha
      or detail.get('headBranch') != 'main' or detail.get('event') != 'push'
      or detail.get('status') != 'completed' or detail.get('conclusion') != 'success'):
    raise ValueError('The workflow details do not confirm successful push CI for this main commit.')
  jobs = detail.get('jobs')
  if not isinstance(jobs, list) or any(not isinstance(job, dict) for job in jobs):
    raise ValueError('Workflow job results are unavailable.')
  for name in REQUIRED_JOBS:
    matching = [job for job in jobs if job.get('name') == name]
    if (len(matching) != 1 or matching[0].get('status') != 'completed'
        or matching[0].get('conclusion') != 'success'):
      raise ValueError(f'Required release job did not succeed: {name}.')


def verify(root, tag):
  if not tag or tag.startswith('-'):
    raise ValueError('Supply a nonempty Git tag name without a leading dash.')
  checked = subprocess.run(['git', 'check-ref-format', f'refs/tags/{tag}'],
                           cwd=root, capture_output=True)
  if checked.returncode:
    raise ValueError('The proposed tag is not a valid Git tag name.')
  sha = local_state(root, tag)
  repository = remote_state(root, tag, sha)
  result = subprocess.run([str(root / 'scripts/ci/test.sh')], cwd=root)
  if result.returncode:
    raise ValueError('The local repository suite failed.')
  if local_state(root, tag) != sha or remote_state(root, tag, sha) != repository:
    raise ValueError('Repository state changed during verification; start again.')
  remote_ci(root, repository, sha)
  print(f'Release readiness verified for {tag} at {sha}. No tag or release was created.')


def main():
  if len(sys.argv) != 2:
    sys.exit('Usage: ./scripts/ops/verify-release.sh <tag-name>')
  try:
    verify(Path(__file__).resolve().parents[2], sys.argv[1])
  except (ValueError, OSError) as error:
    sys.exit(f'Release verification failed: {error}')


if __name__ == '__main__':
  main()
