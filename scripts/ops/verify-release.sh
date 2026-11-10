#!/usr/bin/env bash
# Verify release readiness without creating tags or publishing a release.
set -euo pipefail

for tool in git python3 gh; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Error: $tool is required for release verification." >&2
    exit 1
  fi
done
if ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))'; then
  echo "Error: Python 3.9 or newer is required." >&2
  exit 1
fi

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
export PYTHONDONTWRITEBYTECODE=1
exec python3 "$root_dir/scripts/ops/release_checks.py" "$@"
