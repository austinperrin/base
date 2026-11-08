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

Phases 0–5 are Completed. Phase 6 is in progress: the shared local suite is
established, including pinned ShellCheck validation at `d159e44`. actionlint
integration is committed at `f66c14e`. Vale integration, configuration, vocabulary,
and tests are committed at `0613df8`. Gitleaks integration and its regression tests
are committed at `2995ab8`. The core CI workflow is committed at `f1210d7`. Verified tool installation and the
external-check job are established with this change. PR-title checks,
dependency updates, and required settings
remain to be introduced or verified.

[ADR-0001](../adr/0001-adopt-google-documentation-style.md) accepts Google
Developer Documentation Style. [ADR-0002](../adr/0002-secret-management.md) remains
Proposed for adopting projects. [ADR-0003](../adr/0003-enforce-repository-quality-checks.md)
accepts the shared quality-checking approach; its implementation is incremental.

The `chore/reference-scaffolding-drafts` branch retains the original draft snapshot
for reference. Its files do not establish implementation or phase completion.

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

Completed means the phase's scoped deliverables have been reviewed, verified, and
committed. It does not by itself assert merge status; Git history and pull requests
record integration into `main`. Paths below identify existing files or planned
deliverables; future paths are not links to implemented content.

| Phase | Status | Work and steps | Relevant files and deliverables |
| :--- | :--- | :--- | :--- |
| **0. Initialize the repository** | Completed | Establish repository identity and license. | Initial `README.md` and `LICENSE`. |
| **1. Establish file hygiene** | Completed | Set editor defaults, Git file handling, and exclusions. | `.editorconfig`, `.gitattributes`, `.gitignore`. |
| **2. Establish the documentation and decision framework** | Completed | Define the repository's purpose; establish documentation ownership and navigation; define how decisions are proposed and recorded. | Narrowed `README.md`, `docs/README.md`, `docs/standards/documentation.md`, standards index, ADR index and template, and `docs/standards/architecture-decisions.md`. ADR-0001 records the approved Google documentation style decision. The roadmap records the scaffolding plan. |
| **3. Establish repository policies and contribution practices** | Completed | Review Git conventions, dependency standards, community expectations, security reporting, contributor guidance, and agent instructions. Add issue and PR templates alongside the practices they support. Define maintainer ownership, CODEOWNERS adoption guidance, and basic issue triage and label conventions. | `docs/standards/git-workflow.md`, `docs/standards/dependencies.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `AGENTS.md`, `docs/AGENTS.md`, `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`, `docs/standards/ownership.md`, `docs/standards/issue-triage.md`, and `.github/CODEOWNERS`. |
| **4. Record project-specific decisions** | Completed | Introduce proposed ADRs containing requirements, options, use cases, trade-offs, and open outcomes. Separate mandatory hygiene from implementation choices. Begin with secrets and review any other decisions the project must own. | Proposed records in `docs/adr/`, starting with ADR-0002. Hold `.env.example` outside the intended baseline unless explicitly approved; a proposed comparison does not select an implementation. |
| **5. Add local developer tooling** | Completed | Implement helpers for established practices, document prerequisites and behavior, and test each helper as introduced. Setup must respect the secrets decision rather than automatically assuming `.env`. | `.githooks/`, `scripts/dev/`, focused helper tests, and an incremental `scripts/README.md`. |
| **6. Add automated enforcement** | In progress; external CI job defined | Implement checks for approved standards, add their regression coverage, then connect them to CI. Document actual enforcement and required GitHub settings, including a repository settings checklist for review requirements, required status checks, merge behavior, and force-push protections. | `scripts/ci/`, regression tests, `.github/workflows/`, `.github/dependabot.yml`, `.vale.ini`, vocabulary, CI architecture documentation, and an ADR for the quality-checking approach. |
| **7. Add repository maintenance procedures** | Pending | Define release verification, dependency maintenance, credential-exposure response, and an issue triage procedure based on the Phase 3 conventions. Introduce release notes categories and `.github/release.yml` alongside the release process. Introduce operational scripts and associated tests together. | `docs/runbooks/`, `scripts/ops/`, associated tests, and corresponding architecture updates. |
| **8. Complete project setup and extension guidance** | Pending | Explain how to implement the repository foundation, replace its identity, and handle scaffolding-specific material. Include replacing repository-specific URLs in issue forms, issue chooser contacts, and the pull request template so links and reports target the adopting project. Assign project owners and configure CODEOWNERS with the adopting project's people or teams; verify the repository settings checklist. Provide reference guidance for extending standards as the project grows. Reconsider the application tutorial when reviewing this group. | Getting Started, scaling guidance, troubleshooting, `docs/guides/README.md`, and the completed root README. The reference `docs/guides/building-your-project.md` is material to reconsider, not a committed deliverable. |
| **9. Verify the assembled repository** | Pending | Check a clean checkout and a representative initialized project, confirm navigation and automation, and prepare the scaffolding branch for merge. | The resulting committed repository, not the surrounding drafts. Verify the full foundation and its project-initialization path. |

### Phase Boundaries

- The ADR framework belongs to Phase 2. ADR-0002 was introduced alongside it as
  an open comparison. The Phase 4 review below confirms that no unresolved
  choice is forced by the baseline.
- Written policies belong to Phase 3; their local helpers and automated enforcement
  follow in Phases 5 and 6. Do not introduce an entire future toolchain to satisfy
  a reference document's existing links or claims.
- Introduce tests with the functionality they verify. Release helpers and their
  tests belong to Phase 7, even if the reference test module groups them with CI checks.
- Phase 8 is the implementation and extension guidance group. Application tutorial
  material remains subject to review there; the roadmap does not require adopting it.

## Next Review Group

Introduce PR-title validation using pull request metadata without checking out
contribution code, plus scheduled credential scanning using the reviewed installer
and scanner. Validate event handling and representative failures. Dependency
updates and the required repository settings checklist follow in focused groups.

### Evaluation Checkpoint Before Phase 7

At the user's request, stop after Phase 6 for an evaluation discussion before
starting any Phase 7 maintenance procedures, release configuration, or operational
scripts. Before Phase 7:

1. Stop for the requested evaluation discussion.
2. Preserve the existing scaffolding history, map commits to their phases, and
   prepare separate phase branches with their prerequisite changes. Review mixed
   commits and documentation updates rather than assuming every commit belongs
   wholly to one phase.
3. Validate each branch's actual contents, including its roadmap statuses and
   links, and open pull requests for the completed phases in dependency order.
   Keep each pull request focused on its phase; use dependent branches where needed.
4. Use **Completed** for finished phases. Keep each pull request's roadmap accurate
   for the content it introduces; Git history and pull requests track merge status.

Completing Phase 6 does not authorize starting Phase 7 or merging the phase pull
requests without the required review.

### Phase 4 Decision Review

- **Secrets**: ADR-0002 provides requirements, three options with use cases and
  trade-offs, an open outcome, and implementation evidence to complete. Its
  decision owner and selected approach remain pending for the adopting project.
- **Baseline independence**: The committed baseline at `fb545fa` includes ignore
  rules for common credential files but no `.env.example`, secret loader, or
  provider integration. Ignore rules do not select an implementation.
- **Application technology and web design**: No application or interface exists
  yet to provide meaningful decision drivers. Defer these ADRs until an adopting
  project has concrete requirements instead of inventing choices now.
- **Quality tooling**: Record the planned quality-checking decision with its
  implementation in Phase 6, where the checks and their consequences can be reviewed.

The Phase 4 review is complete. It confirms the decision framework and open
comparison, without accepting a secrets implementation for adopters.

The contribution templates become available through GitHub after they reach the
default branch; verify their rendered behavior during the assembled-repository
review. Local validation does not confirm GitHub activation.

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
