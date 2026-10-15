---
name: api-security
title: API security
area: security
tags: [security, api, rest, authorization, rate-limiting, owasp]
detect: []
related: [idor, mass-assignment, rate-limiting, authorization, input-validation, cors, jwt]
---
HTTP API baseline: authenticate every route, authorize each object and property, validate input and output, limit resources, and expose nothing extra.

## Verify
- `curl -si localhost:8000/v1/orders/1`: an unauthenticated call returns 401, not data.
- `curl -si -X OPTIONS localhost:8000/v1/orders -H 'Origin: https://evil.example' -H 'Access-Control-Request-Method: GET' | grep -i access-control`: no permissive CORS for a foreign origin.
- `pytest -q -k "api_security or authz"`: the route-matrix test below passes.
- `semgrep --config auto .`: common injection and auth pitfalls flagged.

## Test first
Walk every registered route and require authentication by default.
```python
PUBLIC = {("POST", "/v1/login"), ("GET", "/healthz")}

def test_every_route_requires_auth(app, client):
    for r in app.routes:
        for method in r.methods - {"HEAD", "OPTIONS"}:
            if (method, r.path) in PUBLIC:
                continue
            path = r.path.replace("{id}", "1")
            resp = client.request(method, path)
            assert resp.status_code in (401, 403), (method, r.path, resp.status_code)
```

## Do
- Deny by default: attach auth at the router or middleware level, and list public routes explicitly.
- Authorize per object and per property (see IDOR and mass-assignment). Do not trust client-sent ids, roles or prices.
- Validate every input with schemas: types, ranges, lengths, enums. Reject unknown fields. Validate responses against a model so internal fields cannot leak.
- Limit resources: request body size, page size, timeouts, rate limits per identity and per route, and stricter limits on login, reset and expensive endpoints.
- Use parameterised queries, and never build SQL, shell or paths from input.
- Return generic errors with a request id, with no stack traces and no framework banners.
- Set an explicit CORS allow-list, and security headers, and require TLS.
- Version the API, inventory every endpoint, and retire old versions and debug routes.
- Treat third-party API responses as untrusted input as well.

## Avoid
- Per-route `@login_required` decorators you must remember: forgetting one exposes it. Apply default-deny globally.
- Verbose errors with SQL or stack traces in production responses: log them, and return a short code.
- Unbounded list endpoints and uploads: enforce limits and pagination.
- Using HTTP verbs loosely (state change on GET): changes belong in POST, PUT, PATCH or DELETE with CSRF or token protection.
- Shadow endpoints (`/debug`, `/admin`, old `/v0`) left live: remove or protect them and audit the route list.
- Excessive data exposure ("the UI hides it"): return only fields the caller may see.

## Review
- [ ] A route-matrix test proves default-deny auth.
- [ ] Object and property level authorization is tested with two users.
- [ ] Inputs are schema-validated, unknown fields rejected and sizes capped.
- [ ] Rate limits and timeouts exist, with stricter ones on sensitive routes.
- [ ] Errors, CORS and headers are explicit and minimal.
