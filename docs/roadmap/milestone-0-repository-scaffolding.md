# Milestone 0: Repository Scaffolding

[Docs](../README.md) > [Roadmap](README.md) > Milestone 0

* **Status**: In progress
* **Owner**: Pending assignment; link to the contributors document once introduced.
* **Scope**: Establish the repository foundation and its standards, documentation,
  decisions, tooling, and enforcement.

This milestone establishes the repository foundation. Its phases follow the
dependency order below. Keep this record as the history of the initial scaffolding
and plan subsequent project work from Milestone 1.

## Current Position

The `chore/scaffold-repository` branch has completed Phases 1 and 2, with the
completion commits recorded below. **Phase 3: Repository Policies and Contribution
Practices** is in progress. The Git workflow standard is committed at `99053d0`;
the dependency management policy is committed at `4e00771`. Security reporting
and community expectations are established; contributor guidance is next.

| Branch | Committed state |
| :--- | :--- |
| `main` and `origin/main` | Phase 0: initial README and license at `28e9950` |
| `chore/scaffold-repository` and its remote branch | Phase 1 at `59f58a1`; Phase 2 at `a86081f`, with the roadmap at `91bc7f4`; Git workflow work within Phase 3 at `99053d0`. These changes are not yet merged into `main`. |
| `chore/reference-scaffolding-drafts` and its remote branch | Reference snapshot at `6f09186`; its contents are drafts, not completed scaffolding phases |

The committed [ADR-0001](../adr/0001-adopt-google-documentation-style.md) accepts
Google Developer Documentation Style. [ADR-0002](../adr/0002-secret-management.md)
provides a secrets comparison for the project maintainers and remains Proposed. Vale and
other automation are pending Phase 6.

## Dependency Order

Follow this order when introducing the remaining work. Each phase may contain
several small review and commit groups.

```mermaid
flowchart TD
    P0["Phase 0: Initialize Repository"] --> P1["Phase 1: File Hygiene"]
    P1 --> P2["Phase 2: Documentation and Decision Framework"]
    P2 --> P3["Phase 3: Policies and Contribution Practices"]
    P3 --> P4["Phase 4: Record Project-Specific Decisions"]
    P4 --> P5["Phase 5: Local Developer Tooling"]
    P5 --> P6["Phase 6: Automated Enforcement"]
    P6 --> P7["Phase 7: Repository Maintenance"]
    P7 --> P8["Phase 8: Project Setup and Extension Guidance"]
    P8 --> P9["Phase 9: Verify the Assembled Repository"]
```

This is the working sequence, not a requirement to invent content for every phase.
Earlier groups can introduce supporting material for later work, as the secrets
comparison in Phase 2 does. That does not complete the later phase or select an
implementation for the project.

## Phases and Deliverables

The numbered phases preserve the original scaffolding dependency order. The work
and file groups below define each phase's scope; a file existing on the reference
branch does not mean its phase is implemented.

Completion means reviewed and committed on the scaffolding branch. The branch
table above separately identifies what has reached `main`. Paths below identify
existing files or planned deliverables; future paths are not links to implemented content.

