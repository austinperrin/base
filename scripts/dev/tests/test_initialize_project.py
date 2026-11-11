"""Exercise one-time project setup in disposable Git repositories."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[3]


class ProjectInitializationTests(unittest.TestCase):
  def setUp(self):
    self.directory = tempfile.TemporaryDirectory(prefix='project-initialization-test-')
    self.addCleanup(self.directory.cleanup)
    self.root = Path(self.directory.name) / 'project'
    self.root.mkdir()
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=SOURCE)
    for raw_name in tracked.split(b'\0'):
      if not raw_name:
        continue
      name = raw_name.decode('utf-8')
      source = SOURCE / name
      if source.is_file():
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for name in ('scripts/dev/initialize-project.py',
                 'scripts/dev/tests/test_initialize_project.py'):
      target = self.root / name
      target.parent.mkdir(parents=True, exist_ok=True)
      shutil.copy2(SOURCE / name, target)
    self.git('init', '-q', '-b', 'main')
    self.git('config', 'user.name', 'Fixture Maintainer')
    self.git('config', 'user.email', 'fixture@example.test')
    self.git('add', '.')
    self.git('commit', '-qm', 'test: create project fixture')
    self.git('remote', 'add', 'origin', 'https://github.com/example/project.git')

  def git(self, *arguments):
    return subprocess.run(['git', *arguments], cwd=self.root,
                          capture_output=True, text=True, check=True)

  def helper(self, *arguments, check=True):
    return subprocess.run(
      [sys.executable, str(self.root / 'scripts/dev/initialize-project.py'), *arguments],
      cwd=self.root, capture_output=True, text=True, check=check)

  def configure(self, *arguments, check=True):
    return self.helper('configure', '--repository', 'example/project',
                       '--security-email', 'security@example.test',
                       '--conduct-email', 'conduct@example.test',
                       *arguments, check=check)

  def prepare_finish(self):
    self.configure('--apply')
    (self.root / 'README.md').write_text('# Example Project\n\nProject overview.\n')
    (self.root / '.github/CODEOWNERS').write_text(
      '# Project owners\n* @example\n/.github/CODEOWNERS @example\n')

  def test_preview_does_not_modify_source_files(self):
    result = self.configure()
    self.assertIn('Would update: .github/ISSUE_TEMPLATE/config.yml', result.stdout)
    self.assertEqual(self.git('status', '--porcelain').stdout, '')

  def test_apply_replaces_values_and_finish_removes_only_source_files(self):
    self.prepare_finish()
    self.assertIn('https://github.com/example/project/security/policy',
                  (self.root / '.github/ISSUE_TEMPLATE/config.yml').read_text())
    self.assertIn('security@example.test',
                  (self.root / 'SECURITY.md').read_text())
    self.assertIn('conduct@example.test',
                  (self.root / 'CODE_OF_CONDUCT.md').read_text())
    preview = self.helper('finish')
    self.assertIn('Would remove: docs/architecture/phase-6-verification.md', preview.stdout)
    self.assertTrue((self.root / 'docs/architecture/phase-6-verification.md').exists())
    self.helper('finish', '--apply')
    for name in ('docs/architecture/phase-6-verification.md',
                 'docs/runbooks/initialize-repository.md',
                 'scripts/dev/initialize-project.py',
                 'scripts/dev/tests/test_initialize_project.py'):
      self.assertFalse((self.root / name).exists())
    self.assertTrue((self.root / 'docs/adr/template.md').exists())
    self.assertTrue((self.root / 'docs/runbooks/template.md').exists())
    self.assertIn('https://github.com/austinperrin/base/blob/main/docs/architecture/phase-6-verification.md',
                  (self.root / 'docs/roadmap/milestone-0-repository-scaffolding.md').read_text())

  def test_modified_removal_candidate_blocks_finish(self):
    self.prepare_finish()
    record = self.root / 'docs/architecture/phase-6-verification.md'
    record.write_text(record.read_text() + '\nProject note.\n')
    result = self.helper('finish', '--apply', check=False)
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('modified', result.stderr)
    self.assertTrue(record.exists())

  def test_source_remote_blocks_changes(self):
    self.git('remote', 'set-url', 'origin', 'https://github.com/austinperrin/base.git')
    result = self.configure('--apply', check=False)
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('foundation repository', result.stderr)
    self.assertEqual(self.git('status', '--porcelain').stdout, '')

  def test_example_owners_block_finish(self):
    self.configure('--apply')
    (self.root / 'README.md').write_text('# Example Project\n')
    result = self.helper('finish', '--apply', check=False)
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('CODEOWNERS', result.stderr)
    self.assertTrue((self.root / 'docs/architecture/phase-6-verification.md').exists())

  def test_wrong_destination_link_blocks_finish(self):
    self.prepare_finish()
    chooser = self.root / '.github/ISSUE_TEMPLATE/config.yml'
    chooser.write_text(chooser.read_text().replace('example/project', 'example/other'))
    result = self.helper('finish', '--apply', check=False)
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('Confirm the new repository links', result.stderr)
    self.assertTrue((self.root / 'docs/architecture/phase-6-verification.md').exists())

  def test_failed_link_check_restores_all_cleanup_candidates(self):
    self.prepare_finish()
    (self.root / 'README.md').write_text('# Example Project\n\n[Missing](missing.md)\n')
    result = self.helper('finish', '--apply', check=False)
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('check-links.sh failed', result.stderr)
    self.assertTrue((self.root / 'docs/architecture/phase-6-verification.md').exists())
    self.assertTrue((self.root / 'scripts/dev/initialize-project.py').exists())
    self.assertIn('initialize-repository.md',
                  (self.root / 'docs/runbooks/README.md').read_text())

  def test_unexpected_incoming_link_blocks_finish(self):
    self.prepare_finish()
    extra = self.root / 'docs' / 'project-note.md'
    extra.write_text('# Project Note\n\n[Setup](runbooks/initialize-repository.md)\n')
    result = self.helper('finish', '--apply', check=False)
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('incoming initialization-runbook link', result.stderr)
    self.assertTrue((self.root / 'docs/runbooks/initialize-repository.md').exists())


if __name__ == '__main__':
  unittest.main()
