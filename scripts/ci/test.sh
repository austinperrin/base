#!/usr/bin/env bash
# Run the available repository checks and regression tests without repairing files.
set -euo pipefail

if [[ $# -ne 0 ]]; then
  echo "Usage: ./scripts/ci/test.sh" >&2
  exit 1
fi
for tool in git python3; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Error: $tool is required." >&2
    exit 1
  fi
done
if ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))'; then
  echo "Error: Python 3.9 or newer is required." >&2
  exit 1
fi

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
cd "$root_dir"
export PYTHONDONTWRITEBYTECODE=1

echo "Running local repository suite..."
for script in scripts/*/*.sh .githooks/commit-msg; do
  if [[ ! -f "$script" || -L "$script" || ! -x "$script" ]]; then
    echo "Error: $script must be an executable regular file." >&2
    exit 1
  fi
  bash -n "$script"
done

./scripts/ci/check-links.sh
./scripts/ci/check-docs.sh
./scripts/ci/check-secrets.sh
./scripts/ci/check-repository.sh
python3 -B -m unittest discover -s scripts/dev/tests -v
python3 -B -m unittest discover -s scripts/ci/tests -v
python3 -B -m unittest discover -s scripts/ops/tests -v

echo "Local repository suite passed. External linters and CI are separate."
