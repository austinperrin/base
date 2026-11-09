"""Verify cleanup boundaries and preview behavior in disposable repositories."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]


class CleanupTests(unittest.TestCase):
  def setUp(self):
    self.workspace = tempfile.TemporaryDirectory()
    self.addCleanup(self.workspace.cleanup)
    self.repo = Path(self.workspace.name) / 'project with spaces'
    self.repo.mkdir()
    self.script = self.repo / 'scripts/dev/clean.sh'
    self.script.parent.mkdir(parents=True)
    shutil.copy2(ROOT / 'scripts/dev/clean.sh', self.script)
    self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
    self.git('init', '-q')
    self.write('.gitignore', 'tmp/\n.tmp/\ntemp/\nscratch/\n.cache/\n.env\nbuild/\n*.log\n')

  def write(self, name, content='Keep or clean by policy.\n'):
    path = self.repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path

  def git(self, *args):
    result = subprocess.run(['git', *args], cwd=self.repo, env=self.env,
                            capture_output=True, text=True)
    self.assertEqual(result.returncode, 0, result.stderr)
    return result

  def clean(self, *args):
    return subprocess.run(['bash', str(self.script), *args], cwd=self.workspace.name,
                          env=self.env, capture_output=True, text=True)

  def test_preview_is_default_and_matches_explicit_dry_run(self):
    path = self.write('.tmp/sub dir/generated.txt')
    default = self.clean()
    explicit = self.clean('--dry-run')
    self.assertEqual(default.returncode, 0, default.stderr)
    self.assertEqual(default.stdout, explicit.stdout)
    self.assertIn('.tmp/sub dir/generated.txt', default.stdout)
    self.assertTrue(path.exists())

  def test_apply_removes_only_eligible_files(self):
    removable = [self.write(f'{directory}/generated.txt')
                 for directory in ['tmp', '.tmp', 'temp', 'scratch', '.cache']]
    tracked = self.write('tmp/tracked.txt')
    self.git('add', '-f', 'tmp/tracked.txt')
    with (self.repo / '.gitignore').open('a') as rules:
      rules.write('!tmp/\ntmp/*\n!tmp/source.txt\n')
    preserved = [tracked, self.write('tmp/source.txt'), self.write('src/new.py'),
                 self.write('.env'), self.write('build/output.txt'), self.write('root.log'),
                 self.write('nested/tmp/file.txt')]
    result = self.clean('--apply')
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertTrue(all(not path.exists() for path in removable))
    self.assertTrue(all(path.exists() for path in preserved))
    self.assertTrue((self.repo / 'tmp').is_dir())

  def test_symlinks_and_their_targets_are_preserved(self):
    external = Path(self.workspace.name) / 'external'
    external.mkdir()
    target = external / 'important.txt'
    target.write_text('Keep me.\n')
    (self.repo / 'tmp').mkdir()
    (self.repo / 'tmp/file-link').symlink_to(target)
    (self.repo / 'tmp/directory-link').symlink_to(external, target_is_directory=True)
    (self.repo / '.tmp').symlink_to(external, target_is_directory=True)
    result = self.clean('--apply')
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertTrue(target.exists())
    self.assertTrue((self.repo / 'tmp/file-link').is_symlink())
    self.assertTrue((self.repo / 'tmp/directory-link').is_symlink())
    self.assertTrue((self.repo / '.tmp').is_symlink())

  def test_nested_repositories_and_worktree_markers_are_preserved(self):
    nested = self.repo / 'tmp/nested'
    nested.mkdir(parents=True)
    self.git('init', '-q', str(nested))
    files = [self.write('tmp/nested/valuable.txt'),
             self.write('scratch/worktree/.git', 'gitdir: /not-used\n'),
             self.write('scratch/worktree/valuable.txt')]
    result = self.clean('--apply')
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertTrue(all(path.exists() for path in files))
    self.assertTrue((nested / '.git').is_dir())

  def test_unusual_names_are_handled_as_single_paths(self):
    path = self.write('tmp/-odd\nname.txt')
    result = self.clean('--apply')
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("'tmp/-odd\\nname.txt'", result.stdout)
    self.assertFalse(path.exists())

  def test_conflicting_or_unknown_arguments_do_not_delete_files(self):
    path = self.write('tmp/keep.txt')
    for args in [('--apply', '--dry-run'), ('--unknown',)]:
      with self.subTest(args=args):
        self.assertNotEqual(self.clean(*args).returncode, 0)
        self.assertTrue(path.exists())

  def test_missing_repository_does_not_delete_files(self):
    shutil.rmtree(self.repo / '.git')
    path = self.write('tmp/keep.txt')
    self.assertNotEqual(self.clean('--apply').returncode, 0)
    self.assertTrue(path.exists())


if __name__ == '__main__':
  unittest.main()
