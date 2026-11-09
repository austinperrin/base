#!/usr/bin/env bash
# Validate repository state without repairing files or changing configuration.
set -euo pipefail

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)
export PYTHONDONTWRITEBYTECODE=1
python3 "$root_dir/scripts/ci/repo_checks.py" repository "$@"
