---
name: fly-io
title: Fly.io
area: cloud
tags: [fly, flyctl, deploy, machines, volumes, containers]
detect: [file:fly.toml, file:fly.*.toml]
related: [railway, heroku, cloud-cost]
---
Fly.io apps: Docker images run as Machines, configured in `fly.toml`, with health checks, volumes and regions.

## Verify
- `fly config validate`: `fly.toml` is valid.
- `fly deploy --remote-only`: builds remotely and rolls out with the configured strategy.
- `fly status`: machines are started and health checks pass.
- `fly logs`: live logs, including crash and OOM messages.
- `fly checks list`: the state of each health check.

## Test first
Smoke-test the deployed health route and fail on config rules.
```python
import tomllib

def test_fly_config_is_safe():
    cfg = tomllib.load(open("fly.toml", "rb"))
    svc = cfg["http_service"]
    assert svc["internal_port"] == 8080
    assert svc["force_https"] is True
    assert svc.get("checks")
```
After deploy: `curl -fsS https://APP.fly.dev/healthz`.

## Do
- Make the app listen on `0.0.0.0` at the `internal_port` set in `[http_service]`, not `localhost`.
- Set `force_https = true`, and `auto_stop_machines`, `auto_start_machines` and `min_machines_running` to match latency and cost goals.
- Add `[[http_service.checks]]` with a path, interval and grace period.
- Run at least two machines for production, so a deploy or host failure does not take you down.
- Set secrets with `fly secrets set`; keep `[env]` for non-secret values.
- Use `[deploy] release_command` for migrations; it runs in a temporary machine before the rollout.
- Mount volumes with `[mounts]`; they are per machine and per region, so plan replication yourself.
- Set `primary_region` near your database; use `fly-replay` for writes to a primary.
- Set `[[vm]]` size and swap deliberately.

## Avoid
- Binding to `127.0.0.1`: the proxy can't reach it, and checks fail.
- Storing state on the root filesystem: it resets on every deploy. Use a volume, a database or object storage.
- One machine and one volume with no snapshot or replica: a host loss means downtime or data loss.
- Secrets in `fly.toml` `[env]`: it is committed.
- Scaling machines in a region that has no volume for them: they fail to start.
- Running migrations on app boot across several machines: use `release_command`.
- `fly deploy` from a dirty tree in CI without `--remote-only` or a pinned image: results differ per machine.

## Review
- [ ] `fly config validate` passes; ports and bind addresses match.
- [ ] Health checks and at least two production machines.
- [ ] Secrets only via `fly secrets`.
- [ ] Persistent data is on volumes with snapshots or external storage.
- [ ] Migrations run in `release_command`.
