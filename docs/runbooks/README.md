# Operational Runbooks

[Docs](../README.md) > Runbooks

Runbooks describe how to carry out maintenance and operational tasks. Each
procedure identifies its trigger, required access, execution steps, verification,
and recovery actions. Link to the owning standard for policy and conventions.

## Index

| Runbook | When to use it |
| :--- | :--- |
| [Runbook template](template.md) | Create a procedure for a repeatable task |
| [Initialize a project repository](initialize-repository.md) | Turn the foundation into a new project repository |
| [Issue triage](issue-triage.md) | Review incoming requests and reassess open work |
| [Dependency maintenance](dependency-maintenance.md) | Review automated and manual dependency updates |
| [Release process](release-process.md) | Verify and publish a reviewed repository version |
| [Credential exposure response](secret-rotation.md) | Contain an exposure, restore access, and verify remediation |

## Authoring and Maintenance

Start with the template and follow the
[documentation standard](../standards/documentation.md). Register the procedure
here and link it from the standard or implementation it supports.

Describe commands and expected results for tools already available to the
operator. State required permissions without requesting credentials in issues
or logs. Include recovery actions appropriate to the operation; do not imply
that every action can be undone. Verify the procedure when its dependencies change.
