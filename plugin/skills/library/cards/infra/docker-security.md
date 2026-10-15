---
name: docker-security
title: Docker security
area: infra
tags: [docker, security, containers, hardening, capabilities, seccomp, scanning]
detect: []
related: [docker, dockerfile-best-practices, docker-compose, podman, kubernetes-rbac]
---
Container hardening: non-root, dropped capabilities, read-only filesystems, scanned images and no secrets baked in.

## Verify
- `docker run --rm IMAGE id -u`: the process does not run as root.
- `docker inspect --format '{{.HostConfig.Privileged}} {{.HostConfig.CapAdd}}' CONTAINER`: not privileged, no added capabilities.
- `trivy image IMAGE`: known vulnerabilities and misconfigurations (when Trivy is installed).
- `docker history --no-trunc IMAGE`: no secrets in build commands.
- `hadolint Dockerfile`: Dockerfile lint.

## Test first
Make the hardening a failing assertion on a run.
```bash
c=$(docker run -d --read-only --cap-drop ALL --security-opt no-new-privileges --user 10001 IMAGE)
sleep 2
test "$(docker inspect -f '{{.State.Running}}' $c)" = true       # app still works hardened
! docker exec $c sh -c 'touch /x' 2>/dev/null                    # read-only fs
```
Also fail CI on `trivy image --exit-code 1 --severity HIGH,CRITICAL IMAGE`.

## Do
- Run as a numeric non-root user (`USER 10001`) and set `--cap-drop ALL`, adding back only what is needed.
- Use `--read-only` with `tmpfs` for writable paths, and `--security-opt no-new-privileges`.
- Keep the default seccomp profile; add AppArmor or SELinux profiles where available.
- Use minimal or distroless bases and pin by digest; rebuild regularly to pick up fixes.
- Pass secrets via files, Docker or Compose secrets, or runtime mounts, not `ENV` or image layers.
- Set resource limits (`--memory`, `--cpus`, `--pids-limit`) to bound abuse.
- Scan images in CI and sign them (for example with cosign) and verify at deploy time.
- Consider rootless Docker or Podman for developer and CI hosts.

## Avoid
- `--privileged`: it disables most isolation. Add the single capability or device you need.
- Mounting `/var/run/docker.sock` into containers: it is root on the host. Use a socket proxy with limited API, or avoid it.
- `-v /:/host` or broad bind mounts of host paths: write access to the host. Mount the narrowest path read-only.
- `--net=host` for convenience: removes network isolation. Publish only needed ports.
- Credentials in `ARG`, `ENV` or `COPY .env`: readable through `docker history` and `inspect`. Use secret mounts.
- Trusting `latest` and unsigned images: supply chain drift. Pin digests and verify signatures.
- Publishing ports on `0.0.0.0` by default (`-p 5432:5432`): bind to `127.0.0.1:` when local only.

## Review
- [ ] Non-root user, capabilities dropped, no-new-privileges set.
- [ ] No privileged mode, docker socket or broad host mounts.
- [ ] Image scanned and bases pinned.
- [ ] Secrets absent from layers and env.
- [ ] Limits and published-port bindings are intentional.
