---
name: cors
title: CORS policy
area: security
tags: [security, cors, browser, headers, origin, api]
detect: [dep:cors, dep:flask-cors, dep:django-cors-headers, dep:github.com/rs/cors, dep:fastapi, dep:@fastify/cors]
related: [csrf, security-headers, sessions, xss]
---
CORS: an explicit allowlist of origins, no wildcard with credentials, and never a reflected `Origin`; CORS relaxes the browser, it is not access control.

## Verify
- `curl -si localhost:8000/api/me -H "Origin: https://evil.example" | grep -i "access-control"`: a foreign origin gets no `Access-Control-Allow-Origin`.
- `curl -si -X OPTIONS localhost:8000/api/me -H "Origin: https://app.example" -H "Access-Control-Request-Method: PUT" | grep -i "access-control"`: the preflight returns only the allowed origin, methods and headers.
- `pytest -q tests/security/test_cors.py`: the allowlist tests pass.

## Test first
```python
def test_foreign_origin_gets_no_cors_headers(client):
    r = client.get("/api/me", headers={"Origin": "https://evil.example"})
    assert "access-control-allow-origin" not in r.headers

def test_allowed_origin_is_echoed_exactly_with_vary(client):
    r = client.get("/api/me", headers={"Origin": "https://app.example"})
    assert r.headers["access-control-allow-origin"] == "https://app.example"
    assert "Origin" in r.headers.get("vary", "")

def test_null_origin_rejected(client):
    r = client.get("/api/me", headers={"Origin": "null"})
    assert "access-control-allow-origin" not in r.headers
```

## Do
- Keep a list of exact origins (scheme, host, port) in configuration, per environment.
- Reply with `Access-Control-Allow-Origin` only for a matching origin, and add `Vary: Origin` so caches stay correct.
- Enable `Access-Control-Allow-Credentials: true` only for the origins that need cookies, and then never combine it with `*`.
- Restrict `Access-Control-Allow-Methods` and `Access-Control-Allow-Headers` to what the API uses, and set a modest `Access-Control-Max-Age`.
- Set CORS in one place (middleware or the gateway), not both, to avoid duplicate headers.
- Keep authentication and authorization on the server regardless of CORS.
- Do not allow CORS on endpoints that are not meant for browsers.

## Avoid
- `Access-Control-Allow-Origin: *` on authenticated APIs: any site can read responses if credentials are not required, and the wildcard cannot carry credentials anyway. List origins.
- Reflecting the request `Origin` header as the allowed origin: it is a wildcard in disguise. Compare against an allowlist.
- Regex or `endsWith` origin checks like `example.com`: `evilexample.com` and `example.com.evil.io` match. Compare full origins exactly.
- Allowing `null` origin: sandboxed iframes and `file://` send it. Reject it.
- Treating CORS as protection from CSRF or from non-browser clients: curl ignores it, and simple POSTs are sent regardless. Use tokens and auth.
- Allowing all subdomains when one may be compromised or host user content: list specific ones.

## Review
- [ ] Allowed origins are an exact, configured list.
- [ ] No reflected origin, no `null`, no wildcard with credentials.
- [ ] `Vary: Origin` is present.
- [ ] Methods and headers are minimal.
- [ ] Auth does not depend on CORS.
