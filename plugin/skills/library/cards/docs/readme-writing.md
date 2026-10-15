---
name: readme-writing
title: Writing a README
area: docs
tags: [readme, onboarding, docs, quickstart, markdown]
detect: []
related: [technical-writing, docs-as-code, changelogs, api-docs]
---
READMEs that get a new reader from "what is this" to a running example in minutes, with commands that were actually run.

## Verify
- `grep -n "^#" README.md`: headings show the expected order (name, purpose, install, usage, development, license).
- `grep -nE "\]\((\./|docs/)[^)]*\)" README.md`: lists relative links, each of which must point to an existing file.
- `markdownlint README.md`: markdown style passes (when markdownlint is installed).
- Run the Install and Usage commands in a clean checkout or container: the steps work exactly as written.

## Test first
A README is correct only if a stranger's first run succeeds. Write the quickstart, then execute it in a fresh directory before publishing.
```sh
git clone . /tmp/readme-check && cd /tmp/readme-check
# paste the README quickstart commands here, one per line
# expected: the documented output appears and the exit code is 0
```
If a step fails, fix the README or the project, not the reader.

## Do
- Open with one sentence saying what the project does and for whom, then the single most useful example.
- Put Install and a minimal Usage example in the first screenful, with copyable code blocks and expected output.
- State requirements (language version, OS, services) before the install commands.
- Add a short Development section: how to run tests, lint and build, using the same commands CI uses.
- Link out for depth (docs, API reference, contributing, changelog) instead of growing the README.
- Show status honestly: stability, supported versions, known limits.
- State the license and how to report a bug or a security issue.
- Keep badges few and meaningful (build, version), and place them under the title.

## Avoid
- A table of contents and history before any example: readers leave. Lead with what it does and how to run it.
- Commands that were never run: they fail on a clean machine. Execute them and keep them updated.
- Screenshots as the only explanation: not searchable and they rot. Pair with text and output.
- Jargon and internal names with no definition: newcomers stall. Define a term at first use.
- Duplicating API reference in the README: it drifts. Link to the generated reference.
- Stale version numbers hard-coded in install steps: use the latest-version mechanism or update on release.

## Review
- [ ] The first paragraph says what it is and who it is for.
- [ ] Quickstart commands were run from a clean checkout and work.
- [ ] Requirements, test command, license and issue-reporting path are present.
- [ ] Links resolve, and badges reflect real state.
- [ ] Depth lives in linked docs, not in the README.
