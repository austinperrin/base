# Domain AI Agent Guidelines: Documentation (docs/AGENTS.md)

[Repository Home](../README.md) > [Docs](README.md) > Documentation Agent Guidelines

These instructions apply to AI assistants working within `docs/`. They inherit
the [repository-wide agent guidelines](../AGENTS.md) and specialize how to apply
the canonical documentation and decision standards.

## Documentation Ownership

Read the relevant category index and canonical documents before changing a topic.
Use the [documentation standard](standards/documentation.md#1-single-source-of-truth-anti-drift-rule)
for ownership, summaries, and incoming-link maintenance rather than creating a
second explanation of an established policy.

## Navigation and Registration

Register new documents in their category index and keep categories reachable from
this [documentation hub](README.md). Follow the canonical
[navigation rules](standards/documentation.md#2-hub-and-spoke-navigation) for
breadcrumbs and curated Related Documents sections.

## Writing and Formatting

Apply the editorial, Markdown, and Mermaid conventions in the
[documentation standard](standards/documentation.md), together with
[`.editorconfig`](../.editorconfig). Keep examples accurate for the files and
capabilities introduced in the current repository.

## Decisions and Project Progress

Follow the [Architecture Decision Record (ADR) standards](standards/architecture-decisions.md)
when creating or updating a decision. Keep the record and index statuses aligned;
reviewing an options comparison does not select its pending outcome.

Use the [roadmap](roadmap/README.md) as the source for project progress and
implementation dependencies. Guides and agent instructions should link to that
status rather than reproduce milestone or phase details.

## Documentation Review

Review changes against the [documentation standard](standards/documentation.md),
including navigation and the boundaries between established content and pending
implementation. Report the checks performed; a reference to future automation
must not be presented as an implemented check.

## Related Documents

- [Repository-wide agent guidelines](../AGENTS.md) - Shared agent instructions.
- [Documentation standards](standards/documentation.md) - Canonical editorial and navigation rules.
- [Architecture Decision Record (ADR) standards](standards/architecture-decisions.md) - Decision structure and review.
