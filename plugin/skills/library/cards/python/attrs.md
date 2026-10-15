---
name: attrs
title: attrs
area: python
tags: [python, classes, dataclasses, validation, immutability, typing]
detect: [dep:attrs, dep:cattrs]
related: [pydantic, mypy, pyright, pytest]
---
attrs: concise value classes with validators, converters and frozen or slotted instances, plus cattrs for structuring.

## Verify
- `mypy .` (or `pyright`): attrs fields and `define` classes type check.
- `pytest -q`: construction, validation and equality tests.
- `python -c "import attrs; print(attrs.__version__)"`: the modern `attrs` namespace is installed (not only legacy `attr`).

## Test first
```python
import pytest
import attrs
from app.models import Port

def test_port_validates_range():
    with pytest.raises(ValueError):
        Port(70000)

def test_port_is_frozen():
    p = Port(80)
    with pytest.raises(attrs.exceptions.FrozenInstanceError):
        p.number = 81
```

## Do
- Use the modern API: `from attrs import define, field, frozen, evolve, asdict`. `@define` gives slots and eq by default.
- Use `@frozen` for values. Change with `attrs.evolve(obj, x=1)`.
- Validate with `field(validator=validators.instance_of(int))` or a decorator `@x.validator` method that raises. Chain with `validators.and_(...)`.
- Convert input with `field(converter=int)`. Converters run before validators.
- Mutable defaults use `field(factory=list)`, never `default=[]`.
- Use `kw_only=True` on classes with many fields, and `field(repr=False)` for secrets.
- Structure and unstructure nested data, JSON or dicts with `cattrs.structure(data, Cls)` and `cattrs.unstructure(obj)`.
- Use `@define(order=False)` plus `eq=False` for identity-compared entities, `hash` only when frozen.

## Avoid
- `import attr` with `@attr.s` and `attr.ib()` in new code: legacy style, no slots by default. Use `attrs.define` and `attrs.field`.
- `default=[]` or `default={}`: shared across instances. Use `factory=`.
- Expecting validators to run on attribute assignment with `attr.s`: only `define` runs validators on `setattr` (and converters). Use `@frozen` if values must not change.
- Using `asdict` with nested non-attrs objects and expecting JSON output: convert with cattrs or `value_serializer`.
- Defining `__init__` by hand on an attrs class: it is overwritten. Use `__attrs_post_init__`.
- Adding attributes not declared on a slotted class: `AttributeError`. Declare the field.

## Review
- [ ] Value objects are `frozen` and mutable defaults use `factory`.
- [ ] Validators and converters sit on fields, not scattered in call sites.
- [ ] Secrets are excluded from `repr`.
- [ ] External data goes through `cattrs.structure` or an explicit parser, not `Cls(**raw)`.
