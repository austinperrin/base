# Repository Roadmap

[Docs](../README.md) > Roadmap

Use this index as the project's schedule and progress view. The schedule records
milestone and phase ownership, estimates, dates, variance, and status. Milestone
pages define outcomes, dependencies, review steps, and completion evidence.
Issues and pull requests track individual changes.

## Schedule

Estimates are planning ranges for focused maintainer work, including
implementation, review, and verification. They are not delivery commitments or
measured durations. One week means five working days.

Use `YYYY-MM-DD` dates in the `America/Chicago` time zone. For Milestone 0, use
the repository creation date as its actual start. Use the first commit for each
phase start and the closing pull request's merge date for its end. When a phase
has no pull request, use its completion commit. Set planned dates when the owner
commits to a target. Use `TBD` for a future estimate or date that is still open;
use `Not recorded` when a historical value was never recorded.

### Status and Variance Legend

Use the same status text in this schedule and any milestone or phase progress
notes. Inline color helps in renderers that support it; the text remains
readable without styling.

| Status | Meaning |
| --- | --- |
| <span style="color: #6b7280;">Planned</span> | Scope is proposed, but work has not started. |
| <span style="color: #ca8a04;">In Progress</span> | The owner has started work and is tracking delivery. |
| <span style="color: #b91c1c;">Blocked</span> | A named dependency or decision prevents the next planned work. |
| <span style="color: green;">Completed</span> | The exit criteria are met, reviewed, and supported by evidence. |

| Variance | Meaning |
| --- | --- |
| TBD | No planned end date exists yet. |
| On track | Current work is expected to meet the planned end date. |
| At risk | The planned end date may be missed; record a recovery action. |
| Delayed | The planned end date passed and work remains incomplete. |
| Completed early / on time / late | Compare actual completion with the planned end date. |
| Not measured | A historical planned end date was not recorded. |

| Milestone | Stage / Phase | Owner | Estimate | Planned Start | Planned End | Actual Start | Actual End | Variance | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Milestone 0: Repository Scaffolding](milestone-0-repository-scaffolding.md) |  | Repository maintainers | 5–9 weeks | Not recorded | Not recorded | 2026-11-07 | 2026-11-11 | Not measured | <span style="color: green;">Completed</span> |
|  | [Phase 0: Initialize repository](milestone-0-repository-scaffolding.md#phase-0-initialize-repository) | Repository maintainers | 0.5–1 day | Not recorded | Not recorded | 2026-11-07 | 2026-11-07 | Not measured | <span style="color: green;">Completed</span> |
|  | [Phase 1: File hygiene](milestone-0-repository-scaffolding.md#phase-1-file-hygiene) | Repository maintainers | 1–2 days | Not recorded | Not recorded | 2026-11-07 | 2026-11-09 | Not measured | <span style="color: green;">Completed</span> |
|  | [Phase 2: Documentation and decisions](milestone-0-repository-scaffolding.md#phase-2-documentation-and-decisions) | Repository maintainers | 2–4 days | Not recorded | Not recorded | 2026-11-07 | 2026-11-09 | Not measured | <span style="color: green;">Completed</span> |
|  | [Phase 3: Policies and contribution](milestone-0-repository-scaffolding.md#phase-3-policies-and-contribution) | Repository maintainers | 3–5 days | Not recorded | Not recorded | 2026-11-08 | 2026-11-09 | Not measured | <span style="color: green;">Completed</span> |
|  | [Phase 4: Open project decisions](milestone-0-repository-scaffolding.md#phase-4-open-project-decisions) | Repository maintainers | 1–2 days | Not recorded | Not recorded | 2026-11-08 | 2026-11-09 | Not measured | <span style="color: green;">Completed</span> |
|  | [Phase 5: Local developer tooling](milestone-0-repository-scaffolding.md#phase-5-local-developer-tooling) | Repository maintainers | 2–4 days | Not recorded | Not recorded | 2026-11-08 | 2026-11-09 | Not measured | <span style="color: green;">Completed</span> |
|  | [Phase 6: Automated enforcement](milestone-0-repository-scaffolding.md#phase-6-automated-enforcement) | Repository maintainers | 5–10 days | Not recorded | Not recorded | 2026-11-08 | 2026-11-09 | Not measured | <span style="color: green;">Completed</span> |
|  | [Phase 7: Maintenance procedures](milestone-0-repository-scaffolding.md#phase-7-maintenance-procedures) | Repository maintainers | 3–5 days | Not recorded | Not recorded | 2026-11-09 | 2026-11-10 | Not measured | <span style="color: green;">Completed</span> |
|  | [Phase 8: Project setup guidance](milestone-0-repository-scaffolding.md#phase-8-project-setup-guidance) | Repository maintainers | 3–5 days | Not recorded | Not recorded | 2026-11-10 | 2026-11-10 | Not measured | <span style="color: green;">Completed</span> |
|  | [Phase 9: Assembled verification](milestone-0-repository-scaffolding.md#phase-9-assembled-verification) | Repository maintainers | 2–4 days | Not recorded | Not recorded | 2026-11-10 | 2026-11-11 | Not measured | <span style="color: green;">Completed</span> |

Milestone rows summarize their phase work. Link each milestone and phase to its
owning page or section. Record the accountable owner in each row; assign an owner
before committing a delivery target.

## Delivery Rules

Follow the dependencies and exit criteria in the active milestone page. The
[milestone planning template](milestone-template.md) supplies readiness,
development, review, and handoff checklists. Keep work small enough for focused
pull requests, and link issues or pull requests when they exist.

To add a milestone, copy the planning template, define its outcome, owner,
dependencies, and phases, then register its rows in the schedule. Check the
[ADR index](../adr/README.md) for decisions the work depends on; a Proposed ADR
does not establish its outcome.

For a milestone with multiple phases, create `milestone-N-short-name/`. Use its
`README.md` for the milestone outcome, dependencies, phase index, and final
review. Put each phase plan in a separate `phase-N-short-name.md` in that
directory, starting from the [phase planning template](phase-template.md).
Link the milestone row to its `README.md` and each phase row to its phase page.
Keep owners, estimates, dates, variance, and status in this schedule; milestone
and phase pages link here for those values. A short milestone with one phase can
remain a single file. Keep the completed
[Milestone 0 record](milestone-0-repository-scaffolding.md) at its existing path.

Review active milestones at least weekly. Update the schedule when ownership,
dates, variance, or status changes. Record progress, blockers, scope changes,
schedule changes, and completion evidence in the milestone page. When a target
changes, record the old and new dates and the reason there. Do not assign a
variance that requires a planned end date when none exists.

Keep detailed requirements in their canonical standards and decisions. Link to
them from the milestone instead of copying their rules. Keep each phase page
focused on its own work, review, and exit criteria. Follow the
[documentation standard](../standards/documentation.md) for navigation and page
scope.

## Related Documents

- [Milestone planning template](milestone-template.md) - Reusable outcome, phase, and evidence structure.
- [Phase planning template](phase-template.md) - Focused work, review, and exit criteria for one phase.
- [Documentation hub](../README.md) - Repository documentation categories.
- [Architecture Decision Records (ADRs) index](../adr/README.md) - Decisions that inform milestone work.
