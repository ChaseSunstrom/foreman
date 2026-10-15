---
name: pyright
title: Pyright
area: python
tags: [python, typing, pyright, static-analysis, type-checking]
detect: [dep:pyright, file:pyrightconfig.json, dep:basedpyright]
related: [mypy, pydantic, ruff, pytest]
---
Pyright static type checking: `typeCheckingMode`, per-directory config, venv resolution.

## Verify
- `pyright`: type errors for the configured include set; exit code is nonzero on errors.
- `pyright --outputjson`: machine-readable results, handy for counting errors by rule.
- `pyright --verifytypes PKG`: public-API type completeness of a library, only for packages that ship `py.typed`.
- `pyright --pythonpath "$(which python)"`: points it at the right interpreter when imports show as unresolved.

## Test first
The failing check is a type error. Add the bad call, confirm the report, then fix the signature.
```python
from typing import TypedDict

class User(TypedDict):
    id: int

u: User = {"id": "7"}   # error: "str" is not assignable to "int"
```
Keep intentional error cases out of the main source; a type-only fixture file in `tests/typing/` works.

## Do
- Configure in `pyproject.toml` under `[tool.pyright]` (or `pyrightconfig.json`): `include`, `exclude`, `pythonVersion`, `typeCheckingMode`.
- Use `"strict"` for new packages and `strict = ["src/new"]` to promote chosen paths while the rest stays at `"standard"`.
- Point at the project environment with `venvPath` and `venv` (or run inside the activated env).
- Narrow with `isinstance`, `is None`, `TypeGuard`, `TypeIs` and `assert_never` for exhaustive matches.
- Use `reveal_type(x)` to see what Pyright inferred while debugging.
- Prefer `# pyright: ignore[ruleName]` with the rule, and turn on `reportUnnecessaryTypeIgnoreComment`.
- Install via the package manager (a pinned version) so CI and editors agree.

## Avoid
- `# type: ignore` without a rule: it silences everything on the line (and is honored by default). Use `# pyright: ignore[rule]`.
- Unresolved-import noise ("reportMissingImports") fixed by `reportMissingImports = false`: the environment is wrong. Set `venv` or install the package.
- `reportMissingTypeStubs` ignored for real libraries: add the `types-*` stub package or a local `stubPath`.
- `Any`-typed `**kwargs` and untyped JSON passed along: errors surface late. Validate to a model or `TypedDict` at the edge.
- Assuming mypy and Pyright agree: inference differs (for example on `list` literals and unannotated returns). Pick one as the gate.
- `basic` mode kept forever on a new codebase: start at `standard` or `strict`.

## Review
- [ ] `pyright` passes in CI using a pinned version and the project's environment.
- [ ] Ignore comments name a rule and are reported when unused.
- [ ] New or touched modules are held to strict mode.
- [ ] Public functions and class attributes are annotated; no stray `Any`.
- [ ] Only one of Pyright or mypy is the required gate.
