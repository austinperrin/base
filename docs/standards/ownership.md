# Repository Ownership

[Docs](../README.md) > [Standards](README.md) > Repository Ownership

This standard defines responsibility for repository maintenance and review.
Ownership applies to documentation, configuration, automation, and application
components as they are introduced.

## Responsibilities

Maintainers coordinate issue triage, reviews, repository settings, and releases.
Area owners review changes affecting their scope and keep its implementation and
canonical documentation aligned. One person can fulfill both roles in a small
project; split responsibility when the project needs it.

Assign owners who can maintain the area and arrange a replacement when they step
away. Being listed as a contributor does not automatically grant ownership,
repository access, or merge authority.

## CODEOWNERS

Use [`.github/CODEOWNERS`](../../.github/CODEOWNERS) as the canonical mapping of
paths to review owners. Its initial examples are commented out; no owners are
assigned until maintainers replace them with valid project accounts and activate
the entries. Do not retain the scaffolding author's identity by default.

When adopting or changing the mapping:

1. Choose a default owner for the repository, then add narrower area mappings
   where responsibility differs. Include ownership of the CODEOWNERS file itself.
2. Use real GitHub users or visible teams with the required write access.
   Arrange access separately; an entry does not grant permissions.
3. Put broad patterns first and specific patterns later. The last matching
   pattern determines the owners; list multiple owners on the same line.
4. Review the file on GitHub for syntax or account errors and verify review
   requests with a representative pull request into the branch containing it.

GitHub uses CODEOWNERS from the pull request's base branch to request reviews on
non-draft pull requests. A mapping does not itself make owner approval mandatory;
required approvals depend on repository rules and feature availability. See
[GitHub's CODEOWNERS guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

## Review and Handover

Follow the [Git workflow](git-workflow.md) for review and merging. Changes to
ownership must be reviewed with the affected maintainers; confirm the new owners
have access and understand their responsibilities before completing a handover.

Use the [roadmap](../roadmap/README.md) for planned ownership setup and repository
settings verification. Assigning an owner does not change a milestone's status or
select a Proposed architectural decision.

## Related Documents

- [Git workflow](git-workflow.md) - Review and merge requirements.
- [Issue triage](issue-triage.md) - Responsibilities for incoming requests.
- [Contributing](../../CONTRIBUTING.md) - Preparing and submitting changes.
