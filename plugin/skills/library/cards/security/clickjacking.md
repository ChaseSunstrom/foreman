---
name: clickjacking
title: Clickjacking defence
area: security
tags: [security, clickjacking, framing, csp, headers, web]
detect: []
related: [security-headers, csrf, xss, secure-cookies]
---
Stop pages being framed by other origins: CSP frame-ancestors, legacy X-Frame-Options, SameSite cookies, and confirmation on risky actions.

## Verify
- `curl -sI https://localhost:8443/ -k | grep -iE 'content-security-policy|x-frame-options'`: both headers are present on HTML responses.
- `curl -sI https://localhost:8443/login -k | grep -i frame-ancestors`: auth pages specifically are covered.
- `pytest -q -k framing`: the header tests below pass for every HTML route class.

## Test first
Check headers on error pages and redirects too.
```python
import pytest

@pytest.mark.parametrize("path", ["/", "/login", "/settings", "/404-nope"])
def test_pages_cannot_be_framed(client, path):
    r = client.get(path)
    csp = r.headers.get("content-security-policy", "")
    assert "frame-ancestors 'none'" in csp or "frame-ancestors 'self'" in csp
    assert r.headers.get("x-frame-options") in ("DENY", "SAMEORIGIN")
```

## Do
- Send `Content-Security-Policy: frame-ancestors 'none'` by default. Use `'self'` or an explicit origin list only for pages that must embed.
- Add `X-Frame-Options: DENY` (or `SAMEORIGIN`) for old browsers. Both headers should agree.
- Set headers in one middleware so every response gets them, errors included.
- Use SameSite=Lax or Strict session cookies so a framed page is not authenticated cross-site.
- For widgets meant to embed, serve them from a separate path or origin with a narrow allow-list and no sensitive actions.
- Require a deliberate step (re-auth or typed confirm) for destructive actions.
- Do not rely on JavaScript frame-busting.

## Avoid
- Only `X-Frame-Options: ALLOW-FROM`: it is obsolete and ignored. Use `frame-ancestors`.
- A frame-ancestors list with a wildcard like `https:` or `*`: any site can embed. Name each origin.
- Header added on the app but stripped or missing on the CDN, static host or error page: test the deployed edge.
- JS `if (top !== self)` busters: sandboxed iframes defeat them. Use headers.
- Allowing framing everywhere because one page is a widget: scope the exception by path.
- Reflecting the `Origin` or `Referer` into frame-ancestors: use a fixed list.

## Review
- [ ] Every HTML response (including 4xx and 5xx) carries frame-ancestors.
- [ ] Default is `'none'`, and each exception is named and justified.
- [ ] X-Frame-Options matches the CSP intent.
- [ ] The CDN and reverse proxy do not drop the headers.
- [ ] Sensitive actions need more than one click.
