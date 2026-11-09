#!/usr/bin/env bash
# Check selected repository prose with the reviewed Vale engine and Google rules.
set -euo pipefail

if [[ $# -ne 0 ]]; then
  echo "Usage: ./scripts/ci/check-prose.sh" >&2
  exit 1
fi
readonly required_version=3.26.0
if ! command -v vale >/dev/null 2>&1; then
  echo "Error: Vale $required_version is required; see docs/architecture/ci-cd.md." >&2
  exit 1
fi
version_output=$(vale --version)
if [[ "$version_output" != "vale version $required_version" ]]; then
  echo "Error: Vale $required_version is required; found $version_output." >&2
  exit 1
fi

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
cd "$root_dir"
if [[ ! -f .github/styles/Google/Spacing.yml ]]; then
  echo "Error: Google style rules are missing; run vale sync --config=.vale.ini first." >&2
  exit 1
fi
vale --no-global --config="$root_dir/.vale.ini" --minAlertLevel=error \
  docs README.md CONTRIBUTING.md SECURITY.md AGENTS.md scripts/README.md .githooks/README.md
echo "Prose checks passed."
