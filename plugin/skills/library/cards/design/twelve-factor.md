---
name: twelve-factor
title: Twelve-factor apps
area: design
tags: [twelve-factor, cloud-native, config, stateless, logs, processes]
detect: [file:Procfile, file:Dockerfile, file:.env.example, file:app.json]
related: [configuration, microservices, background-jobs, zero-downtime-migrations]
---
Deployable services: config in the environment, stateless processes, logs to stdout, disposable and fast to start.

## Verify
- `grep -rnE "(password|secret|api[_-]?key)\s*[:=]\s*['\"][^'\"]{6,}" src config`: no secrets committed in code or config (review every hit).
- `docker run --rm -e PORT=8081 -p 8081:8081 app:latest & sleep 3 && curl -fsS localhost:8081/healthz`: the container starts from environment only and binds `$PORT`.
- `docker stop -t 10 CONTAINER; docker inspect CONTAINER --format '{{.State.ExitCode}}'`: it shuts down on SIGTERM within the grace period (use 0 or the app's clean code).
- `git ls-files | grep -E "\.env$"`: no real `.env` is tracked (expect no output).

## Test first
Prove the app takes everything from the environment and fails fast without it.
```python
def test_missing_required_config_fails_at_startup(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ConfigError, match="DATABASE_URL"):
        load_settings()

def test_port_comes_from_env(monkeypatch):
    monkeypatch.setenv("PORT", "9000")
    assert load_settings().port == 9000
```

## Do
- Keep one codebase and many deploys. The same build artifact runs in staging and production, with differences only in config.
- Read config from environment variables: URLs, credentials, feature toggles. Commit only `.env.example`.
- Treat backing services (DB, queue, cache) as attached resources addressed by URL, so swapping one is a config change.
- Keep processes stateless and share-nothing. Store sessions, uploads and caches in external services.
- Bind the port from `$PORT` and exit on SIGTERM after finishing in-flight work.
- Write logs as an event stream to stdout, preferably as JSON lines, and let the platform route them.
- Run admin tasks (migrations, one-off scripts) as one-off processes from the same release.
- Keep dev and prod close: same database type and versions, same dependencies, and containers locally.

## Avoid
- Config files per environment baked into the image (`config.prod.yml`): the artifact differs per environment. Inject environment variables at runtime.
- Writing logs to local files or rotating them in-app: containers lose them. Write to stdout.
- Sticky in-memory sessions or local-disk uploads: a second instance breaks them. Use a shared store.
- Long startup (cold caches, migrations on boot, warm-up of minutes): scaling and restarts lag. Make startup fast and run migrations separately.
- Ignoring SIGTERM: the platform kills in-flight requests after the grace period. Handle the signal and drain.
- Different DB engines in dev and production (SQLite versus Postgres): behavior differs. Use the same engine.
- Reading environment variables deep inside the code at call time: config scatters. Load once into a typed settings object.

## Review
- [ ] The same artifact is promoted across environments, and all differences are env vars.
- [ ] No secrets in the repo or image, and required config fails at startup.
- [ ] Processes hold no local state and handle SIGTERM.
- [ ] Logs go to stdout as structured lines.
- [ ] Migrations and admin tasks run as separate release steps.
