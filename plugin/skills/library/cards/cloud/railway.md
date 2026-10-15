---
name: railway
title: Railway
area: cloud
tags: [railway, deploy, paas, nixpacks, services, variables]
detect: [file:railway.json, file:railway.toml, dep:@railway/cli]
related: [fly-io, heroku, vercel]
---
Railway projects: services built by Railway's builder or a Dockerfile, shared variables, private networking, config as code.

## Verify
- `railway status`: the linked project, environment and service.
- `railway variables`: variables available to the linked service (check names, not values).
- `railway up`: uploads and deploys the current directory.
- `railway logs`: build and deploy logs for the latest deployment.
- `railway run -- <cmd>`: runs a local command with the service's environment.

## Test first
Fail on the config file, then smoke-test the deployed health route.
```python
import json

def test_railway_config_has_healthcheck_and_start():
    cfg = json.load(open("railway.json"))
    d = cfg["deploy"]
    assert d["healthcheckPath"].startswith("/")
    assert d.get("startCommand")
```
Then `curl -fsS https://SERVICE_DOMAIN/healthz`.

## Do
- Commit config as code in `railway.json` or `railway.toml` (`build.builder`, `deploy.startCommand`, `deploy.healthcheckPath`, `deploy.restartPolicyType`).
- Bind to `0.0.0.0` on the injected `PORT`.
- Reference other services with variables like `${{Postgres.DATABASE_URL}}` instead of copying values.
- Use private networking (`SERVICE.railway.internal`) between services; expose only the public one.
- Use separate environments (production, staging) with their own variables.
- Run migrations as a pre-deploy command, not at process start.
- Pin the builder or use a Dockerfile when the auto-detected build is ambiguous; pin runtime versions.
- Add volumes for persistent data and know they attach to one service.

## Avoid
- Hard-coding the port: the platform assigns `PORT`. Read it.
- Copying a database URL into a variable by hand: it goes stale when credentials rotate. Use a reference.
- Using the public database URL from app services: it adds egress cost and latency. Use the private one.
- Writing to the container filesystem for persistence: it resets on deploy.
- Committing `.env` files or tokens: use variables and `RAILWAY_TOKEN` in CI.
- No health check path: deploys are marked live before the app is ready.
- Several replicas with a volume: volumes attach to one instance.

## Review
- [ ] Start command, health check and restart policy in config.
- [ ] Port from `PORT`, bound to all interfaces.
- [ ] Services connect over private networking with variable references.
- [ ] No secrets in the repo.
- [ ] Migrations run in a pre-deploy step.
