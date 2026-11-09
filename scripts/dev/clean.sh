#!/usr/bin/env bash
# Preview or remove ignored files in designated root disposable directories.
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: Python 3.9 or newer is required." >&2
  exit 1
fi
root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
python3 - "$root_dir" "$@" <<'PYTHON'
import argparse
import os
from pathlib import Path
import subprocess
import sys


def main():
  if sys.version_info < (3, 9):
    sys.exit('Error: Python 3.9 or newer is required.')
  parser = argparse.ArgumentParser(description='Preview ignored disposable files; use --apply to remove them.')
  mode = parser.add_mutually_exclusive_group()
  mode.add_argument('--dry-run', action='store_true', help='Preview only (the default)')
  mode.add_argument('--apply', action='store_true', help='Remove the eligible files')
  args = parser.parse_args(sys.argv[2:])
  root = Path(sys.argv[1]).resolve()
  repository = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=root)
  if Path(os.fsdecode(repository).rstrip('\n')).resolve() != root:
    sys.exit('Error: cleanup must belong to the root of a Git working tree.')

  # Git selects only ignored, untracked candidates using the effective ignore rules.
  result = subprocess.check_output(
    ['git', 'ls-files', '--others', '--ignored', '--exclude-standard', '-z'], cwd=root)
  count = 0
  for raw_name in result.split(b'\0'):
    if not raw_name:
      continue
    name = os.fsdecode(raw_name)
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts:
      continue
    if len(relative.parts) < 2 or relative.parts[0] not in {'tmp', '.tmp', 'temp', 'scratch', '.cache'}:
      continue
    path = root / relative
    # Never follow links or clean inside a nested repository/worktree.
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
      continue
    if any((parent / '.git').exists() for parent in path.parents if parent != root and root in parent.parents):
      continue
    if '.git' in relative.parts or not path.is_file():
      continue
    print(('Removing: ' if args.apply else 'Would remove: ') + repr(name))
    if args.apply:
      path.unlink()
    count += 1
  print(f'{count} disposable file(s) ' + ('removed.' if args.apply else 'found; preview only.'))


try:
  main()
except (OSError, subprocess.CalledProcessError) as error:
  sys.exit(f'Error: cleanup failed: {error}')
PYTHON
