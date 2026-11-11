# Initialize a Project Repository

[Docs](../README.md) > [Runbooks](README.md) > Initialize a Project Repository

## Objective and Triggers

Use this procedure when starting a new project from this repository's foundation.
It establishes the new repository's identity, reporting contacts, ownership, local
checks, and setup evidence. To improve the foundation itself, use the
[contribution guide](../../CONTRIBUTING.md) instead.

This procedure is for initial setup. Keep the [roadmap](../roadmap/README.md),
standards, decision records, and maintenance runbooks as the project's working
documentation after setup.

## Prerequisites and Access

- Choose the new repository's name, owner, visibility, and default branch. Have
  permission to create it and configure its settings.
- Identify a maintainer, a private security-reporting contact, and a conduct-reporting
  contact. Confirm both contacts are monitored before publishing them.
- Use Git and a clean copy of the foundation's reviewed default branch. Decide
  whether to start with a new history or retain the foundation's Git history.
- Review the [repository ownership standard](../standards/ownership.md) and the
  [repository settings checklist](../architecture/repository-settings.md). Access
  to GitHub settings and review-owner accounts is needed for their activation.

## Procedure

### Create the New Repository

1. For a new history, select **Use this template > Create a new repository** when
   template creation is enabled for the foundation. Enter the new owner, name,
   description, and visibility. Copy the default branch only. Clone the new
   repository and confirm `git remote -v` points to it. GitHub's
   [template instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
   describe the current interface and how template history differs from a fork.
2. If you need to retain the foundation's history, clone its reviewed default
   branch and create an empty destination repository. Change the clone's `origin`
   URL to the destination before pushing. Replace `PROJECT_DIRECTORY`, `OWNER`,
   and `REPOSITORY` in these commands with the new project's values:

   ```bash
   git clone https://github.com/austinperrin/base.git PROJECT_DIRECTORY
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

4. Replace the title, description, and foundation-specific introduction in the
   [root README](../../README.md) with the project's purpose and first steps.
   Keep useful paths to documentation, contribution, security, and the roadmap.
5. Set the private reporting address in [SECURITY.md](../../SECURITY.md) and the
   conduct-reporting address in [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md).
   Review the security policy's supported-version and response-time statements
   against the new project's actual maintenance commitments. Keep the Contributor
   Covenant attribution and existing copyright notices intact.
6. Replace the source repository URL in the issue chooser's security contact,
   both issue forms, and the pull request template. Check that each resulting
   link opens the new repository's security policy or contribution document.
   These five links live under `.github/`; inspect each before publishing forms.
7. Assign real users or teams in [`.github/CODEOWNERS`](../../.github/CODEOWNERS).
   Confirm their access, then activate only the mappings the project needs. The
   commented examples do not request reviews. Use the
   [ownership standard](../standards/ownership.md#codeowners) for precedence and
   verification.

### Continue the Project's Decisions and Roadmap

8. Review [ADR-0002](../adr/0002-secret-management.md) and
   [ADR-0004](../adr/0004-release-versioning.md). Their outcomes remain Proposed;
   choose an implementation only when the project has the needed requirements and
   a responsible decision maker. Update the ADR and its index when a decision is
   approved. Do not add sample secret files merely to complete setup.
9. Keep [Milestone 0](../roadmap/milestone-0-repository-scaffolding.md) as the
   foundation record. Create a project-specific Milestone 1 through the
   [roadmap index](../roadmap/README.md#continuing-with-milestone-1). Source
   verification evidence describes the original repository; record the new
   repository's checks and settings separately.

### Enable and Verify the Foundation

10. Run [local developer setup](../../scripts/README.md) in the new checkout to
    enable the commit hook, then run the local repository suite:

    ```bash
    ./scripts/dev/setup.sh
    ./scripts/ci/test.sh
    ```

11. For a GitHub project, follow the
    [GitHub configuration runbook](configure-github.md). It applies the
    [repository settings checklist](../architecture/repository-settings.md) to
    the new repository. A copied workflow file does not activate branch
    protection or prove that a hosted check passed.
12. Open an initialization PR. Record the selected history path, changed contacts
    and links, local results, hosted checks, settings still pending, and the owner
    of each follow-up. Merge under the [Git workflow](../standards/git-workflow.md)
    after the applicable checks and review.

## Verification and Evidence

Review the final diff and confirm that the README describes this project, the
reporting contacts are monitored, GitHub forms point to the new repository, and
CODEOWNERS names eligible reviewers. Search the active identity files for the
foundation's old URL and contact; inspect any matches before merging:

```bash
git grep -n -E 'austinperrin/base|perrinaustin@gmail.com|@your-maintainer|@your-org' \
  -- README.md SECURITY.md CODE_OF_CONDUCT.md .github
```

Run `./scripts/ci/check-links.sh` and `./scripts/ci/check-docs.sh` after editing
navigation. Record hosted CI and settings verification for the new repository in
the initialization PR or a linked setup record. Historical foundation results do
not replace these checks.

## Recovery and Escalation

If a contact is unavailable or a link points to the foundation, correct it before
publishing the new repository's issue forms or security policy. If settings differ
from the checklist, record the gap and responsible maintainer; do not claim the
control is active. Reverse unmerged setup changes on the topic branch and rerun
the checks. A published reporting address or exposed credential may require the
[credential-exposure procedure](secret-rotation.md), not only a Git revert.

## Related Documents

- [GitHub configuration runbook](configure-github.md) - Platform setup and live verification.
- [Repository ownership](../standards/ownership.md) - Maintainer and review-owner responsibilities.
- [Repository roadmap](../roadmap/README.md) - Foundation history and project milestones.
- [Documentation standards](../standards/documentation.md) - Project documentation and navigation.
