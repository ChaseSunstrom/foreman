---
name: podman
title: Podman
area: infra
tags: [podman, container, rootless, quadlet, buildah, systemd]
detect: [file:Containerfile, file:Containerfile.*, file:*.container, file:*.pod, file:podman-compose.yml]
related: [docker, systemd, kubernetes, docker-compose]
---
Podman: daemonless rootless containers, pods, Quadlet units under systemd, and Kubernetes YAML round-trips.

## Verify
- `podman build -t app:test -f Containerfile .`: the image builds.
- `podman run --rm app:test <cmd> --version`: the entrypoint runs rootless.
- `podman generate kube <ctr>` or `podman kube play --down f.yaml`: the manifest round-trips with no host-specific paths.
- `systemctl --user daemon-reload && systemctl --user status app.service`: the Quadlet unit generated and started.
- `podman healthcheck run <ctr>`: the container's health command passes.

## Test first
The failing check is a rootless smoke run, ideally in the same user context CI uses.
```sh
podman build -t app:test .
podman run -d --name t -p 8080:8080 app:test
podman healthcheck run t   # fails until HEALTHCHECK/--health-cmd exists
curl -fsS localhost:8080/healthz
```
Quadlet check: `/usr/lib/systemd/system-generators/podman-system-generator --user --dryrun` prints the unit it would generate.

## Do
- Run rootless by default. Check `podman info` for `rootless: true` and the storage driver.
- Run long-lived services as Quadlet files (`~/.config/containers/systemd/app.container` with `[Container]`, `[Service]`, `[Install]`), not hand-written `podman generate systemd` output.
- Add `Volume=data:/var/lib/app:Z` for SELinux hosts. `:Z` is private to one container, `:z` shared.
- Use pods or a `.kube` file to run co-located services that share localhost.
- Add `AutoUpdate=registry` plus `podman-auto-update.timer` to roll images.
- Use fully qualified image names (`docker.io/library/nginx`) since short names prompt or resolve per `registries.conf`.
- Enable lingering (`loginctl enable-linger USER`) so rootless services survive logout.

## Avoid
- Assuming a daemon or `docker.sock`: there is none by default. Enable `podman.socket` only for tools that need the API, and mount it deliberately.
- Binding ports below 1024 rootless: it fails. Use a high port or lower `net.ipv4.ip_unprivileged_port_start`.
- `podman generate systemd`: deprecated in favor of Quadlet. Write `.container` files.
- Bind-mounting host dirs without `:Z` on SELinux: permission denied with no obvious cause. Add the label.
- Expecting bind-mounted files to be owned by the host user: rootless maps uids. Use `--userns=keep-id` or `:U`.
- Running `sudo podman` and rootless `podman` interchangeably: images and containers live in separate stores.

## Review
- [ ] Images use fully qualified names and pinned tags.
- [ ] Services are Quadlet units with restart policy and lingering where needed.
- [ ] Volumes carry correct SELinux labels and uid mapping.
- [ ] No reliance on a Docker daemon or socket unless intentionally exposed.
