---
name: api-gateway-pattern
title: API gateway
area: design
tags: [gateway, routing, authentication, rate-limiting, edge, microservices]
detect: []
related: [backend-for-frontend, rate-limiter-algorithms, microservices, api-versioning, timeouts]
---
One edge entry point handles cross-cutting concerns (auth, limits, routing, TLS, observability) and holds no business logic.

## Verify
- `curl -si https://GATEWAY/api/ITEMS -H "Authorization: Bearer bad"`: expect 401 without reaching any upstream.
- `curl -si https://GATEWAY/api/ITEMS -H "Authorization: Bearer $TOKEN"`: expect 200 with a correlation id header.
- `pytest -q -k gateway`: routing, auth, timeout and header tests.

## Test first
Unauthenticated calls never reach upstream, and the gateway strips spoofable headers.
```python
def test_gateway_rejects_and_sanitises(gateway, upstream):
    r = gateway.get("/api/items", headers={"X-User-Id": "admin"})
    assert r.status_code == 401
    assert upstream.requests == []
    r = gateway.get("/api/items", headers={"Authorization": valid_token("u7"),
                                           "X-User-Id": "admin"})
    assert r.status_code == 200
    assert upstream.last.headers["X-User-Id"] == "u7"      # set from token, not client
    assert "X-Request-Id" in upstream.last.headers
```

## Do
- Terminate TLS, authenticate (JWT or token introspection), and pass a verified identity to upstreams in a header they trust only from the gateway.
- Apply rate limits, request size limits and per-route timeouts here, and a circuit breaker per upstream.
- Route by path or host; version through the route; keep config declarative and in version control.
- Generate or propagate a request id and trace context on every call.
- Keep it stateless and horizontally scaled, with its own health checks and graceful drain.
- Authorise coarse access at the edge, and fine-grained checks in the service that owns the data.
- Use an off-the-shelf gateway (Envoy, Kong, NGINX, a cloud gateway) before building one.

## Avoid
- Business logic or data aggregation in the gateway: it becomes a monolith. Move to a service or a BFF.
- Trusting inbound `X-User-*` headers from clients: strip and re-set them.
- Services reachable directly, bypassing the gateway: the controls are void. Restrict network access.
- Default timeouts of minutes: tied-up connections. Set per-route limits.
- A single gateway instance: it is the single point of failure. Run several with health checks.

## Review
- [ ] Auth enforced at the edge and upstreams not publicly reachable.
- [ ] Spoofable headers stripped.
- [ ] Per-route timeouts and limits set.
- [ ] No business logic in gateway config.
