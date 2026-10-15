---
name: technical-writing
title: Technical writing
area: docs
tags: [documentation, writing, readme, markdown, style, docs]
detect: []
related: [mermaid, latex, typst]
---
Technical docs: READMEs, how-tos, references and changelogs that a reader can follow and a linter can check.

## Verify
- `vale .`: prose style rules from `.vale.ini` pass (when configured).
- `markdownlint-cli2 "**/*.md"`: Markdown structure (heading levels, lists, fences) is valid.
- `lychee --offline .`: relative links and anchors resolve (drop `--offline` to check external URLs).
- `codespell docs README.md`: no common misspellings.
- `grep -rn "TODO\|TBD\|lorem" docs README.md`: no placeholders left.

## Test first
Treat each documented instruction as a test: run it from a clean checkout and let it fail before the doc is right.
```bash
# fails until the quickstart in README.md actually works
set -e
git clone . /tmp/qs && cd /tmp/qs
bash -c "$(sed -n '/^```bash/,/^```/p' README.md | sed '1d;$d')"
```
Better, extract the commands into a script or doctest that CI runs, and have the README include or mirror it. For API docs, a failing example is a failing build.

## Do
- Open with what it is and who it is for in one or two sentences, then the fastest working example.
- Separate the four kinds: tutorial (learn), how-to (task), reference (facts), explanation (why). One page, one kind.
- Write steps as numbered imperatives, one action each, with the expected output shown after.
- Give copy-pasteable commands in fenced blocks with a language tag; state prerequisites and versions up front.
- Use the same term for the same thing everywhere; define each acronym on first use.
- Keep headings descriptive and stable (they become anchors); one H1 per file.
- Show the failure case: the exact error text and its fix.
- Update docs in the same change as the behavior, and note breaking changes in the changelog (Keep a Changelog headings: Added, Changed, Fixed, Removed).

## Avoid
- Instructions never run by the author: they rot. Run them in CI or a clean container.
- Screenshots of terminal text: not searchable or diffable. Paste text.
- Passive filler ("it should be noted that", "simply", "just"): cut it; if a step isn't easy to the reader, "simply" insults them.
- Absolute local paths and personal names in examples: use placeholders such as `<project-dir>`.
- Documenting every option in prose that duplicates `--help` or the schema: generate reference from the source of truth.
- Links with text like "click here": use descriptive text so scanning works.
- Undated version claims ("latest"): state the version or link the changelog.

## Review
- [ ] The first screen says what this is, who it is for and how to start.
- [ ] Every command was run from a clean state and its output matches.
- [ ] Links, anchors and code samples are checked by a tool.
- [ ] Terminology and heading levels are consistent; no placeholders remain.
- [ ] Changelog and affected pages updated with the code change.
