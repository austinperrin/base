# Release Process

[Docs](../README.md) > [Runbooks](README.md) > Release Process

## Objective and Triggers

Verify and publish a reviewed snapshot of the repository when maintainers decide
a versioned release is useful. Milestone completion does not publish a release
automatically. This procedure covers repository verification and publication;
application packaging, deployment, and release channels need their own requirements.

## Prerequisites and Access

- A maintainer with permission to create tags and publish releases.
- An approved release-versioning policy recorded through
  [ADR-0004](../adr/0004-release-versioning.md). While the decision remains Proposed,
  use this runbook to plan the process and stop before publication.
- A clean checkout of `main`, matching the live `main` commit on `origin`.
- Git, Bash 3.2 or newer, Python 3.9 or newer, and an authenticated GitHub CLI
  (`gh`) with access to the repository and its Actions results.
- Matching GitHub repository targets for the origin fetch and push URLs. The
  current helper supports `github.com`; other hosting providers need equivalent
  release verification before using this procedure there.
- A release scope, compatibility assessment, and reviewed notes. Resolve release
  blockers and review the [security policy](../../SECURITY.md) before promising
  support for older versions.

## Procedure

### Select the Version and Commit

1. Review changes since the previous release and select the identifier under the
   project's approved policy. Explain compatibility changes and any migration
   requirements in the release review. Commit types alone do not determine the
   identifier or imply a versioning scheme.
2. Confirm the proposed Git tag follows that policy and the selected distribution
   tools' requirements. The readiness helper checks Git tag syntax and availability;
   it does not enforce the policy's format, increment, ordering, or compatibility
   rules. Enter the reviewed tag when prompted below; no default is selected.
3. Update the release checkout without introducing local changes:

   ```bash
   git switch main
   git pull --ff-only origin main
   read -r -p 'Reviewed release tag: ' release_tag
   ./scripts/ops/verify-release.sh "$release_tag"
   ```

   The [release-verification reference](../architecture/ci-cd.md#release-verification)
   defines the helper's checks and limits. If it fails, resolve the reported
   condition before continuing. The helper does not create a tag or publish.
4. Record the verified commit and successful workflow run in the release review.
   Confirm that the release scope is ready; unrelated open issues or PRs do not
   automatically block a release. Resolve or explicitly exclude relevant blockers.

### Create the Tag and Publish

5. Confirm the verified checkout has not changed, then create an annotated tag at
   that exact commit. Review the resolved commit before pushing:

   ```bash
   git tag -a "$release_tag" -m "Release $release_tag"
   git rev-parse "refs/tags/${release_tag}^{commit}"
   git push origin "refs/tags/$release_tag"
   ```

   If `main` advances or the checkout changes before tagging, rerun verification
   for the chosen candidate. Do not move an existing published version tag.
6. Open the repository's Releases page and draft a release using the pushed tag.
   Generate notes, then review them against the actual changes. Explain
   compatibility changes, migration steps, verification, and known limitations.
   Automated note categories remain a separate roadmap item until configured.
7. Confirm the intended repository, tag, commit, version, and visibility before
   publishing. Do not attach credentials, local configuration, or unreviewed build
   output as assets. This procedure does not produce application packages.

## Verification and Evidence

After publishing, confirm the release is visible as intended and its tag resolves
to the verified commit. Check the notes and any intentionally supplied assets.
Record the release URL, commit, CI evidence, and known limitations in the release
review. The tag itself does not trigger a deployment through the current workflows.

## Recovery and Escalation

If verification fails, stop before tagging or publishing. If an unpublished local
tag points to the wrong commit, confirm it was not pushed before removing it and
starting verification again. If a tag was pushed but no release was published,
stop for maintainer review rather than assuming the tag has no consumers.

For a defective published release, preserve its tag, explain the affected behavior
in the release notes, and prepare a reviewed corrective release. Link the
replacement from the affected release. Follow the security policy for private
reports and credential exposure; do not put sensitive incident details in notes.

## Related Documents

- [Repository checks and CI](../architecture/ci-cd.md#release-verification) - Release gates and limitations.
- [Git workflow](../standards/git-workflow.md) - Change review and merge conventions.
- [Dependency maintenance](dependency-maintenance.md) - Reviewing dependency changes.
- [Security policy](../../SECURITY.md) - Reporting and supported-version policy.
- [ADR-0004: Release Versioning](../adr/0004-release-versioning.md) - Options and pending policy decision.
