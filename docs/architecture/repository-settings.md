# Repository Settings and Verification

[Docs](../README.md) > [Architecture](README.md) > Repository Settings

This checklist owns the GitHub settings and live verification needed to enforce
repository policies. It applies to this repository and projects adopting it.
Its presence does not configure the platform. Record results for the target
repository separately; the [Phase 6 verification record](phase-6-verification.md)
contains this repository's observed settings, results, and remaining cases.

## Prerequisites and Ownership

- [ ] Identify the target repository, its default branch, maintainers, and applicable
  organization rules. Confirm feature availability for its visibility and plan.
- [ ] Inspect existing settings and protections before making changes. Preserve
  protections already in place and resolve conflicts with the responsible maintainers.
- [ ] Assign review owners according to the [ownership standard](../standards/ownership.md).
  The commented CODEOWNERS scaffold does not assign real owners or grant access.
- [ ] Confirm that the workflow files and their supporting scripts exist on the
  branches where GitHub requires them. Initial phase PRs can precede activation;
  record the remaining setup rather than claiming those checks are already enforced.

Use GitHub's [ruleset guidance](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
and the [external platform guidance](../standards/README.md#external-platform-guidance)
when applying these requirements. Adopters using another provider need equivalent
controls and verification appropriate to that provider.

## Actions and Workflow Activation

- [ ] Enable the reviewed workflows under the repository and organization Actions
  policies. Keep token permissions minimal and allow only the actions needed by
  the approved implementation.
- [ ] Run the [repository suite and external-check jobs](ci-cd.md#core-ci-workflow)
  on a representative PR. Inspect each job, tool version, test result, expected
  real-tool integration coverage, and checkout-cleanliness step for that commit.
- [ ] Verify contribution behavior from a fork without providing project secrets
  or exposing a privileged checkout. Confirm any required maintainer approval.
- [ ] Verify the [title check](ci-cd.md#pull-request-titles) on valid and invalid
  titles and after title edits. Confirm its check is attached to the intended PR.
- [ ] After the default branch contains the workflow, dispatch the
  [scheduled scanner](ci-cd.md#scheduled-credential-scanning) and confirm full
  history, redacted output, and the expected checkout commit. Check schedule activation.

Workflow behavior, commands, and limitations belong to the
[checks reference](ci-cd.md). Local validation alone does not satisfy these items.

## Required Pull Request Checks

Select check names from actual runs and compare them with this list before making
them required. Use the GitHub Actions check source when the platform offers that
restriction. Keep this list aligned when job names or runner labels change.

| Check name | Workflow | Purpose |
| :--- | :--- | :--- |
| `Repository checks (ubuntu-24.04)` | [Repository Checks](../../.github/workflows/repo-lint.yml) | Core checks and regression tests on Linux |
| `Repository checks (macos-15)` | [Repository Checks](../../.github/workflows/repo-lint.yml) | Core checks and regression tests on macOS |
| `External checks (Linux)` | [Repository Checks](../../.github/workflows/repo-lint.yml) | Pinned tools, real-tool fixtures, and external checks |
| `Validate Conventional Commit PR title` | [Pull Request Title](../../.github/workflows/pr-title.yml) | Conventional PR title validation |

- [ ] Make the verified PR checks required for the protected default branch.
  Confirm the rule applies to the intended branch and is enforcing its requirements.
- [ ] Confirm an ordinary PR with a missing or failed required check cannot merge.
  Resolve failures through the owning standard and check implementation.
- [ ] Confirm passing checks still require the configured human review.
- [ ] Keep scheduled-only jobs out of required PR checks. They do not run for each PR.

See GitHub's [required-check guidance](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/troubleshooting-rules#troubleshooting-required-status-checks)
for naming and configuration. If a project adopts a merge queue, add and verify
`merge_group` handling before relying on these workflows for queued merges.

## Review and Merge Controls

Follow the [Git workflow](../standards/git-workflow.md) for policy; configure its
controls in the target repository:

- [ ] Require pull requests for default-branch changes and resolution of review
  conversations before merging.
- [ ] Record the required approval count and eligible reviewers under the project's
  review policy. Confirm those reviewers can satisfy the requirement; unresolved
  reviewer assignments remain pending setup.
- [ ] Configure required owner reviews once real CODEOWNERS mappings and reviewer
  access have been verified. Review dismissal and latest-change approval options
  against the project's review policy.
- [ ] Protect the default branch against deletion and force pushes. Inspect all
  applicable rules so that protection is effective for the intended users and apps.
- [ ] Enable squash merging and select the PR title as the default squash commit
  title. Limit merge methods to the approved squash workflow and verify the
  proposed title before merging. See GitHub's
  [squash settings](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests).

## Dependency and Security Features

- [ ] Confirm [Dependabot configuration](../../.github/dependabot.yml) is on the
  default branch and its update job can inspect GitHub Actions. Verify an update
  PR has the intended title and passes the same checks and review as other changes.
- [ ] Evaluate dependency graph, advisory alerts, and security updates for the
  project's actual supported ecosystems. The Actions version-update configuration
  does not establish coverage for every dependency or downloaded tool.
- [ ] Verify the reporting channels documented in the [security policy](../../SECURITY.md).
  Enable private vulnerability reporting if the project intends to use it and the
  feature is available; otherwise confirm the documented private contact works.
- [ ] Recheck repository-specific URLs and accounts when adopting the foundation.
  Keep tool and rule updates covered by the [dependency standard](../standards/dependencies.md).

## Verification Evidence

Record the target repository, date, responsible maintainer, applicable rule names,
and links to representative runs and PRs in a setup issue or review record.
Include successful and rejected cases, configuration still pending, and feature
limitations. Keep project progress in the [roadmap](../roadmap/README.md) and link
to that evidence rather than duplicating status throughout the documentation.

The initial phase-branch integration must account for workflows that become
available only after earlier changes reach the target branch. Do not mark a
setting verified solely because its intended value appears in this checklist.

## Related Documents

- [Repository checks and CI](ci-cd.md) - Implemented jobs and their limits.
- [Git workflow](../standards/git-workflow.md) - Contribution and merge policy.
- [Ownership](../standards/ownership.md) - Maintainer and review-owner responsibilities.
- [Dependency management](../standards/dependencies.md) - Evaluation and update policy.
