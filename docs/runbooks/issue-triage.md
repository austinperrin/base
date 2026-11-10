# Issue Triage Procedure

[Docs](../README.md) > [Runbooks](README.md) > Issue Triage Procedure

## Objective and Triggers

Review incoming issues and keep open requests actionable. Use this procedure
when a request arrives, new information changes its assessment, or maintainers
review the backlog. The [issue-triage standard](../standards/issue-triage.md)
owns classification, outcomes, label meanings, and prioritization.

## Prerequisites and Access

The operator is a maintainer or delegated owner under the
[ownership standard](../standards/ownership.md). Confirm that the repository
platform grants the permissions needed for each action, including editing
labels, assigning work, and closing or reopening issues.

Use the repository's issue interface. This procedure requires no local scripts,
API credentials, or additional automation.

## Procedure

1. Read the request and linked context. For a vulnerability or exposed credential,
   use the [security policy](../../SECURITY.md) and avoid copying sensitive details
   into the triage discussion.
2. Search open and closed issues for related requests. Inspect the linked evidence
   before deciding whether an existing issue covers the same need.
3. Apply the standard's assessment outcome. If information is missing, ask a
   focused question that explains what is needed to assess the request.
4. Inspect the repository's existing labels and compare them with the
   [label conventions](../standards/issue-triage.md#label-conventions). Apply only
   labels whose meaning fits. If a required label is missing, have an authorized
   maintainer create it using the standard's linked platform guidance, then verify
   its name and description. Document new recurring categories in the standard
   before using them as shared conventions.
5. For actionable work, confirm its scope and acceptance criteria in the issue.
   Check the [roadmap](../roadmap/README.md) for dependencies and milestone intent.
   Assign an owner when someone agrees to take the work. Associate an existing
   platform milestone when it matches the request; the milestone description
   should link to its roadmap document once that document is available.
6. Record the assessment and next action in the discussion. When closing a
   request, explain the resolution and link relevant evidence. If implementation
   proceeds, link the pull request according to the
   [Git workflow](../standards/git-workflow.md#pr-requirements).
7. During backlog review, reassess requests with new evidence, unanswered questions,
   or changed dependencies. Apply the standard's closure policy rather than
   treating inactivity as a resolution.

## Verification and Evidence

Confirm that the issue's labels, owner, milestone, and open or closed state match
the recorded assessment. Check that related issues and implementation links point
to the intended work. Leave unresolved questions and the next action visible in
the discussion; link to the phase checklist in the roadmap instead of copying it.

If required access is unavailable, record the remaining action and refer it to a
maintainer who can perform it. Verify the required platform settings and labels
in the repository before relying on them.

## Recovery and Escalation

Correct mistaken labels, assignments, or milestone selections and explain material
changes in the discussion. Reopen an incorrectly closed issue with the reason and
next action. For disputed scope or ownership, refer the request to the responsible
maintainer. Follow the security policy for sensitive disclosures instead of
reproducing their contents while correcting the triage record.

## Related Documents

- [Issue triage](../standards/issue-triage.md) - Assessment outcomes and label conventions.
- [Repository ownership](../standards/ownership.md) - Responsibility and review ownership.
- [Security policy](../../SECURITY.md) - Private reporting and credential exposure.
- [Roadmap](../roadmap/README.md) - Milestone intent and dependencies.
