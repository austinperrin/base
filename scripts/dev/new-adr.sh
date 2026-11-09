#!/usr/bin/env bash
# Create the next Proposed ADR from the repository's current template.
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: Python 3.9 or newer is required." >&2
  exit 1
fi
root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
python3 - "$root_dir" "$@" <<'PYTHON'
from datetime import date
import os
from pathlib import Path
import re
import sys
import tempfile


def main():
  if sys.version_info < (3, 9):
    sys.exit('Error: Python 3.9 or newer is required.')
  if len(sys.argv) != 3:
    sys.exit('Usage: ./scripts/dev/new-adr.sh "Title of Decision"')
  title = sys.argv[2].strip()
  if not title or any(ord(char) < 32 or ord(char) == 127 for char in sys.argv[2]):
    sys.exit('Error: provide a nonempty title on one line without control characters.')
  slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
  if not slug:
    sys.exit('Error: the title must contain an ASCII letter or digit for its filename.')

  adrs = Path(sys.argv[1]) / 'docs/adr'
  lock = adrs / '.new-adr.lock'
  try:
    lock.mkdir()
  except FileExistsError:
    sys.exit('Error: ADR generation is locked; see scripts/README.md before retrying.')
  try:
    template = (adrs / 'template.md').read_text(encoding='utf-8')
    if (not template.startswith('# ADR-XXXX: [Decision Title]\n')
        or '[YYYY-MM-DD]' not in template or '* **Status**: Proposed\n' not in template):
      sys.exit('Error: the ADR template has changed; update the generator before using it.')
    identifiers = [int(match[1]) for path in adrs.iterdir()
                   if (match := re.fullmatch(r'([0-9]{4})-.+\.md', path.name))]
    number = max(identifiers, default=0) + 1
    if number > 9999:
      sys.exit('Error: ADR numbering exceeds four digits.')
    identifier = f'{number:04d}'
    destination = adrs / f'{identifier}-{slug}.md'
    content = template.replace('ADR-XXXX', f'ADR-{identifier}')
    content = content.replace('[YYYY-MM-DD]', date.today().isoformat())
    # Insert the title last, so text resembling placeholders stays literal.
    _, _, remainder = content.partition('\n')
    content = f'# ADR-{identifier}: {title}\n{remainder}'
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=adrs,
                                     prefix='.adr-', delete=False) as output:
      temporary = Path(output.name)
      try:
        output.write(content)
        output.flush()
        temporary.chmod(0o644)
        # Publish the completed file without replacing an existing destination.
        os.link(temporary, destination)
      finally:
        temporary.unlink()
  finally:
    lock.rmdir()
  print(f'Created Proposed ADR: {destination}')
  print('Complete its content and register it in docs/adr/README.md before review.')


try:
  main()
except OSError as error:
  sys.exit(f'Error: ADR generation failed: {error}')
PYTHON
