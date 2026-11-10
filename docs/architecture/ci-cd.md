# Repository Checks and CI

[Docs](../README.md) > [Architecture](README.md) > Repository Checks and CI

This document owns the commands, coverage, and limitations of repository-wide
validation. [ADR-0003](../adr/0003-enforce-repository-quality-checks.md) records the
accepted approach. The current implementation contains local documentation, credential-filename,
and repository-configuration checks. Core and external-check CI jobs run on pull requests and main-branch changes. The
[verification record](phase-6-verification.md) contains observed enforcement
results and maintainer-approved follow-ups; the
[roadmap](../roadmap/milestone-0-repository-scaffolding.md#phase-6-verification)
records phase completion.

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
assume renaming a real secret makes it safe. The separate [Gitleaks check](#gitleaks)
covers staged content and current-branch history; credential handling follows the
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
Neither this check nor filename hygiene selects how the adopting project stores
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

## Core CI Workflow

The [Repository Checks workflow](../../.github/workflows/repo-lint.yml) runs the
same core suite on `ubuntu-24.04` and `macos-15`. It runs for pull requests against
any base branch, pushes to `main`, and manual dispatch where GitHub permits it.
Unfiltered pull request bases support the planned phase branches without adding
scaffolding-specific branch names. There are no path filters that could leave a
required check waiting after an unrelated file change.

Each job has a 15-minute timeout and runs on a fresh hosted runner. The workflow
uses `contents: read` permissions and a pinned checkout action with persisted
credentials disabled. Pull request code runs under `pull_request`, without project
secrets or a privileged `pull_request_target` checkout. It does not publish,
deploy, modify repository settings, or upload artifacts. A final step rejects
tracked changes or ordinary untracked files left by the suite.

The core suite relies on runner-provided Bash, Git, and Python and checks its
prerequisites. Optional real-tool integration tests run only when the exact pinned
version is available; mismatched runner tools cause explicit skips rather than
making the core suite depend on ambient versions. The external-check job installs the required versions and reruns the suite so
those integration tests execute with the pinned tools.

### External-Check Job

`External checks (Linux)` uses `ubuntu-24.04` with the same read-only token and a
15-minute timeout. It checks out full history, installs the pinned executables into
`RUNNER_TEMP`, prepares the Google cache, reruns the core suite with the real tools,
and invokes all four external check wrappers. The final checkout-cleanliness step
permits ignored tool caches while rejecting ordinary source changes.

Full history supports the documented Gitleaks scan scope. This job does not upload
scan reports, publish packages, or require project secrets. It is defined for the
same events as the core matrix. Separate scheduled scanning and PR-title
workflows are described below. Verify execution in each target repository.

### Checkout Dependency Evaluation

The workflow pins `actions/checkout` to the upstream commit for `v7.0.1`, verified
against that repository's release tag. Its
[release documentation](https://github.com/actions/checkout/blob/v7.0.1/README.md)
describes security and dependency updates and the hosted-runner requirements. The
[MIT-licensed action](https://github.com/actions/checkout/blob/v7.0.1/LICENSE)
provides the checkout without adding an application dependency; it brings its own
Node runtime and packaged dependencies, which still require update review.

Supported runner labels were checked against the
[runner image list](https://github.com/actions/runner-images#available-images).
OS labels limit major image changes but do not freeze installed software. Review
image retirements and action updates under the
[dependency standard](../standards/dependencies.md). A local actionlint pass checks
the workflow definition; it does not verify a live run or repository permissions.

### Activation and Verification

The initial project run passed both matrix jobs and the external-check job; see
the roadmap evidence above. For each adopting repository or subsequent workflow
change, inspect the intended commit, results and skips, tool versions, and
clean-checkout steps. External-check integration tests must not be
skipped when their prerequisites are installed.
Fork pull requests may require maintainer approval under GitHub settings. Manual
dispatch availability depends on the workflow being on the default branch.

The [repository settings checklist](repository-settings.md#required-pull-request-checks)
owns required check names and live setup. A YAML definition alone does not make
these checks mandatory.

## Pull Request Titles

The [Pull Request Title workflow](../../.github/workflows/pr-title.yml) validates
the title against the [Git workflow convention](../standards/git-workflow.md) on
opened, edited, synchronized, reopened, and ready-for-review pull requests. It
checks the complete title, including the optional scope and breaking marker, and
rejects empty descriptions and control characters.

This workflow uses `pull_request_target` only to process event metadata. It checks
out no repository code, invokes no external action, grants no token permissions,
and reads the title from `GITHUB_EVENT_PATH` as JSON data rather than inserting it
into a shell script. It prints generic results instead of echoing untrusted titles.
A per-PR concurrency group cancels stale runs after later title updates.

The inline Python uses the hosted runner's standard library so validation needs
neither contribution code nor a package installation. Its exact code is exercised
by regression fixtures, including hostile-looking shell text and agreement with
the local hook on representative subjects. Human review still assesses whether
the title describes the change accurately.

Activation requires GitHub to use a base-branch workflow containing this definition; initial
phase PRs may precede that availability. Verify title edits, fork PR behavior, and
the attached check on GitHub before making it required. See GitHub's
[event guidance](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target)
and [script-injection guidance](https://docs.github.com/en/actions/reference/security/secure-use#good-practices-for-mitigating-script-injection-attacks).

## Scheduled Credential Scanning

The [Scheduled Credential Scan workflow](../../.github/workflows/security.yml)
uses the same verified installer and Gitleaks wrapper as the external-check job.
It runs weekly on Monday at 04:23 UTC and supports manual dispatch. It installs
only Gitleaks, checks out full history without persisting credentials, and uses
`contents: read` permissions with a ten-minute timeout. No project secrets or
report uploads are configured.

GitHub schedules run from the default branch and can be delayed or disabled by
platform conditions. Confirm the schedule is active after the workflow reaches
the default branch; see GitHub's
[schedule guidance](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).
Manual dispatch also depends on default-branch workflow availability. Inspect a
live run and its checkout commit before claiming operational coverage.

`Scheduled credential scan` is a maintenance check, not a pull request check;
do not add it to required PR status checks. Main pushes and PRs already receive
credential scanning through `External checks (Linux)`. Handling findings follows
the [security policy](../../SECURITY.md); scheduled scanning does not rotate or
revoke credentials.

## Repository Settings and Dependency Updates

The [repository settings checklist](repository-settings.md) owns required checks,
review and merge controls, activation requirements, and live verification evidence.
The [dependency standard](../standards/dependencies.md#automated-updates-and-auditing)
describes configured update coverage and tool pins that still require manual review.
Neither document configures live GitHub settings by itself.

## Release Verification

The [release helper](../../scripts/ops/verify-release.sh) runs the local suite and
verifies Git tag syntax and availability, a clean `main` checkout, live origin state, and
the latest `Repository Checks` push run for the exact commit. It requires all
three named core and external jobs to have succeeded, rejecting missing, skipped,
failed, or ambiguous job results. A previous success cannot mask a newer pending
or failed run. It queries the workflow by `repo-lint.yml`, not a display-name guess.

The helper uses Bash, Git, Python, and authenticated GitHub CLI access. It supports
GitHub origins with HTTPS or SSH URLs, explicitly targets the origin repository
for API calls, and checks the push destination against the fetch destination.
It checks local and live remote tag availability and compares local `HEAD` with
live remote `main`, rather than trusting a potentially stale tracking ref. It
rechecks repository state after the local suite and then verifies hosted CI.

Release verification does not modify source files, Git configuration, branches,
or tags, and it does not publish a release. It requires network access and a
successful push run; an API failure or unavailable results stop verification.
The PR-title workflow runs on PR metadata, and the scheduled credential scanner
runs separately; neither is incorrectly required as a push job. The external
push job already includes credential scanning with full-history checkout.

The helper uses `git check-ref-format` for tag syntax and rejects empty or
option-like names. It does not enforce SemVer, calendar fields, version increments,
or package-registry rules. [ADR-0004](../adr/0004-release-versioning.md) leaves the
versioning policy Proposed; the release runbook requires the project to approve
that policy before publication. Accepting a tag is not evidence of policy approval.

Readiness applies to the inspected commit and state, not to future changes.
There is no atomic reservation of a version tag. The operator must retain the
verified commit, confirm the final target, and review notes and support scope
through the [release process](../runbooks/release-process.md).

Regression coverage uses temporary Git repositories, a local bare remote, and a
fake GitHub CLI. It tests exact-commit and job gates, stale successes, dirty or
wrong-branch checkouts, tag collisions, failure propagation, and explicit API
targeting. It creates no real release and requires no GitHub authentication.

## Enforcement Status

| Area | State |
| :--- | :--- |
| Documentation links and structure | Local scripts and focused regression tests |
| Developer helpers | Regression tests included in the local suite; individual usage in the [script reference](../../scripts/README.md) |
| Credential filenames and repository configuration | Local scripts and regression tests |
| ShellCheck | Pinned local check and external CI job; initial PR execution verified |
| actionlint | Pinned local check and external CI job; initial PR execution verified |
| Vale | Pinned local check, Google rules, vocabulary, and external CI job; initial PR execution verified |
| Gitleaks | Pinned local check and external CI job with redacted output; initial PR execution verified |
| Core CI workflow | Initial Linux and macOS PR jobs verified; see roadmap evidence |
| External-check CI job | Initial PR job verified with all real-tool fixtures; see roadmap evidence |
| PR-title validation and scheduled scanning | Title edits and manual scanner dispatch verified; see the [verification record](phase-6-verification.md) for scheduled-event follow-up |
| Dependency updates | GitHub Actions update job verified; update-PR follow-up is recorded in the [verification record](phase-6-verification.md) |
| Required status checks and review/merge settings | Live configuration and merge blocking verified; see the [verification record](phase-6-verification.md) for the approved review policy |

Local checks do not configure merge protection. Apply the repository settings
checklist against verified workflow behavior, and update this document as each
part becomes available. The [roadmap](../roadmap/README.md) tracks those groups.

## Related Documents

- [Documentation standards](../standards/documentation.md) - Canonical writing and navigation rules.
- [ADR-0003](../adr/0003-enforce-repository-quality-checks.md) - Shared quality-checking approach.
- [Script reference](../../scripts/README.md) - Developer helpers and their regression suite.
- [Git workflow](../standards/git-workflow.md) - Review requirements and enforcement status.
