# Configure GitHub Repository Settings

[Docs](../README.md) > [Runbooks](README.md) > Configure GitHub Repository Settings

## Objective and Triggers

Use this procedure after creating a GitHub repository from the foundation or
when its owners, workflows, or review requirements change. Configure the controls
in the [repository settings checklist](../architecture/repository-settings.md)
and verify them in the target repository. This runbook gives the sequence; the
checklist owns the required controls and check names.

## Prerequisites and Access

- Identify the target repository, its default branch, visibility, applicable
  organization rules, and a maintainer with permission to change its settings.
- Complete the [identity and contact setup](initialize-repository.md#set-identity-and-reporting-contacts)
  for identity and reporting contacts before inviting reports or relying on
  the issue forms.
- Confirm `.github/workflows/`, `.github/dependabot.yml`, and the scripts they call
  are on the default branch. Have a representative pull request available for
  observing check names and results.
- Decide who can review changes and whether CODEOWNERS entries name eligible
  accounts. A single maintainer cannot supply an independent approval of their
  own PR; choose an approval requirement that the project can satisfy.

## Procedure

### Inspect the Existing Configuration

1. Open the target repository's **Settings** page. Record existing branch rules,
   organization policies, Actions permissions, merge methods, security features,
   and labels before changing them. Confirm which rules already apply to the
   default branch. Preserve stronger controls unless the responsible maintainers
   approve a change.
2. Review the [repository settings checklist](../architecture/repository-settings.md)
   against the repository's visibility and GitHub plan. Record unavailable
   features and the maintainer responsible for any alternative control.

### Activate Workflows and Supporting Features

3. In **Settings > Actions > General**, allow the reviewed workflows and actions
   under the repository and organization policy. Keep `GITHUB_TOKEN` permissions
   restricted to what the workflow files request. See GitHub's
   [Actions settings instructions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository).
4. Open a representative PR and inspect the Repository Checks and PR title runs.
   Confirm the jobs exercise the intended commit and complete successfully. Copy
   the exact required check names from the
   [settings checklist](../architecture/repository-settings.md#required-pull-request-checks)
   only after matching them to the observed check runs. Investigate missing or
   skipped integration jobs before making checks required.
5. Under **Issues > Labels**, create any missing labels used by
   [issue triage](../standards/issue-triage.md#label-conventions),
   [Dependabot](../../.github/dependabot.yml), and
   [release notes](../../.github/release.yml).
   GitHub's [label instructions](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
   describe creation and permissions. Verify the labels exist before expecting
   automation to apply them.
6. In the repository's **Security and quality** settings, review dependency
   alerts and update features for the ecosystems actually used. Confirm that
   Dependabot can read its configuration on the default branch and inspect its
   first applicable update job or PR when one exists. The included configuration
   covers GitHub Actions version updates; other ecosystems need their own review.
7. Verify the [security policy](../../SECURITY.md) points to a monitored private
   contact. If the project chooses GitHub Private Vulnerability Reporting and
   the feature is available, enable it under **Settings > Advanced Security** and
   confirm the private reporting path. GitHub's
   [reporting instructions](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)
   describe the current controls.

### Configure Review and Merge Controls

8. In **Settings > General > Pull Requests**, allow squash merging and set the
   default squash commit title to the PR title. Review any other allowed merge
   methods against the [Git workflow](../standards/git-workflow.md). See GitHub's
   [squash settings instructions](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests).
9. In **Settings > Rulesets**, inspect existing branch protections before
   creating or changing a rule. Use a branch ruleset that targets the actual
   default branch. Set it to active, then configure the PR, review-conversation,
   required-check, force-push, and deletion controls from the
   [settings checklist](../architecture/repository-settings.md#review-and-merge-controls).
   Set the approval count to match eligible reviewers; enable owner approval only
   after CODEOWNERS and reviewer access are verified. Review bypass permissions
   explicitly. GitHub's [ruleset instructions](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
   describe the interface and feature availability.
10. Add the observed PR checks listed in the
    [settings checklist](../architecture/repository-settings.md#required-pull-request-checks)
    as required checks. Select the GitHub Actions source when available. Do not
    require scheduled-only jobs. Inspect the saved rule to confirm that it targets
    the intended branch and is active.

## Verification and Evidence

On a representative PR, confirm that the required checks pass and the merge box
shows the intended rules. Test an invalid PR title, confirm it blocks merging, and
restore the valid title. Verify owner review requests only when real CODEOWNERS
mappings are active. Confirm that branch deletion and force pushes are blocked by
the effective rule without performing a destructive push.

Record the repository, date, maintainer, rule names, check-run and PR links,
reporting channel, and any unavailable or untested cases in a setup issue or PR.
The [settings checklist](../architecture/repository-settings.md#verification-evidence)
owns the complete verification criteria. Do not treat the foundation's historical
results as evidence for the new repository.

## Recovery and Escalation

If required checks are missing or a ruleset blocks all PRs, inspect the workflow
run and the rule's target and check names. Have an authorized maintainer correct
the configuration, then repeat the PR verification. If organization policy or a
GitHub plan prevents a control, record the gap and ask the responsible owner to
approve an equivalent approach. Do not bypass a failing check or disable a
security scanner to make a PR mergeable.

## Related Documents

- [Repository settings checklist](../architecture/repository-settings.md) - Required controls and evidence.
- [Repository checks and CI](../architecture/ci-cd.md) - Workflow behavior and limitations.
- [Git workflow](../standards/git-workflow.md) - Branch, PR, and merge policy.
- [Initialize a project repository](initialize-repository.md) - Identity and reporting-contact setup.
