---
name: linkerd
title: Linkerd
area: infra
tags: [linkerd, service-mesh, mtls, kubernetes, proxy, observability]
detect: [file:serviceprofile*.yaml]
related: [istio, envoy, kubernetes-network-policies, cert-manager]
---
Linkerd service mesh: automatic mTLS through injected proxies, with certificate rotation and policy resources checked by the CLI.

## Verify
- `linkerd check`: control plane health, certificates and versions.
- `linkerd check --proxy`: data plane proxies are healthy and current.
- `linkerd viz stat deploy -n NS`: success rate and latency per workload (needs the viz extension).
- `linkerd identity -n NS -l app=NAME`: pods hold valid workload certificates.

## Test first
Prove the mesh behavior first, then the policy.
```bash
# before the Server and policy: caller succeeds; after: unauthorized caller must fail
kubectl exec -n other client -c client -- curl -s -m 3 -o /dev/null -w '%{http_code}' http://api.app:8080/
# expect 403 or a connection failure once the AuthorizationPolicy applies
```
Also assert in CI that annotated namespaces carry `linkerd.io/inject: enabled`.

## Do
- Inject through the namespace or workload annotation `linkerd.io/inject: enabled`, then restart the pods.
- Run with issuer certificates you manage (cert-manager or your own CA) rather than the default demo setup, and track expiry of the trust anchor and issuer.
- Install CRDs and control plane as separate steps (`linkerd install --crds`, then `linkerd install`) or through Helm charts.
- Use `Server`, `AuthorizationPolicy` and `MeshTLSAuthentication` to restrict who talks to a port.
- Set `config.linkerd.io/skip-outbound-ports` or `skip-inbound-ports` only for protocols that need to bypass the proxy.
- Use `HTTPRoute` for retries, timeouts and traffic splits where your release supports it; `ServiceProfile` is the older route.
- Upgrade control plane first, then restart workloads to refresh proxies.

## Avoid
- Letting the trust anchor expire: the whole mesh stops authenticating. Monitor expiry and rotate ahead of time.
- Using the default-generated CA for production: the key is not managed. Issue from cert-manager.
- Opaque or server-first protocols (MySQL, SMTP) treated as HTTP: connections hang. Mark ports opaque with `config.linkerd.io/opaque-ports`.
- Enabling default-deny policy before authorizing probes: kubelet health checks fail. Authorize them explicitly.
- Skipping restarts after enabling injection: pods have no proxy.
- Treating `ServiceProfile` retries as safe for non-idempotent routes: set `isRetryable` only on safe ones.

## Review
- [ ] `linkerd check` passes before and after the change.
- [ ] Certificate issuance and rotation are automated.
- [ ] Opaque and skip ports are listed with reasons.
- [ ] Authorization has a negative test.
- [ ] Probes are authorized under any default-deny.
