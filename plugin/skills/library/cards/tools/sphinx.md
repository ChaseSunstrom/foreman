---
name: sphinx
title: Sphinx
area: tools
tags: [sphinx, docs, python, rst, autodoc, myst]
detect: [file:conf.py, dep:sphinx, file:*.rst]
related: [mkdocs, docusaurus, pre-commit]
---
Sphinx: reStructuredText or MyST documentation with autodoc, cross-references and warnings as errors.

## Verify
- `sphinx-build -W --keep-going -b html docs docs/_build/html`: builds; warnings fail the build, but all are reported.
- `sphinx-build -b linkcheck docs docs/_build/linkcheck`: external links resolve.
- `sphinx-build -b doctest docs docs/_build/doctest`: doctest blocks in docs and docstrings pass.
- `sphinx-autobuild docs docs/_build/html`: live reload preview (needs the `sphinx-autobuild` package).

## Test first
Practice check: an unresolved reference must fail the build.
```sh
printf 'See :ref:`no-such-label`.\n' > docs/_probe.rst
sphinx-build -W -b html docs /tmp/out; echo $?    # expect non-zero
rm docs/_probe.rst
```
Use `nitpicky = True` in `conf.py` to flag missing cross-reference targets.

## Do
- Use `-W --keep-going` in CI and a Makefile target for builds.
- Enable extensions in `conf.py`: `sphinx.ext.autodoc`, `sphinx.ext.napoleon` (Google or NumPy docstrings), `sphinx.ext.intersphinx`, `sphinx.ext.viewcode`.
- Use `myst_parser` for Markdown sources; set `source_suffix` for both.
- Cross-reference with roles: `:class:`, `:func:`, `:ref:` and `:doc:`; give labels for pages you link to.
- Configure `intersphinx_mapping` so references to Python and other libraries resolve.
- Use `autodoc_typehints` and keep docstrings accurate to the signature; use `sphinx-apidoc` once to scaffold.
- Run doctests (`sphinx.ext.doctest`) so examples stay true.
- Pin Sphinx, the theme and extensions in docs requirements.

## Avoid
- Building without `-W`: broken references and bad RST only warn. Make warnings errors.
- Importing the package from `conf.py` in an environment where it is not installed: autodoc fails. Install the project in the docs environment, or mock imports with `autodoc_mock_imports`.
- Markdown headings in `.rst` files or RST syntax in `.md`: mixed syntax renders wrong. Match the parser.
- Inconsistent heading underline lengths or levels: warnings. Keep a consistent adornment order.
- Committing `_build/`: generated. Ignore it.
- Unpinned theme and extension versions: layout and warnings change under you.
- Hand-written signatures in prose: they drift. Use autodoc directives.

## Review
- [ ] The strict build passes in CI with pinned requirements.
- [ ] linkcheck and doctest were run.
- [ ] Public API is documented through autodoc, with intersphinx links.
- [ ] `_build/` is not committed.
