#!/usr/bin/env bash
# Configure the repository's local commit-message hook without replacing other hooks.
set -euo pipefail

if [[ $# -ne 0 ]]; then
  echo "Usage: ./scripts/dev/setup.sh" >&2
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  echo "Error: Git is required." >&2
  exit 1
fi

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
repo_dir=$(git -C "$root_dir" rev-parse --show-toplevel)
repo_dir=$(cd "$repo_dir" && pwd -P)
if [[ "$root_dir" != "$repo_dir" ]]; then
  echo "Error: setup must belong to the root of a Git working tree." >&2
  exit 1
fi
if [[ ! -x "$root_dir/.githooks/commit-msg" ]]; then
  echo "Error: .githooks/commit-msg is missing or not executable." >&2
  exit 1
fi

existing=$(git -C "$root_dir" config --get core.hooksPath || [[ $? -eq 1 ]])
if [[ -n "$existing" && "$existing" != .githooks ]]; then
  echo "Error: core.hooksPath already points to another location." >&2
  echo "Review the existing configuration before enabling this repository's hooks." >&2
  exit 1
fi

git -C "$root_dir" config --local core.hooksPath .githooks
echo "Configured local Git hooks (.githooks/)."
echo "See scripts/README.md for usage and verification."
