"""Install reviewed Linux tool artifacts after checking their committed SHA-256 pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import sys
import tarfile
import tempfile
import urllib.request
import zipfile


ROOT = Path(__file__).resolve().parents[2]
MAX_BYTES = 100 * 1024 * 1024


def download(url, destination):
  if not url.startswith('https://github.com/'):
    raise ValueError('Artifact URL must use the reviewed GitHub HTTPS source')
  request = urllib.request.Request(url, headers={'User-Agent': 'repository-tool-installer'})
  size = 0
  with urllib.request.urlopen(request, timeout=60) as response, destination.open('wb') as output:
    while True:
      chunk = response.read(1024 * 1024)
      if not chunk:
        break
      size += len(chunk)
      if size > MAX_BYTES:
        raise ValueError('Artifact exceeds the download limit')
      output.write(chunk)


def digest(path):
  result = hashlib.sha256()
  with path.open('rb') as source:
    for chunk in iter(lambda: source.read(1024 * 1024), b''):
      result.update(chunk)
  return result.hexdigest()


def install_asset(name, asset, destination, styles_path):
  with tempfile.TemporaryDirectory(prefix='repository-artifact-') as tmp:
    archive = Path(tmp) / 'download'
    download(asset['url'], archive)
    if digest(archive) != asset['sha256']:
      raise ValueError(f'{name}: archive checksum does not match the reviewed pin')
    if name == 'google':
      unpacked = Path(tmp) / 'styles'
      unpacked.mkdir()
      with zipfile.ZipFile(archive) as package:
        total = 0
        for member in package.infolist():
          parts = PurePosixPath(member.filename).parts
          if not parts or parts[0] != 'Google' or '..' in parts or PurePosixPath(member.filename).is_absolute():
            raise ValueError('Google package contains an unexpected path')
          if stat.S_ISLNK(member.external_attr >> 16):
            raise ValueError('Google package contains a symbolic link')
          total += member.file_size
          if total > MAX_BYTES:
            raise ValueError('Google package exceeds the extraction limit')
          target = unpacked.joinpath(*parts)
          if member.is_dir():
            target.mkdir(parents=True, exist_ok=True)
          else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with package.open(member) as source, target.open('wb') as output:
              shutil.copyfileobj(source, output)
      if not (unpacked / 'Google/Spacing.yml').is_file():
        raise ValueError('Google package is missing its expected rules')
      styles_path.mkdir(parents=True, exist_ok=True)
      target = styles_path / 'Google'
      if target.is_symlink():
        raise ValueError('Google cache must not be a symbolic link')
      # Prepare the replacement on the destination filesystem before publication.
      with tempfile.TemporaryDirectory(prefix='.google-install-', dir=styles_path) as stage:
        staged = Path(stage) / 'Google'
        shutil.copytree(unpacked / 'Google', staged)
        backup = Path(stage) / 'previous'
        if target.exists():
          target.rename(backup)
        try:
          staged.rename(target)
        except OSError:
          if backup.exists():
            backup.rename(target)
          raise
    else:
      with tarfile.open(archive, 'r:*') as package:
        member = package.getmember(asset['member'])
        if not member.isfile() or member.size > MAX_BYTES:
          raise ValueError(f'{name}: expected a regular executable within the size limit')
        destination.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(prefix='.install-', dir=destination, delete=False) as output:
          temporary = Path(output.name)
          try:
            with package.extractfile(member) as source:
              shutil.copyfileobj(source, output)
            output.flush()
            temporary.chmod(0o755)
            os.replace(temporary, destination / name)
          finally:
            temporary.unlink(missing_ok=True)
  print(f'Installed {name} {asset["version"]} from its verified archive.')


def main():
  if sys.version_info < (3, 9):
    sys.exit('Error: Python 3.9 or newer is required.')
  manifest = json.loads((ROOT / 'scripts/ci/tools.json').read_text(encoding='utf-8'))
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--platform', required=True, choices=[manifest['platform']])
  parser.add_argument('--destination', type=Path, required=True, help='Directory for the Linux executables')
  parser.add_argument('--styles-path', type=Path, default=ROOT / '.github/styles')
  parser.add_argument('--tool', action='append', choices=list(manifest['artifacts']))
  args = parser.parse_args()
  for name in args.tool or manifest['artifacts']:
    install_asset(name, manifest['artifacts'][name], args.destination.resolve(), args.styles_path.resolve())


if __name__ == '__main__':
  try:
    main()
  except (OSError, ValueError, KeyError, tarfile.TarError, zipfile.BadZipFile) as error:
    sys.exit(f'Error: tool installation failed: {error}')
