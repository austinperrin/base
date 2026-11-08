"""Test prose wrapper prerequisites and real pinned rules when installed."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from tool_support import pinned_tool


ROOT = Path(__file__).resolve().parents[3]
BASH = shutil.which('bash')
REAL_VALE = pinned_tool('vale', ['--version'], 'vale version 3.26.0')
RULES = ROOT / '.github/styles/Google'


class ValeTests(unittest.TestCase):
  def setUp(self):
    self.workspace = tempfile.TemporaryDirectory(prefix='base-vale-')
    self.addCleanup(self.workspace.cleanup)
    self.root = Path(self.workspace.name).resolve() / 'project with spaces'
    self.script = self.root / 'scripts/ci/check-prose.sh'
    self.script.parent.mkdir(parents=True)
    shutil.copy2(ROOT / 'scripts/ci/check-prose.sh', self.script)
    self.bin = Path(self.workspace.name) / 'bin'
    self.bin.mkdir()
    self.env = dict(os.environ)
    self.rules = self.root / '.github/styles/Google'
    self.rules.mkdir(parents=True)
    (self.rules / 'Spacing.yml').write_text('fixture marker\n')

  def fake_tool(self, body):
    path = self.bin / 'vale'
    path.write_text(f'#!{BASH}\n{body}')
    path.chmod(0o755)
    self.env['PATH'] = str(self.bin) + os.pathsep + os.environ['PATH']

  def run_check(self, *args):
    return subprocess.run([BASH, str(self.script), *args], cwd=self.workspace.name,
                          env=self.env, capture_output=True, text=True)

  def test_missing_tool_and_wrong_version_are_rejected(self):
    self.env['PATH'] = str(self.bin)
    self.assertNotEqual(self.run_check().returncode, 0)
    self.fake_tool("echo 'vale version 0.1.0'\n")
    result = self.run_check()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('3.26.0 is required', result.stderr)

  def test_missing_styles_fail_without_downloading(self):
    self.fake_tool('''if [[ "$1" == --version ]]; then
  echo 'vale version 3.26.0'
  exit 0
fi
exit 9
''')
    (self.rules / 'Spacing.yml').unlink()
    result = self.run_check()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('vale sync', result.stderr)
    self.assertFalse((self.rules / 'Spacing.yml').exists())

  def test_invocation_has_explicit_config_global_isolation_and_error_threshold(self):
    self.fake_tool('''if [[ "$1" == --version ]]; then
  echo 'vale version 3.26.0'
  exit 0
fi
printf '<%s>\\n' "$@"
''')
    result = self.run_check()
    self.assertEqual(result.returncode, 0, result.stderr)
    for argument in ['<--no-global>', f'<--config={self.root}/.vale.ini>',
                     '<--minAlertLevel=error>', '<SECURITY.md>', '<docs>']:
      self.assertIn(argument, result.stdout)
    self.assertNotIn('<sync>', result.stdout)

  def test_failure_status_is_preserved(self):
    self.fake_tool('''if [[ "$1" == --version ]]; then
  echo 'vale version 3.26.0'
  exit 0
fi
exit 6
''')
    result = self.run_check()
    self.assertEqual(result.returncode, 6)
    self.assertNotIn('checks passed', result.stdout)

  def test_unknown_arguments_are_rejected(self):
    self.assertNotEqual(self.run_check('--unknown').returncode, 0)

  @unittest.skipUnless(REAL_VALE and (RULES / 'Spacing.yml').exists(),
                       'Pinned Vale or Google rules missing; real-rule integration is checked separately')
  def test_real_rules_reject_exclamations_and_ignore_fenced_examples(self):
    self.env['PATH'] = str(Path(REAL_VALE).parent) + os.pathsep + os.environ['PATH']
    shutil.rmtree(self.rules)
    shutil.copytree(RULES, self.rules)
    shutil.copy2(ROOT / '.vale.ini', self.root / '.vale.ini')
    vocab = self.root / '.github/styles/config/vocabularies/Base'
    vocab.mkdir(parents=True)
    shutil.copy2(ROOT / '.github/styles/config/vocabularies/Base/accept.txt', vocab / 'accept.txt')
    for name in ['README.md', 'CONTRIBUTING.md', 'SECURITY.md', 'AGENTS.md',
                 'scripts/README.md', '.githooks/README.md', 'docs/README.md']:
      path = self.root / name
      path.parent.mkdir(parents=True, exist_ok=True)
      path.write_text('# Reference\n\nUse actionlint and pyflakes.\n\n```text\nThis is important!\n```\n')
    result = self.run_check()
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    with (self.root / 'README.md').open('a') as output:
      output.write('\nThis is important!\n')
    result = self.run_check()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('Google.Exclamation', result.stdout)


if __name__ == '__main__':
  unittest.main()
