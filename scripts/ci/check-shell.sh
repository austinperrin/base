#!/usr/bin/env bash
# Run the reviewed ShellCheck version without inheriting personal lint settings.
set -euo pipefail

if [[ $# -ne 0 ]]; then
  echo "Usage: ./scripts/ci/check-shell.sh" >&2
  exit 1
fi
readonly required_version=0.11.0
if ! command -v shellcheck >/dev/null 2>&1; then
  echo "Error: ShellCheck $required_version is required; see docs/architecture/ci-cd.md." >&2
  exit 1
fi
version_output=$(shellcheck --version)
actual_version=''
while IFS= read -r line; do
  case "$line" in
    'version: '*) actual_version=${line#version: } ;;
  esac
done <<< "$version_output"
if [[ "$actual_version" != "$required_version" ]]; then
  echo "Error: ShellCheck $required_version is required; found ${actual_version:-unknown}." >&2
  exit 1
fi

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
cd "$root_dir"
SHELLCHECK_OPTS='' shellcheck --norc --severity=style scripts/*/*.sh .githooks/commit-msg
echo "ShellCheck checks passed."
