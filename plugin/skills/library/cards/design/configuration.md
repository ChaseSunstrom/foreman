---
name: configuration
title: Configuration
area: design
tags: [configuration, settings, environment, secrets, validation, defaults]
detect: [dep:pydantic-settings, dep:python-dotenv, dep:dotenv, dep:envalid, dep:viper, dep:spf13/viper, dep:figment, dep:dynaconf]
related: [twelve-factor, feature-flags, multi-tenancy, dependency-injection]
---
Typed, validated, centrally loaded settings with safe defaults, secrets kept apart and failure at startup.

## Verify
- `python -c "from app.settings import Settings; Settings()"`: the settings load and validate from the current environment.
- `env -i python -c "from app.settings import Settings; Settings()"`: with an empty environment it fails loudly naming the missing keys.
- `git ls-files | grep -E "(^|/)\.env($|\.)" | grep -v example`: no real env files are tracked (expect no output).
- `grep -rn "os.environ\|process.env\|os.Getenv" src | grep -v settings`: environment reads are confined to the settings module (review hits).

## Test first
Test precedence and validation of the settings object.
```python
def test_invalid_pool_size_rejected(monkeypatch):
    monkeypatch.setenv("DB_POOL_SIZE", "0")
    with pytest.raises(ValidationError):
        Settings(_env_file=None)

def test_env_overrides_default(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    assert Settings(_env_file=None).log_level == "DEBUG"
```

## Do
- Load all settings once at startup into one typed, immutable object (pydantic-settings, `envalid`, `viper` with a struct) and pass it in.
- Fix a precedence order and document it: defaults, then file, then environment, then explicit overrides or flags.
- Validate types, ranges and formats (URLs, positive integers, enums) when loading, and report every error together.
- Give a default only when it is safe in production. Make dangerous values (DB URL, secret keys) required with no default.
- Keep secrets out of config files and images: inject from a secret manager or the platform, and mask them in logs and `repr`.
- Separate settings by concern (database, auth, features) into nested objects with a common prefix.
- Commit an `.env.example` listing every key with a placeholder, and keep it in sync with the settings class.
- Make time units explicit in names (`timeout_seconds`, `cache_ttl_ms`).

## Avoid
- `os.environ["X"]` scattered through the code: missing and misspelled keys surface at runtime in random places. Centralize.
- Booleans parsed with `bool(os.getenv("DEBUG"))`: the string `"false"` is truthy. Parse explicitly or use a typed settings library.
- Defaults like `SECRET_KEY = "changeme"` or `DEBUG = True`: they reach production. Make them required, and default debug to off.
- Printing or logging the whole settings object: secrets leak. Mask secret fields (`SecretStr`).
- Reloading config mid-request or reading files per request: inconsistent state. Load once, or reload atomically on a signal.
- Different config shapes per environment (separate files with different keys): behavior diverges. Same keys, different values.
- Committing `.env` with real credentials: rotate the credentials if it happened.

## Review
- [ ] One settings module owns all environment reads, with typed fields.
- [ ] Required keys fail at startup, and secrets have no defaults.
- [ ] Secrets are masked in logs and never committed.
- [ ] `.env.example` matches the settings class.
- [ ] Units and ranges are validated and named explicitly.
