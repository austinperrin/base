# Script Reference

[Repository Home](../README.md) > Script Reference

This index documents the helpers currently available in the repository.

## Prerequisites

The setup script and hook require Bash 3.2 or newer, Git, and standard command-line
utilities. On Windows, run them in Git Bash or a compatible environment. The ADR generator and regression tests additionally require Python 3.9 or newer
with its standard library.

## Developer Tools

| Script | Behavior | Usage from the repository root |
| :--- | :--- | :--- |
| [setup.sh](dev/setup.sh) | Configures the local commit-message hook after checking for conflicts | `./scripts/dev/setup.sh` |
| [new-adr.sh](dev/new-adr.sh) | Creates the next numbered Proposed ADR from the current template | `./scripts/dev/new-adr.sh "Choose storage"` |

Setup resolves the repository from its own location, so it can also be invoked by
path from another working directory. It sets this checkout's local
`core.hooksPath` to `.githooks`; it does not install dependencies or create secret
configuration. Repeating setup is safe when that path is already selected.

If an existing effective hook path differs, setup stops without replacing it.
Inspect its origin with `git config --show-origin --get core.hooksPath` and arrange
any integration with the existing hooks before enabling this configuration.

See [local Git hooks](../.githooks/README.md) for validation scope and the
[Git workflow](../docs/standards/git-workflow.md) for the canonical conventions.
Run setup again in each new clone that should use these hooks.

## ADR Generation

The generator resolves the repository from its own location and can be invoked
by path from another directory. It uses the next identifier after the highest
four-digit record filename and inserts the supplied title and local date into the
[ADR template](../docs/adr/template.md). Titles must be one nonempty line without
control characters and contain an ASCII letter or digit for the filename; other
characters become separators in the filename while the heading retains the title.

Generation creates one file without replacing existing records. It leaves the
[decision index](../docs/adr/README.md) unchanged. Complete the remaining fields
and register the record according to the
[ADR standard](../docs/standards/architecture-decisions.md) before review.

A temporary `docs/adr/.new-adr.lock/` directory serializes generation. Concurrent
runs may stop with a lock message; retry after the running generator finishes.
If a process is forcibly terminated, confirm no generator is running before
removing its leftover lock directory and inspecting any `.adr-*` temporary file.
Parallel branches can still choose the same identifier; resolve numbering conflicts
before merging. The generator stops when numbering exceeds `9999` or the required
template structure no longer matches.

## Verification

From the repository root, run:

```bash
python3 -m unittest discover -s scripts/dev/tests -v
```

The tests exercise setup, real Git commits, and ADR generation in temporary repositories. They do
not change the current checkout's Git configuration. Review and CI enforcement
remain separate from local hook activation.

## Related Documents

- [Contributing](../CONTRIBUTING.md) - Preparing and reviewing changes.
- [Local Git hooks](../.githooks/README.md) - Commit-message validation boundaries.
- [Milestone 0 roadmap](../docs/roadmap/milestone-0-repository-scaffolding.md) - Remaining tooling and automation work.
