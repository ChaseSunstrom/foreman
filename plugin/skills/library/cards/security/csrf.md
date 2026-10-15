---
name: csrf
title: Cross-site request forgery
area: security
tags: [security, csrf, cookies, samesite, web, forms]
detect: [dep:csurf, dep:csrf-csrf, dep:flask-wtf, dep:django-csp, dep:gorilla/csrf, dep:github.com/gorilla/csrf]
related: [sessions, cors, xss, security-headers, authorization]
---
CSRF: any cookie-authenticated, state-changing request needs a token or origin check plus SameSite cookies; GET never mutates.

## Verify
- `pytest -q tests/security/test_csrf.py`: cross-origin and tokenless writes are refused.
- `curl -si -X POST localhost:8000/transfer -H "Cookie: sid=VALID" -H "Origin: https://evil.example" -d "to=x&amt=1" | head -1`: a forged cross-origin POST returns 403.
- `curl -sI localhost:8000/login -X POST | grep -i set-cookie`: the session cookie has `SameSite`.

## Test first
```python
def test_post_without_csrf_token_is_rejected(client, user):
    client.login(user)
    r = client.post("/settings/email", data={"email": "evil@x.io"})
    assert r.status_code == 403

def test_post_from_foreign_origin_is_rejected(client, user, csrf_token):
    client.login(user)
    r = client.post("/settings/email", data={"email": "a@b.io", "csrf": csrf_token},
                    headers={"Origin": "https://evil.example"})
    assert r.status_code == 403
```

## Do
- Mark session cookies `SameSite=Lax` at minimum (`Strict` for sensitive apps) and `Secure`, `HttpOnly`.
- Require a per-session (or signed double-submit) token on every `POST`, `PUT`, `PATCH`, `DELETE` that relies on cookies.
- Verify the `Origin` header (fall back to `Referer`) matches your own origin on unsafe methods.
- Use the framework's protection and leave it on: Django `CsrfViewMiddleware`, Flask-WTF `CSRFProtect`, Rails `protect_from_forgery`, Spring Security's default.
- Make GET, HEAD and OPTIONS side-effect free.
- For SPAs with cookie auth, send the token in a custom header (`X-CSRF-Token`) and require `Content-Type: application/json`.
- Re-authenticate or confirm for high-risk actions (password, email, payment).

## Avoid
- `@csrf_exempt` or disabling protection to make a test pass: fix the test to send the token. Exempt only signed webhooks.
- State changes on GET (`/delete?id=1`, `/logout`): an `<img>` triggers them. Use POST.
- Relying on CORS to stop CSRF: simple form POSTs are not preflighted. Use tokens and origin checks.
- A token that is not tied to the session, or is compared with `==`: use constant-time compare and bind to the session.
- Token stored in a cookie only, with no header or form echo: the browser sends it automatically. The server must compare it to a value from the request body or header.
- Treating bearer-token API calls (Authorization header) as needing CSRF tokens while ignoring cookie routes on the same app: protect whichever auth the route accepts.

## Review
- [ ] Every cookie-authenticated unsafe route is protected.
- [ ] Cookies carry `SameSite`, `Secure`, `HttpOnly`.
- [ ] Origin is checked on unsafe methods.
- [ ] No GET mutates state.
- [ ] Exemptions are limited to signed webhooks.
