---
name: security-headers
title: HTTP security headers
area: security
tags: [security, headers, csp, hsts, http, browser]
detect: [dep:helmet, dep:django-csp, dep:flask-talisman, dep:secure, dep:github.com/unrolled/secure]
related: [xss, cors, csrf, tls, sessions]
---
Security headers: set a strict CSP, HSTS, `nosniff`, framing and referrer policies once, centrally, and test them.

## Verify
- `curl -sI https://localhost:8443/ | grep -iE "strict-transport|content-security|x-content-type|referrer-policy|frame-ancestors|permissions-policy"`: the headers are present on a real response.
- `curl -sI localhost:8000/api/x | grep -i "x-powered-by\|^server"`: version-revealing headers are gone.
- `pytest -q tests/security/test_headers.py`: header assertions pass for HTML, API and error responses.

## Test first
```python
import pytest
@pytest.mark.parametrize("path", ["/", "/api/health", "/missing-404"])
def test_security_headers_on_every_response(client, path):
    h = client.get(path).headers
    assert h["x-content-type-options"] == "nosniff"
    assert "frame-ancestors" in h["content-security-policy"]
    assert "max-age=" in h.get("strict-transport-security", "max-age=")  # HTTPS only
    assert "x-powered-by" not in h
```

## Do
- Install the stack's helper (Express `helmet`, Django `SecurityMiddleware` settings plus `django-csp`, Flask `flask-talisman`) at the top of the middleware chain.
- CSP: start with `default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'`, add per-request nonces for inline scripts, and trial it with `Content-Security-Policy-Report-Only` first.
- HSTS: `Strict-Transport-Security: max-age=31536000; includeSubDomains` once all subdomains are HTTPS. Add `preload` only after deciding to submit.
- `X-Content-Type-Options: nosniff` everywhere, and correct `Content-Type` with charset.
- `Referrer-Policy: strict-origin-when-cross-origin` (or `no-referrer`), and a minimal `Permissions-Policy`.
- Use `frame-ancestors` in CSP to control framing, with `X-Frame-Options: DENY` for older browsers.
- Add `Cache-Control: no-store` to authenticated and sensitive responses.
- Apply headers to error pages, redirects and static files too.

## Avoid
- A CSP with `unsafe-inline`, `unsafe-eval` or a bare `*`: it provides little protection. Use nonces or hashes.
- Enabling CSP in enforce mode with no testing: it breaks the site and gets switched off. Use report-only first.
- Setting HSTS over HTTP or on a domain with an HTTP-only subdomain plus `includeSubDomains`: HSTS only counts on HTTPS and can lock out subdomains.
- `X-XSS-Protection` as a defense: it is obsolete. Set `0` or omit it, and rely on CSP.
- Headers set only in the app while a proxy or CDN overwrites or drops them: check the live response, not the config.
- `Access-Control-Allow-Origin: *` as a "fix" for a blocked request: see the CORS card.
- Revealing `Server` and `X-Powered-By` versions: remove them.

## Review
- [ ] CSP, HSTS, `nosniff`, referrer and framing headers appear on real responses, including errors.
- [ ] CSP has no `unsafe-inline` for scripts.
- [ ] Sensitive responses are not cacheable.
- [ ] Banner headers are removed.
- [ ] A header test runs in CI.
