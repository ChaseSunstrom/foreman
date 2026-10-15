---
name: docker
title: Docker
area: infra
tags: [docker, container, image, dockerfile, buildkit, registry]
detect: [file:Dockerfile, file:Dockerfile.*, file:*.dockerfile, file:.dockerignore]
related: [docker-compose, podman, kubernetes, github-actions]
---
Docker images: small reproducible multi-stage builds that run as non-root with a healthcheck and a tight build context.

## Verify
- `docker build --check .`: BuildKit's Dockerfile linter (bad FROM casing, undefined vars, unpinned patterns).
- `docker build -t app:test .`: the image builds from a clean context.
- `docker run --rm app:test <cmd> --version`: the entrypoint starts and the binary resolves.
- `docker image inspect app:test --format '{{.Config.User}}'`: the final user is not empty or root.
- `docker history --no-trunc app:test`: no secret or token in any layer's command.

## Test first
No unit harness: the failing check is a smoke run of the built image. Put it in a script or CI step.
```sh
docker build -t app:test . \
 && test "$(docker run --rm --entrypoint id app:test -u)" != 0 \
 && docker run -d --name t -p 8080:8080 app:test \
 && curl -fsS --retry 10 --retry-connrefused localhost:8080/healthz
```
Red first: the non-root and health checks fail until the Dockerfile adds `USER` and the endpoint.

## Do
- Use multi-stage builds: compile in a `builder` stage, `COPY --from=builder` only the artifact into a slim or distroless runtime stage.
- Order layers by change rate: copy manifests and install dependencies first, then source, so the dependency layer caches.
- Pin base images by tag plus digest (`FROM image:tag@sha256:...`) for reproducibility.
- Write `.dockerignore` (`.git`, `node_modules`, `.env`, build output) so the context stays small and secrets stay out.
- Add `USER` with a numeric uid, and `HEALTHCHECK` or an orchestrator probe.
- Use exec-form `ENTRYPOINT ["app"]` so the process is PID 1 and receives SIGTERM.
- Use `RUN --mount=type=cache` for package caches and `--mount=type=secret` for build credentials.
- Set `WORKDIR` explicitly and use `COPY --chown` instead of a later `chown -R` layer.

## Avoid
- `FROM x:latest`: builds drift. Pin a tag and digest.
- `ARG` or `ENV` for tokens: they persist in image history. Use `--mount=type=secret`.
- `COPY . .` before installing dependencies: any source edit busts the dependency cache. Copy manifests first.
- `apt-get update` and `apt-get install` in separate `RUN`s, or without cleanup: stale cache and bloat. Chain them with `--no-install-recommends` and remove `/var/lib/apt/lists/*`.
- Shell-form `CMD app`: the shell is PID 1 and swallows signals, so stops take 10 s. Use exec form.
- `ADD` for local files or URLs: use `COPY`; fetch and verify checksums explicitly.
- Running as root, or `--privileged` and mounting `docker.sock` to "fix" permissions: fix file ownership instead.

## Review
- [ ] Final stage is minimal, non-root, and has no compilers, caches or secrets.
- [ ] Base images are pinned and `.dockerignore` exists.
- [ ] Layer order puts rarely changing steps first.
- [ ] Signals reach the app (exec form) and a health probe exists.
- [ ] `docker build --check` is clean.
