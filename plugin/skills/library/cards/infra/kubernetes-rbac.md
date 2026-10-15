---
name: kubernetes-rbac
title: Kubernetes RBAC
area: infra
tags: [kubernetes, rbac, security, serviceaccount, roles, least-privilege]
detect: []
related: [kubernetes, kubernetes-network-policies, helm, docker-security]
---
Kubernetes RBAC: namespaced Roles and ServiceAccounts with the fewest verbs, never wildcards or cluster-admin by default.

## Verify
- `kubectl auth can-i --list --as=system:serviceaccount:NS:SA -n NS`: the effective permissions of the account.
- `kubectl auth can-i delete secrets --as=system:serviceaccount:NS:SA -n NS`: a specific denial holds (expect `no`).
- `kubectl get clusterrolebinding -o wide | grep -E 'cluster-admin'`: who holds cluster-admin.
- `kubectl apply --dry-run=server -f rbac.yaml`: manifests are valid.

## Test first
Assert the denials before writing the Role.
```bash
SA=system:serviceaccount:app:worker
test "$(kubectl auth can-i get configmaps -n app --as=$SA)" = yes
test "$(kubectl auth can-i get secrets -n app --as=$SA)" = no
test "$(kubectl auth can-i list pods -n other --as=$SA)" = no
```
Run in CI against a kind cluster after applying the manifests.

## Do
- One ServiceAccount per workload; set `serviceAccountName` explicitly rather than using `default`.
- Prefer `Role` plus `RoleBinding` in the workload namespace; use `ClusterRole` only for cluster-scoped resources or nodes.
- List exact `apiGroups`, `resources` and `verbs`; narrow with `resourceNames` where the object name is known.
- Set `automountServiceAccountToken: false` on pods that never call the API.
- Bind groups from the identity provider rather than individual users.
- A ClusterRole can be bound by a RoleBinding to scope it to one namespace.
- Treat `secrets` `get`/`list`/`watch` as full read of credentials, and `pods/exec` as shell access.

## Avoid
- `verbs: ["*"]` or `resources: ["*"]`: grants future resources too. Enumerate.
- Binding `cluster-admin` to a workload SA for convenience: a pod compromise owns the cluster. Write a scoped Role.
- Granting `create` on `pods`, `rolebindings` or `serviceaccounts/token`: allows privilege escalation. Review each as admin-equivalent.
- Editing the `default` ServiceAccount: every pod in the namespace inherits it. Make a dedicated SA.
- `list` on secrets assumed harmless: it returns the data. Remove it or use `resourceNames` with `get`.
- Role without a matching binding (or the reverse), assumed to work: verify with `auth can-i`.

## Review
- [ ] No wildcards and no new cluster-admin bindings.
- [ ] Every permission maps to an API call the workload makes.
- [ ] Token automount disabled where unused.
- [ ] Subjects name the right namespace on ServiceAccounts.
- [ ] `can-i` assertions exist for at least two denials.
