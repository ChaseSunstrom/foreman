---
name: marshmallow
title: marshmallow
area: python
tags: [python, serialization, validation, schema, api, flask]
detect: [dep:marshmallow, dep:marshmallow-sqlalchemy, dep:flask-marshmallow]
related: [pydantic, flask, sqlalchemy, pytest]
---
marshmallow: declarative schemas for validating input and serializing output, with explicit load and dump.

## Verify
- `pytest -q`: schema tests for valid, invalid and partial input.
- `mypy .` (or `pyright`): schema usage and typed results.
- `python -W error -c "import app.schemas"`: schemas import with no deprecation warnings promoted to errors.

## Test first
```python
import pytest
from marshmallow import ValidationError
from app.schemas import UserSchema

def test_rejects_bad_email_and_unknown_field():
    with pytest.raises(ValidationError) as e:
        UserSchema().load({"email": "nope", "is_admin": True})
    assert "email" in e.value.messages
    assert "is_admin" in e.value.messages
```
Default `unknown` is `RAISE`, so the extra field fails. Tests live beside the schema code.

## Do
- Validate with `schema.load(data)` and catch `ValidationError`, returning `err.messages` (a dict keyed by field).
- Serialize with `schema.dump(obj)`. Use `many=True` for lists.
- Set `unknown = RAISE` explicitly in `class Meta` for input schemas. Use `EXCLUDE` only when ignoring is intended.
- Mark inputs `required=True`. Use `load_only=True` for passwords and `dump_only=True` for ids and timestamps.
- Add cross-field checks with `@validates_schema` and field checks with `@validates("field")` or `validate=validate.Length(...)`.
- Transform with `@pre_load`, `@post_load` (return a dataclass or model), `@post_dump`.
- Use `partial=True` or `partial=("name",)` for PATCH updates.
- Use `fields.Nested(OtherSchema, exclude=(...))` and `fields.Method` / `fields.Function` for computed output.

## Avoid
- Passing user data into a model without `load`: no validation, mass assignment. Always load first.
- Treating `dump` as validation: it does not validate. Use `validate` or `load`.
- `unknown = INCLUDE` on request schemas: extra keys flow through. Use `RAISE`.
- Mutable defaults in `load_default=[]`: shared state. Pass a callable such as `list`.
- The removed `missing=` / `default=` field arguments in new code: use `load_default` and `dump_default`.
- Expecting `load` to return a tuple `(data, errors)`: that was marshmallow 2. Version 3 returns data and raises.

## Review
- [ ] Input schemas set `unknown` explicitly and mark required fields.
- [ ] Secrets are `load_only` and server fields are `dump_only`.
- [ ] Validation errors map to a 4xx response using `messages`.
- [ ] Tests cover invalid, unknown and partial cases.
