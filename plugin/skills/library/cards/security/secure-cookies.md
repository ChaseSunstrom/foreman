---
name: secure-cookies
title: Secure cookies
area: security
tags: [security, cookies, session, samesite, httponly, web]
detect: []
related: [sessions, csrf, security-headers, xss, tls]
---
Session and auth cookies: HttpOnly, Secure, SameSite, narrow scope, prefixed names, server-side expiry.

## Verify
- `curl -si https://localhost:8443/login -d 'u=a&p=b' -k | grep -i '^set-cookie'`: the real response carries every attribute.
- `curl -sI http://localhost:8080/ | grep -i '^location'`: plain HTTP redirects to HTTPS before any cookie is set.
- `git grep -nEi "httponly|samesite|secure *[:=]" -- ':!*test*'`: every cookie-setting site is found and reviewed.
- `pytest -q -k cookie`: the attribute tests below pass.

## Test first
Assert on the raw `Set-Cookie` header, not the framework config.
```python
def test_session_cookie_attributes(client):
    r = client.post("/login", json={"user": "a", "password": "right"})
    c = r.headers["set-cookie"].lower()
    assert "httponly" in c
    assert "secure" in c
    assert "samesite=lax" in c or "samesite=strict" in c
    assert "domain=" not in c
    assert c.startswith("__host-")
```

## Do
- Set `HttpOnly; Secure; SameSite=Lax` (Strict for admin or banking) on every auth cookie.
- Use the `__Host-` prefix: it forces Secure, Path=/ and no Domain, so subdomains cannot overwrite it.
- Omit `Domain`. A set Domain shares the cookie with every subdomain, including forgotten ones.
- Hold only an opaque random id in the cookie. Keep data and expiry on the server so logout and revocation really work.
- Rotate the session id on login and privilege change. Set both an idle and an absolute timeout.
- Keep SameSite and add CSRF tokens for state-changing routes. SameSite alone is not the defence.
- Behind a proxy, trust the forwarded scheme explicitly so Secure is not dropped.

## Avoid
- `httponly=False` so front-end JS can read the token: XSS then steals it. Pass the CSRF token separately, never the session.
- `Secure` off in dev copied into prod: drive it from environment config and test the prod profile.
- `SameSite=None` to "fix" a cross-site embed: this opens CSRF. Use a token flow or a narrow partitioned cookie.
- Putting JWTs or user data in `localStorage` instead: any script reads it. Use a cookie with the flags above.
- Long `Max-Age` on session cookies: a stolen cookie lives for months. Use session cookies plus server expiry.
- Cookie name with no prefix and a parent Domain: a sibling subdomain can fixate it. Use `__Host-`.

## Review
- [ ] Every Set-Cookie for auth has HttpOnly, Secure, SameSite, Path, and no Domain.
- [ ] Session id is regenerated at login and invalidated server-side at logout.
- [ ] A test inspects the raw header in the prod config.
- [ ] CSRF protection exists independently of SameSite.
- [ ] HTTP never serves an authenticated page, and HSTS is set.
