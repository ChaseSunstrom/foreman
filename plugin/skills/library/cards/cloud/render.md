---
name: render
title: Render
area: cloud
tags: [render, paas, deploy, blueprint, web-service, postgres]
detect: [file:render.yaml]
related: [railway, fly-io, heroku, vercel]
---
Render services described in a render.yaml Blueprint: health checks, secrets from env groups, private networking for datastores, pre-deploy migrations and pinned runtimes.

## Verify
- `python -c "import yaml,sys; yaml.safe_load(open('render.yaml'))"`: the Blueprint at least parses as YAML.
- `curl -fsS https://SERVICE.onrender.com/healthz`: the deployed health endpoint answers 200.
- `docker build -t app . && docker run --rm -p 8080:8080 -e PORT=8080 app`: the same image or build starts locally and binds to `$PORT`.

## Test first
Test the health endpoint and the `PORT` binding locally before the first deploy.
```python
def test_health_ok_and_reads_port(client, monkeypatch):
    r = client.get("/healthz")
    assert r.status_code == 200 and r.json()["db"] == "ok"
    assert load_config({"PORT": "10000"}).port == 10000
```

## Do
- Define services in `render.yaml` (type, runtime, build and start commands, region, plan) so infrastructure is reviewed in git.
- Bind to `0.0.0.0` on the `PORT` environment variable (the default is 10000) and set `healthCheckPath` to a cheap endpoint that checks dependencies.
- Declare secrets with `sync: false` so values are entered in the dashboard, and share common values through environment groups (`envVarGroups`).
- Pin the runtime (`NODE_VERSION`, `PYTHON_VERSION` or a Dockerfile) so builds are reproducible.
- Run database migrations in `preDeployCommand` so a failing migration stops the deploy.
- Connect to Render Postgres and Key Value through the internal URL from `fromDatabase` or `fromService` references, and restrict the IP allow list on external access.
- Use `autoDeploy` on a branch with CI gating, or deploy through a deploy hook from CI after tests pass.
- Create preview environments for pull requests when the Blueprint supports it, and keep them off production data.
- Use a persistent disk only for services that need local state, since a disk limits the service to one instance and disables zero-downtime deploys.

## Avoid
- Committing secret values in `render.yaml`: use `sync: false` or `generateValue: true` for generated secrets.
- Listening on `localhost` or a hardcoded port: the deploy hangs on "no open ports detected". Use `0.0.0.0:$PORT`.
- Free-tier instances for production: they spin down after idle and the first request is slow. Choose a paid plan.
- The external database URL from services in the same region: it adds latency and exposure. Use the internal URL.
- Skipping a health check: bad deploys go live. Set `healthCheckPath`.
- Running migrations in the start command on multiple instances: they race. Use `preDeployCommand`.
- Writing uploads to the local filesystem without a disk: files vanish on each deploy. Use object storage.

## Review
- [ ] render.yaml validates and holds no secret values.
- [ ] The service binds to `$PORT` and has a health check.
- [ ] Migrations run pre-deploy, runtimes are pinned.
- [ ] Datastores connect over internal URLs with limited external access.
- [ ] Production uses a plan without idle spin-down.
