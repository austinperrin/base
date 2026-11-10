# Issue Triage

[Docs](../README.md) > [Standards](README.md) > Issue Triage

This standard defines how maintainers assess incoming issues, classify work, and
communicate outcomes. Use it for defects, documentation changes, enhancements,
and other repository requests.

## Assessment and Outcomes

Maintainers or delegated area owners review new issues and determine the next
useful action. Follow the [ownership standard](ownership.md) for responsibility.

- **Security report**: Direct the reporter to the [security policy](../../SECURITY.md).
  Avoid quoting sensitive details into other public issues.
- **Duplicate**: Link the existing issue and close the duplicate with an explanation.
  Preserve useful new evidence in the existing discussion without exposing private data.
- **Needs clarification**: Ask for the missing reproduction details, context, or
  desired outcome. Explain what is needed before work can be assessed.
- **Actionable request**: Classify it, assess impact and urgency, and assign an owner
  when someone agrees to take it. Confirm scope before implementation.
- **Declined or out of scope**: Explain the reason and close the issue. Reconsider
  when new evidence or project direction changes the assessment.

An open issue records a request, not a promise to implement it. Do not close a
request solely because it has been inactive; use an explained resolution or ask
whether the need still applies.

## Label Conventions

Start with a small vocabulary. Apply labels only after confirming they exist in
the repository; issue forms do not provision them. Labels can overlap when useful.

| Label | Meaning |
| :--- | :--- |
| `bug` | Existing behavior or content is incorrect. |
| `documentation` | Documentation needs correction or improvement. |
| `enhancement` | A new capability or improvement is requested. |
| `dependencies` | A dependency is added, updated, removed, or reconfigured. |
| `github-actions` | GitHub Actions workflows or their configuration change. |
| `breaking-change` | Users must change how they use an established interface, configuration, or workflow. |
| `question` | The request asks for guidance or needs further information. |
| `duplicate` | Another linked issue tracks the same need. |
| `wontfix` | Maintainers have explained why the request will not be implemented. |
| `help wanted` | Maintainers welcome implementation help. |
| `good first issue` | The work has clear scope, supporting context, and a manageable entry point for a new contributor. |

Remove labels when their meaning no longer applies. Add project-specific labels
only when they support a recurring need, and document their meaning here. See
[GitHub's label management guidance](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
for creating and applying labels with the necessary permissions.

Use `breaking-change` alongside the change's other applicable labels. Explain
the migration in its PR and release notes; this label does not select a version
increment or resolve the [versioning decision](../adr/0004-release-versioning.md).

## Prioritization and Tracking

Consider impact, urgency, dependencies, and available maintainers when selecting
work. Record the rationale in the issue when the priority is not obvious; labels
alone do not communicate a delivery commitment.

Use the [roadmap](../roadmap/README.md) for milestone intent and progress. Link
issues to the relevant milestone document rather than copying its phase checklist
into issue descriptions. Link implementation pull requests to their issues and
follow the [Git workflow](git-workflow.md) for verification and closure.

## Maintenance Procedure

Use the [issue-triage procedure](../runbooks/issue-triage.md) for incoming requests,
backlog review, and checking or provisioning the labels defined here. The
[release process](../runbooks/release-process.md#release-note-preparation) describes
how these classifications support release notes. The procedure does not install
a triage bot or enforce response times.

## Related Documents

- [Ownership](ownership.md) - Maintainer and area-owner responsibilities.
- [Contributing](../../CONTRIBUTING.md) - Issue forms and contribution entry points.
- [Security policy](../../SECURITY.md) - Private vulnerability reporting.
- [Roadmap](../roadmap/README.md) - Milestone priorities and maintenance follow-up.
- [Issue-triage procedure](../runbooks/issue-triage.md) - Execution, verification, and recovery steps.
