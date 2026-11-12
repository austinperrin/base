# Credential Exposure Response

[Docs](../README.md) > [Runbooks](README.md) > Credential Exposure Response

## Objective and Triggers

Contain a suspected credential exposure, restore authorized access, and document
the outcome privately. Start when a contributor reports an exposure, a scanner
flags a possible credential, or provider activity suggests unauthorized use.
The [security policy](../../SECURITY.md) owns immediate handling and reporting.

This procedure applies regardless of where credentials are stored. It does not
select the storage or delivery approach left open in
[ADR-0002](../adr/0002-secret-management.md).

## Prerequisites and Access

Identify a responsible maintainer under the
[ownership standard](../standards/ownership.md) and an authorized operator for
the affected service. Confirm access to its credential controls, activity records,
and the workloads that use the credential. If access is unavailable, contact the
responsible owner through the private reporting channel; do not wait for repository
cleanup to request containment.

Keep the incident discussion and evidence in an approved private location. Record
credential identifiers, affected paths, commit IDs, and timestamps without copying
credential values into issues, commands, logs, or this repository.

## Procedure

### Contain and Assess

1. Follow the security policy's immediate revocation or rotation requirement at
   the issuing provider. Confirm that the affected credential is disabled, expired,
   or replaced according to that provider's documented behavior. Determine whether
   dependent sessions or derived credentials also need invalidation.
2. Identify the affected service, permissions, workloads, exposure interval, and
   distribution paths. Consider branches and tags, forks and clones, PR content,
   workflow logs, artifacts, caches, and release assets where applicable. Record
   what is confirmed separately from what still needs investigation.
3. Review available provider activity for unexpected access or changes. Escalate
   suspected misuse or access to sensitive data to the responsible maintainer.
   Keep necessary evidence private and redact it before sharing. If investigation
   establishes a false positive, record that basis without declaring other findings
   resolved automatically.

### Restore Access and Remove Exposure

4. If the workload still needs access, issue a replacement through the approved
   provider process with the required permissions. Update only its authorized
   consumers using the project's selected delivery mechanism. Verify access with
   a normal operation that does not print credentials. Do not introduce a local
   configuration file or a secret-store integration solely to follow this runbook.
5. Remove sensitive content from current tracked files and other affected locations.
   Keep changes focused on the incident and follow the normal review process.
   Check the applicable ignore rules and configuration examples; removing a file
   from the current checkout does not remove earlier copies.
6. Assess historical cleanup separately from credential invalidation. Follow the
   platform's current [sensitive-data removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
   with a maintainer-reviewed plan identifying affected references, collaborators,
   recovery requirements, and any platform-support actions. Invalidate access first;
   a history rewrite may not be necessary once the credential is revoked.
7. If historical cleanup is required, coordinate it with repository owners and
   platform support before executing it. Preserve branch protections and reviewed
   change controls. This runbook does not authorize a history rewrite or bulk force
   pushes. If the approved controls prevent the proposed cleanup, stop and escalate
   for a supported remediation plan. Coordinate affected forks and clones to avoid
   reintroducing removed content; a central cleanup cannot erase independent copies.

## Verification and Evidence

Confirm invalidation through provider status or an approved check that does not
log the old value. Verify that authorized workloads function with the replacement,
and review available activity records for unresolved misuse. Record any access
or visibility limitations explicitly.

For a repository exposure, use the
[credential-check reference](../architecture/external-checks.md#gitleaks) to prepare the pinned
scanner and complete current-branch history, then run:

```bash
./scripts/ci/check-credentials.sh
```

Inspect redacted findings and the result. This check covers current-branch history
and staged changes; it does not cover every branch, external copy, untracked file,
or provider state. A revoked credential retained in history can still cause a
failure. Resolve that finding through the reviewed remediation plan rather than
treating revocation as a passing scan or bypassing the required check.

Before closing the incident, the responsible maintainer reviews containment,
replacement access, misuse assessment, cleanup results, and outstanding actions.
Record owners for remaining work and the changes that will prevent recurrence.
Use provider-specific instructions and the [OWASP secrets-management guidance](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
when checking credential lifecycle and audit requirements.

## Recovery and Escalation

If replacement access fails, correct its permissions or delivery with the service
owner. Keep the exposed credential invalidated; do not restore it to recover
availability. If removal or cleanup fails, preserve the private incident record,
stop the unsuccessful operation, and escalate with the affected references and
remaining risks. A successful scanner run does not by itself close the incident.

## Related Documents

- [Security policy](../../SECURITY.md) - Immediate handling and private reporting.
- [ADR-0002: Secret Management](../adr/0002-secret-management.md) - Pending storage and delivery decision.
- [External checks and installation](../architecture/external-checks.md#gitleaks) - Scanner scope and limitations.
- [Repository ownership](../standards/ownership.md) - Maintainer responsibilities.
