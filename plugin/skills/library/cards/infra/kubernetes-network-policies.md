---
name: kubernetes-network-policies
title: Kubernetes NetworkPolicies
area: infra
tags: [kubernetes, networkpolicy, security, cni, egress, ingress]
detect: []
related: [kubernetes, kubernetes-rbac, istio, cert-manager]
---
NetworkPolicies: default-deny per namespace, then explicit allows for ingress, egress and DNS, on a CNI that enforces them.

## Verify
- `kubectl get networkpolicy -A`: policies exist in each namespace.
- `kubectl describe networkpolicy NAME -n NS`: selectors resolve as intended.
- `kubectl exec -n NS POD -- wget -qO- -T 3 http://svc.other-ns`: a denied path times out.
- `kubectl exec -n NS POD -- nslookup kubernetes.default`: DNS still works after egress deny.

## Test first
Write the connectivity matrix as a script, with the denial first.
```bash
# fails until default-deny exists
! kubectl exec -n app client -- wget -qO- -T 3 http://db.data:5432
# passes once the allow exists
kubectl exec -n app client -- wget -qO- -T 3 http://api.app:8080/healthz
```
Run it in CI on kind with a policy-enforcing CNI such as Calico or Cilium.

## Do
- Start with a deny-all policy: `podSelector: {}` and `policyTypes: [Ingress, Egress]` with no rules.
- Add allows by label: `podSelector` for pods in the same namespace, `namespaceSelector` for others.
- Allow DNS explicitly: egress to the cluster DNS pods on UDP and TCP 53, matched by `kubernetes.io/metadata.name` namespace label.
- Allow ingress from the ingress controller namespace only on the serving port.
- Restrict egress to external hosts with `ipBlock` CIDRs, using `except` to carve out metadata addresses.
- Policies are additive: the union of all matching policies applies, there is no explicit deny.
- Keep policies in the same chart or kustomization as the workload.

## Avoid
- Assuming policies work on any CNI: without an enforcing plugin they are silently ignored. Verify with the denial test.
- Egress deny without a DNS allow: every lookup fails. Add the port 53 rule.
- Putting `namespaceSelector` and `podSelector` as two list items when you mean both: that is OR. Put them in one `from` element for AND.
- Empty `from: []` believed to mean deny: it matches nothing in that list only if the key is present with no entries; verify with the test instead of reading.
- Forgetting node-level health checks: kubelet probes can be affected by some CNIs. Test readiness after applying.
- Relying on policies alone for sensitive hops: add mTLS in the mesh too.

## Review
- [ ] Each namespace has a default-deny policy for ingress and egress.
- [ ] DNS egress is explicitly allowed.
- [ ] Selectors use stable labels, and AND versus OR is intended.
- [ ] Connectivity tests cover one allowed and one denied path.
- [ ] The CNI in use enforces NetworkPolicy.
