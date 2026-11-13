# Dependency Maintenance

[Docs](../README.md) > [Runbooks](README.md) > Dependency Maintenance

## Objective and Triggers

Review automated update PRs, upstream releases, and security advisories for the
dependencies used by the repository. Run this procedure when an update or
advisory arrives and during regular maintenance review. The
[dependency standard](../standards/dependencies.md) owns evaluation, pinning,
compatibility, and update-review requirements.

## Prerequisites and Access

Assign a maintainer under the [ownership standard](../standards/ownership.md).
Use a clean checkout and a topic branch for manual updates; review automated
updates on their proposed branch. Confirm access to upstream release information
and the repository's checks. Local reproduction requires the prerequisites in
the [local checks reference](../architecture/repository-checks.md#commands-and-prerequisites).

## Procedure

### Assess the Update

1. Identify the dependency, its current pin, the proposed version, and the source
   of the update. Read the relevant upstream release notes and advisories, then
   apply the standard's [update-review requirements](../standards/dependencies.md#dependency-update-review).
2. Compare the proposal with existing issues and PRs. Record compatibility concerns,
   affected behavior, security exposure, and any migration work before selecting
   the next action. A successful installation or passing CI does not replace this
   assessment.
3. For a reported vulnerability, determine whether this repository uses the
   affected version and capability. Follow the [security policy](../../SECURITY.md)
   when the report involves an exposed credential or information needing private
   handling. Record unresolved exposure and the responsible maintainer.

### Review All Relevant Pins

Use this map to identify the files requiring review. It describes the current
implementation; introduce application dependency manifests only with their owning
components.

| Dependency | Review locations |
| :--- | :--- |
| GitHub Actions | References and version comments in `.github/workflows/`; changes proposed by the [Dependabot configuration](../../.github/dependabot.yml) |
| Downloaded checking tools | Versions, URLs, hashes, and archive members in the [artifact manifest](../../scripts/ci/tools.json); wrapper version requirements in `scripts/ci/`; affected regression fixtures and versioned CI documentation |
| Google prose rules | Package URL in [Vale configuration](../../.vale.ini), the artifact manifest, affected fixtures and vocabulary, and the corresponding CI documentation |

4. For an action update, verify the proposed commit against the intended upstream
   repository and keep its version comment aligned, following the standard's
   [action-pinning requirements](../standards/dependencies.md#2-github-actions).
5. For a downloaded tool or rule package, review the upstream artifacts and
   integrity information. Update the related manifest entries, wrapper
   requirements, fixtures, and documented versions together. Use the
   [verified installation reference](../architecture/external-checks.md#verified-tool-installation)
   to prepare the candidate dependencies outside tracked source paths. Investigate
   a checksum mismatch before proceeding; replacing a reviewed hash merely to
   accept an unexpected download does not verify its source.
6. Check changes outside automation coverage, including the custom artifact
   manifest and Vale package URL. A successful Dependabot job does not update
   those pins or establish advisory coverage for every tool.

### Verify and Review

7. Install the candidate pinned versions and prepare the rule package as described
   in the local checks reference. Run the local suite and each affected external check:

   ```bash
   ./scripts/ci/test.sh
   ./scripts/ci/check-shell.sh
   ./scripts/ci/check-workflows.sh
   ./scripts/ci/check-prose.sh
   ./scripts/ci/check-credentials.sh
   ```

8. Inspect the test results for skipped integration cases. Confirm that fixtures
   for the updated dependency actually ran, including valid input and expected
   rejection cases. Add regression coverage when behavior changes.
9. Review the resulting diff for unexpected generated files, unrelated changes,
   and inconsistent pins. Record upstream evidence, compatibility findings, checks,
   and remaining limitations in the PR. Use the
   [Git workflow](../standards/git-workflow.md#pr-requirements) for required checks,
   review, and squash merging. Do not merge an update solely because its automation
   reports success.

## Verification and Evidence

Confirm the proposed commit contains the matching pins, integrity metadata,
documentation, and tests. Inspect required hosted checks for that commit and
confirm the external job ran the intended versions and integration cases. After
merging, inspect the default-branch run for regressions and link follow-up work
from the PR when needed.

## Recovery and Escalation

If verification fails before merging, keep the PR open with the failure and next
action recorded. Resolve incompatible updates through their migration plan or
defer them with an explained risk and follow-up owner.

For a regression after merging, prepare a focused revert or fix on a topic branch
from the latest `main`. Review the current dependency state before restoring a
previous pin, especially if the update addressed an advisory. Verify the proposed
recovery through the same required checks and PR process; keep related pins and
integrity metadata consistent. Do not rewrite reviewed branch history to undo an
update.

## Related Documents

- [Dependency management](../standards/dependencies.md) - Evaluation and update policy.
- [External checks and installation](../architecture/external-checks.md) - Tool installation and coverage limits.
- [Git workflow](../standards/git-workflow.md) - Review and merge requirements.
- [Security policy](../../SECURITY.md) - Private reporting and credential exposure.
