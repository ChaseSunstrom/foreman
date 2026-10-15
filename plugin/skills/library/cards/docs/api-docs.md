---
name: api-docs
title: API documentation
area: docs
tags: [api, openapi, docs, reference, typedoc, examples]
detect: [dep:typedoc, dep:@redocly/cli, dep:swagger-ui-express, dep:sphinx, dep:pdoc, file:openapi.yaml, file:openapi.json]
related: [docs-as-code, readme-writing, changelogs, technical-writing]
---
API reference docs generated from the source of truth (types, schema or annotations), with runnable examples and a lint in CI.

## Verify
- `npx @redocly/cli lint openapi.yaml`: the OpenAPI document is valid and follows the rules (when Redocly CLI is available).
- `npx typedoc --emit none`: TypeScript doc comments resolve with no errors or warnings about missing exports.
- `sphinx-build -W -b html docs docs/_build`: the Sphinx site builds with warnings treated as errors.
- `pdoc -o /tmp/apidocs mypackage`: the Python API docs generate from docstrings.

## Test first
Make the docs fail before you document: an example in the docs that must run, or a lint rule that must pass.
```python
# test_docs_examples.py: doctest-style check of every documented example
def test_documented_example_runs():
    import mylib
    assert mylib.parse("a=1") == {"a": 1}   # same call as in the docs
```
For OpenAPI, add the failing lint rule (such as required `operationId` and `description`) first, then fix the spec.

## Do
- Generate reference from one source of truth (OpenAPI, type annotations, docstrings), and never hand-copy it into prose.
- Give every operation or public symbol a one-line summary, its parameters with types and constraints, return or response shapes, and errors.
- Put a minimal working example next to each entry. Run the examples in tests.
- Document error responses with status code, body shape and cause, and the retry guidance.
- Document auth, rate limits, pagination, idempotency and versioning once, in a clear overview page.
- Mark deprecations with the replacement and removal version.
- Use stable operation IDs and anchors so links do not break across releases.
- Build the docs in CI with warnings as errors, and publish from main.

## Avoid
- Hand-written reference that drifts from the code: wrong in a release. Generate it and fail CI on diffs.
- Examples that were never run: copy-paste fails for readers. Execute them in tests.
- Describing fields as "the name" or "the id": restating the identifier. State meaning, format, units and limits.
- Missing error documentation: clients guess. List each error code and what to do.
- Leaking internal types or private endpoints into public docs: use visibility tags or exclusion rules.
- Undated breaking changes buried in prose: record them in the changelog and migration notes.

## Review
- [ ] Reference output is generated, and the build passes with warnings as errors.
- [ ] Each public item has a summary, types, constraints, errors and a tested example.
- [ ] Auth, pagination, limits and versioning have a single overview.
- [ ] Deprecations name the replacement and removal version.
- [ ] No internal-only symbols appear in the published docs.
