# Repository Checks and CI

[Docs](../README.md) > [Architecture](README.md) > Repository Checks and CI

This document owns the commands, coverage, and limitations of repository-wide
validation. [ADR-0003](../adr/0003-enforce-repository-quality-checks.md) records the
accepted approach. The current implementation contains local documentation, credential-filename,
and repository-configuration checks. CI workflows and required GitHub checks
remain pending.

## Commands and Prerequisites

Use Bash 3.2 or newer and Python 3.9 or newer with its standard library. Credential-filename checks and the
regression tests also use Git. Run the local suite from the repository root:

```bash
./scripts/ci/test.sh
```

The suite checks executable shell entry points and Bash syntax, runs the four
repository checks, and then runs the developer and repository regression tests.
It stops at the first failed command. It does not run setup, cleanup, external
linters, or change hook activation or Git settings. Source verification does not
repair files; regression fixtures and Git configuration changes stay in temporary
repositories.

For individual checks or repository regression tests, run:

```bash
./scripts/ci/check-links.sh
./scripts/ci/check-docs.sh
./scripts/ci/check-secrets.sh
./scripts/ci/check-repository.sh
python3 -B -m unittest discover -s scripts/ci/tests -v
```

The shell entry points can also be invoked by path from another working directory.
They report failures and return a nonzero status without repairing source files or
changing Git settings. The tests create temporary repositories and fixtures.

## Documentation Coverage

| Check | Behavior |
| :--- | :--- |
| Links | Checks local Markdown link and image destinations, explicit reference definitions, and Markdown heading fragments; rejects destinations that resolve outside the repository |
| Structure | Requires one ATX top-level heading, sequential heading levels, and closed fenced blocks with a language |
| Documentation navigation | Checks category and document registration, leaf breadcrumbs, Related Documents links, and reachability from the documentation hub under `docs/` |
| Root policies | Checks repository-home breadcrumbs and Related Documents links in CONTRIBUTING, SECURITY, and CODE_OF_CONDUCT |

The Python implementation in [`repo_checks.py`](../../scripts/ci/repo_checks.py)
scans Markdown files in the working checkout, including untracked drafts. It skips
symbolic links and generated, dependency, cache, and disposable directories named
in its `EXCLUDED` set, plus downloaded `.github/styles/` content. CI must run these
same commands against its checkout when workflows are introduced.

## Credential and Configuration Coverage

The [credential-filename check](../../scripts/ci/check-secrets.sh) inspects the Git
index, including newly staged paths. It reports filenames without reading or
printing their contents. It flags environment-file names and common key/container
names defined by `secret_path` in the shared checker. Paths ending in `.example`
are allowed as configuration examples; examples must still contain no credentials.
Untracked local configuration is outside this check's scope.

This is filename hygiene, not content or history scanning. It can flag harmless
files with credential-like names and miss credentials stored under ordinary names.
Resolve reports by reviewing the file's purpose and the canonical policy; do not
assume renaming a real secret makes it safe. Content/history scanning remains
pending the Gitleaks implementation, and credential handling follows the
[security policy](../../SECURITY.md).

The [repository-configuration check](../../scripts/ci/check-repository.sh) verifies
foundation files listed in `REQUIRED_FILES`, executable shell entry points under
`scripts/*/*.sh`, and the commit-message hook. It reports missing permissions
without changing them. The baseline requires neither `.env.example` nor workflows
that have not been introduced.

When `.github/workflows/` contains `.yml` or `.yaml` files, the configuration check
also examines literal `uses:` entries on their own lines. Local `./` references
are allowed; external action and reusable-workflow references must use a full
40-character commit SHA according to the
[dependency standard](../standards/dependencies.md). This narrow text check does
not parse all YAML forms, verify that commits belong to the intended upstream,
or validate workflow semantics; actionlint integration and manual review remain
necessary. Container-action digest support is outside the current check's scope.

## Supported Syntax and Limits

These are bounded repository checks, not a complete Markdown parser or renderer.
They recognize ATX headings, backtick and tilde fences, inline links with optional
titles, reference links, code-formatted link labels, encoded paths, and simple
balanced parentheses in destinations. Fenced examples, inline code examples,
and HTML comments are excluded from link checks.

Heading fragments use an approximation of GitHub's generated anchors, including
suffixes for repeated headings. Unusual markup and custom anchors need manual
verification; extend the checker with regression cases when adopting new syntax.
HTML links, embedded YAML links, external URL availability, and every Markdown
extension are outside this check's coverage. External URLs are skipped, so this
check also does not enforce the documentation standard's relative-link preference.

Navigation checks verify the presence of links, not their usefulness or the
technical accuracy of the text. The documentation agent file is exempt from leaf
breadcrumb and related-link checks, but must remain registered and reachable.
Manual review remains responsible for the full
[documentation standard](../standards/documentation.md).

## Enforcement Status

| Area | State |
| :--- | :--- |
| Documentation links and structure | Local scripts and focused regression tests |
| Developer helpers | Regression tests included in the local suite; individual usage in the [script reference](../../scripts/README.md) |
| Credential filenames and repository configuration | Local scripts and regression tests; content/history scanning remains pending |
| ShellCheck, actionlint, Vale, and Gitleaks integration | Pending configuration, dependency evaluation, and reproducible commands |
| CI workflows and dependency updates | Pending implementation |
| Required status checks and review/merge settings | Pending configuration and verification in the target repository |

Local checks do not configure merge protection. Introduce workflows and required
settings only with verified implementation, and update this document as each
part becomes available. The [roadmap](../roadmap/README.md) tracks those groups.

## Related Documents

- [Documentation standards](../standards/documentation.md) - Canonical writing and navigation rules.
- [ADR-0003](../adr/0003-enforce-repository-quality-checks.md) - Shared quality-checking approach.
- [Script reference](../../scripts/README.md) - Developer helpers and their regression suite.
- [Git workflow](../standards/git-workflow.md) - Review requirements and enforcement status.
