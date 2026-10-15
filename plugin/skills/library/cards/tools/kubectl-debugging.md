---
name: kubectl-debugging
title: kubectl debugging
area: tools
tags: [kubernetes, kubectl, pods, debugging, logs, events]
detect: []
related: [log-analysis, lsof, tcpdump, yamllint]
---
kubectl debugging: find why a workload is unhealthy by reading status, events, logs and a live shell, in that order.

## Verify
- `kubectl get pods -o wide`: state, restarts, node and IP for each pod.
- `kubectl describe pod NAME`: events at the bottom (scheduling, image pull, probe failures, OOMKilled) and last state.
- `kubectl logs NAME -c CONTAINER --previous`: logs of the last crashed container instance.
- `kubectl get events --sort-by=.lastTimestamp`: recent cluster events in order.
- `kubectl apply --dry-run=server -f manifest.yaml`: the API server accepts the manifest (schema and admission).

## Test first
Reproduce with the exact state you see, then read why.
```
kubectl get pods -l app=web
# CrashLoopBackOff -> read the dying container's output
kubectl logs deploy/web --previous --tail=50
kubectl describe pod -l app=web | sed -n '/Events:/,$p'
```
Fix the manifest, apply, and watch `kubectl rollout status deploy/web` finish.

## Do
- Read pod status first: Pending (scheduling, quotas, PVC), ImagePullBackOff (name, tag, secret), CrashLoopBackOff (app or probe), OOMKilled (limits).
- Check `kubectl get endpoints SVC`: an empty list means the selector or readiness is wrong.
- Reach a service from inside: `kubectl run tmp --rm -it --image=busybox --restart=Never -- wget -qO- http://svc:80`.
- Use `kubectl exec -it POD -- sh` for a shell, or `kubectl debug -it POD --image=busybox --target=CONTAINER` when the image has no shell.
- Use `kubectl port-forward svc/web 8080:80` to test from your machine.
- Use `kubectl rollout undo deploy/web` to revert a bad release, then fix forward.
- Always pass `-n NAMESPACE` or set the context namespace, and check `kubectl config current-context` before a mutating command.

## Avoid
- Running a change against the wrong context: you edit production. Check the context and namespace first.
- Reading `kubectl logs` of the new container and missing the crash: use `--previous`.
- Raising limits to hide OOMKilled without finding the leak: check memory use and the app.
- Liveness probes that mirror readiness or hit a slow dependency: restarts cascade. Use a startup probe and a cheap liveness check.
- Editing live objects with `kubectl edit` and losing the change on the next deploy: change the manifest in git.
- Leaving debug pods or `port-forward` sessions behind: delete them when done.

## Review
- [ ] The root cause is stated from events or logs, not guessed.
- [ ] The fix is in the manifest in git and applied through the normal path.
- [ ] `kubectl rollout status` and the endpoints show healthy pods.
- [ ] Context and namespace were confirmed, and temporary debug resources removed.
