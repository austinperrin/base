# External Checks and Installation

[Docs](../README.md) > [Architecture](README.md) > External Checks and Installation

This document owns the pinned external check tools, their local use, installation,
coverage, and limits. The [CI workflow](ci-cd.md#core-ci-workflow) installs and runs
them on pull requests and main.

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
provides the pinned version. The [verified tool installer](#verified-tool-installation) provides the Linux CI
installation and archive-integrity checks.

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
package-manager installations must provide the required version. The [verified tool installer](#verified-tool-installation) provides the Linux CI
installation.

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
fails with setup instructions when the package is missing. The [verified tool installer](#verified-tool-installation) installs the pinned
package for CI after checking its archive hash; it does not invoke `vale sync`.

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

The [project vocabulary](../../.github/styles/config/vocabularies/Project/accept.txt)
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

## Gitleaks

Run the separate [credential content check](../../scripts/ci/check-credentials.sh)
after installing its pinned Gitleaks version:

```bash
./scripts/ci/check-credentials.sh
```

The wrapper's `required_version` pins Gitleaks to `8.30.1`. Obtain the matching
OS/architecture binary from the
[fixed upstream release](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1),
verify it against the published release checksums, and install it outside the
checkout on `PATH`. Confirm the version with `gitleaks version`. The [verified tool installer](#verified-tool-installation) provides the Linux CI
installation; no binary is bundled here.

### Scan Scope and Output

The wrapper scans commits reachable from the checkout's `HEAD`, then staged
changes, using the explicit [project configuration](../../.gitleaks.toml). That
configuration extends the pinned engine's default rules and upstream allowlists;
it adds no project exclusions. Inline `gitleaks:allow` comments do not suppress
findings through this wrapper. Any future exception configuration must be reviewed
with its rationale instead of being used to dismiss a real exposure.

The command requires an existing commit and complete current-branch history. A
shallow checkout fails with instructions to fetch history; CI must provide that
history. It does not scan unrelated branches, unreachable commits, untracked files,
or unstaged edits. It does not create a report artifact or modify Git history.
Output uses full redaction and no verbose findings. Filenames and scan metadata
can still appear in diagnostic messages; do not publish sensitive context casually.

The first failed scan stops the command. Detection is pattern-based and incomplete;
a pass is not proof that credentials are absent. Use the
[security policy](../../SECURITY.md) for reporting and revoking exposed credentials.
Neither this check nor filename hygiene selects how the project stores
or delivers secrets.

### Dependency Evaluation

Gitleaks provides content and history detection beyond filename matching. Its
[upstream project](https://github.com/gitleaks/gitleaks) publishes MIT-licensed
sources, release binaries, configuration documentation, and rule definitions.
The reviewed release includes security-relevant report-template changes; pinned
rules and representative fixtures allow updates to be assessed together.

A standalone executable avoids a Go compiler dependency for contributors while
adding tool updates and scan-scope maintenance. Default allowlists and detection
patterns can miss exposures or report harmless values. Review changes and upstream
security information under the [dependency standard](../standards/dependencies.md).
See the [upstream usage and configuration](https://github.com/gitleaks/gitleaks/tree/v8.30.1)
for the scanner's behavior and limitations.

Tests use temporary repositories and synthetic, unusable token-shaped values.
They verify redaction, staged detection, detection after a value is removed from
history, scan arguments, shallow-checkout rejection, and failure propagation.
Real-scanner integration tests require the pinned executable on `PATH`; otherwise
they are explicitly skipped. The core suite does not require external scanners.

## Verified Tool Installation

The [tool manifest](../../scripts/ci/tools.json) records versions, official release
URLs, archive SHA-256 hashes, and executable archive members. Hashes were checked
against upstream release metadata. Update these pins and wrapper versions together,
then review the upstream releases and run the installer and real-tool fixtures.

The [installer](../../scripts/ci/install-tools.py) requires Python 3.9 or newer and
network access. It prepares Linux AMD64 artifacts only and never executes them;
macOS and Windows contributors can continue to use the individual installation
instructions above. For Linux tools, run:

```bash
python3 scripts/ci/install-tools.py --platform linux-amd64 --destination /tmp/repository-tools
export PATH="/tmp/repository-tools:$PATH"
```

Choose a destination for your environment; CI uses its job-local runner temporary
directory. By default, all four executables are installed there and Google rules
replace only the ignored `.github/styles/Google/` cache. Project vocabulary under
`config/` is preserved. Use repeatable `--tool` options to select individual tools,
and `--styles-path` to prepare a style cache elsewhere.

The installer checks each complete archive before publishing its contents. It
extracts only the expected executable from tar archives, rejects unexpected ZIP
paths and symbolic links, limits download and extraction sizes, and does not run
remote installation scripts. A mismatched hash fails without replacing that tool.
Installation is per artifact rather than a transaction across all tools; earlier
successful installations remain if a later download fails. It does not change
shell profiles or automatically add executables to `PATH`.

Checksums bind installation to the reviewed bytes; they do not establish that an
upstream release is free from vulnerabilities. Archive updates require the
[dependency evaluation](../standards/dependencies.md), including applicable upstream
integrity and attestation guidance. The installer does not verify build
attestations automatically; it uses reviewed hash pins without adding a GitHub CLI
or authentication prerequisite. Review available upstream attestations when
refreshing pins. The installer is separate from read-only check commands and is
not invoked by the core suite.

## Related Documents

- [Local repository checks](repository-checks.md) - Built-in checks and their limits.
- [CI workflows and enforcement](ci-cd.md) - Hosted execution and required settings.
- [Dependency management](../standards/dependencies.md) - Tool evaluation and updates.
