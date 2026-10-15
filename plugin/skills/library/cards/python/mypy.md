---
name: mypy
title: mypy
area: python
tags: [python, typing, mypy, static-analysis, type-checking]
detect: [dep:mypy, file:mypy.ini, file:.mypy.ini]
related: [pyright, pydantic, ruff, pytest]
---
mypy static type checking: strict flags, per-module overrides, stubs and plugins.

## Verify
- `mypy .`: type errors across the configured files.
- `mypy --strict PKG`: the full strict flag set on a package, to see what a stricter baseline would need.
- `mypy --warn-unused-ignores .`: stale `# type: ignore` comments (also settable in config).
- `mypy --install-types --non-interactive`: fetches missing third-party stub packages.

## Test first
The failing check is a type error. Add a call that should be rejected and confirm mypy reports it.
```python
def parse(port: str) -> int:
    return int(port)

parse(8080)  # error: Argument 1 to "parse" has incompatible type "int"
```
To assert that a bad call stays an error, use `typing.assert_type` or `# type: ignore[arg-type]` with `warn_unused_ignores` on.

## Do
- Configure in `[tool.mypy]` or `mypy.ini`: set `python_version`, `strict = true` for new code, and `files`.
- Adopt gradually with `[[tool.mypy.overrides]]` per module (`module = "legacy.*"`, `ignore_errors = true`) and shrink the list over time.
- Annotate public function signatures completely; let locals infer.
- Use `Protocol`, `TypedDict`, `Literal`, `Self` and `TypeVar` instead of `Any` and casts.
- Narrow `Optional` with an explicit `if x is None:` branch.
- Use the pydantic plugin (`plugins = ["pydantic.mypy"]`) for pydantic models and the SQLAlchemy 2.x annotations rather than an old plugin.
- Cache `.mypy_cache` in CI and run `mypy` after `ruff`.

## Avoid
- Bare `# type: ignore`: hides every error on the line. Use `# type: ignore[code]`.
- `Any` creeping in through `dict`, `json.loads` and untyped imports: use `TypedDict` or validate with pydantic at the edge.
- `cast()` to make an error go away: it asserts without checking. Narrow with `isinstance` or fix the type.
- `ignore_missing_imports = true` globally: silences real missing stubs. Scope it per module.
- Old `typing.List`/`Optional[X]` style in new code: use `list[int]` and `X | None` on supported Python.
- Running mypy only on changed files with `follow_imports=skip`: misses errors across modules. Run on the whole package in CI.
- Mutable default `list` or `dict` typed as `list[int] = []`: a runtime bug mypy cannot flag. Use `None` or `field(default_factory=...)`.

## Review
- [ ] `mypy` passes in CI with a pinned version and no new global ignores.
- [ ] Each `type: ignore` names an error code and `warn_unused_ignores` is on.
- [ ] New code satisfies `--strict` even if legacy modules are overridden.
- [ ] Public APIs have complete annotations with no stray `Any`.
- [ ] Third-party stubs are installed as dev dependencies.
