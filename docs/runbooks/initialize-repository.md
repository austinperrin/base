# Initialize a Project Repository

[Docs](../README.md) > [Runbooks](README.md) > Initialize a Project Repository

## Objective and Triggers

Use this procedure when starting a new project from this repository's scaffold.
It establishes the new repository's identity, reporting contacts, ownership, local
checks, and setup evidence. To improve the scaffold itself, use the
[contribution guide](../../CONTRIBUTING.md) instead.

This procedure is for initial setup. Keep the [roadmap](../roadmap/README.md),
standards, decision records, and maintenance runbooks as the project's working
documentation after setup.

## Prerequisites and Access

- Choose the new repository's name, owner, visibility, and default branch. Have
  permission to create it and configure its settings.
- Identify a maintainer, a private security-reporting contact, and a conduct-reporting
  contact. Confirm both contacts are monitored before publishing them.
- Use Git and a clean copy of the scaffold's reviewed default branch. Decide
  whether to start with a new history or retain the scaffold's Git history.
- Review the [repository ownership standard](../standards/ownership.md) and the
  [repository settings checklist](../architecture/repository-settings.md). Access
  to GitHub settings and review-owner accounts is needed for their activation.

## Procedure

### Create the New Repository

1. For a new history, select **Use this template > Create a new repository** when
   template creation is enabled for the scaffold. Enter the new owner, name,
   description, and visibility. Copy the default branch only. Clone the new
   repository and confirm `git remote -v` points to it. GitHub's
   [template instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
   describe the current interface and how template history differs from a fork.
2. If you need to retain the scaffold's history, clone its reviewed default
   branch and create an empty destination repository. Change the clone's `origin`
   URL to the destination before pushing. Replace `PROJECT_DIRECTORY`, `OWNER`,
   and `REPOSITORY` in these commands with the new project's values:

   ```bash
   git clone https://github.com/austinperrin/scaffolding.git PROJECT_DIRECTORY
   cd PROJECT_DIRECTORY
   git remote set-url origin https://github.com/OWNER/REPOSITORY.git
   git remote -v
   ```

   Confirm that `origin` names the new repository. A normal clone carries the
   source commits; do not mirror-push source branches or tags into a new project
   without reviewing them.
3. Confirm the working tree is clean with `git status --short`. Create a topic
   branch for initialization changes under the [Git workflow](../standards/git-workflow.md).

### Set Identity and Reporting Contacts

4. Replace the title, description, and scaffold-specific introduction in the
   [root README](../../README.md) with the project's purpose and first steps.
   Keep useful paths to documentation, contribution, security, and the roadmap.
5. Preview the one-time replacement of the source repository links and reporting
   contacts. Replace the uppercase placeholders with the project's GitHub path
   and monitored addresses:

   ```bash
   python3 scripts/dev/initialize-project.py configure \
     --repository OWNER/REPOSITORY \
     --security-email SECURITY_EMAIL \
     --conduct-email CONDUCT_EMAIL
   ```

   Review every listed file. Repeat the command with `--apply` to update the
   source URLs in `.github/` and the addresses in [SECURITY.md](../../SECURITY.md)
   and [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md). The helper refuses to run
   while `origin` still points to the scaffold.
6. Open each resulting issue-form and pull-request-template link and confirm it
   points to the new repository. Review the security policy's supported-version
   and response-time statements against actual maintenance commitments. Keep the
   Contributor Covenant attribution and existing copyright notices intact.
7. Assign real users or teams in [`.github/CODEOWNERS`](../../.github/CODEOWNERS).
   Confirm their access, then activate only the mappings the project needs. The
   commented examples do not request reviews; remove or update the pending-setup
   comments when the mapping is ready. Use the
   [ownership standard](../standards/ownership.md#codeowners) for precedence and
   verification.

### Continue the Project's Decisions and Roadmap

8. Review [ADR-0002](../adr/0002-secret-management.md) and
   [ADR-0004](../adr/0004-release-versioning.md). Their outcomes remain Proposed;
   choose an implementation only when the project has the needed requirements and
   a responsible decision maker. Update the ADR and its index when a decision is
   approved. Do not add sample secret files merely to complete setup.
9. The cleanup step replaces [Milestone 0](../roadmap/milestone-0-repository-scaffolding.md)
   with a concise record of this repository's starting practices. Create Milestone 1
   for the next project goal through the
   [roadmap index](../roadmap/README.md#continuing-with-milestone-1). Record this
   repository's checks and settings in the initialization PR.

### Enable and Verify the Scaffold

10. Run [local developer setup](../../scripts/README.md) in the new checkout to
    enable the commit hook, then run the local repository suite:

    ```bash
    ./scripts/dev/setup.sh
    ./scripts/ci/test.sh
    ```

11. Commit and push the setup changes on the topic branch, then open a draft
    initialization PR. Use it to observe hosted checks. For GitHub, follow the
    [GitHub configuration runbook](configure-github.md), which applies the
    [repository settings checklist](../architecture/repository-settings.md).
    Verify workflow permissions, review owners, merge rules, and private reporting.
    A copied workflow file does not activate branch protection.
12. After the setup and settings are verified, preview the source-only removals:

    ```bash
    python3 scripts/dev/initialize-project.py finish
    ```

    Review the exact updates and removals, then repeat with `--apply`. This removes
    the one-time runbook and helper, its tests, and the original scaffold's
    Phase 6 verification record; it updates their incoming links and replaces
    Milestone 0 with the project-owned setup summary. The helper
    refuses modified removal candidates or unexpected incoming links, and rolls
    back its changes if documentation checks fail.
13. Review the final diff, run local checks, and push the cleanup commit to the
    draft PR. Record the selected history path, contacts, links, local and hosted
    results, settings, and remaining follow-ups. After the updated hosted checks
    pass, complete review and merge under the
    [Git workflow](../standards/git-workflow.md).

## Verification and Evidence

Review the final diff and confirm that the README describes this project, the
reporting contacts are monitored, GitHub forms point to the new repository, and
CODEOWNERS names eligible reviewers. Search the active identity files for the
scaffold's old URL and contact; inspect any matches before merging:

```bash
git grep -n -E 'austinperrin/(base|scaffolding)|perrinaustin@gmail.com|@your-maintainer|@your-org' \
  -- README.md SECURITY.md CODE_OF_CONDUCT.md .github
```

Run `./scripts/ci/check-links.sh` and `./scripts/ci/check-docs.sh` after editing
navigation and after final cleanup. Record hosted CI and settings verification for
the new repository in the initialization PR or a linked setup record. Historical
scaffold results do not replace these checks.

## Recovery and Escalation

If a contact is unavailable or a link points to the scaffold, correct it before
publishing the new repository's issue forms or security policy. If settings differ
from the checklist, record the gap and responsible maintainer; do not claim the
control is active. Reverse unmerged setup changes on the topic branch and rerun
the checks. A published reporting address or exposed credential may require the
[credential-exposure procedure](secret-rotation.md), not only a Git revert.

## Related Documents

- [GitHub configuration runbook](configure-github.md) - Platform setup and live verification.
- [Repository ownership](../standards/ownership.md) - Maintainer and review-owner responsibilities.
- [Repository roadmap](../roadmap/README.md) - Scaffold history and project milestones.
- [Documentation standards](../standards/documentation.md) - Project documentation and navigation.
