---
name: python-typing
title: Python typing
area: idioms
tags: [python, typing, mypy, pyright, protocols, generics]
detect: [file:mypy.ini, file:pyrightconfig.json]
related: [python, pytest, ruff, pydantic]
---
Modern Python annotations: built-in generics, `X | None`, Protocols, TypedDict and a strict checker that runs in CI.

## Verify
- `mypy --strict .`: full strict type check (or `pyright` when the repo uses it).
- `ruff check --select UP,ANN .`: flags outdated typing idioms and missing annotations.
- `pytest -q`: runtime behavior still matches the annotations.

## Test first
Types are checked, not run. Pin a type contract with `assert_type`, plus a runtime test for the behavior.
```python
from typing import assert_type
from app.util import first

def test_first_keeps_element_type() -> None:
    xs: list[int] = [1, 2]
    assert_type(first(xs), int | None)
    assert first(xs) == 1
    assert first([]) is None
```
Run the checker over the test files too, so `assert_type` is enforced.

## Do
- Use built-in generics (`list[int]`, `dict[str, int]`) and `X | None`, not `List`, `Dict` or `Optional`.
- Prefer `collections.abc` types (`Sequence`, `Mapping`, `Iterable`) for parameters and concrete types for returns.
- Use `Protocol` for structural interfaces so callers need no inheritance.
- Use `TypedDict` or dataclasses for shaped data. Mark optional keys with `NotRequired`.
- Use `Self` for fluent methods and `@override` when overriding.
- Use `Literal` and `Final` for fixed values, and `TypeAlias` or the `type` statement for named aliases.
- Narrow with `isinstance`, `TypeGuard` or `TypeIs`, and finish `match` statements with `assert_never`.

## Avoid
- `Any` as an escape hatch: it silently disables checking downstream. Use `object`, a Protocol or a TypeVar.
- Blanket `# type: ignore`: it hides real errors. Use `# type: ignore[code]` with a reason, and enable `warn_unused_ignores`.
- Mutable default arguments like `def f(x: list[int] = [])`: shared across calls. Use `None` and create the list inside.
- `Optional[X]` meaning "may be omitted": it only means "may be None". Give the parameter a default if it can be omitted.
- Annotating `*args` as `tuple[int, ...]`: annotate each element, `*args: int`.
- Importing heavy modules only for annotations: guard with `if TYPE_CHECKING:` and quote the annotation, or use `from __future__ import annotations`.

## Review
- [ ] The checker passes in strict mode with no new ignores.
- [ ] Public functions have full parameter and return annotations.
- [ ] No `Any` leaks through a public signature.
- [ ] Narrowing is done by the type system, not by `cast` on unchecked data.
- [ ] External data is validated at the boundary, not trusted by annotation alone.
