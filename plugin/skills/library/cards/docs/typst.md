---
name: typst
title: Typst
area: docs
tags: [typst, documents, typesetting, markup, pdf, scripting]
detect: [file:*.typ, file:typst.toml, ext:.typ]
related: [latex, technical-writing]
---
Typst documents: markup with embedded scripting, fast incremental compiles, packages from the Typst universe.

## Verify
- `typst compile main.typ`: the document compiles to PDF with no errors or warnings.
- `typst compile --root . main.typ out.pdf`: the project root is explicit so imports of files outside the entry directory resolve.
- `typst fonts`: the fonts the document names are actually installed (add `--font-path` if not).
- `typst query main.typ "<fig-results>"`: a labeled element exists (prints JSON; empty means missing).

## Test first
The compile is the check. Add the failing reference or content first and let `typst compile` report it.
```bash
# fails while @fig:results or the imported function does not exist
typst compile main.typ /tmp/out.pdf
```
Reference a label that doesn't exist yet (`@fig:results`), see the error with its line, then add `<fig:results>` after the figure. For reusable templates, keep a small sample document per template and compile each in CI.

## Do
- Set document defaults once at the top: `#set page(paper: "a4", margin: 2cm)`, `#set text(font: "...", size: 11pt)`, `#set heading(numbering: "1.")`.
- Use `#show` rules for global styling instead of repeating formatting.
- Label elements with `<name>` and reference with `@name`; cite with `@key` after `#bibliography("refs.bib")`.
- Put reusable pieces in functions in a separate file and `#import "lib.typ": func`.
- Use `#figure(image("x.png"), caption: [...])` so figures are numbered and referenceable.
- Import packages with a pinned version: `#import "@preview/name:0.1.0": *`.
- Use `typst watch main.typ` while writing for incremental recompiles.
- Declare package metadata in `typst.toml` (name, version, entrypoint) when publishing a package.

## Avoid
- Writing LaTeX commands (`\section`, `$$`): not Typst. Use `= Heading`, `$ x^2 $` for math with spaces for display.
- Forgetting the `#` before code in markup mode: it prints as text. Inside code blocks and brackets no `#` is needed.
- Unpinned or invented `@preview` package versions: the compile fails or changes later. Pin a version that exists.
- Mixing content mode `[...]` and code mode `{...}` wrongly in arguments: a string passed where content is expected. Use `[text]` for content, `"text"` for strings.
- Absolute file paths in `image()` or `#import`: break elsewhere. Use paths relative to the file, and `--root` when needed.
- Assuming fonts exist on CI: warnings about unknown font family. Bundle fonts and pass `--font-path`.
- Heavy computation in scripts on every compile: slow. Precompute data into a file.

## Review
- [ ] `typst compile` exits cleanly with no warnings.
- [ ] Package imports have exact versions; templates are imported, not copied.
- [ ] Labels referenced in text all exist.
- [ ] Fonts and images are bundled or documented, with relative paths.
- [ ] Styling is in `set` and `show` rules, not repeated inline.
