"""Test ADR generation against isolated copies of the current template."""
from datetime import date
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]


class AdrGeneratorTests(unittest.TestCase):
  def setUp(self):
    self.workspace = tempfile.TemporaryDirectory()
    self.addCleanup(self.workspace.cleanup)
    self.repo = Path(self.workspace.name) / 'project with spaces'
    self.adrs = self.repo / 'docs/adr'
    self.adrs.mkdir(parents=True)
    self.script = self.repo / 'scripts/dev/new-adr.sh'
    self.script.parent.mkdir(parents=True)
    shutil.copy2(ROOT / 'scripts/dev/new-adr.sh', self.script)
    shutil.copy2(ROOT / 'docs/adr/template.md', self.adrs / 'template.md')
    (self.adrs / 'README.md').write_text('Index must remain unchanged.\n')

  def generate(self, *args):
    return subprocess.run(['bash', str(self.script), *args], cwd=self.workspace.name,
                          capture_output=True, text=True)

  def test_numbering_uses_highest_id_and_preserves_existing_files(self):
    existing = self.adrs / '0007-existing.md'
    existing.write_text('Existing decision.\n')
    result = self.generate('Choose storage')
    self.assertEqual(result.returncode, 0, result.stderr)
    content = (self.adrs / '0008-choose-storage.md').read_text()
    self.assertIn('# ADR-0008: Choose storage\n', content)
    self.assertIn('> ADR-0008\n', content)
    self.assertIn('* **Status**: Proposed', content)
    self.assertIn(date.today().isoformat(), content)
    self.assertIn('[Authors]', content)
    self.assertEqual(existing.read_text(), 'Existing decision.\n')
    self.assertEqual((self.adrs / 'README.md').read_text(), 'Index must remain unchanged.\n')
    self.assertFalse((self.adrs / '.new-adr.lock').exists())
    self.assertEqual(list(self.adrs.glob('.adr-*')), [])

  def test_title_is_literal(self):
    title = 'Use [YYYY-MM-DD] and ADR-XXXX & `storage`'
    result = self.generate(title)
    self.assertEqual(result.returncode, 0, result.stderr)
    generated = list(self.adrs.glob('0001-*.md'))
    self.assertEqual(len(generated), 1)
    self.assertEqual(generated[0].read_text().splitlines()[0], f'# ADR-0001: {title}')

  def test_invalid_titles_leave_no_output(self):
    before = sorted(path.name for path in self.adrs.iterdir())
    for args in [(), ('',), ('   ',), ('!!!',), ('first\nsecond',), ('first\tsecond',), ('a', 'b')]:
      with self.subTest(args=args):
        self.assertNotEqual(self.generate(*args).returncode, 0)
        self.assertEqual(sorted(path.name for path in self.adrs.iterdir()), before)

  def test_exhausted_numbering_preserves_records_and_removes_lock(self):
    (self.adrs / '9999-last.md').write_text('Last record.\n')
    self.assertNotEqual(self.generate('Next decision').returncode, 0)
    self.assertEqual((self.adrs / '9999-last.md').read_text(), 'Last record.\n')
    self.assertFalse((self.adrs / '.new-adr.lock').exists())

  def test_changed_template_fails_without_output(self):
    (self.adrs / 'template.md').write_text('# Unexpected template\n')
    self.assertNotEqual(self.generate('New decision').returncode, 0)
    self.assertEqual(list(self.adrs.glob('0001-*')), [])
    self.assertFalse((self.adrs / '.new-adr.lock').exists())

  def test_existing_lock_is_preserved(self):
    lock = self.adrs / '.new-adr.lock'
    lock.mkdir()
    self.assertNotEqual(self.generate('New decision').returncode, 0)
    self.assertTrue(lock.is_dir())
    self.assertEqual(list(self.adrs.glob('0001-*')), [])

  def test_concurrent_runs_never_share_an_identifier(self):
    commands = [['bash', str(self.script), f'Decision {number}'] for number in range(4)]
    processes = [subprocess.Popen(command, cwd=self.workspace.name,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                 for command in commands]
    successes = 0
    for process in processes:
      _, error = process.communicate(timeout=20)
      if process.returncode == 0:
        successes += 1
      else:
        self.assertIn('locked', error)
    generated = list(self.adrs.glob('[0-9][0-9][0-9][0-9]-*.md'))
    self.assertGreater(successes, 0)
    self.assertEqual(len(generated), successes)
    self.assertEqual(len({path.name[:4] for path in generated}), successes)
    self.assertFalse((self.adrs / '.new-adr.lock').exists())


if __name__ == '__main__':
  unittest.main()