| Phase | Status | Work and steps | Relevant files and deliverables |
| :--- | :--- | :--- | :--- |
| **0. Initialize the repository** | Complete on `main` | Establish repository identity and license. | Initial `README.md` and `LICENSE`. |
| **1. Establish file hygiene** | Complete on scaffolding branch | Set editor defaults, Git file handling, and exclusions. | `.editorconfig`, `.gitattributes`, `.gitignore`. |
| **2. Establish the documentation and decision framework** | Complete on scaffolding branch | Define the repository's purpose; establish documentation ownership and navigation; define how decisions are proposed and recorded. | Narrowed `README.md`, `docs/README.md`, `docs/standards/documentation.md`, standards index, ADR index and template, and `docs/standards/architecture-decisions.md`. ADR-0001 records the approved Google documentation style decision. The roadmap records the scaffolding plan. |
| **3. Establish repository policies and contribution practices** | In progress; Git, dependency, security, and community policies established | Review Git conventions, dependency standards, community expectations, security reporting, contributor guidance, and agent instructions. Add issue and PR templates alongside the practices they support. | `docs/standards/git-workflow.md`, `docs/standards/dependencies.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `AGENTS.md`, `docs/AGENTS.md`, `.github/ISSUE_TEMPLATE/`, and `.github/PULL_REQUEST_TEMPLATE.md`. |
| **4. Record project-specific decisions** | Pending; proposed secrets comparison already available | Introduce proposed ADRs containing requirements, options, use cases, trade-offs, and open outcomes. Separate mandatory hygiene from implementation choices. Begin with secrets and review any other decisions the project must own. | Proposed records in `docs/adr/`, starting with ADR-0002. Hold `.env.example` outside the intended baseline unless explicitly approved; a proposed comparison does not select an implementation. |
| **5. Add local developer tooling** | Pending | Implement helpers for established practices, document prerequisites and behavior, and test each helper as introduced. Setup must respect the secrets decision rather than automatically assuming `.env`. | `.githooks/`, `scripts/dev/`, focused helper tests, and an incremental `scripts/README.md`. |
| **6. Add automated enforcement** | Pending | Implement checks for approved standards, add their regression coverage, then connect them to CI. Document actual enforcement and required GitHub settings. | `scripts/ci/`, regression tests, `.github/workflows/`, `.github/dependabot.yml`, `.vale.ini`, vocabulary, CI architecture documentation, and an ADR for the quality-checking approach. |
| **7. Add repository maintenance procedures** | Pending | Define release verification, dependency maintenance, and credential-exposure response. Introduce operational scripts and associated tests together. | `docs/runbooks/`, `scripts/ops/`, associated tests, and corresponding architecture updates. |
| **8. Complete project setup and extension guidance** | Pending | Explain how to implement the repository foundation, replace its identity, and handle scaffolding-specific material. Provide reference guidance for extending standards as the project grows. Reconsider the application tutorial when reviewing this group. | Getting Started, scaling guidance, troubleshooting, `docs/guides/README.md`, and the completed root README. The reference `docs/guides/building-your-project.md` is material to reconsider, not a committed deliverable. |
| **9. Verify the assembled repository** | Pending | Check a clean checkout and a representative initialized project, confirm navigation and automation, and prepare the scaffolding branch for merge. | The resulting committed repository, not the surrounding drafts. Verify the full foundation and its project-initialization path. |

### Phase Boundaries

- The ADR framework belongs to Phase 2. ADR-0002 was introduced alongside it as
  an open comparison; Phase 4 still requires reviewing the project-decision set
  and checking that no unresolved choice is forced by the baseline.
- Written policies belong to Phase 3; their local helpers and automated enforcement
  follow in Phases 5 and 6. Do not introduce an entire future toolchain to satisfy
  a reference document's existing links or claims.
- Introduce tests with the functionality they verify. Release helpers and their
  tests belong to Phase 7, even if the reference test module groups them with CI checks.
- Phase 8 is the implementation and extension guidance group. Application tutorial
  material remains subject to review there; the roadmap does not require adopting it.

## Next Review Group

Prepare contributor guidance in `CONTRIBUTING.md`, using the established
[Git workflow](../standards/git-workflow.md),
[dependency policy](../standards/dependencies.md),
[security policy](../../SECURITY.md), and [Code of Conduct](../../CODE_OF_CONDUCT.md).
Keep instructions limited to the files, policies, and tools already introduced.

Agent instructions and contribution templates remain later Phase 3 review groups.

## Review and Commit Process

1. Select a focused group whose prerequisites are already committed or will be
   introduced in the same group.
2. Bring in only the relevant reference material and adapt it to the current phase.
3. Review the files together and revise them until approved.
4. Verify the proposed commit snapshot, including links and dependencies. Files
   stored only on the reference branch do not satisfy a working-branch dependency.
5. Commit and push the approved group, then update this milestone's status and
   completion evidence as appropriate.

Update this document when phases advance, dependencies change, or completed work
is merged. Keep detailed requirements in their canonical standards and link to
them rather than repeating their instructions here.

## Milestone Completion

Mark Milestone 0 Complete once its required phases have been reviewed, verified,
and merged into the repository's `main` branch. Proposed project decisions can
remain open; completing a comparison does not select its outcome.

The completed milestone records the foundation for subsequent project work.
Use the [roadmap index](README.md#continuing-with-milestone-1) to add the next
milestone and any dependencies on unfinished scaffolding work.

## Related Documents

- [Roadmap index](README.md) - Milestone status and project continuation.
- [Documentation hub](../README.md) - Documentation categories and references.
- [Documentation standards](../standards/documentation.md) - Ownership and navigation conventions.
- [Architecture Decision Records (ADRs) index](../adr/README.md) - Decisions and their current status.
