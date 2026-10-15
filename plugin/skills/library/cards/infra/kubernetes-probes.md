---
name: kubernetes-probes
title: Kubernetes probes
area: infra
tags: [kubernetes, probes, liveness, readiness, startup, health, rollout]
detect: []
related: [kubernetes, kubernetes-autoscaling, helm, kustomize]
---
Liveness, readiness and startup probes: each answers a different question, and mixing them up causes restart loops and outages.

## Verify
- `kubectl apply --dry-run=server -f deploy.yaml`: the API server accepts the probe fields.
- `kubectl rollout status deploy/NAME --timeout=120s`: new pods actually become Ready.
- `kubectl describe pod POD`: Events show `Liveness probe failed` or `Readiness probe failed` with the reason.
- `kubectl get endpointslices -l kubernetes.io/service-name=NAME`: only Ready pods are listed as endpoints.

## Test first
Make the health endpoint fail first, then wire the probe to it.
```python
def test_ready_fails_when_db_down(client, db):
    db.stop()
    assert client.get("/readyz").status_code == 503
    assert client.get("/livez").status_code == 200   # process still alive
```
Then assert in a render test that the manifest has `readinessProbe.httpGet.path == "/readyz"` and `livenessProbe.httpGet.path == "/livez"`.

## Do
- Readiness gates traffic: check what this pod needs to serve (warm cache, own DB pool). Liveness answers only "is this process wedged".
- Add a `startupProbe` for slow boots (`failureThreshold` x `periodSeconds` covers worst-case start); liveness and readiness do not run until it passes.
- Keep liveness local and cheap: no downstream calls, no DB query.
- Set `timeoutSeconds` above the endpoint's p99 under load; the default is 1 second.
- Use `httpGet` or `grpc` (with the standard health service) over `exec`, which forks a process per check.
- Handle SIGTERM: stop reporting ready, drain, then exit; set `terminationGracePeriodSeconds` above the drain time.
- Give each container its own probes in multi-container pods.

## Avoid
- Liveness probe hitting a dependency: a DB blip restarts every pod at once. Point it at a local-only endpoint.
- Identical liveness and readiness endpoints: pods are killed instead of just drained. Split them.
- Aggressive `initialDelaySeconds` guesses instead of a startup probe: either slow rollouts or kills on boot. Use `startupProbe`.
- No readiness probe: Service sends traffic to booting pods. Always set one on serving containers.
- `failureThreshold: 1` on liveness: one slow GC pause means a restart. Use 3 or more.
- Probes on a port the app binds to localhost only: kubelet probes the pod IP. Bind to 0.0.0.0.

## Review
- [ ] Every serving container has readiness; long-boot ones have a startup probe.
- [ ] Liveness touches no external dependency.
- [ ] Timeouts and thresholds are justified against measured start and latency.
- [ ] SIGTERM handling and grace period match the drain time.
- [ ] PodDisruptionBudget exists for replicated workloads.
