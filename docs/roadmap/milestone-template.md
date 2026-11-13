# Milestone Planning Template

[Docs](../README.md) > [Roadmap](README.md) > Milestone Planning Template

For a milestone with multiple phases, copy this page to
`milestone-N-short-name/README.md`. Replace the title, breadcrumb, prompts, and
relative links for its new location. Copy the
[phase planning template](phase-template.md) once per phase into that directory,
then register the milestone and phase pages in the
[roadmap schedule](README.md#schedule). Keep this page focused on the milestone;
put phase work and evidence in the phase files. For a short, single-phase
milestone, this page can remain one file with its phase plan included.
For that case, replace the phase index with the phase template's goal, work,
review, exit, and evidence sections.

## Milestone Summary

- **Outcome:** State what will be true when this milestone is complete.
- **Owner and schedule:** Record the accountable owner, estimates, dates, variance,
  and status in the [roadmap schedule](README.md#schedule).
- **Last review:** Record the date of the latest progress and schedule review.
- **Dependencies:** Link preceding milestones, required decisions, and external blockers.
- **Scope:** State the deliverables; link to canonical standards for their rules.

## Milestone Readiness

- [ ] The outcome and phase order are clear.
- [ ] Required decisions and dependencies are identified.
- [ ] Phase owners and reviewable work are identified in the roadmap grid.
- [ ] Verification and exit criteria are defined before work starts.

## Phase Index

List and summarize every phase file in this directory. Replace the example row
with a relative link to each phase page after copying its template. The
[roadmap schedule](README.md#schedule) owns phase status and timing.

| Phase | Outcome |
| :--- | :--- |
| Phase 1: Name the first phase | State its observable result; link this title to its phase page after creating it. |

## Progress and Changes

Record the latest reviewed progress, delivery risks, active blocker and owner,
and the next corrective action. Explain any target or scope change with its
reason. Keep discussion and implementation detail in linked issues or pull
requests. Clear a blocker only after its dependency is resolved.

## Milestone Review and Handoff

- [ ] Every phase meets its exit criteria and has linked evidence.
- [ ] The reviewed PRs are merged and applicable checks passed.
- [ ] Standards, ADRs, and documentation reflect the delivered behavior.
- [ ] Accepted follow-ups have an owner and a tracking destination.
- [ ] The [roadmap schedule](README.md#schedule) records final dates, variance,
  and status.

Link the reviewed PRs, check runs, decisions, or other evidence here. Identify
the next milestone or project outcome after completion.

## Related Documents

- [Roadmap index](README.md) - Milestone status and planning rules.
- [Phase planning template](phase-template.md) - Work and exit criteria for each phase.
- [Documentation standards](../standards/documentation.md) - Page ownership and navigation.
- [Architecture Decision Records (ADRs) index](../adr/README.md) - Required project decisions.
