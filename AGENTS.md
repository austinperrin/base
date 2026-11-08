# AI Agent Guidelines (AGENTS.md)

[Repository Home](README.md) > AI Agent Guidelines

This file defines repository-wide instructions for AI assistants. Apply these
instructions alongside the user's requested scope and review process.

> **Principles**: Domain isolation, deterministic quality, and zero documentation drift.

---

## Navigation and Hierarchical Context Discovery

Before working in a directory, read the `AGENTS.md` files in that directory and
its ancestors. Local instructions specialize the repository-wide guidance for
their own scope; keep shared policies in their canonical documents.

| Domain | Scope | Instructions |
| :--- | :--- | :--- |
| Repository | Shared workflow, security, style, and change boundaries | This file |
| Documentation | Documentation ownership, navigation, and decision records | [Documentation agent guidelines](docs/AGENTS.md) |

When application or service directories are introduced, add local instructions
for their runtime, testing, and formatting requirements. Keep technology-specific
instructions with the component they govern.

## Core Rules and Invariants

### 1. Single Source of Truth

Follow the [documentation standard](docs/standards/documentation.md) for canonical
ownership, summaries, links, and navigation. Link to established policies rather
than copying convention tables or detailed procedures into agent instructions.

### 2. Git and Review Hygiene

Follow the [Git workflow](docs/standards/git-workflow.md) and
[contribution guide](CONTRIBUTING.md). Keep changes focused on the user's request
and include their required files and documentation.

Respect the user's review and commit process. Stage, commit, or push only when
authorized, and keep unrelated or unapproved work out of the approved group.

### 3. Security and Secret Hygiene

Never expose or propose committing live credentials, private keys, or passwords;
follow the [security policy](SECURITY.md) for reporting and exposed credentials.
Do not recommend bypassing security scanners or disabling branch protections.

Check the [decision log](docs/adr/README.md) before implementing a project-specific
choice. A Proposed record with a pending outcome does not authorize selecting a
secret-storage mechanism or another unresolved implementation.

### 4. Preservation of Existing Style

Respect [`.editorconfig`](.editorconfig) and [`.gitattributes`](.gitattributes).
Preserve existing comments, docstrings, license notices, covenant text, and
attribution unless the requested change explicitly requires updating them.

### 5. Dependencies and Decisions

Use the [dependency standard](docs/standards/dependencies.md) when adding or
updating tools and packages. Record significant choices through the
[Architecture Decision Record (ADR) standards](docs/standards/architecture-decisions.md)
and keep the decision log consistent with the records.

### 6. Verification

Verify the files that will actually be included in the change. Material on a
reference branch does not satisfy a dependency in the working branch.

Use checks available in the repository or introduced with the change, and state
what was verified and any limitations. Do not claim that absent checks ran or
that planned automation is already enforcing a standard.

## Project Status and Progress

Consult the [project roadmap](docs/roadmap/README.md) for priorities, dependencies,
and implementation progress. Keep status updates in the roadmap and its milestone
documents rather than repeating phase details here.

## Key Reference Points for Agents

| Topic | Canonical source |
| :--- | :--- |
| Contribution and review | [Contributing](CONTRIBUTING.md) |
| Branches, commits, and pull requests | [Git workflow](docs/standards/git-workflow.md) |
| Dependency evaluation and updates | [Dependency management](docs/standards/dependencies.md) |
| Documentation and navigation | [Documentation standards](docs/standards/documentation.md) |
| Decision structure and lifecycle | [Architecture Decision Record (ADR) standards](docs/standards/architecture-decisions.md) |
| Decisions and their status | [Architecture Decision Records (ADRs) index](docs/adr/README.md) |
| Vulnerability reporting | [Security policy](SECURITY.md) |
| Community expectations | [Code of Conduct](CODE_OF_CONDUCT.md) |
| Project progress | [Roadmap](docs/roadmap/README.md) |

## Related Documents

- [Documentation agent guidelines](docs/AGENTS.md) - Instructions for work under `docs/`.
- [Contributing](CONTRIBUTING.md) - Human contribution and review guidance.
