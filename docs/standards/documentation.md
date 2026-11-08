# Documentation Standards & Style Guide

[Docs](../README.md) > [Standards](README.md) > Documentation Standards

This document defines the canonical rules for writing, organizing, and maintaining documentation across this repository. Both human contributors and AI coding assistants are required to follow these guidelines.

---

## Editorial Style Guide: Google Developer Documentation Style

This repository adopts the **[Google Developer Documentation Style Guide](https://developers.google.com/style)** as its editorial standard, as recorded in [ADR-0001](../adr/0001-adopt-google-documentation-style.md). All documentation should strive to be clear, concise, direct, and accessible to developers worldwide.

### Core Writing Rules

1. **Use Active Voice**:
   * Incorrect: *The documentation index should be updated by the contributor.*
   * Correct: *Update the documentation index.*
2. **Write in the Second Person ("You")**:
   * Address the reader directly rather than referring to an ambiguous group or a third person.
3. **Use Present Tense**:
   * Incorrect: *This index will list the repository standards.*
   * Correct: *This index lists the repository standards.*
4. **Be Direct and Concise**:
   * State the most important information first. Avoid filler phrases such as *"in order to,"* *"please note that,"* or *"it is important to remember that."*
5. **Use Plain Language**:
   * Choose simple, everyday words over complex terminology. Prefer *use* to *utilize* and *start* to *commence*.
6. **Descriptive Hyperlink Text**:
   * Use a descriptive destination name for each link. The anchor text must describe the destination:
   * Incorrect: *For repository standards, click [here](README.md).*
   * Correct: *Follow the [Repository Standards](README.md).*

---

## Navigation and Anti-Drift Architecture

### 1. Single Source of Truth (Anti-Drift Rule)
* **Never duplicate instructions or explanations** across multiple files.
* Every documented technical concept, workflow, or architectural pattern has exactly one canonical owning document in `docs/`.
* When another document references that concept, it **must summarize in 1–2 sentences and provide a direct relative Markdown hyperlink** to the canonical document.
* When updating a standard, inspect all linking documents to ensure consistency.

### 2. Hub-and-Spoke Navigation
All documentation files must fit cleanly into our navigation hierarchy:
* **Breadcrumbs**: Every leaf document inside `docs/` must start with a breadcrumb trail linking back to the documentation hub:
  ```markdown
  [Docs](../README.md) > [Category](README.md) > Document Name
  ```
* **Directory Index (`README.md`)**: Every directory inside `docs/` must contain a `README.md` listing and summarizing every document in that folder.
* **Related Documents**: Every leaf document must end with a `## Related Documents` section providing at least one useful companion link; prefer 2–4 relevant links. Select documents that help readers continue or understand the topic.

Related Documents is a curated reading list, not an inventory of every reference.
Keep supporting links near the content they explain. The section does not need to
repeat breadcrumbs, links used only in examples, a category's index entries, or an
existing canonical-reference table. A particularly useful companion document may
appear in both the body and the related section.

### 3. Root-Level Documents and Indexes

Standalone root-level guides and policies, including `CONTRIBUTING.md`, `SECURITY.md`,
and `CODE_OF_CONDUCT.md`, use a breadcrumb below their title:

```markdown
[Repository Home](README.md) > Document Name
```

These documents also end with a curated Related Documents section. Keep navigation
outside preserved license, covenant, or attribution text rather than rewriting that text.

The root README and category indexes provide their own navigation and do not
require a separate Related Documents section, though they may include one.
License files retain their original format and notices.

---

## Markdown Formatting Rules

Adhere to GitHub Flavored Markdown (GFM) and standard linter conventions:

### Headings
* Use **ATX-style headings** (`#`, `##`, `###`) exclusively. Do not use underline-style (`===` or `---`).
* Every document must have exactly one top-level `# Heading` matching the document title.
* Maintain a strict hierarchical heading order (do not jump from `##` directly to `####`).

### Code Blocks
* **Always declare the language** on fenced code blocks. Never leave triple backticks bare:
  ````markdown
  ```bash
  git status
  ```
  ````
* Use `text` or `plaintext` for terminal output or generic text snippets.

### Relative Linking
* Always use **relative paths** for links within the repository (for example, `[Documentation Standards](documentation.md)` or `[Architecture Decision Records (ADRs)](../adr/README.md)`).
* Do not use absolute GitHub web URLs for internal repository links, as these break across forks and branches.

---

## Diagram Standards (Mermaid.js)

We use **Mermaid.js** for all diagrams so that architecture and workflows remain editable, version-controlled, and searchable.

### Guidelines for Mermaid Diagrams:
1. **Supported Diagram Types**:
   * Flowcharts: `flowchart TD` (top-to-bottom) or `flowchart LR` (left-to-right).
   * Sequence Diagrams: `sequenceDiagram`.
   * State Diagrams: `stateDiagram-v2`.
   * Entity Relationship: `erDiagram`.
2. **Quote Node Labels**: Always wrap labels containing special characters, brackets, or parentheses in double quotes to prevent syntax errors:
   ```text
   flowchart TD
       A["Client (Web Browser)"] --> B["API Gateway"]
   ```
3. **Keep Diagrams Focused**: Do not exceed 15–20 nodes in a single diagram. Break large diagrams into subsystem overviews.

---

## Automated Style Linting (Vale)

**Status: Local check available; CI integration pending.** [Vale](https://docs.vale.sh/) is a prose linter
that checks enabled style rules. The [Google style package](https://github.com/vale-cli/Google)
implements machine-checkable parts of Google's guide; it is maintained separately
and is not maintained or endorsed by Google.

These checks can flag patterns such as terminology, capitalization, and punctuation.
They do not guarantee full compliance with the guide, technical accuracy, or useful
explanations. Human review remains necessary. Documentation structure and link
integrity are separate concerns, described below.

The [Vale implementation reference](../architecture/ci-cd.md#vale) owns setup,
commands, pinned engine and rule versions, vocabulary, scope, and blocking
severity. Configuration lives in [`.vale.ini`](../../.vale.ini). Enabled errors
block the local check; warnings and suggestions support editorial review.
A failed check can block merging once CI and required repository settings are
implemented and verified.

---

## Automated Structure Checks

**Status: Local checks available; core CI defined, with live verification pending.** The
[repository checks and CI reference](../architecture/ci-cd.md) documents commands,
coverage, and parsing limits for heading structure, fenced blocks, registration,
navigation, and local link integrity.

Run the applicable checks and verify the full conventions during review.
Check that examples are accurate, indexes are current, and linked files are
already committed or included in the same change. When creating or changing an
architectural decision, follow the
[Architecture Decision Record (ADR) standards](architecture-decisions.md).

## Related Documents

* [Standards Index](README.md) - Category index for repository standards.
* [Architecture Decision Record (ADR) standards](architecture-decisions.md) - Decision structure and lifecycle.
* [Architecture Decision Records (ADRs) index](../adr/README.md) - Decisions and their review status.
* [ADR-0001: Google Developer Documentation Style](../adr/0001-adopt-google-documentation-style.md) - Rationale for the adopted editorial standard.
