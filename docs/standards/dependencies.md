# Dependency Management Standards

[Docs](../README.md) > [Standards](README.md) > Dependency Management

This document defines the canonical rules for selecting, adding, updating, and
auditing third-party dependencies. It applies to application packages, developer
tools, and automation as they are introduced into the repository.

---

## Guiding Principles

1. **Evaluate the maintenance cost**: Add a dependency when its benefits justify
   its security, compatibility, and ongoing maintenance requirements. Consider
   existing capabilities before introducing another package.
2. **Reproducible resolution**: Record resolved versions and integrity information
   using the chosen ecosystem's supported mechanisms. Document required runtime
   and package-manager versions alongside them.
3. **Ongoing review**: Review dependencies and their transitive dependencies for
   relevant advisories and compatibility changes. Confirm the coverage of available
   automation and review dependencies outside that coverage manually.

---

## Evaluation Criteria for New Dependencies

Before proposing a dependency, evaluate it against this scorecard and include
relevant findings in the pull request:

| Criterion | Requirement | Rationale |
| :--- | :--- | :--- |
| **Purpose** | Explain the capability needed and why existing tools are insufficient. | Avoids overlapping packages and unnecessary maintenance. |
| **License compatibility** | Review compatibility with the project's license and intended distribution; resolve questions before adoption. | Makes licensing requirements part of the selection decision. |
| **Maintenance health** | Review releases, issue handling, documentation, and support for the required runtime. | Activity and support should fit the project's needs; a release date alone does not establish quality. |
| **Security** | Review known advisories for the selected version and its dependency tree; resolve applicable high or critical findings before adoption. | Identifies known risks before they enter the project. |
| **Adoption and support** | Evaluate documentation, issue triage, and evidence of use relevant to the project. | Popularity alone does not establish reliability or fitness. |
| **Dependency weight** | Review transitive packages, installation behavior, and build or runtime impact. | A small direct dependency can introduce substantial additional requirements. |

Use an [Architecture Decision Record (ADR)](architecture-decisions.md) when the
choice establishes or changes a significant architectural direction. Routine
package changes can be explained in their pull requests.

---

## Version Pinning and Dependency Metadata

### 1. Semantic Versioning (SemVer)

For dependencies that follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html),
interpret `MAJOR.MINOR.PATCH` as:

* `MAJOR`: Incompatible public API changes.
* `MINOR`: Backward-compatible functionality.
* `PATCH`: Backward-compatible bug fixes.

Review upstream release notes rather than relying only on the version label.
Initial development versions (`0.x`) and projects using other version schemes
need their own compatibility assessment. This section does not select the
repository's application release process or implement release automation.

### 2. GitHub Actions

When introducing third-party actions, pin each reference to a full 40-character
commit SHA and include a version comment for readability. Verify that the commit
belongs to the intended upstream repository. See GitHub's
[third-party action guidance](https://docs.github.com/en/actions/reference/security/secure-use#using-third-party-actions).

Review updates as dependency changes. The [update coverage](#automated-updates-and-auditing)
below distinguishes configured automation from manual maintenance.

### 3. Lockfiles and Integrity Metadata

When introducing a package manager:

* Commit its supported lockfile or other dependency-resolution and integrity metadata.
* Update generated metadata through the package manager rather than hand-editing it.
* Include manifest and generated metadata changes together in the same commit.
* Use the ecosystem's locked or frozen installation mode for verification when available.
* Avoid floating references such as `latest`. Manifest ranges are acceptable when
  the committed resolution mechanism fixes the versions used for installation.

For example, npm's [package-lock.json](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/)
records a resolved dependency tree. In Go, commit `go.mod` and `go.sum`; the
[Go modules reference](https://go.dev/ref/mod#go-sum-files) explains that `go.sum`
contains integrity checksums rather than serving as a lockfile.

These are ecosystem examples, not selected application tools. Dependency metadata
supports repeatable installations, but does not by itself guarantee identical
build output across runtime versions, platforms, or external services.

---

## Dependency Update Review

Apply these requirements when updates are proposed, whether manually or by an
update service:

| Update | Review expectation |
| :--- | :--- |
| **Security advisory** | Assess affected versions, project exposure, and available fixes promptly. Prioritize remediation according to impact; verify the fix and document any remaining follow-up. |
| **Patch** | Review release notes and run applicable checks before merging. |
| **Minor** | Review compatibility and test the behaviors that use the dependency. |
| **Major** | Record a migration and verification plan. Use an ADR if the update changes a significant architectural choice. |

Use the [Git workflow](git-workflow.md) for focused changes and review. Record
what was verified and any relevant limitations. A version label or a successful
installation alone is insufficient evidence that an update is safe to merge.

## Automated Updates and Auditing

**Status: GitHub Actions update configuration implemented.**
[`.github/dependabot.yml`](../../.github/dependabot.yml) configures weekly version
updates for GitHub Actions, a bounded open-PR count, and Conventional Commits
prefixes. It assigns labels from the
[triage conventions](issue-triage.md#label-conventions), but no project-specific
reviewers, and does not enable auto-merge. Its schedule and other values are owned
by the configuration file. Provision the configured labels before relying on
them; Dependabot ignores custom labels that do not exist in the target repository.

Dependabot activation requires the configuration on the default branch and
compatible repository settings. Verify its update job and a resulting PR through
the [repository settings checklist](../architecture/repository-settings.md).
See the [official options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)
when extending its supported ecosystems.

This configuration does not update the custom tool archive manifest, wrapper
version requirements, or Vale package URL. Maintainers must review those upstream
releases and update their related pins, configuration, and regression evidence
together using the [verified installation reference](../architecture/external-checks.md#verified-tool-installation).
It also does not establish automated vulnerability coverage for every dependency;
review feature availability and the project's actual ecosystems before making
that claim. Add application package ecosystems when their manifests are introduced.

Use the [dependency-maintenance procedure](../runbooks/dependency-maintenance.md)
to review automated and manual updates and verify the related pins. This policy
does not select an application stack or add a package manager.

---

## Related Documents

* [Standards index](README.md) - Canonical repository conventions.
* [Git workflow](git-workflow.md) - Commit and pull request requirements.
* [Architecture Decision Record (ADR) standards](architecture-decisions.md) - Significant dependency and technology choices.
* [Repository roadmap](../roadmap/README.md) - Project milestones and planned maintenance work.
* [Dependency maintenance](../runbooks/dependency-maintenance.md) - Execution, verification, and recovery steps.
