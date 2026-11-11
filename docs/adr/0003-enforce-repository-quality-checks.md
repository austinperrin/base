# ADR-0003: Enforce Repository Quality Checks

[Docs](../README.md) > [ADR](README.md) > ADR-0003

* **Status**: Accepted
* **Date**: 2026-11-08
* **Authors**: @austinperrin
* **Deciders**: @austinperrin
* **Approval Date**: 2026-11-08

## 1. Context and Problem Statement

The repository defines standards for documentation, contributions, dependencies,
and security. Local developer helpers now have regression tests, but there is no
committed repository-wide check suite or CI enforcement. Manual review can miss
broken navigation, configuration errors, and accidental credential exposure.

This record selects an approach for enforcing the repository's established
standards without choosing an application language or package manager. The
[secret-management decision](0002-secret-management.md) remains separate and
Proposed. Approval of an approach does not prove its implementation.

## 2. Decision Drivers

- Check established standards with reproducible commands locally and in CI.
- Keep validation independent of the project's application technology stack.
- Report actionable failures without modifying source files or repository settings.
- Test failure cases in temporary repositories, preserving the working checkout.
- Keep provider-specific workflow configuration separate from reusable check logic.
- Limit custom parsing and ongoing dependency maintenance to what the project needs.
- Distinguish automated evidence from human review and configured merge controls.

## 3. Considered Options

| Option | Use case | Pros | Cons and responsibilities |
| :--- | :--- | :--- | :--- |
| **A. Manual review and local helpers** | Early exploration or very small changes | Minimal tooling; reviewers can assess meaning and context | Repeated mechanical review; inconsistent coverage; no shared automated merge evidence |
| **B. Platform-focused checks and integrations** | Projects centered on one hosting platform | Can reuse hosted capabilities and existing integrations | Availability and behavior depend on the platform; local reproduction may differ; repository-specific documentation rules can remain uncovered |
| **C. Shared repository checks with focused external linters** | A repository that grows across applications and services | Consistent local and CI checks; custom rules reflect repository standards; external tools handle specialized analysis | Requires regression coverage, version management, documented prerequisites, and clear parsing limits |

These approaches can overlap. Human review and useful platform controls remain
necessary even when a shared suite supplies automated evidence.

## 4. Decision Outcome

**Selected approach: Option C.** Use Bash entry points and Python's
standard library for repository-specific checks, building on the local tooling's
existing prerequisites. Keep those commands usable independently of CI. Use
GitHub Actions as the initial CI integration, following the
[external platform guidance](../standards/README.md#external-platform-guidance).

Do not build general-purpose Markdown, shell, or workflow parsers. Check the
repository's documented structural conventions with explicit limits and use
specialized tools where appropriate. The initial candidates are:

| Area | Proposed implementation | Limits |
| :--- | :--- | :--- |
| Documentation integrity | Repository-specific link and structure checks | A bounded subset of Markdown; not a complete renderer or external-link availability monitor |
| Script correctness | Bash syntax checks, existing helper tests, and [ShellCheck](https://www.shellcheck.net/) | Static analysis and tests cannot establish correctness for every environment |
| Workflow correctness | [actionlint](https://github.com/rhysd/actionlint) | Does not verify live GitHub settings or guarantee successful execution |
| Editorial consistency | [Vale](https://docs.vale.sh/) with selected Google style rules and project vocabulary | Enforces enabled patterns, not the complete style guide or factual accuracy |
| Credential hygiene | Repository filename checks and [Gitleaks](https://github.com/gitleaks/gitleaks) content/history scanning with a documented scan scope | Detection is incomplete and does not revoke exposed credentials |
| Contribution conventions | Pull request title validation against the Git workflow | Does not assess the description's quality or substitute for review |

Manual review remains responsible for technical accuracy, significant trade-offs,
and decision approval. Option A alone does not provide repeatable automated
evidence. Option B alone couples validation too closely to the initial host and
leaves repository-specific rules dependent on manual review.

## 5. Consequences and Trade-offs

- **Expected benefits**: Earlier detection of mechanical errors and repeatable
  verification without introducing an application package ecosystem.
- **Accepted costs**: Maintainers must support custom checks, tests, external tool
  updates, and CI configuration. False positives require investigation and scoped
  rule changes consistent with the owning standard.
- **Portability**: Shared commands can be reused with another CI provider; workflows
  and merge controls still require provider-specific configuration and verification.
- **Reconsideration triggers**: Markdown requirements exceed the supported subset,
  maintenance costs exceed the value of custom checks, or the project changes its
  platform or runtime requirements.

## 6. Implementation and Verification

Implementation is tracked in the [repository checks and CI reference](../architecture/ci-cd.md).
Introduce each group with regression coverage and document its exact behavior and
commands there; decision approval does not establish enforcement.

| Group | Required evidence before claiming enforcement |
| :--- | :--- |
| Repository checks and regression tests | Passing valid cases; useful failures for invalid fixtures; no source repairs; tests confined to disposable repositories |
| External linters and configuration | Dependency evaluation, recorded tool and rule versions, selected severities and scan scopes, reproducible installation, and representative failure cases |
| CI integration and dependency updates | Pinned third-party actions, limited permissions, safe handling of contribution code, local/CI command alignment, and successful runs on the intended commits |
| Repository settings checklist | Required checks and review/merge controls verified in the target repository, with feature availability and setup steps documented |
| Adoption verification | Project-specific values replaced and checks exercised in a representative initialized project |

Follow the [dependency standard](../standards/dependencies.md) when selecting tools
and actions. Keep implementation status in the [roadmap](../roadmap/README.md) and
[architecture reference](../architecture/ci-cd.md) rather than in this decision
record.

## Related Documents

- [Architecture Decision Records (ADRs) index](README.md) - Decision status and history.
- [Documentation standards](../standards/documentation.md) - Editorial and structural requirements.
- [Git workflow](../standards/git-workflow.md) - Contribution requirements and enforcement status.
- [Dependency management](../standards/dependencies.md) - Tool evaluation and version control.
- [ADR-0002: Secret Management](0002-secret-management.md) - Separate decision about secret storage and delivery.
