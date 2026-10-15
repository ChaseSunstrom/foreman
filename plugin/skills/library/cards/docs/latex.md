---
name: latex
title: LaTeX
area: docs
tags: [latex, tex, documents, bibtex, pdf, typesetting]
detect: [file:*.tex, file:*.bib, file:latexmkrc, file:.latexmkrc, ext:.tex]
related: [typst, technical-writing, mermaid]
---
LaTeX documents: reproducible builds with latexmk, bibliographies with biblatex, warning-free output.

## Verify
- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: a full build, including bibliography and repeated passes, succeeds.
- `grep -nE "Warning|undefined|Overfull" main.log`: no undefined references, citations or bad boxes remain.
- `chktex -q main.tex`: style lint (spacing, dashes, punctuation).
- `latexmk -C`: clean build artifacts so the next build proves it starts from nothing.

## Test first
The document is the test: add the reference or citation first, build, and let the log fail it.
```bash
# fails while \ref{sec:new} or \cite{key} has no target
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
! grep -E "undefined|Citation .* undefined|Overfull \\\\hbox" main.log
```
Then add the `\label` or `.bib` entry and rebuild until the grep is clean. For templates, keep a minimal `.tex` per feature under `tests/` and build each in CI.

## Do
- Build with `latexmk`, never by hand-running `pdflatex` N times; keep options in `latexmkrc`.
- Use `biblatex` with `biber` (`\usepackage[backend=biber]{biblatex}`, `\addbibresource{refs.bib}`, `\printbibliography`).
- Put `\label` right after `\caption` or the sectioning command, and cite with `\cref` (cleveref) or `\ref`; add `~` before refs to avoid line breaks.
- Load `hyperref` late and `cleveref` after it; `\usepackage[utf8]{inputenc}` is unnecessary on modern engines.
- Use `\input` or `\include` to split chapters; keep figures in a `figures/` folder with `\graphicspath`.
- Prefer vector figures (PDF, or TikZ/pgfplots) over screenshots.
- Use `siunitx` for numbers and units, `booktabs` for tables.
- Pick the engine for the need: `lualatex` or `xelatex` for system fonts via `fontspec`.

## Avoid
- `$$ ... $$` display math: bad spacing. Use `\[ ... \]` or `equation`/`align`.
- `\bibliographystyle`/`bibtex` mixed with `biblatex`: conflicting. Use one system.
- Hardcoded numbers in text ("see Figure 3"): breaks on reorder. Use `\ref`.
- `eqnarray`: obsolete spacing. Use `align` from amsmath.
- Ignoring Overfull `\hbox` warnings: text runs off the margin. Rephrase, allow hyphenation or use `\sloppy` locally.
- Committing generated files (`*.aux`, `*.bbl`, `*.log`, `*.pdf` unless wanted): ignore them.
- Special characters unescaped (`%`, `&`, `_`, `#`, `$`): compile errors or silent truncation after `%`. Escape with a backslash.

## Review
- [ ] A clean `latexmk` build succeeds with no undefined references or citations.
- [ ] No Overfull boxes of consequence remain.
- [ ] Figures and tables have captions and labels and are referenced in text.
- [ ] One bibliography system is used and every `\cite` resolves.
- [ ] Build artifacts are gitignored; build options live in `latexmkrc`.
