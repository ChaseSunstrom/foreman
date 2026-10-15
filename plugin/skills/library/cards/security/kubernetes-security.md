---
name: kubernetes-security
title: Kubernetes security
area: security
tags: [security, kubernetes, rbac, pod-security, network-policy, containers]
detect: [file:Chart.yaml, file:kustomization.yaml]
related: [iam-least-privilege, sandboxing, secrets-management, trivy, zero-trust]
---
Workloads run non-root with dropped capabilities, namespaced least-privilege RBAC, default-deny network policy, and secrets kept out of manifests.

## Verify
- `kubectl apply --dry-run=server -f k8s/`: the API server and admission accept the manifests under the enforced policy.
- `kubectl auth can-i --list --as=system:serviceaccount:app:web -n app`: the service account holds only what it needs.
- `trivy config k8s/`: misconfiguration scan of manifests.
- `kubectl get networkpolicy -n app`: a default-deny policy exists in the namespace.

## Test first
Lint the rendered manifests in CI, and fail on risky settings.
```python
import yaml, glob

def test_pods_run_hardened():
    for f in glob.glob("k8s/*.yaml"):
        for d in yaml.safe_load_all(open(f)):
            if d and d.get("kind") == "Deployment":
                c = d["spec"]["template"]["spec"]["containers"][0]["securityContext"]
                assert c["runAsNonRoot"] is True, f
                assert c["allowPrivilegeEscalation"] is False, f
                assert c["readOnlyRootFilesystem"] is True, f
                assert c["capabilities"]["drop"] == ["ALL"], f
```

## Do
- Set per container: `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `capabilities.drop: [ALL]`, and `seccompProfile.type: RuntimeDefault`.
- Enforce the Pod Security `restricted` level with namespace labels.
- Give each workload its own ServiceAccount. Set `automountServiceAccountToken: false` unless the pod calls the API.
- Write Roles, not ClusterRoles, with named verbs and resources. No wildcards.
- Start each namespace with a default-deny ingress and egress NetworkPolicy, then allow specific flows.
- Set resource requests and limits to bound abuse.
- Pull secrets from an external store or sealed secrets. Avoid plain Secret manifests in git.
- Pin images by digest and scan them. Use a private registry.

## Avoid
- `privileged: true`, `hostNetwork`, `hostPath` or `hostPID` to make something work: find the exact capability or volume instead.
- Binding `cluster-admin` to a CI or app account: write a narrow Role.
- Running as root because the image expects it: rebuild the image with a numeric non-root USER.
- Using the `default` ServiceAccount and the `latest` tag: name accounts and pin digests.
- Secrets in ConfigMaps or env values committed to git: use secret references from a store.
- Exposing the dashboard or kubelet port without authentication: restrict and require auth.

## Review
- [ ] Every container sets the hardened securityContext.
- [ ] RBAC has no wildcards and no cluster-admin for workloads.
- [ ] A default-deny NetworkPolicy and explicit allows exist.
- [ ] Images are pinned and scanned, and secrets come from a store.
- [ ] Token automount is off where unused.
