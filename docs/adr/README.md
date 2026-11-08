# Architecture Decision Records (ADRs)

[Docs](../README.md) > ADR

This index lists proposed and recorded architectural decisions. The
[Architecture Decision Record (ADR) standards](../standards/architecture-decisions.md)
define their structure, numbering, review, and status lifecycle.

## Contents

- [Decision log](#decision-log)
- [Create a record](#create-a-record)
- [Related documents](#related-documents)

## Decision Log

| ID | Title | Status | Date | Summary |
| :--- | :--- | :--- | :--- | :--- |
| [ADR-0001](0001-adopt-google-documentation-style.md) | Adopt Google Developer Documentation Style | Accepted | 2026-11-07 | Use Google's guide as the editorial baseline; automated checks remain pending. |
| [ADR-0002](0002-secret-management.md) | Secret Management | Proposed | 2026-11-07 | Compare secret storage and delivery approaches for the adopting project to choose. |
| [ADR-0003](0003-enforce-repository-quality-checks.md) | Enforce Repository Quality Checks | Accepted | 2026-11-08 | Use shared repository checks with focused linters; implementation remains pending. |

## Create a Record

Copy the [Architecture Decision Record (ADR) template](template.md) and complete it
following the [ADR standards](../standards/architecture-decisions.md).
You can also create a numbered draft using the
[ADR generator](../../scripts/README.md#adr-generation).
Register the record in the decision log and update its status when the responsible
decision maker approves an outcome.

## Related Documents

- [Architecture Decision Record (ADR) standards](../standards/architecture-decisions.md) - Required content and lifecycle.
- [Documentation standards](../standards/documentation.md) - Writing, formatting, and navigation rules.
