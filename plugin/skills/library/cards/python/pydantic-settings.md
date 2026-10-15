---
name: pydantic-settings
title: pydantic-settings
area: python
tags: [python, config, settings, pydantic, environment, secrets]
detect: [dep:pydantic-settings]
related: [pydantic, fastapi, pytest, loguru]
---
pydantic-settings: typed configuration from environment variables, .env files and secrets, validated at startup.

## Verify
- `python -c "from app.config import Settings; print(Settings())"`: loads and validates with the current environment (secrets print masked as `**********`).
- `pytest -q`: settings tests that set env vars through `monkeypatch`.
- `ruff check . && pyright`: field types and no leftover Pydantic v1 `BaseSettings` import.
- `git ls-files | grep -E "(^|/)\.env$"`: no real `.env` file is tracked.

## Test first
```python
import pytest
from pydantic import ValidationError
from app.config import Settings

def test_requires_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)

def test_reads_prefixed_env(monkeypatch):
    monkeypatch.setenv("APP_DEBUG", "true")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///x.db")
    assert Settings(_env_file=None).debug is True
```

## Do
- Import from the separate package: `from pydantic_settings import BaseSettings, SettingsConfigDict`.
- Configure with `model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", env_nested_delimiter="__", extra="ignore")`.
- Use `SecretStr` and `SecretBytes` for passwords and tokens, and read with `.get_secret_value()` only at the point of use.
- Use precise types: `PostgresDsn`, `HttpUrl`, `Path`, `Literal["dev", "prod"]`, `int` with `Field(ge=1)`.
- Make required values required (no default), so startup fails fast with a clear error.
- Build the settings once with `@lru_cache` in a `get_settings()` function and inject it (FastAPI: `Depends(get_settings)`), then override in tests.
- Load Docker or Kubernetes secrets through `secrets_dir="/run/secrets"`. <!-- pragma: allowlist secret -->
- Customize source order with `settings_customise_sources` when you need files or other sources, noting init values win over env by default.
- Parse lists and dicts from env as JSON strings (`APP_HOSTS='["a","b"]'`).

## Avoid
- `from pydantic import BaseSettings`: moved out in v2 and raises an import error. Use `pydantic_settings`.
- v1 `class Config: env_prefix`: use `model_config = SettingsConfigDict(...)`.
- Module-level `settings = Settings()` read at import in a way tests cannot override: import-time failures and leakage. Use a cached getter.
- Committing `.env` with real secrets: add it to ignore and ship a `.env.example` with placeholders.
- Defaults for secrets like `secret_key="changeme"`: insecure in production. Require them.
- Forgetting `_env_file=None` in tests: a developer's local `.env` changes results.
- Logging `settings.model_dump()` with secrets unmasked: `SecretStr` masks only if you keep the type.

## Review
- [ ] Required secrets have no defaults and use `SecretStr`.
- [ ] Settings load once, validate at startup and are injectable and overridable in tests.
- [ ] Prefix, nesting and `extra` policy are explicit.
- [ ] `.env` is untracked and an example file documents each key.
