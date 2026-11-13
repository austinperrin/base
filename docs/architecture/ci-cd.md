# CI Workflows and Enforcement

[Docs](../README.md) > [Architecture](README.md) > CI Workflows and Enforcement

This document owns hosted workflow behavior and enforcement boundaries.
[ADR-0003](../adr/0003-enforce-repository-quality-checks.md) records the accepted
approach. The [local repository checks](repository-checks.md) and
[external checks](external-checks.md) document commands, coverage, installation,
and limitations. Verify settings and workflows in each project repository.

## Core CI Workflow

The [Repository Checks workflow](../../.github/workflows/repo-lint.yml) runs the
same core suite on `ubuntu-24.04` and `macos-15`. It runs for pull requests against
any base branch, pushes to `main`, and manual dispatch where GitHub permits it.
Unfiltered pull request bases support topic branches without adding
branch-specific names. There are no path filters that could leave a
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

For each repository or subsequent workflow change, inspect the intended commit,
results and skips, tool versions, and clean-checkout steps. External-check
integration tests must not be skipped when their prerequisites are installed.
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
| ShellCheck | Pinned local check and external CI job; confirm execution in the target repository |
| actionlint | Pinned local check and external CI job; confirm execution in the target repository |
| Vale | Pinned local check, Google rules, vocabulary, and external CI job |
| Gitleaks | Pinned local check and external CI job with redacted output |
| Core CI workflow | Linux and macOS jobs; inspect the target commit and results |
| External-check CI job | Real-tool fixtures; inspect the target commit and results |
| PR-title validation and scheduled scanning | Separate workflows; verify title edits and scanner dispatch in the target repository |
| Dependency updates | GitHub Actions version-update configuration; verify the first applicable job and PR |
| Required status checks and review/merge settings | Configure and verify in each target repository using the [settings checklist](repository-settings.md) |

Local checks do not configure merge protection. Apply the repository settings
checklist against verified workflow behavior, and update this document as each
part becomes available. The [roadmap](../roadmap/README.md) tracks those groups.

## Related Documents

- [Local repository checks](repository-checks.md) - Built-in commands and supported syntax.
- [External checks and installation](external-checks.md) - Pinned tools and scan limits.
- [ADR-0003](../adr/0003-enforce-repository-quality-checks.md) - Shared quality-checking approach.
- [Repository settings and verification](repository-settings.md) - Required checks and live controls.
