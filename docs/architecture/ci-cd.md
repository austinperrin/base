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

## ShellCheck

Run the separate [shell check](../../scripts/ci/check-shell.sh) after installing
the version it requires:

```bash
./scripts/ci/check-shell.sh
```

The wrapper pins ShellCheck to `0.11.0`, as recorded in its `required_version`.
Obtain the matching OS/architecture archive from the
[fixed upstream release](https://github.com/koalaman/shellcheck/releases/tag/v0.11.0),
extract it outside the checkout, and put the executable on `PATH`. Follow the
[upstream installation instructions](https://github.com/koalaman/shellcheck#installing)
for supported distributions or building that release from source. Verify with
`shellcheck --version`; a package manager installation is suitable only if it
provides the pinned version. No automatic installer is included. CI installation
and artifact-integrity verification remain part of the workflow review group.

The check covers `scripts/*/*.sh` and `.githooks/commit-msg`. It reports enabled
diagnostics at style severity and above, uses `--norc`, and clears
`SHELLCHECK_OPTS` for a consistent baseline. It does not execute scripts or repair
files. The core local suite remains independent of an external linter installation.

### Dependency Evaluation

ShellCheck adds semantic shell analysis beyond `bash -n`, without introducing an
application package manager. Its published release and upstream diagnostic wiki
provide versioned tooling and explanations. The
[upstream project](https://github.com/koalaman/shellcheck) identifies its license as
GPLv3; the tool remains an external development dependency and is not bundled in
this repository. Review any future redistribution separately.

The reviewed release notes describe the selected version's changes. The upstream
[security page](https://github.com/koalaman/shellcheck/security) is a reporting and
review reference, not evidence that the tool has no vulnerabilities. Installation
provenance and future updates remain maintainer responsibilities under the
[dependency standard](../standards/dependencies.md). Using a release binary avoids
a Haskell build dependency for contributors, at the cost of maintaining an external
executable for each supported platform.

Regression tests cover missing and incorrect versions, consistent invocation,
argument handling, and nonzero status propagation. A real-tool integration test
verifies a valid script and an unquoted-expansion failure when ShellCheck is on
`PATH`; otherwise that integration test is explicitly skipped. Verify the wrapper
against the real pinned tool before accepting an update.

## actionlint

Run the separate [workflow check](../../scripts/ci/check-workflows.sh) with its
pinned actionlint version installed:

```bash
./scripts/ci/check-workflows.sh
```

The wrapper's `required_version` pins actionlint to `1.7.12`. Select the matching
OS/architecture archive from the
[fixed upstream release](https://github.com/rhysd/actionlint/releases/tag/v1.7.12),
verify it against the release's published checksums and follow the upstream
recommendation to verify its artifact attestation, extract it outside the checkout, and put the executable on `PATH`. See the
[versioned installation guide](https://github.com/rhysd/actionlint/blob/v1.7.12/docs/install.md)
for supported installation methods. Confirm the version with `actionlint -version`;
package-manager installations must provide the required version. CI installation
will be introduced with the workflows.

The wrapper checks `.github/workflows/*.yml` and `*.yaml` with explicit file
arguments, including paths with spaces. When no workflows exist, it reports that
validation is not applicable instead of claiming workflows passed.

This entry point checks workflow structure, expressions, and action usage. Its
ShellCheck and pyflakes integrations are explicitly off so results do not depend
on which optional run-block linters happen to be installed. The separate shell
check covers repository shell files, not embedded workflow scripts; run-block
linting must be reviewed with the actual workflows. See
[actionlint usage](https://github.com/rhysd/actionlint/blob/v1.7.12/docs/usage.md)
for those boundaries. Static validation does not verify live permissions, remote
action provenance, or repository settings, and does not execute a workflow.

### Dependency Evaluation

The project-specific action-reference check only covers literal SHA pinning;
actionlint adds workflow syntax and expression validation without requiring an
application runtime or package manager. The upstream provides release binaries,
checksums, installation documentation, and versioned check descriptions. Its
[MIT license](https://github.com/rhysd/actionlint/blob/v1.7.12/LICENSE.txt) is retained
upstream; no binary is bundled here.

The selected release's notes were reviewed for supported runner labels and workflow
syntax. Its built-in data can lag GitHub changes, so updates require representative
valid and invalid workflow fixtures under the
[dependency standard](../standards/dependencies.md). A standalone binary avoids a
Go compiler dependency for contributors but adds version and platform maintenance.
Review upstream security notices and installation provenance with updates; static
linting does not establish that workflow execution is safe.

Regression tests cover prerequisites, both filename extensions, argument handling,
nonzero exit propagation, and the no-workflow case. When the pinned tool is on
`PATH`, an integration test checks a valid workflow and rejects an unknown
expression context; otherwise that test is explicitly skipped.

## Vale

Use the separate [prose check](../../scripts/ci/check-prose.sh) with the pinned
Vale engine and installed style package:

```bash
vale sync --config=.vale.ini
./scripts/ci/check-prose.sh
```

Install Vale `3.26.0`, as pinned by the wrapper's `required_version`, from the
[fixed upstream release](https://github.com/vale-cli/vale/releases/tag/v3.26.0).
Choose the artifact for your OS and architecture, verify its published integrity
information, and install it outside the checkout on `PATH`. Confirm the result
with `vale --version` before syncing styles.

[`.vale.ini`](../../.vale.ini) pins the Google style package by release URL and
defines the enabled styles and default alert level. `vale sync` downloads that
package into ignored `.github/styles/` paths; it is a separate preparation step
that requires network access. The check itself does not sync or repair files and
fails with setup instructions when the package is missing. Verify installation
provenance when introducing automated downloads in CI.

The wrapper uses the explicit project configuration and `--no-global` to exclude
personal configuration. It checks `docs/`, the root README, CONTRIBUTING, SECURITY,
AGENTS, the script reference, and local-hook documentation. Contributor Covenant
text and contribution templates are outside this entry point's scope. Code spans,
fenced examples, and configured Mermaid content are excluded from prose analysis.

Enabled errors block the check. Warnings and suggestions remain available for
editorial review by running the pinned engine without the wrapper's error-level
override:

```bash
vale --no-global --config=.vale.ini docs README.md CONTRIBUTING.md
```

The [project vocabulary](../../.github/styles/config/vocabularies/Base/accept.txt)
contains reviewed technical terms that would otherwise produce spelling or term
alerts. Add terms with context and review; avoid blanket exclusions for prose that
should be corrected. Any rule changes belong in the configuration with an explained
reason. The [documentation standard](../standards/documentation.md) remains the
canonical editorial policy; these enabled rules cover only its mechanical subset.

### Dependency Evaluation

Vale supplies configurable prose analysis without selecting an application stack.
Its [upstream project](https://github.com/vale-cli/vale) and the
[Google rule package](https://github.com/vale-cli/Google) publish MIT-licensed
sources. The rule package is maintained separately from Google and does not
establish complete compliance with Google's guide.

The selected engine and rule releases were reviewed together using the current
repository and a fixture that rejects an exclamation in prose while allowing the
same text inside a fenced example. A release executable avoids a Go build toolchain
for contributors. Maintenance includes reviewing both engine and rule updates,
false positives, vocabulary, and upstream security information under the
[dependency standard](../standards/dependencies.md).

Wrapper tests verify prerequisites, configuration isolation, error severity, and
failure propagation without downloading packages. The real-rule integration test
runs when the pinned engine and downloaded Google rules are available, and is
explicitly skipped otherwise. CI must install those prerequisites to exercise it.

## Enforcement Status

| Area | State |
| :--- | :--- |
| Documentation links and structure | Local scripts and focused regression tests |
| Developer helpers | Regression tests included in the local suite; individual usage in the [script reference](../../scripts/README.md) |
| Credential filenames and repository configuration | Local scripts and regression tests; content/history scanning remains pending |
| ShellCheck | Separate pinned local check and regression tests; CI installation pending |
| actionlint | Separate pinned local check and regression tests; no workflows introduced yet |
| Vale | Pinned local prose check, Google rules, vocabulary, and regression tests; CI installation pending |
| Gitleaks integration | Pending configuration, dependency evaluation, and reproducible commands |
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
