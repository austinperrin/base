#!/usr/bin/env bash
# Validate workflow structure and expressions with the reviewed actionlint version.
set -euo pipefail

if [[ $# -ne 0 ]]; then
  echo "Usage: ./scripts/ci/check-workflows.sh" >&2
  exit 1
fi
readonly required_version=1.7.12
if ! command -v actionlint >/dev/null 2>&1; then
  echo "Error: actionlint $required_version is required; see docs/architecture/ci-cd.md." >&2
  exit 1
fi
version_output=$(actionlint -version)
actual_version=${version_output%%$'\n'*}
if [[ "$actual_version" != "$required_version" ]]; then
  echo "Error: actionlint $required_version is required; found ${actual_version:-unknown}." >&2
  exit 1
fi

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
cd "$root_dir"
shopt -s nullglob
workflows=(.github/workflows/*.yml .github/workflows/*.yaml)
if [[ ${#workflows[@]} -eq 0 ]]; then
  echo "No workflow files found; actionlint validation is not applicable yet."
  exit 0
fi
# External run-block linting is separate from workflow structure/expression checks.
actionlint -no-color -oneline -shellcheck= -pyflakes= "${workflows[@]}"
echo "Workflow checks passed."
