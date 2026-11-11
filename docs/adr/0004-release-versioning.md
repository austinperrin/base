# ADR-0004: Release Versioning

[Docs](../README.md) > [ADR](README.md) > ADR-0004

* **Status**: Proposed
* **Date**: 2026-11-09
* **Authors**: @austinperrin
* **Deciders**: Pending assignment by the project

## 1. Context and Problem Statement

The project needs a way to identify releases that fits its users, compatibility
expectations, distribution tools, and maintenance practices. Those requirements
can differ between an internal repository, a library, and a deployed application.

This record compares approaches without selecting one. Leave it Proposed until
the project needs versioned releases and approves a policy. A project can use
reviewed commits without publishing releases while the decision remains open.

The [release process](../runbooks/release-process.md) owns verification and
publication. Its helper checks Git tag syntax, availability, and exact-commit
readiness; passing it does not select or validate a versioning policy.

## 2. Decision Drivers

- Whether users need compatibility signals, release dates, simple ordering, or
  exact source identification.
- The compatibility surface, such as public APIs, documented commands, file
  formats, configuration, and supported runtimes.
- Package-manager and registry syntax, ordering, and dependency-resolution rules.
- Release cadence, support periods, prerelease channels, and maintenance branches.
- Whether repository releases, application packages, and deployed builds share a
  version or need separate identifiers.
- The cost of maintaining the policy, documentation, and any release automation.

## 3. Considered Options

| Option | Use case | Pros | Cons and responsibilities |
| :--- | :--- | :--- | :--- |
| **A. Semantic Versioning**, such as `2.4.1` | Libraries, APIs, and tools with a defined compatibility contract | Communicates incompatible changes, compatible features, and fixes | Requires a clear compatibility contract and consistent change classification; does not communicate release timing. |
| **B. Calendar Versioning**, such as `2026.11.1` | Date-oriented releases of applications, documentation, or internal tools | Communicates release timing and can align with maintenance cycles | Define the date fields, revision counter, and ordering rules; explain breaking changes separately. |
| **C. Sequential identifiers**, such as `release-42` | Products or internal tools needing a simple ordered release history | Easy to assign and compare within a defined sequence | Does not encode timing or compatibility; define numbering ownership and parallel-branch behavior. |
| **D. Project-defined major/minor versions**, such as `3.7` | Products organized around generations or a custom compatibility model | Can match the project's release and support model | Define the meaning and increment rules; readers cannot assume SemVer semantics from the numeric format. |
| **E. Commit-based snapshots**, such as `snapshot-a1b2c3d` | Continuous delivery or development snapshots | Identifies source without inventing compatibility semantics | Less readable as a release sequence; retain the full commit identity and define support and promotion rules separately. |

The examples are illustrative, not selected tag formats. Sequential and
project-defined identifiers are conventions that need a project specification,
not universal standards. See [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
and [Calendar Versioning](https://calver.org/) for their respective rules.

These approaches can coexist when their scopes are clear. For example, a public
package can use SemVer while internal builds also carry a commit identifier.
Ecosystem requirements constrain the choice: the
[Python version specification](https://packaging.python.org/en/latest/specifications/version-specifiers/)
illustrates syntax and ordering rules that a distribution tool can impose.
It is an example, not a selected application ecosystem.

## 4. Decision Outcome

**Pending.** Complete these fields before publishing under the selected policy.

| Item | Project decision |
| :--- | :--- |
| Decision owner and approval date | Pending |
| Release scopes and intended consumers | Pending |
| Selected approach and rationale | Pending |
| Exact format, prefix, ordering, and increment rules | Pending |
| Compatibility and breaking-change communication | Pending |
| Prerelease and build identifiers, if needed | Pending |
| Support periods and maintenance branches, if needed | Pending |
| Alternatives declined and reasons | Pending |

## 5. Consequences and Trade-offs

Complete these after selecting an approach:

- **Benefits for this project**: Pending.
- **Accepted limitations and risks**: Pending.
- **Operational ownership and automation cost**: Pending.
- **Reconsideration triggers**: New distribution requirements, compatibility
  expectations, release channels, or independently released components.

Commit conventions, release cadence, support duration, and publication automation
are separate choices. Conventional Commits do not require SemVer or automatically
assign a release number.

## 6. Implementation and Verification

Keep the release tooling independent of a version scheme while this record is
Proposed. Do not infer acceptance from examples or from the helper accepting a
syntactically valid tag. Once the project decides:

1. Record the outcome, rationale, owner, and approval date, then update this record
   and the decision index under the [ADR standard](../standards/architecture-decisions.md).
2. Document the selected ongoing policy in its canonical standard and link it from
   the release process. Explain how existing identifiers map to the policy.
3. Implement any policy-specific validation and tests for representative valid,
   invalid, prerelease, and migration cases relevant to the selected scheme.
4. Verify ordering and compatibility with the chosen distribution tools and record
   the evidence. Keep publication commands in the release runbook.

## Related Documents

- [Architecture Decision Records (ADRs) index](README.md) - Decision log and statuses.
- [Release process](../runbooks/release-process.md) - Release verification and publication.
- [Repository checks and CI](../architecture/ci-cd.md#release-verification) - Helper behavior and limits.
- [Git workflow](../standards/git-workflow.md) - Commit and review conventions.
