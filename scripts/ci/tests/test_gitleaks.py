"""Test credential scanning with synthetic values confined to temporary repositories."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import uuid


ROOT = Path(__file__).resolve().parents[3]
BASH = shutil.which('bash')
REAL_GITLEAKS = shutil.which('gitleaks')


class GitleaksTests(unittest.TestCase):
  def setUp(self):
    self.workspace = tempfile.TemporaryDirectory(prefix='base-gitleaks-')
    self.addCleanup(self.workspace.cleanup)
    self.root = Path(self.workspace.name).resolve() / 'project with spaces'
    self.script = self.root / 'scripts/ci/check-credentials.sh'
    self.script.parent.mkdir(parents=True)
    shutil.copy2(ROOT / 'scripts/ci/check-credentials.sh', self.script)
    shutil.copy2(ROOT / '.gitleaks.toml', self.root / '.gitleaks.toml')
    self.bin = Path(self.workspace.name) / 'bin'
    self.bin.mkdir()
    self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
    self.git('init', '-q')
    self.git('config', 'user.name', 'Credential Test')
    self.git('config', 'user.email', 'test@example.invalid')
    (self.root / 'README.md').write_text('# Test repository\n')
    self.git('add', 'README.md')
    self.git('commit', '-qm', 'docs: initialize fixture')

  def git(self, *args):
    result = subprocess.run(['git', *args], cwd=self.root, env=self.env,
                            capture_output=True, text=True)
    self.assertEqual(result.returncode, 0, result.stderr)
    return result

  def run_check(self, *args):
    return subprocess.run([BASH, str(self.script), *args], cwd=self.workspace.name,
                          env=self.env, capture_output=True, text=True)

  def fake_tool(self, body):
    path = self.bin / 'gitleaks'
    path.write_text(f'#!{BASH}\n{body}')
    path.chmod(0o755)
    self.env['PATH'] = str(self.bin) + os.pathsep + os.environ['PATH']

  def real_tool(self):
    self.env['PATH'] = str(Path(REAL_GITLEAKS).parent) + os.pathsep + os.environ['PATH']

  def test_missing_tool_and_wrong_version_are_rejected(self):
    self.env['PATH'] = str(self.bin)
    self.assertNotEqual(self.run_check().returncode, 0)
    self.fake_tool("echo '0.1.0'\n")
    result = self.run_check()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('8.30.1 is required', result.stderr)

  def test_both_scans_use_explicit_config_and_redaction(self):
    self.fake_tool('''if [[ "$1" == version ]]; then
  echo '8.30.1'
  exit 0
fi
printf '<%s>\\n' "$@"
''')
    result = self.run_check()
    self.assertEqual(result.returncode, 0, result.stderr)
    for argument in ['<--redact=100>', '<--ignore-gitleaks-allow>',
                     f'<--config={self.root}/.gitleaks.toml>']:
      self.assertEqual(result.stdout.count(argument), 2)
    self.assertIn('<--log-opts=HEAD>', result.stdout)
    self.assertIn('<--staged>', result.stdout)

  def test_history_failure_stops_before_staged_scan(self):
    self.fake_tool('''if [[ "$1" == version ]]; then
  echo '8.30.1'
  exit 0
fi
printf '<%s>\\n' "$@"
exit 7
''')
    result = self.run_check()
    self.assertEqual(result.returncode, 7)
    self.assertNotIn('<--staged>', result.stdout)
    self.assertNotIn('checks passed', result.stdout)

  def test_unknown_arguments_are_rejected(self):
    self.assertNotEqual(self.run_check('--unknown').returncode, 0)

  def test_shallow_history_is_rejected(self):
    self.fake_tool("echo '8.30.1'\n")
    source = self.root
    shallow = Path(self.workspace.name).resolve() / 'shallow'
    self.git('clone', '-q', '--depth=1', source.as_uri(), str(shallow))
    self.root = shallow
    self.script = self.root / 'scripts/ci/check-credentials.sh'
    self.script.parent.mkdir(parents=True)
    shutil.copy2(ROOT / 'scripts/ci/check-credentials.sh', self.script)
    shutil.copy2(ROOT / '.gitleaks.toml', self.root / '.gitleaks.toml')
    result = self.run_check()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('complete current-branch history', result.stderr)

  @unittest.skipUnless(REAL_GITLEAKS, 'Gitleaks not installed; real-scanner integration is checked separately')
  def test_real_scanner_detects_staged_synthetic_value_and_redacts_it(self):
    self.real_tool()
    self.assertEqual(self.run_check().returncode, 0)
    synthetic = 'ghp_' + uuid.uuid4().hex + 'Ab9X'
    path = self.root / 'sample.txt'
    path.write_text(f'github_token = "{synthetic}" # gitleaks:allow\n')
    self.git('add', 'sample.txt')
    result = self.run_check()
    self.assertNotEqual(result.returncode, 0)
    self.assertNotIn(synthetic, result.stdout + result.stderr)
    self.git('rm', '--cached', 'sample.txt')
    # The local untracked file is deliberately outside the chosen scan scope.
    self.assertEqual(self.run_check().returncode, 0)

  @unittest.skipUnless(REAL_GITLEAKS, 'Gitleaks not installed; real-scanner integration is checked separately')
  def test_real_scanner_detects_removed_value_in_history(self):
    self.real_tool()
    synthetic = 'ghp_' + uuid.uuid4().hex + 'Ab9X'
    path = self.root / 'sample.txt'
    path.write_text(f'github_token = "{synthetic}"\n')
    self.git('add', 'sample.txt')
    self.git('commit', '-qm', 'test: add synthetic fixture')
    self.git('rm', 'sample.txt')
    self.git('commit', '-qm', 'test: remove synthetic fixture')
    result = self.run_check()
    self.assertNotEqual(result.returncode, 0)
    self.assertNotIn(synthetic, result.stdout + result.stderr)


if __name__ == '__main__':
  unittest.main()
