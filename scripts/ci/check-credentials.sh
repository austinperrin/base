#!/usr/bin/env bash
# Scan current-branch history and staged changes with fully redacted output.
set -euo pipefail

if [[ $# -ne 0 ]]; then
  echo "Usage: ./scripts/ci/check-credentials.sh" >&2
  exit 1
fi
readonly required_version=8.30.1
for tool in git gitleaks; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Error: $tool is required; see docs/architecture/ci-cd.md." >&2
    exit 1
  fi
done
actual_version=$(gitleaks version)
if [[ "$actual_version" != "$required_version" ]]; then
  echo "Error: Gitleaks $required_version is required; found $actual_version." >&2
  exit 1
fi

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
cd "$root_dir"
repo_dir=$(git rev-parse --show-toplevel)
repo_dir=$(cd "$repo_dir" && pwd -P)
if [[ "$repo_dir" != "$root_dir" ]]; then
  echo "Error: credential scanning must belong to the root of a Git working tree." >&2
  exit 1
fi
if [[ "$(git rev-parse --is-shallow-repository)" == true ]]; then
  echo "Error: complete current-branch history is required; fetch it before scanning." >&2
  exit 1
fi
git rev-parse --verify HEAD >/dev/null
common=(--config="$root_dir/.gitleaks.toml" --redact=100 --no-banner --no-color --ignore-gitleaks-allow)
gitleaks git "${common[@]}" --log-opts=HEAD "$root_dir"
gitleaks git "${common[@]}" --staged "$root_dir"
echo "Credential content and history checks passed."
