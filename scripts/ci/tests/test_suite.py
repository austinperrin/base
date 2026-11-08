"""Exercise suite orchestration with real checks and isolated test fixtures."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]


class SuiteTests(unittest.TestCase):
  def setUp(self):
    self.workspace = tempfile.TemporaryDirectory(prefix='base-suite-')
    self.addCleanup(self.workspace.cleanup)
    self.root = Path(self.workspace.name).resolve() / 'project with spaces'
    self.root.mkdir()
    self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1',
                    GIT_CONFIG_GLOBAL=os.devnull, PYTHONDONTWRITEBYTECODE='1')
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).split(b'\0')
    for raw in names:
      if not raw:
        continue
      name = os.fsdecode(raw)
      if 'tests' in Path(name).parts:
        continue
      target = self.root / name
      target.parent.mkdir(parents=True, exist_ok=True)
      shutil.copy2(ROOT / name, target)
    for script in (ROOT / 'scripts/ci').glob('*.sh'):
      shutil.copy2(script, self.root / 'scripts/ci' / script.name)
    subprocess.run(['git', 'init', '-q'], cwd=self.root, env=self.env, check=True,
                   capture_output=True)
    for domain in ['ci', 'dev']:
      folder = self.root / 'scripts' / domain / 'tests'
      folder.mkdir(parents=True)
      (folder / 'test_fixture.py').write_text(
        'import unittest\n'
        'class Fixture(unittest.TestCase):\n'
        f'  def test_{domain}_fixture(self):\n'
        '    self.assertTrue(True)\n')

  def run_suite(self, *args):
    return subprocess.run(['bash', str(self.root / 'scripts/ci/test.sh'), *args],
                          cwd=self.workspace.name, env=self.env,
                          capture_output=True, text=True, timeout=30)

  def snapshot(self):
    return {path.relative_to(self.root): (path.read_bytes(), path.stat().st_mode)
            for path in self.root.rglob('*') if path.is_file()
            and '.git' not in path.relative_to(self.root).parts}

  def test_suite_runs_both_test_groups_from_another_directory_without_repairs(self):
    before = self.snapshot()
    result = self.run_suite()
    self.assertEqual(result.returncode, 0, result.stderr)
    for label in ['Links checks passed.', 'Docs checks passed.',
                  'Secrets checks passed.', 'Repository checks passed.']:
      self.assertIn(label, result.stdout)
    self.assertIn('test_ci_fixture', result.stderr)
    self.assertIn('test_dev_fixture', result.stderr)
    self.assertEqual(before, self.snapshot())

  def test_nonexecutable_script_is_not_repaired(self):
    path = self.root / 'scripts/ci/check-links.sh'
    path.chmod(0o644)
    result = self.run_suite()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('must be an executable regular file', result.stderr)
    self.assertEqual(path.stat().st_mode & 0o111, 0)
    self.assertNotIn('suite passed', result.stdout)

  def test_bash_syntax_failure_stops_suite(self):
    (self.root / 'scripts/dev/setup.sh').write_text('#!/usr/bin/env bash\nif then\n')
    result = self.run_suite()
    self.assertNotEqual(result.returncode, 0)
    self.assertNotIn('Links checks passed.', result.stdout)
    self.assertNotIn('suite passed', result.stdout)

  def test_broken_link_stops_before_regression_tests(self):
    with (self.root / 'README.md').open('a') as output:
      output.write('\n[Missing](absent.md)\n')
    result = self.run_suite()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('absent.md', result.stderr)
    self.assertNotIn('test_ci_fixture', result.stderr)
    self.assertNotIn('suite passed', result.stdout)

  def test_failures_in_either_test_group_fail_suite(self):
    for domain in ['dev', 'ci']:
      with self.subTest(domain=domain):
        path = self.root / 'scripts' / domain / 'tests/test_fixture.py'
        original = path.read_text()
        path.write_text(original.replace('self.assertTrue(True)', 'self.fail("expected fixture failure")'))
        result = self.run_suite()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('expected fixture failure', result.stderr)
        self.assertNotIn('suite passed', result.stdout)
        path.write_text(original)

  def test_unknown_arguments_fail_without_checks(self):
    result = self.run_suite('--unknown')
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('Usage:', result.stderr)
    self.assertNotIn('Links checks passed.', result.stdout)


if __name__ == '__main__':
  unittest.main()
