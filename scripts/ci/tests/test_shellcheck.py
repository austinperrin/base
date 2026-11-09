"""Exercise ShellCheck prerequisites and the real linter when installed."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from tool_support import pinned_tool


ROOT = Path(__file__).resolve().parents[3]
REAL_SHELLCHECK = pinned_tool('shellcheck', ['--version'], 'version: 0.11.0')
BASH = shutil.which('bash')


class ShellCheckTests(unittest.TestCase):
  def setUp(self):
    self.workspace = tempfile.TemporaryDirectory(prefix='base-shellcheck-')
    self.addCleanup(self.workspace.cleanup)
    self.root = Path(self.workspace.name) / 'project with spaces'
    self.script = self.root / 'scripts/ci/check-shell.sh'
    self.script.parent.mkdir(parents=True)
    shutil.copy2(ROOT / 'scripts/ci/check-shell.sh', self.script)
    (self.root / '.githooks').mkdir()
    (self.root / '.githooks/commit-msg').write_text('#!/usr/bin/env bash\nexit 0\n')
    self.bin = Path(self.workspace.name) / 'bin'
    self.bin.mkdir()
    self.env = dict(os.environ)

  def run_check(self, *args):
    return subprocess.run([BASH, str(self.script), *args], cwd=self.workspace.name,
                          env=self.env, capture_output=True, text=True)

  def fake_tool(self, body):
    path = self.bin / 'shellcheck'
    path.write_text(f'#!{BASH}\n{body}')
    path.chmod(0o755)
    self.env['PATH'] = str(self.bin) + os.pathsep + os.environ['PATH']

  def test_missing_tool_is_reported(self):
    self.env['PATH'] = str(self.bin)
    result = self.run_check()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('ShellCheck 0.11.0 is required', result.stderr)

  def test_wrong_or_unknown_version_is_rejected(self):
    for version in ['version: 0.10.0', 'unrecognized version output']:
      with self.subTest(version=version):
        self.fake_tool(f"printf '%s\\n' '{version}'\n")
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('0.11.0 is required', result.stderr)

  def test_invocation_ignores_personal_settings_and_preserves_arguments(self):
    self.fake_tool('''if [[ "$1" == --version ]]; then
  echo 'version: 0.11.0'
  exit 0
fi
[[ -z "${SHELLCHECK_OPTS:-}" ]] || exit 5
printf '<%s>\\n' "$@"
''')
    self.env['SHELLCHECK_OPTS'] = '--exclude=SC2086'
    (self.root / 'scripts/ci/spaced file.sh').write_text('#!/usr/bin/env bash\nexit 0\n')
    result = self.run_check()
    self.assertEqual(result.returncode, 0, result.stderr)
    for argument in ['<--norc>', '<--severity=style>', '<scripts/ci/spaced file.sh>', '<.githooks/commit-msg>']:
      self.assertIn(argument, result.stdout)

  def test_linter_failure_is_propagated(self):
    self.fake_tool('''if [[ "$1" == --version ]]; then
  echo 'version: 0.11.0'
  exit 0
fi
exit 7
''')
    result = self.run_check()
    self.assertEqual(result.returncode, 7)
    self.assertNotIn('checks passed', result.stdout)

  def test_unknown_arguments_are_rejected(self):
    self.assertNotEqual(self.run_check('--unknown').returncode, 0)

  @unittest.skipUnless(REAL_SHELLCHECK, 'ShellCheck pinned version not installed; real-tool integration is checked separately')
  def test_real_shellcheck_accepts_valid_script_and_rejects_unquoted_expansion(self):
    self.env['PATH'] = str(Path(REAL_SHELLCHECK).parent) + os.pathsep + os.environ['PATH']
    path = self.root / 'scripts/ci/example.sh'
    path.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$1"\n')
    result = self.run_check()
    self.assertEqual(result.returncode, 0, result.stderr)
    path.write_text('#!/usr/bin/env bash\necho $1\n')
    result = self.run_check()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('SC2086', result.stdout)


if __name__ == '__main__':
  unittest.main()
