# Local Git Hooks

[Repository Home](../README.md) > Local Git Hooks

This directory contains the local commit-message hook. Use the
[script reference](../scripts/README.md) for prerequisites, activation, and tests.
The [Git workflow standard](../docs/standards/git-workflow.md) owns commit conventions.

## Validation Scope

The [commit-msg hook](commit-msg) validates the first line's type, optional scope,
optional breaking-change marker, separator, and nonempty description. It does not
validate the body, breaking-change footers, or whether the description accurately
explains the change. Human review remains necessary.

Generated merge and revert subjects must follow the repository's commit convention;
the hook does not exempt them. Local validation does not enforce pull request
titles or replace required server-side checks.

## Related Documents

- [Script reference](../scripts/README.md) - Setup and regression checks.
- [Git workflow](../docs/standards/git-workflow.md) - Commit and review requirements.
