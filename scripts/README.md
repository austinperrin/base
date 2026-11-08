# Script Reference

[Repository Home](../README.md) > Script Reference

This index documents the helpers currently available in the repository.

## Prerequisites

The setup script and hook require Bash 3.2 or newer, Git, and standard command-line
utilities. On Windows, run them in Git Bash or a compatible environment. The ADR generator, cleanup helper, and regression tests additionally require
Python 3.9 or newer with its standard library.

## Developer Tools

| Script | Behavior | Usage from the repository root |
| :--- | :--- | :--- |
| [setup.sh](dev/setup.sh) | Configures the local commit-message hook after checking for conflicts | `./scripts/dev/setup.sh` |
| [new-adr.sh](dev/new-adr.sh) | Creates the next numbered Proposed ADR from the current template | `./scripts/dev/new-adr.sh "Choose storage"` |
| [clean.sh](dev/clean.sh) | Previews disposable ignored files; deletes only with `--apply` | `./scripts/dev/clean.sh --dry-run` |

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

## Disposable-File Cleanup

Run `./scripts/dev/clean.sh` or `./scripts/dev/clean.sh --dry-run` to preview files.
Review that list, then use `./scripts/dev/clean.sh --apply` to remove the currently
eligible files. Each invocation computes a fresh list; stop processes that write
to these directories before previewing and applying cleanup.

Cleanup is limited to ignored, untracked regular files within the repository's
root `tmp/`, `.tmp/`, `temp/`, `scratch/`, and `.cache/` directories. Selection uses
Git's effective ignore rules through
[`git ls-files`](https://git-scm.com/docs/git-ls-files). Do not use these directories
for work you need to keep; deleted untracked files cannot be recovered from Git.

The helper leaves tracked files, unignored files, symbolic links and their targets,
nested repositories and worktrees identified by `.git` markers, and files outside
the listed directories in place. It leaves empty directories in place and does not
remove root environment files, editor state, or build output elsewhere. It can be
invoked by path from another working directory and stops if its location is not
the root of a Git working tree.

## Verification

From the repository root, run:

```bash
python3 -m unittest discover -s scripts/dev/tests -v
```

The tests exercise setup, real Git commits, ADR generation, and cleanup in temporary repositories. They do
not change the current checkout's Git configuration. Review and CI enforcement
remain separate from local hook activation.

## Repository Checks

Documentation, credential-filename, and repository-configuration check entry
points are available under `scripts/ci/`. Use the
[repository checks and CI reference](../docs/architecture/ci-cd.md) for their
commands, prerequisites, regression tests, and supported syntax. CI workflows
remain pending.

## Related Documents

- [Contributing](../CONTRIBUTING.md) - Preparing and reviewing changes.
- [Local Git hooks](../.githooks/README.md) - Commit-message validation boundaries.
- [Milestone 0 roadmap](../docs/roadmap/milestone-0-repository-scaffolding.md) - Remaining tooling and automation work.
