"""Exercise local tooling in isolated repositories, including Git hook invocation."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]


class LocalToolingTests(unittest.TestCase):
  def setUp(self):
    self.workspace = tempfile.TemporaryDirectory()
    self.addCleanup(self.workspace.cleanup)
    self.repo = Path(self.workspace.name) / 'repository with spaces'
    self.repo.mkdir()
    for name in ['.githooks', 'scripts/dev']:
      source = ROOT / name
      target = self.repo / name
      target.mkdir(parents=True, exist_ok=True)
      for path in source.iterdir():
        if path.is_file():
          shutil.copy2(path, target / path.name)
    self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1',
                    GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT='0')
    self.git('init', '-q')
    self.git('config', 'user.name', 'Tooling Test')
    self.git('config', 'user.email', 'test@example.invalid')

  def run_command(self, *args, cwd=None):
    return subprocess.run(args, cwd=cwd or self.repo, env=self.env,
                          capture_output=True, text=True)

  def git(self, *args):
    result = self.run_command('git', *args)
    self.assertEqual(result.returncode, 0, result.stderr)
    return result.stdout.strip()

  def setup_hooks(self):
    return self.run_command('bash', str(self.repo / 'scripts/dev/setup.sh'),
                            cwd=self.workspace.name)

  def test_setup_is_repeatable_from_another_directory_and_does_not_create_env(self):
    (self.repo / '.env.example').write_text('EXAMPLE=placeholder\n')
    for _ in range(2):
      result = self.setup_hooks()
      self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(self.git('config', '--local', '--get', 'core.hooksPath'), '.githooks')
    self.assertFalse((self.repo / '.env').exists())

  def test_existing_hook_configuration_is_preserved(self):
    self.git('config', 'core.hooksPath', 'existing-hooks')
    self.assertNotEqual(self.setup_hooks().returncode, 0)
    self.assertEqual(self.git('config', '--get', 'core.hooksPath'), 'existing-hooks')

  def test_inherited_hook_configuration_is_preserved(self):
    config = Path(self.workspace.name) / 'global-gitconfig'
    config.write_text('[core]\n  hooksPath = shared-hooks\n')
    self.env['GIT_CONFIG_GLOBAL'] = str(config)
    self.assertNotEqual(self.setup_hooks().returncode, 0)
    self.assertEqual(self.git('config', '--get', 'core.hooksPath'), 'shared-hooks')

  def test_missing_hook_does_not_configure_git(self):
    (self.repo / '.githooks/commit-msg').unlink()
    self.assertNotEqual(self.setup_hooks().returncode, 0)
    self.assertEqual(self.run_command('git', 'config', '--get', 'core.hooksPath').returncode, 1)

  def test_git_accepts_conventional_subjects(self):
    self.assertEqual(self.setup_hooks().returncode, 0)
    types = 'feat fix docs style refactor perf test build ci chore revert'.split()
    for subject in [f'{kind}: explain change' for kind in types] + [
        'feat(api)!: change interface', 'docs(adr): record decision']:
      with self.subTest(subject=subject):
        self.git('commit', '--allow-empty', '-q', '-m', subject)

  def test_git_rejects_invalid_subjects(self):
    self.assertEqual(self.setup_hooks().returncode, 0)
    for subject in ['wip', 'unknown: change', 'docs:', 'docs:   ',
                    'docs(): change', 'docs(bad scope): change']:
      with self.subTest(subject=subject):
        result = self.run_command('git', 'commit', '--allow-empty', '-q', '-m', subject)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Commit rejected', result.stderr)


if __name__ == '__main__':
  unittest.main()
