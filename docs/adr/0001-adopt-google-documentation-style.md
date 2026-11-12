# ADR-0001: Adopt Google Developer Documentation Style

[Docs](../README.md) > [ADR](README.md) > ADR-0001

* **Status**: Accepted
* **Date**: 2026-11-07
* **Authors**: Repository maintainers
* **Deciders**: @austinperrin
* **Approval Date**: 2026-11-07

## 1. Context and Problem Statement

The repository needs a consistent editorial baseline for documentation written by
multiple contributors. A shared reference should support clear technical writing
while allowing explicit project-specific terminology and conventions.

The choice concerns editorial style. Documentation organization, decision records,
and automated checks have their own repository conventions and implementation work.

## 2. Decision Drivers

- Clear and consistent documentation for developers and maintainers.
- A published reference that contributors can consult.
- Limited maintenance of custom editorial rules.
- Support for automated checks where rules can be evaluated reliably.
- Room for documented project-specific guidance and terminology.

## 3. Considered Options

| Option | Use case | Pros | Cons and responsibilities |
| :--- | :--- | :--- | :--- |
| A: Google Developer Documentation Style | Technical documentation for software developers | Published editorial guidance focused on a developer audience; a Vale-compatible rule package is available | Some guidance requires editorial judgment; the rule package covers only machine-checkable parts and is maintained separately from Google. |
| B: Microsoft Writing Style Guide | Technical writing across documentation, interfaces, and other communication | Published guidance on writing and terminology across communication formats | Requires selecting and maintaining the applicable conventions for this repository's developer documentation. |
| C: A custom editorial guide | Projects with specialized editorial needs | Full control over conventions and terminology | Maintainers must define, explain, and update the baseline and any automated rules. |

See the [Google guide](https://developers.google.com/style) and
[Microsoft guide](https://learn.microsoft.com/en-us/style-guide/welcome/) for the
external references, and the [Vale Google package](https://github.com/vale-cli/Google)
for the available rule implementation.

## 4. Decision Outcome

**Selected approach: Option A.** Adopt the Google Developer Documentation Style
Guide as the editorial baseline.

Use the [documentation standard](../standards/documentation.md) as the canonical
home for repository-specific conventions. Follow those explicit conventions first,
then Google's guide for editorial questions they do not address. Record any
project-specific exceptions with their rationale.

The selected approach supplies an existing developer-focused reference and a path
to automated checks. A custom guide would require maintaining that baseline from
scratch; Microsoft's broader communication guidance does not provide the same
focus on developer documentation for this project's intended use.

## 5. Consequences and Trade-offs

Contributors share an editorial reference while the repository maintains only its
own conventions and exceptions. Maintainers still need to review technical accuracy,
clarity, and whether explanations meet readers' needs. Upstream guidance and rule
package changes may require reviewing local conventions and configuration.

Reconsider the choice if the project's audience or documentation needs change
substantially, or if maintaining exceptions becomes more work than another baseline.

## 6. Implementation and Verification

The editorial guidance is defined in the [documentation standard](../standards/documentation.md).
Review documentation changes against that standard and the linked Google guide.

The [Vale implementation reference](../architecture/external-checks.md#vale) documents local
configuration, selected versions, blocking severity, and verification. The
[Phase 6 verification record](../architecture/phase-6-verification.md) documents a
successful hosted external-check run with the pinned tools.
Vale cannot guarantee full compliance with Google's guide; editorial review is
still required for guidance that cannot be checked mechanically.

## Related Documents

- [Documentation standards](../standards/documentation.md) - Repository conventions and automation status.
- [Architecture Decision Record (ADR) standards](../standards/architecture-decisions.md) - Decision review and status lifecycle.
- [Architecture Decision Records (ADRs) index](README.md) - Decision log.
