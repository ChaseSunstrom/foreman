---
name: dockerfile-best-practices
title: Dockerfile best practices
area: infra
tags: [docker, dockerfile, buildkit, multi-stage, caching, image, hadolint]
detect: [file:Dockerfile, file:Dockerfile.*, file:.dockerignore]
related: [docker, docker-security, docker-compose, podman]
---
Dockerfile craft: multi-stage builds, layer caching, pinned bases, a small context and a non-root runtime.

## Verify
- `hadolint Dockerfile`: lint for known Dockerfile pitfalls.
- `docker build --check .`: BuildKit's built-in lint rules.
- `docker build -t app:test .`: the image builds from a clean context.
- `docker history app:test`: layer sizes and what each step added.
- `docker run --rm app:test id -u`: the runtime user is not 0.

## Test first
Assert image properties before writing the Dockerfile.
```bash
docker build -t app:test .
test "$(docker run --rm --entrypoint id app:test -u)" != 0
test "$(docker image inspect app:test --format '{{.Size}}')" -lt 200000000
docker run --rm app:test --version
```

## Do
- Use multi-stage builds: a builder stage with compilers, a final stage that copies only artifacts (`COPY --from=build`).
- Order layers by change rate: dependency manifests first, install, then source copy.
- Pin base images by tag and, for reproducibility, by digest (`FROM image:tag@sha256:...`).
- Keep a `.dockerignore` that excludes `.git`, build output, env files and local caches.
- Use BuildKit cache mounts (`RUN --mount=type=cache,target=/root/.cache/pip ...`) and secret mounts (`RUN --mount=type=secret,id=tok ...`).
- Create and switch to a non-root user: `USER app`, with `COPY --chown=app:app`.
- Use exec-form `ENTRYPOINT ["app"]` and `CMD [...]` so signals reach the process.
- Add `HEALTHCHECK` if the orchestrator does not provide probes, and set `WORKDIR` explicitly.

## Avoid
- `FROM image:latest`: builds change under you. Pin a tag or digest.
- `COPY . .` before installing dependencies: any source edit busts the dependency cache. Copy manifests first.
- `ARG` or `ENV` for secrets, or `COPY .env`: they persist in image layers and history. Use secret mounts.
- Shell-form `CMD app start`: PID 1 is `sh`, so SIGTERM is not forwarded. Use exec form.
- `apt-get update` in a separate layer from `install`, and leaving lists behind: stale caches and bloat. Combine with `--no-install-recommends` and remove `/var/lib/apt/lists/*`.
- `ADD` for local files or remote URLs: unexpected extraction and no checksum. Use `COPY`, or `curl` with a checksum.
- Running as root by default: container escape impact grows. Add `USER`.

## Review
- [ ] Final stage has only runtime artifacts and a non-root user.
- [ ] Bases are pinned; `.dockerignore` exists.
- [ ] No secrets in layers, build args or history.
- [ ] Dependency layers cache across source edits.
- [ ] Entrypoint is exec form and handles signals.
