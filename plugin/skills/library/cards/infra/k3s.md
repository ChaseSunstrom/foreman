---
name: k3s
title: K3s
area: infra
tags: [k3s, kubernetes, lightweight, edge, rancher, single-binary]
detect: [file:k3s.yaml, file:config.yaml.d/*.yaml, file:registries.yaml, file:k3s-config.yaml, file:manifests/*.yaml]
related: [kubernetes, helm, systemd, traefik, flux]
---
K3s: a lightweight single-binary Kubernetes with SQLite or embedded etcd, bundled Traefik, and a config file at `/etc/rancher/k3s/`.

## Verify
- `k3s check-config`: the host kernel and cgroup settings support K3s.
- `systemctl status k3s` (or `k3s-agent`): the service is active.
- `k3s kubectl get nodes -o wide`: nodes are `Ready` with the expected roles and IPs.
- `k3s kubectl get pods -A`: system pods (coredns, traefik, metrics-server) are Running.
- `journalctl -u k3s -b --no-pager | tail -50`: startup errors, such as TLS SAN or datastore problems.

## Test first
Validate manifests with a dry run on the server, then assert the workload is ready.
```sh
k3s kubectl apply --dry-run=server -f manifests/
k3s kubectl apply -f manifests/
k3s kubectl rollout status deploy/app --timeout=90s   # red until image, probes and selectors are right
k3s kubectl get ingress app -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

## Do
- Configure through `/etc/rancher/k3s/config.yaml` (keys mirror flags, such as `write-kubeconfig-mode`, `tls-san`, `disable`), not long `INSTALL_K3S_EXEC` strings.
- Pin the version at install with `INSTALL_K3S_VERSION` and `K3S_TOKEN` from a secret.
- Add the load-balancer IP or DNS name with `tls-san` so remote kubectl validates the API certificate.
- Use embedded etcd for HA (`cluster-init: true` on the first server, then `server:` for the others), with an odd count of servers.
- Disable bundled components you replace (`disable: [traefik]` or `servicelb`) before first start.
- Drop manifests or HelmChart resources into `/var/lib/rancher/k3s/server/manifests/` for auto-apply, or use GitOps.
- Configure private registries and mirrors in `/etc/rancher/k3s/registries.yaml`.
- Take etcd snapshots (`k3s etcd-snapshot save`) and set `etcd-snapshot-schedule-cron`.

## Avoid
- Editing the generated `/var/lib/rancher/k3s/server/manifests/*.yaml` bundled add-ons: K3s overwrites them. Customize through a `HelmChartConfig` or disable the component.
- Reusing a node name or hostname across nodes: join failures. Set unique `node-name`.
- Copying `/etc/rancher/k3s/k3s.yaml` with `127.0.0.1` as the server: it points at the client machine. Replace the address.
- A single server with SQLite called highly available: no failover. Use embedded etcd or an external datastore with three servers.
- Mixing server and agent versions beyond skew: instability. Upgrade servers first, then agents.
- Leaving port 6443 or kubelet 10250 open to the internet: restrict by firewall or tailnet.
- `curl | sh` installs in automation with no version pin: surprise upgrades. Pin and verify.
- Forgetting the cgroup memory settings on some ARM boards: the service fails to start. Run `check-config`.

## Review
- [ ] Config lives in `config.yaml`, with pinned version and `tls-san` set.
- [ ] HA uses an odd number of etcd servers with snapshots scheduled.
- [ ] Bundled components are kept deliberately or disabled before first start.
- [ ] API and kubelet ports are firewalled.
