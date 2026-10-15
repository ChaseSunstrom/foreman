---
name: pydantic
title: Pydantic
area: python
tags: [python, validation, typing, pydantic, settings, serialization]
detect: [dep:pydantic, dep:pydantic-settings]
related: [fastapi, litestar, mypy, pyright, pytest]
---
Pydantic v2 models: validation, serialization, `TypeAdapter`, and `pydantic-settings` for configuration.

## Verify
- `python -c "import pydantic; print(pydantic.VERSION)"`: which major is installed (v1 and v2 APIs differ).
- `pytest -q`: validation and serialization tests.
- `pyright` (or `mypy .`): field types; enable the pydantic mypy plugin for `__init__` checks.
- `python -W error -c "import app.models"`: deprecated v1 usages surface as errors at import.

## Test first
Test the boundary: invalid input rejected, valid input normalized.
```python
import pytest
from pydantic import ValidationError
from app.models import User

def test_user_rejects_bad_email():
    with pytest.raises(ValidationError) as e:
        User(email="nope", age=3)
    assert e.value.errors()[0]["loc"] == ("email",)
```

## Do
- Define models with `BaseModel` and `model_config = ConfigDict(...)` (`extra="forbid"`, `frozen=True`, `str_strip_whitespace=True`, `from_attributes=True` as needed).
- Use `Field(..., ge=, le=, min_length=, pattern=)` and `Annotated[...]` for reusable constraints.
- Use `@field_validator("x")` with `@classmethod` for one field, `@model_validator(mode="after")` for cross-field rules.
- Serialize with `.model_dump()` / `.model_dump_json()`; parse with `.model_validate()` / `.model_validate_json()`.
- Use `TypeAdapter(list[Item])` for validating non-model types.
- Use discriminated unions (`Field(discriminator="kind")`) for tagged variants.
- Load config with `pydantic_settings.BaseSettings` and `SettingsConfigDict(env_prefix=..., env_file=...)`; use `SecretStr` for secrets.

## Avoid
- v1 API in v2 code: `.dict()`, `.json()`, `parse_obj`, `@validator`, `class Config`, `orm_mode`. Use `model_dump`, `model_dump_json`, `model_validate`, `field_validator`, `model_config`, `from_attributes`.
- `from pydantic import BaseSettings`: moved. Import from `pydantic_settings`.
- `Optional[int]` assumed to be optional: in v2 it is required-but-nullable. Add `= None`.
- Mutable defaults shared by hand: use `Field(default_factory=list)`.
- Validators that raise `TypeError`/`AssertionError` expecting a clean error: raise `ValueError` (or `PydanticCustomError`).
- `model_construct()` on untrusted input: it skips validation. Use `model_validate`.
- Logging `model_dump()` of settings: leaks secrets. Keep them as `SecretStr`.

## Review
- [ ] No v1 methods or imports remain; `extra` policy is chosen on boundary models.
- [ ] Constraints live on the model, not in scattered handler checks.
- [ ] Secrets use `SecretStr` and are never dumped to logs or responses.
- [ ] Tests cover one rejected input per validator with the `loc` asserted.
- [ ] Models returned from ORM objects set `from_attributes=True`.
