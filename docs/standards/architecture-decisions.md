# Architecture Decision Record (ADR) Standards

[Docs](../README.md) > [Standards](README.md) > Architecture Decision Record Standards

This document owns the conventions for proposing, reviewing, and maintaining
architecture decision records (ADRs). The [Architecture Decision Records (ADRs) index](../adr/README.md) lists the
records; the [template](../adr/template.md) provides their starting structure.

## Purpose and Scope

Use an ADR to explain a significant choice, its alternatives, and the reasons
behind it. Records can describe repository decisions or present an unresolved
choice for an adopting project.

Keep ongoing requirements and procedures in their canonical standards or guides.
The ADR explains why a decision was made and links to those documents rather
than repeating their instructions.

## File Naming and Registration

- Store records in `docs/adr/` with a four-digit sequential identifier and a
  descriptive filename, such as `0001-adopt-google-documentation-style.md`.
- Assign the next available number when introducing a record. Once committed,
  keep its identifier stable and do not reuse it for a different decision.
- Add every record to the [Architecture Decision Records (ADRs) index](../adr/README.md)
  in the same change, including its title, status, date, and a short summary.
- Follow the [documentation standard](documentation.md) for breadcrumbs,
  formatting, and related links. `Docs > ADR` is the abbreviated breadcrumb
  for this category; the index heading spells out its full name and abbreviation.

## Required Content

Use the [Architecture Decision Record (ADR) template](../adr/template.md) and include:

| Section | Required content |
| :--- | :--- |
| Metadata | Identifier, title, status, date, authors, and decision owner; identify pending ownership explicitly |
| Context and problem | The issue, scope, and project constraints |
| Decision drivers | The requirements and evaluation criteria |
| Considered options | Relevant approaches, each with its use case, pros, cons, and ongoing responsibilities |
| Decision outcome | The proposed or selected approach, rationale, and reasons for declining alternatives; state explicitly when the outcome is pending |
| Consequences | Expected benefits, accepted costs and risks, and conditions for reconsidering the choice |
| Implementation and verification | Follow-up work, ownership, and evidence needed to verify implementation |
| Related documents | Links to relevant records, standards, or procedures |

Include enough alternatives to inform the decision rather than adding options
only to fill a table. Explain when approaches overlap or can be combined. Record
separate selections by environment or component when a single choice would be misleading.

## Status Lifecycle

| Status | Meaning |
| :--- | :--- |
| Proposed | Under consideration; the outcome or decision owner can remain pending |
| Accepted | The decision has been reviewed and approved |
| Rejected | The proposed decision was considered and declined |
| Deprecated | The decision no longer applies |
| Superseded by ADR-XXXX | A linked, newer record replaces the decision |

A completed comparison with an unresolved outcome remains Proposed. Reviewing
its presentation does not select an implementation for the adopting project.
An Accepted decision may still have outstanding implementation work; track that
work separately from the decision's approval.

## Review and Maintenance

Create a record from the template, register it in the index, and submit it for
review. Once the responsible decision maker approves an outcome, record the
rationale and approval date, then update both the record and index to Accepted.

When an accepted decision changes, create a new ADR and link both records. Update
the earlier record's status without rewriting its original rationale to describe
a different decision. Keep rejected, deprecated, and superseded records available
as decision history.

## Related Documents

- [Architecture Decision Records (ADRs) index](../adr/README.md) - Decision log.
- [Architecture Decision Record (ADR) template](../adr/template.md) - Record structure.
- [Documentation standards](documentation.md) - Canonical ownership and formatting conventions.
