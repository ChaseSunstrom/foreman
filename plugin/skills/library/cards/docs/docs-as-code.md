---
name: docs-as-code
title: Docs as code
area: docs
tags: [docs, markdown, mkdocs, ci, links, static-site, review]
detect: [dep:mkdocs, dep:mkdocs-material, dep:@docusaurus/core, dep:vitepress, dep:sphinx, file:mkdocs.yml, file:docusaurus.config.js]
related: [api-docs, technical-writing, diagrams-as-code, adrs]
---
Documentation treated like software: plain-text sources in the repo, reviewed in pull requests, built and link-checked in CI, published from main.

## Verify
- `mkdocs build --strict`: the MkDocs site builds and warnings (broken links, missing pages) fail it.
- `npx docusaurus build`: the Docusaurus site builds, and broken links fail the build by default.
- `npx vitepress build docs`: the VitePress site builds (dead links fail unless ignored in config).
- `sphinx-build -W -b html docs docs/_build`: the Sphinx site builds with warnings as errors.

## Test first
Break the build deliberately for the doc problem you are fixing, then fix it. A broken link or missing nav entry is a failing test.
```sh
# CI step: docs must build clean
mkdocs build --strict
# and code samples in docs must run
python -m doctest -v docs/examples.md
```
Add the doc page or the example check first, watch it fail, then write the content.

## Do
- Keep docs in the same repo and pull request as the code, so a code change and its doc change merge together.
- Organise by reader need: tutorial, how-to guide, reference and explanation, and keep each page to one kind.
- Make the navigation explicit in config, and put one stable URL on every page.
- Build in CI with strict mode, check external links on a schedule, and publish from the main branch only.
- Lint prose and markdown (markdownlint, Vale) with the project's rules.
- Execute code samples in tests, or pull snippets from real files so they cannot drift.
- Use relative links between pages, and redirects when a page moves.
- Put an owner and a "last reviewed" convention in front matter or CODEOWNERS for each docs area.

## Avoid
- Docs in a separate wiki: they drift from the code. Keep them in the repo with the code.
- Non-strict builds: broken links ship quietly. Fail on warnings.
- Absolute URLs to your own site in pages: they break in previews and forks. Use relative links.
- Pasting long code that is never run: it rots. Include real files or test the snippet.
- One huge page: nobody finds anything. Split by task and cross-link.
- Moving pages without redirects: bookmarks and search results die. Add a redirect entry.

## Review
- [ ] A strict docs build passes locally and in CI.
- [ ] Links, anchors and navigation entries resolve.
- [ ] Code samples are executed or sourced from tested files.
- [ ] Each page serves one purpose (tutorial, how-to, reference or explanation).
- [ ] Moved or renamed pages have redirects.
