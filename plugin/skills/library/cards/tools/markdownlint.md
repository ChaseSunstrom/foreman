---
name: markdownlint
title: markdownlint
area: tools
tags: [markdown, lint, docs, formatting, ci]
detect: [file:.markdownlint*, dep:markdownlint-cli, dep:markdownlint-cli2]
related: [mkdocs, docusaurus, pre-commit, yamllint]
---
markdownlint: rule-based style checks for Markdown files (headings, lists, fences, line length), configured in .markdownlint files.

## Verify
- `npx markdownlint-cli2 "**/*.md" "#node_modules"`: lint all Markdown, excluding dependencies.
- `npx markdownlint-cli2 --fix "**/*.md" "#node_modules"`: apply fixable rules, then re-run the check.
- `npx markdownlint .`: the same with the original CLI (`markdownlint-cli`).
- `npx markdownlint -c .markdownlint.json README.md`: lint with an explicit config file.
- `git diff --stat`: after `--fix`, only intended files changed.

## Test first
Lint a file with the violation.
```
printf '# Title\n### Skipped level\n\n* item\n- item\n' > /tmp/t.md
npx markdownlint /tmp/t.md
# expect MD001 (heading increment) and MD004 (list marker style)
```
Fix, and rerun to exit 0.

## Do
- Put rule settings in `.markdownlint.json` or `.markdownlint.yaml` (for `markdownlint-cli2`, also `.markdownlint-cli2.jsonc` with `globs` and `ignores`).
- Keep defaults, and disable only rules the repo cannot follow (often MD013 line length, MD033 inline HTML, MD041 first-line heading).
- Give fenced code blocks a language (MD040), so highlighting works.
- Keep a single H1, and increment headings one level at a time.
- Use blank lines around headings, lists and fences.
- Disable one spot with `<!-- markdownlint-disable-next-line MD033 -->`.
- Run in CI and pre-commit on changed Markdown.

## Avoid
- Disabling MD013 globally and also wrapping at 80 by hand: choose one. If you wrap, set `line_length` and exclude tables and code.
- Running `--fix` on generated docs (CHANGELOG from a release tool): it will be regenerated. Add it to ignores.
- Inline HTML in docs sites (MDX, admonitions) tripping MD033: allow the specific elements in `allowed_elements`.
- MD024 duplicate headings in changelogs: set `siblings_only: true`.
- Trailing spaces used as line breaks (MD009): use a backslash or `<br>` instead.
- Linting `node_modules` or vendored docs: ignore them, or the run takes minutes and fails.

## Review
- [ ] markdownlint exits 0 on changed Markdown with the repo config.
- [ ] Each disabled rule has a reason, preferably scoped to a file or line.
- [ ] Code fences have languages and headings have a single H1.
- [ ] Generated Markdown is ignored, not hand-fixed.
