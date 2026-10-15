---
name: mkdocs
title: MkDocs
area: tools
tags: [mkdocs, docs, markdown, material, static-site, python]
detect: [file:mkdocs.yml, dep:mkdocs, dep:mkdocs-material]
related: [sphinx, docusaurus, pre-commit]
---
MkDocs (with Material): a Markdown documentation site configured by `mkdocs.yml`, built strictly in CI.

## Verify
- `mkdocs build --strict`: the site builds and warnings (broken links, missing nav files) become errors.
- `mkdocs serve`: live preview at localhost with reload while editing.
- `mkdocs build --strict --site-dir /tmp/site && ls /tmp/site | head`: the output directory has the expected pages.

## Test first
Practice check: a broken link or missing nav file must fail the strict build.
```sh
printf '[x](missing.md)\n' > docs/_probe.md
mkdocs build --strict; echo $?     # expect non-zero
rm docs/_probe.md
```
Add the strict build to CI so doc breakage fails pull requests.

## Do
- Set `strict: true` in `mkdocs.yml` or always pass `--strict`.
- Define `nav:` explicitly for ordering; keep pages under `docs/`.
- Pin `mkdocs`, the theme and plugins in a requirements or lock file.
- Link between pages with relative paths to `.md` files (`../guide/setup.md`), not site URLs.
- Use Material features via `theme.features` and `markdown_extensions` (`admonition`, `pymdownx.superfences`, `toc` with `permalink`).
- Generate API docs with `mkdocstrings` and a handler for your language, not hand-copied signatures.
- Set `site_url` so sitemap and canonical links work; set `repo_url` and `edit_uri`.
- Deploy built output from CI to Pages or object storage.

## Avoid
- Absolute or root-relative links (`/guide/`): they break when the site is hosted under a path. Use relative file links.
- Skipping `--strict`: broken links and nav entries pass silently. Use it in CI.
- Unpinned plugin versions: a theme or plugin update changes the build. Pin them.
- Putting `docs_dir` content outside the `docs` folder via symlinks: files are skipped on some platforms. Set `docs_dir` or copy.
- Committing `site/`: it is generated. Add it to `.gitignore`.
- Putting secrets, internal hostnames or tokens in docs examples.
- Material-only extensions without installing `mkdocs-material`: the build fails on unknown config.

## Review
- [ ] `mkdocs build --strict` passes in CI with pinned dependencies.
- [ ] Every page is in `nav` (or intentionally not).
- [ ] Links are relative file links and all resolve.
- [ ] Code samples in docs were run.
- [ ] `site/` is ignored.
