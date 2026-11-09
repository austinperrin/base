# Contributing to This Project

[Repository Home](README.md) > Contributing

Use this guide when proposing changes to this repository. Keep contributions
focused, reviewable, and consistent with the established repository standards.

## Before You Start

Review the [roadmap](docs/roadmap/README.md) and discuss significant changes with
the maintainers before beginning work. Proposed decisions in the
[Architecture Decision Records (ADRs) index](docs/adr/README.md) may still need a
project-specific outcome; their presence does not mean an implementation was selected.

Report vulnerabilities privately through the [security policy](SECURITY.md).
Use the [Code of Conduct](CODE_OF_CONDUCT.md) for community expectations and
conduct-reporting channels.

## Canonical References

The [documentation standard](docs/standards/documentation.md) defines ownership
and navigation rules. Use the canonical references below instead of copying their
instructions into new guides.

| Topic | Canonical source |
| :--- | :--- |
| Repository platforms, recognized files, and settings | [External platform guidance](docs/standards/README.md#external-platform-guidance) |
| Branching, commit messages, pull requests, and merging | [Git workflow and commit conventions](docs/standards/git-workflow.md) |
| Maintainer responsibilities and review ownership | [Repository ownership](docs/standards/ownership.md) |
| Issue assessment and labels | [Issue triage](docs/standards/issue-triage.md) |
| Dependency evaluation and updates | [Dependency management](docs/standards/dependencies.md) |
| Documentation style, formatting, and navigation | [Documentation standards](docs/standards/documentation.md) |
| Proposing and recording significant decisions | [Architecture Decision Record (ADR) standards](docs/standards/architecture-decisions.md) |
| Existing decisions and their status | [Architecture Decision Records (ADRs) index](docs/adr/README.md) |
| Instructions for AI-assisted work | [AI agent guidelines](AGENTS.md) |
| Project status, priorities, and progress | [Project roadmap](docs/roadmap/README.md) |

## Report a Bug or Suggest an Improvement

Search open and closed issues for an existing report or related discussion before
submitting. Add relevant details to an existing issue when it covers the same need.

Use the [bug report](.github/ISSUE_TEMPLATE/bug_report.yml) or
[feature request](.github/ISSUE_TEMPLATE/feature_request.yml) form when opening an
issue on GitHub. Blank issues remain available for other requests. Report
vulnerabilities through the [security policy](SECURITY.md).

## Prepare a Contribution

Work in a checkout of this repository or a fork when you do not have write access.
Use a topic branch and the [Git workflow](docs/standards/git-workflow.md) to prepare
and submit a focused change. If contributing from a fork, confirm that the pull
request targets `main` in the repository you intend to change.

Use an editor that respects [`.editorconfig`](.editorconfig). Review the files
included in the proposed commit and keep its documentation and dependencies
self-contained. Files available only in a separate reference branch are not part
of the change being reviewed.

## Pull Request Checklist

Use the [pull request template](.github/PULL_REQUEST_TEMPLATE.md) to describe your
change and record verification results, including checks not run and the reason.
Before submitting, confirm that you have:

- Met the [Git workflow's pull request requirements](docs/standards/git-workflow.md#pr-requirements),
  including the title, description, verification, and review expectations.
- Followed the [documentation standard](docs/standards/documentation.md) for any
  changed documents, category indexes, and incoming links.
- Included the evaluation required by the [dependency policy](docs/standards/dependencies.md)
  when adding or updating dependencies.
- Updated a relevant decision record or proposed a new one according to the
  [ADR standards](docs/standards/architecture-decisions.md) when the architectural
  direction changes.

## Project Status and Progress

Consult the [project roadmap](docs/roadmap/README.md) for current milestones,
priorities, dependencies, and progress before planning a contribution. Keep status
updates in the roadmap and its milestone documents rather than repeating them here.

## Community Standards

By participating in this project, you agree to abide by the
[Code of Conduct](CODE_OF_CONDUCT.md). Report violations through the channels
specified there, and report vulnerabilities through the [security policy](SECURITY.md).

## Related Documents

- [Documentation hub](docs/README.md) - Repository documentation and standards.
- [Security policy](SECURITY.md) - Private vulnerability reporting.
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community expectations and reporting.
