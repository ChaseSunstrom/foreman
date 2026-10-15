---
name: kubernetes
title: Kubernetes
area: infra
tags: [kubernetes, k8s, manifests, kubectl, deployment, probes]
detect: [file:k8s/*.yaml, file:k8s/*.yml, file:manifests/*.yaml, file:*.k8s.yaml, file:deployment.yaml]
related: [helm, kustomize, argo-cd, flux, docker, cert-manager]
---
Kubernetes manifests: Deployments with probes, resource limits, security contexts, PDBs and least-privilege RBAC.

## Verify
- `kubectl apply --dry-run=client -f k8s/ -R`: manifests parse and have valid kinds.
- `kubectl apply --dry-run=server -f k8s/ -R`: the API server admits them, including CRDs and admission policy.
- `kubectl diff -f k8s/ -R`: what would change in the live cluster.
- `kubectl rollout status deploy/app --timeout=120s`: the rollout became ready.
- `kubectl auth can-i --list --as=system:serviceaccount:NS:SA -n NS`: the ServiceAccount's real permissions.

## Test first
Validate the schema and policy offline, then smoke against a throwaway cluster (kind or k3s).
```sh
kubectl apply --dry-run=server -f k8s/ -R
kubectl -n app wait --for=condition=Available deploy/app --timeout=60s
kubectl -n app run curl --rm -i --restart=Never --image=curlimages/curl -- curl -fsS http://app/healthz
```
Red first: the `wait` fails until readiness passes, and the curl fails until the Service selector matches the pod labels.

## Do
- Set `resources.requests` and `limits` (memory limit equals request is safest) on every container.
- Define `readinessProbe` for traffic, `livenessProbe` conservatively, and `startupProbe` for slow boots.
- Set `securityContext`: `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `capabilities.drop: [ALL]`, `seccompProfile.type: RuntimeDefault`.
- Make `Service.spec.selector` match pod template labels exactly, and keep `Deployment.spec.selector` immutable.
- Add a `PodDisruptionBudget` and `topologySpreadConstraints` for replicated services.
- Give each workload its own ServiceAccount with a namespaced `Role`, and set `automountServiceAccountToken: false` if unused.
- Pin image by digest or immutable tag, and set `terminationGracePeriodSeconds` plus a `preStop` for graceful drains.
- Use `NetworkPolicy` default-deny, then allow specific flows.

## Avoid
- Image `:latest` with `imagePullPolicy` left default: pods run different builds. Pin the tag.
- Liveness probe hitting a dependency (DB): a DB blip restarts every pod. Probe only the process.
- No resource requests: scheduling is blind and the pod gets BestEffort QoS. Set them.
- `ClusterRoleBinding` to `cluster-admin` for an app: scope a `Role` to the namespace.
- Secrets in `ConfigMap` or committed `Secret` YAML: use sealed or external secrets. Base64 is not encryption.
- `apiVersion: extensions/v1beta1` or `apps/v1beta1`, and `kubectl run` with generators: removed. Use `apps/v1`, `networking.k8s.io/v1`.
- Editing `spec.selector` of a Deployment: rejected as immutable. Recreate the object.
- `hostNetwork`, `privileged`, or `hostPath` as a quick fix: use the narrowest alternative.

## Review
- [ ] Each container has requests/limits, probes and a restrictive securityContext.
- [ ] Labels and selectors line up between Deployment, Service and PDB.
- [ ] RBAC is namespaced and minimal, and no plaintext secrets are in git.
- [ ] `--dry-run=server` and `kubectl diff` are clean.
- [ ] Rollout strategy and graceful shutdown allow zero-downtime updates.
