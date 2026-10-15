---
name: istio
title: Istio
area: infra
tags: [istio, service-mesh, mtls, gateway, kubernetes, traffic, envoy]
detect: [file:virtualservice*.yaml, file:destinationrule*.yaml, file:peerauthentication*.yaml]
related: [linkerd, envoy, kubernetes-network-policies, cert-manager]
---
Istio service mesh: mTLS by policy, traffic routing through Gateway and VirtualService, and authorization policies tested with real requests.

## Verify
- `istioctl analyze -A`: config lint across namespaces (selectors that match nothing, missing gateways, conflicts).
- `istioctl proxy-status`: every sidecar is synced with the control plane.
- `istioctl x describe pod POD`: which policies and routes apply to a pod.
- `istioctl proxy-config routes POD -n NS`: the routes Envoy actually has.

## Test first
Assert the policy behavior with requests before writing it.
```bash
# deny first: unauthenticated plaintext must fail once STRICT is applied
! kubectl exec -n legacy sleep -- curl -s -m 3 http://api.app:8080/
# mesh client succeeds
kubectl exec -n app client -c client -- curl -s -m 3 -o /dev/null -w '%{http_code}' http://api.app:8080/
```

## Do
- Roll out mTLS with `PeerAuthentication` mode `PERMISSIVE`, confirm traffic is encrypted, then switch to `STRICT`; start mesh-wide in `istio-system` and override per namespace.
- Write `AuthorizationPolicy` with an `ALLOW` rule per workload, matched by `selector` and principals (`cluster.local/ns/NS/sa/SA`).
- Use the Gateway API (`Gateway`, `HTTPRoute`) where your Istio release supports it, otherwise `Gateway` plus `VirtualService`.
- Set `DestinationRule` `trafficPolicy` connection pools and `outlierDetection` for resilience.
- Put retries and timeouts in `VirtualService` `http.retries` and `timeout`; avoid stacking with app-level retries.
- Inject by namespace label (`istio-injection=enabled`, or `istio.io/rev` for revisions) and restart pods after changing it.
- Upgrade with revision-based canaries.

## Avoid
- `STRICT` mTLS applied before all clients are in the mesh: non-mesh callers get connection resets. Go through `PERMISSIVE` first.
- An `AuthorizationPolicy` with an empty `spec` or only a `DENY` expected to allow the rest: semantics differ; test both allowed and denied paths.
- Retries on non-idempotent POSTs: duplicates. Set `retryOn` carefully or disable.
- `VirtualService` host or gateway name typos: traffic silently skips the rule. Run `istioctl analyze`.
- Forgetting pod restart after enabling injection: no sidecar. Check for the `istio-proxy` container.
- Jobs that never exit because of the sidecar: use native sidecar support or quit the proxy at job end.

## Review
- [ ] `istioctl analyze` is clean.
- [ ] mTLS mode and its rollout order are deliberate.
- [ ] Authorization policies have positive and negative tests.
- [ ] Timeouts and retries do not multiply across layers.
- [ ] Injection labels and revisions are consistent.
