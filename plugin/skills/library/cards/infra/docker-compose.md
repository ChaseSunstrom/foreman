---
name: docker-compose
title: Docker Compose
area: infra
tags: [compose, docker, multi-container, local-dev, services]
detect: [file:compose.yaml, file:compose.yml, file:docker-compose.yml, file:docker-compose.yaml, file:docker-compose.*.yml]
related: [docker, podman, kubernetes, nginx]
---
Compose files: multi-service stacks for local dev and CI with health-gated startup, named volumes and env files.

## Verify
- `docker compose config -q`: the file parses, interpolation resolves, and the schema is valid.
- `docker compose config --services`: the expected services exist after merging overrides.
- `docker compose up -d --wait`: every service with a healthcheck reaches healthy.
- `docker compose ps --format json`: no service is restarting or exited.
- `docker compose down -v`: teardown is clean (also resets named volumes for the next red run).

## Test first
The failing check is a smoke request against the stack, or a one-shot test service.
```sh
docker compose up -d --wait
curl -fsS localhost:8080/healthz
docker compose run --rm tests
```
Red first: `--wait` fails until the service has a `healthcheck`, and `tests` fails until the dependency is `service_healthy`.

## Do
- Use the `compose.yaml` name and no top-level `version:` key (it is obsolete and ignored).
- Gate startup with `depends_on: { db: { condition: service_healthy } }` and a real `healthcheck` on `db`.
- Use named volumes for data and bind mounts only for source in dev. Declare named volumes under top-level `volumes:`.
- Keep per-environment differences in `compose.override.yaml` or `-f` layers, or use `profiles:` for optional services.
- Put secrets in the top-level `secrets:` or an `env_file`, and keep that file out of git.
- Set `restart: unless-stopped` for long-lived services and `init: true` where children get orphaned.
- Reach other services by service name on the default network. Publish only ports a host must reach.
- Pin image tags and set `pull_policy` deliberately.

## Avoid
- `docker-compose` (v1 binary): removed from current installs. Use `docker compose`.
- Plain `depends_on: [db]` as readiness: it only orders starts. Add `condition: service_healthy`.
- Publishing `5432:5432` for a database only the app uses: it exposes it on all host interfaces. Drop `ports` or bind `127.0.0.1:5432:5432`.
- Secrets inline under `environment:`: they land in `docker compose config` output and git. Use `secrets:` or `env_file`.
- Hardcoded `container_name`: it blocks `--scale` and parallel projects. Let Compose name them.
- `$` in a value meant literally: Compose interpolates it. Write `$$`.
- Bind-mounting over `node_modules` or a venv: the host dir hides the image's install. Use an anonymous or named volume for it.

## Review
- [ ] Every stateful dependency has a healthcheck and dependents wait on it.
- [ ] Data is on named volumes and no secrets are committed.
- [ ] Only needed ports are published, and loopback-bound for dev databases.
- [ ] `docker compose config -q` passes with each override combination used.
- [ ] A clean `down -v` then `up --wait` works from scratch.
