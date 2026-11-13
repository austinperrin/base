# Script Reference

[Repository Home](../README.md) > Script Reference

This index documents the helpers currently available in the repository.

## Prerequisites

The setup script and hook require Bash 3.2 or newer, Git, and standard command-line
utilities. On Windows, run them in Git Bash or a compatible environment. The ADR
generator, disposable-file cleanup, project-initialization helper, and regression
tests additionally require Python 3.9 or newer with its standard library.

## Developer Tools

| Script | Behavior | Usage from the repository root |
| :--- | :--- | :--- |
| [setup.sh](dev/setup.sh) | Configures the local commit-message hook after checking for conflicts | `./scripts/dev/setup.sh` |
| [new-adr.sh](dev/new-adr.sh) | Creates the next numbered Proposed ADR from the current template | `./scripts/dev/new-adr.sh "Choose storage"` |
| [clean.sh](dev/clean.sh) | Previews disposable ignored files; deletes only with `--apply` | `./scripts/dev/clean.sh --dry-run` |
| [initialize-project.py](dev/initialize-project.py) | Previews or applies one-time project setup and cleanup | `python3 scripts/dev/initialize-project.py --help` |

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

## One-Time Project Initialization

The [initialization runbook](../docs/runbooks/initialize-repository.md) owns the
setup order. `initialize-project.py configure` previews fixed source URL and
reporting-contact replacements; `finish` previews a project-owned Milestone 0
record and removal of one-time files. Each stage requires `--apply` to write
changes. The helper checks the destination GitHub remote, refuses modified
removal candidates, and checks documentation after applying changes. It leaves
the root README, review owners, ADR outcomes, and live repository settings for
the maintainer to resolve.

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

The local suite entry point is [`scripts/ci/test.sh`](ci/test.sh). It runs the
available documentation, credential-filename, and repository-configuration checks,
Bash syntax and permission checks, and developer, CI, and operational regression suites. The separate
[ShellCheck entry point](ci/check-shell.sh) adds static shell analysis when its
pinned tool is installed. The separate
[workflow check](ci/check-workflows.sh) validates workflow files with pinned
actionlint; it reports when there are no workflows to validate. The separate
[prose check](ci/check-prose.sh) applies pinned Vale and Google rules after style
installation. The separate [credential content check](ci/check-credentials.sh)
scans current-branch history and staged changes with redacted Gitleaks output.
The [local checks reference](../docs/architecture/repository-checks.md) describes
suite commands, supported syntax, and limits. The
[external checks reference](../docs/architecture/external-checks.md) covers pinned
tools and their tests. The [CI workflows reference](../docs/architecture/ci-cd.md)
covers hosted jobs. The [tool installer](ci/install-tools.py) prepares pinned Linux
executables and style rules; see the
[verified installation reference](../docs/architecture/external-checks.md#verified-tool-installation)
for its write boundaries and usage. Use the
[repository settings checklist](../docs/architecture/repository-settings.md) to
verify live CI and required checks in each repository.

## Release Verification

Run [`verify-release.sh`](ops/verify-release.sh) with the reviewed Git tag:

```bash
read -r -p 'Reviewed release tag: ' release_tag
./scripts/ops/verify-release.sh "$release_tag"
```

The [release-verification reference](../docs/architecture/ci-cd.md#release-verification)
owns prerequisites, gate behavior, and limitations. The
[release process](../docs/runbooks/release-process.md) owns version selection,
tagging, publication, and recovery. The helper verifies readiness without creating
a tag or release and can be invoked by path from another directory.
It checks Git tag syntax without selecting a versioning scheme. The
[versioning decision](../docs/adr/0004-release-versioning.md) remains Proposed.

Operational regression tests use temporary repositories and a fake GitHub CLI:

```bash
python3 -B -m unittest discover -s scripts/ops/tests -v
```

## Related Documents

- [Contributing](../CONTRIBUTING.md) - Preparing and reviewing changes.
- [Local Git hooks](../.githooks/README.md) - Commit-message validation boundaries.
- [Repository roadmap](../docs/roadmap/README.md) - Project milestones and planned work.
