# ADR-0002: Secret Management

[Docs](../README.md) > [ADR](README.md) > ADR-0002

* **Status**: Proposed
* **Date**: 2026-11-07
* **Authors**: @austinperrin
* **Deciders**: Pending assignment by the project

## 1. Context and Problem Statement

The project needs to decide how secrets are stored, supplied to its
applications and automation, and maintained over time. Local development, CI,
and deployed environments can have different requirements.

This ADR provides options for that decision. No storage mechanism, provider,
configuration file format, or application integration is selected by this record.
Keep this record Proposed until the project records and approves its choice.

A project that does not yet need secrets can leave this decision open. Revisit it
before introducing a workload or integration that requires credentials. Repository
setup alone does not require creating a secret store or configuration file.

The repository's [ignore rules](../../.gitignore) exclude common local credential
files. They do not determine how the project must store or deliver secrets.
Security reporting follows the [security policy](../../SECURITY.md). Detailed
rotation and recovery follow the
[credential-exposure procedure](../runbooks/secret-rotation.md), independently of
the storage approach selected here.

## 2. Decision Drivers

Evaluate the options against the project's actual needs:

- Environments and workloads that need secrets, including developer machines and CI.
- Who may read, change, or revoke credentials, and how that access is removed.
- Required audit history, rotation frequency, and credential lifetime.
- Availability requirements and behavior when the secret source cannot be reached.
- Integration effort, ongoing maintenance, and cost.
- How contributors obtain authorized development credentials without sharing production access.

## 3. Considered Options

| Option | Typical use case | Pros | Cons and responsibilities |
| :--- | :--- | :--- | :--- |
| **A. Local configuration files**, such as an ignored `.env` | Local development, offline work, or a tool running on a developer's machine | Simple to inspect and use; works offline; little supporting infrastructure | Files need protection on each machine; distributing and rotating copies requires coordination; the application needs a loading mechanism. An ignore rule does not protect a file outside Git. |
| **B. Runtime injection** through CI or hosting configuration | Automated jobs and applications running on a platform with secret configuration | Separates credentials from tracked configuration; can use the execution platform's access controls | Configuration may be spread across platforms; auditing and rotation depend on platform capabilities; environment variables can be exposed through logs, diagnostics, or child processes. |
| **C. Managed secret store** | Projects needing shared access policies, auditing, or coordinated rotation across workloads | Central management; access policies; audit and rotation capabilities, depending on the service | Adds integration and an operational dependency; may add cost; workloads need an identity to retrieve secrets and a plan for service failures. |

These options describe different parts of secret handling and can be combined.
For example, a managed store can supply credentials through runtime injection.
Choose the storage source and delivery mechanism for each environment rather
than assuming one option must serve the whole project.

For supporting guidance, see [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html).
[GitHub Actions secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)
illustrates platform storage and delivery for CI; it is an example, not a selected provider.

## 4. Decision Outcome

**Pending.** Complete the following for the project. Mark an environment
Not applicable if the project does not use it.

| Environment | Secret source and storage | Delivery mechanism | Reason for selection |
| :--- | :--- | :--- | :--- |
| Local development | Pending | Pending | Pending |
| CI | Pending | Pending | Pending |
| Production, if applicable | Pending | Pending | Pending |
| Other environments, if applicable | Pending | Pending | Pending |

- **Decision owner**: Pending.
- **Selected tools or providers**: Pending.
- **Alternatives declined and reasons**: Pending.
- **Approval date**: Pending.

## 5. Consequences and Trade-offs

Complete these after selecting an approach:

- **Benefits for this project**: Pending.
- **Accepted limitations and risks**: Pending.
- **Operational ownership and ongoing cost**: Pending.
- **Conditions that would trigger reconsideration**: Pending.

## 6. Implementation and Verification

Repository setup must not create `.env` files, install a secret loader, or require
a provider solely because this Proposed record exists. Introduce configuration
examples and integrations only when the project has selected an approach and has
a concrete need for them.

Record the work needed to implement and verify the decision. This is a decision
checklist; put operational commands in the project's canonical runbooks
and link to them here.

| Item to resolve | Project plan or evidence |
| :--- | :--- |
| Workload authentication and authorization | Pending |
| Developer access, onboarding, and access removal | Pending |
| Separation of development, CI, and production credentials | Pending |
| Rotation, revocation, and handling existing credentials during migration | Pending |
| Safe logging and failure behavior when secrets are missing or unavailable | Pending |
| Verification that authorized workloads can access only their intended secrets | Pending |
| Documentation and checks needed to maintain the selected approach | Pending |

Complete and review this decision using the
[Architecture Decision Record (ADR) standards](../standards/architecture-decisions.md).
Track any remaining implementation work explicitly.

## Related Documents

- [Architecture Decision Records (ADRs) index](README.md) - Decision history.
- [Architecture Decision Record (ADR) standards](../standards/architecture-decisions.md) - Decision structure and status lifecycle.
- [Security policy](../../SECURITY.md) - Private reporting and immediate guidance for exposed credentials.
- [Git ignore rules](../../.gitignore) - Version-control exclusions for local credential files.
