---
name: zero-trust
title: Zero trust architecture
area: security
tags: [security, zero-trust, mtls, identity, segmentation, authorization]
detect: []
related: [tls, authorization, iam-least-privilege, kubernetes-security, audit-logging]
---
No implicit trust from network location: authenticate and authorize every request, service to service too, with short-lived identity and segmentation.

## Verify
- `curl -sk --max-time 5 https://internal-svc.local/health -o /dev/null -w '%{http_code}\n'`: an unauthenticated call to an internal service is refused.
- `openssl s_client -connect internal-svc.local:443 -cert client.pem -key client.key </dev/null`: a valid client certificate completes the mutual TLS handshake.
- `kubectl get networkpolicy -A`: segmentation policies exist per namespace, when on Kubernetes.
- `pytest -q -k zero_trust`: the internal-route tests pass.

## Test first
An internal endpoint must reject calls that lack service identity, including from inside the network.
```python
def test_internal_api_requires_service_identity(internal_client):
    assert internal_client.get("/internal/users/1").status_code == 401

def test_service_token_for_other_audience_is_rejected(internal_client, mint):
    tok = mint(sub="billing", aud="reports")
    r = internal_client.get("/internal/users/1", headers={"Authorization": f"Bearer {tok}"})
    assert r.status_code in (401, 403)

def test_service_cannot_exceed_its_scope(internal_client, mint):
    tok = mint(sub="billing", aud="users", scope="users:read")
    assert internal_client.delete("/internal/users/1", headers={"Authorization": f"Bearer {tok}"}).status_code == 403
```

## Do
- Give every workload a cryptographic identity (SPIFFE-style, cloud workload identity or mTLS certificates) with short lifetimes and automatic renewal.
- Authenticate and authorize each call at the receiving service. Check audience, scope and the end user on whose behalf the call runs.
- Propagate the end-user identity or a signed token, not only the calling service's.
- Segment the network: default-deny between services, explicit allow per flow, and separate environments and accounts.
- Use device and session posture for human access: SSO with MFA and re-authentication for sensitive actions.
- Put admin and data-plane access behind an identity-aware proxy instead of a flat VPN.
- Log every decision for audit, and alert on lateral-movement patterns.
- Limit egress so a compromised service cannot reach arbitrary hosts.

## Avoid
- "Internal network" endpoints with no auth: anything inside can call them. Require identity.
- Shared long-lived service tokens in env files: issue short-lived credentials per workload.
- Verifying that a token is valid but not its audience: reject tokens minted for other services.
- Gateway-only auth with open back-end ports: enforce at each service.
- A flat VPN that grants network access to everything: grant per-application access.
- Skipping end-user context in service calls: the confused deputy returns another tenant's data.

## Review
- [ ] Every service endpoint authenticates callers, including internal ones.
- [ ] Credentials are short-lived and bound to an audience.
- [ ] Default-deny network policy is in place with explicit allows.
- [ ] End-user identity is carried across calls and checked.
- [ ] Decisions are logged.
