# Security Policy

[Repository Home](README.md) > Security Policy

The security of this project and its users is a top priority. We appreciate and
encourage responsible disclosure of vulnerabilities in the repository and its
contents, including tooling and automation as they are introduced.

---

## Supported Versions

Security fixes target the current reviewed contents of `main`. A supported-release
policy will be defined when versioned releases are introduced; `main` is a branch,
not a release version. This scaffolding group does not establish support guarantees
for older release versions.

---

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover or suspect a vulnerability, report it privately through one of
these channels:

1. **GitHub Private Vulnerability Reporting, if enabled**:
   * Open the repository's **Security and quality** tab and select
     **Report a vulnerability** if the option is available.
   * If private reporting is unavailable, use the contact email below.
   * See GitHub's [private reporting guidance](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately).
2. **Direct Contact**:
   * Email [perrinaustin@gmail.com](mailto:perrinaustin@gmail.com) with the
     subject `[SECURITY] Vulnerability Report: <Brief Description>`.

Publishing this policy does not enable GitHub's private vulnerability reporting
feature; its availability depends on the repository's settings.

### What to Include in Your Report

To help maintainers assess and reproduce the issue, include:

* A description of the vulnerability and its potential impact.
* Reproduction steps or a proof of concept, with affected file paths or commit versions.
* Relevant environment and tool versions.
* Suggestions for remediation, if known.

Do not include live credentials, private keys, or unrelated personal data.
Use descriptions and redacted examples to identify affected secrets.

---

## Response Timeline

* **Acknowledgment**: We aim to acknowledge receipt within **48 hours**.
* **Assessment and fix**: We assess the report and provide updates while developing
  and verifying a fix. Resolution time depends on the issue's impact and complexity.
* **Public disclosure**: We coordinate disclosure with the reporter after a fix is
  available and credit the reporter with their consent.

---

## Exposed Credentials

If a credential is exposed, assume it is compromised and revoke or rotate it at
its source immediately. Deleting a file or commit alone does not invalidate it;
report the exposure privately through the channels above without sharing its value.

The project's storage and delivery approach remains open in
[ADR-0002: Secret Management](docs/adr/0002-secret-management.md).
Detailed rotation and repository-cleanup procedures remain pending the repository
maintenance group, and automated security checks remain pending the enforcement
group in the [scaffolding roadmap](docs/roadmap/milestone-0-repository-scaffolding.md).

## Related Documents

- [ADR-0002: Secret Management](docs/adr/0002-secret-management.md) - Options for storing and delivering secrets.
- [Project roadmap](docs/roadmap/README.md) - Planned security tooling and maintenance work.
