"""Verify artifact integrity and extraction boundaries without network access."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import zipfile


ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('tool_installer', ROOT / 'scripts/ci/install-tools.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
  def setUp(self):
    self.workspace = tempfile.TemporaryDirectory(prefix='repository-installer-')
    self.addCleanup(self.workspace.cleanup)
    self.root = Path(self.workspace.name)
    self.destination = self.root / 'bin'
    self.styles = self.root / 'styles'

  def asset(self, content, member='tool'):
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode='w:gz') as package:
      for name, value in [(member, content), ('../../outside', b'never extract this')]:
        info = tarfile.TarInfo(name)
        info.size = len(value)
        package.addfile(info, io.BytesIO(value))
    data = archive.getvalue()
    return data, {'version': 'test', 'url': 'https://github.com/example/tool',
                  'sha256': hashlib.sha256(data).hexdigest(), 'member': member}

  def install(self, name, asset, data):
    def fetch(url, destination):
      destination.write_bytes(data)
    with patch.object(installer, 'download', side_effect=fetch):
      installer.install_asset(name, asset, self.destination, self.styles)

  def test_only_requested_executable_is_installed(self):
    data, asset = self.asset(b'fixture executable')
    self.install('tool', asset, data)
    path = self.destination / 'tool'
    self.assertEqual(path.read_bytes(), b'fixture executable')
    self.assertTrue(path.stat().st_mode & 0o111)
    self.assertFalse((self.root / 'outside').exists())
    self.assertEqual([p.name for p in self.destination.iterdir()], ['tool'])

  def test_checksum_mismatch_preserves_existing_executable(self):
    self.destination.mkdir()
    target = self.destination / 'tool'
    target.write_bytes(b'existing')
    data, asset = self.asset(b'replacement')
    with self.assertRaisesRegex(ValueError, 'checksum'):
      self.install('tool', asset, data + b'changed')
    self.assertEqual(target.read_bytes(), b'existing')

  def test_missing_executable_fails_without_publication(self):
    data, asset = self.asset(b'fixture')
    asset['member'] = 'absent'
    with self.assertRaises(KeyError):
      self.install('tool', asset, data)
    self.assertFalse((self.destination / 'tool').exists())

  def test_google_replacement_preserves_project_vocabulary(self):
    vocab = self.styles / 'config/vocabularies/Project/accept.txt'
    vocab.parent.mkdir(parents=True)
    vocab.write_text('ProjectTerm\n')
    old = self.styles / 'Google/Old.yml'
    old.parent.mkdir()
    old.write_text('obsolete')
    package = io.BytesIO()
    with zipfile.ZipFile(package, 'w') as archive:
      archive.writestr('Google/Spacing.yml', 'fixture rule')
    data = package.getvalue()
    asset = {'version': 'test', 'url': 'https://github.com/example/Google.zip',
             'sha256': hashlib.sha256(data).hexdigest()}
    self.install('google', asset, data)
    self.assertEqual(vocab.read_text(), 'ProjectTerm\n')
    self.assertFalse(old.exists())
    self.assertTrue((self.styles / 'Google/Spacing.yml').exists())

  def test_google_traversal_is_rejected_before_publication(self):
    package = io.BytesIO()
    with zipfile.ZipFile(package, 'w') as archive:
      archive.writestr('Google/../../outside', 'unsafe')
    data = package.getvalue()
    asset = {'version': 'test', 'url': 'https://github.com/example/Google.zip',
             'sha256': hashlib.sha256(data).hexdigest()}
    with self.assertRaisesRegex(ValueError, 'unexpected path'):
      self.install('google', asset, data)
    self.assertFalse(self.styles.exists())

  def test_executable_archive_symlink_is_rejected(self):
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode='w:gz') as package:
      member = tarfile.TarInfo('tool')
      member.type = tarfile.SYMTYPE
      member.linkname = '/outside'
      package.addfile(member)
    data = archive.getvalue()
    asset = {'version': 'test', 'url': 'https://github.com/example/tool',
             'sha256': hashlib.sha256(data).hexdigest(), 'member': 'tool'}
    with self.assertRaisesRegex(ValueError, 'regular executable'):
      self.install('tool', asset, data)
    self.assertFalse(self.destination.exists())

  def test_non_https_source_is_rejected(self):
    with self.assertRaisesRegex(ValueError, 'HTTPS'):
      installer.download('http://example.invalid/tool', self.root / 'download')

  def test_manifest_versions_match_wrappers_and_google_configuration(self):
    artifacts = json.loads((ROOT / 'scripts/ci/tools.json').read_text())['artifacts']
    wrappers = {'shellcheck': 'check-shell.sh', 'actionlint': 'check-workflows.sh',
                'vale': 'check-prose.sh', 'gitleaks': 'check-credentials.sh'}
    for name, wrapper in wrappers.items():
      source = (ROOT / 'scripts/ci' / wrapper).read_text()
      version = re.search(r'readonly required_version=(\S+)', source)[1]
      self.assertEqual(artifacts[name]['version'], version)
      self.assertRegex(artifacts[name]['sha256'], r'^[0-9a-f]{64}$')
    self.assertIn(artifacts['google']['url'], (ROOT / '.vale.ini').read_text())


if __name__ == '__main__':
  unittest.main()
