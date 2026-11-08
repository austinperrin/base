"""Validate actionlint invocation, prerequisites, and representative real workflows."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
BASH = shutil.which('bash')
REAL_ACTIONLINT = shutil.which('actionlint')


class ActionlintTests(unittest.TestCase):
  def setUp(self):
    self.workspace = tempfile.TemporaryDirectory(prefix='base-actionlint-')
    self.addCleanup(self.workspace.cleanup)
    self.root = Path(self.workspace.name) / 'project with spaces'
    self.script = self.root / 'scripts/ci/check-workflows.sh'
    self.script.parent.mkdir(parents=True)
    shutil.copy2(ROOT / 'scripts/ci/check-workflows.sh', self.script)
    self.bin = Path(self.workspace.name) / 'bin'
    self.bin.mkdir()
    self.env = dict(os.environ)

  def workflow(self, name='check.yml', content=None):
    path = self.root / '.github/workflows' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content or 'name: Check\non: push\njobs:\n  check:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo passed\n')
    return path

  def fake_tool(self, body):
    path = self.bin / 'actionlint'
    path.write_text(f'#!{BASH}\n{body}')
    path.chmod(0o755)
    self.env['PATH'] = str(self.bin) + os.pathsep + os.environ['PATH']

  def run_check(self, *args):
    return subprocess.run([BASH, str(self.script), *args], cwd=self.workspace.name,
                          env=self.env, capture_output=True, text=True)

  def test_missing_tool_and_wrong_version_are_rejected(self):
    self.env['PATH'] = str(self.bin)
    self.assertNotEqual(self.run_check().returncode, 0)
    self.fake_tool("echo '1.0.0'\n")
    result = self.run_check()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('1.7.12 is required', result.stderr)

  def test_no_workflows_is_explicitly_not_applicable(self):
    self.fake_tool('''if [[ "$1" == -version ]]; then
  echo '1.7.12'
  exit 0
fi
exit 9
''')
    result = self.run_check()
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn('not applicable yet', result.stdout)
    self.assertNotIn('checks passed', result.stdout)

  def test_both_extensions_and_spaces_are_passed_as_separate_arguments(self):
    self.fake_tool('''if [[ "$1" == -version ]]; then
  echo '1.7.12'
  echo 'build information'
  exit 0
fi
printf '<%s>\\n' "$@"
''')
    self.workflow('first.yml')
    self.workflow('second file.yaml')
    result = self.run_check()
    self.assertEqual(result.returncode, 0, result.stderr)
    for value in ['<.github/workflows/first.yml>', '<.github/workflows/second file.yaml>',
                  '<-shellcheck=>', '<-pyflakes=>']:
      self.assertIn(value, result.stdout)

  def test_linter_failure_is_propagated(self):
    self.fake_tool('''if [[ "$1" == -version ]]; then
  echo '1.7.12'
  exit 0
fi
exit 8
''')
    self.workflow()
    result = self.run_check()
    self.assertEqual(result.returncode, 8)
    self.assertNotIn('checks passed', result.stdout)

  def test_unknown_arguments_are_rejected(self):
    self.assertNotEqual(self.run_check('--unknown').returncode, 0)

  @unittest.skipUnless(REAL_ACTIONLINT, 'actionlint not installed; real-tool integration is checked separately')
  def test_real_tool_accepts_workflow_and_rejects_invalid_expression(self):
    self.env['PATH'] = str(Path(REAL_ACTIONLINT).parent) + os.pathsep + os.environ['PATH']
    path = self.workflow()
    result = self.run_check()
    self.assertEqual(result.returncode, 0, result.stderr)
    path.write_text(path.read_text().replace('echo passed', 'echo ${{ invalid_context.value }}'))
    result = self.run_check()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('invalid_context', result.stdout)


if __name__ == '__main__':
  unittest.main()
