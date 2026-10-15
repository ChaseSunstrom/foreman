---
name: sessions
title: Session management
area: security
tags: [security, sessions, cookies, auth, web, logout]
detect: [dep:express-session, dep:flask-login, dep:django-session-timeout, dep:cookie-session, dep:iron-session]
related: [csrf, jwt, authorization, security-headers, password-hashing]
---
Server-side sessions: random opaque ids in hardened cookies, rotated on login, revoked on logout, expired on idle and absolute limits.

## Verify
- `curl -sI -X POST localhost:8000/login -d "u=a&p=b" | grep -i set-cookie`: the cookie carries `HttpOnly`, `Secure`, `SameSite`, and `Path`.
- `pytest -q tests/security/test_sessions.py`: fixation, logout and expiry tests pass.
- `grep -rniE "session.*(secret|key)\s*=\s*['\"]" src/`: no hardcoded signing key.

## Test first
Test the lifecycle, not the library.
```python
def test_session_id_changes_on_login(client, user):
    client.get("/")
    before = client.cookies.get("sid")
    client.post("/login", json=user.creds)
    assert client.cookies.get("sid") != before

def test_old_session_dead_after_logout(client, user):
    client.post("/login", json=user.creds)
    sid = client.cookies["sid"]
    client.post("/logout")
    client.cookies.set("sid", sid)
    assert client.get("/me").status_code == 401
```

## Do
- Generate ids from the OS CSPRNG with at least 128 bits (`secrets.token_urlsafe(32)`, `crypto.randomBytes(32)`).
- Issue a new id on login and on privilege change, and invalidate the old one.
- Set `HttpOnly; Secure; SameSite=Lax` (or `Strict`), a narrow `Path`, and no `Domain` unless required. Use the `__Host-` prefix where possible.
- Enforce an idle timeout and an absolute lifetime server-side, not only cookie `Max-Age`.
- On logout, delete the server record, then clear the cookie.
- Revoke all sessions on password change and on suspected compromise.
- Store only a hash of the id if the store could leak.

## Avoid
- Session ids in URLs or JSON bodies: they land in logs and Referer. Keep them in the cookie.
- Keeping the pre-login id: session fixation. Rotate on authentication.
- Client-side-only logout (deleting the cookie): a stolen cookie still works. Delete the server record.
- Default `express-session` `MemoryStore` in production: it leaks memory and does not scale. Use a Redis or database store.
- A weak or default `secret` like `"keyboard cat"`: load from the environment and rotate.
- Long-lived "remember me" using the same session cookie: use a separate rotating token bound to a device.

## Review
- [ ] Cookie flags are set and tested over HTTPS.
- [ ] Id rotates on login, privilege change and password change.
- [ ] Idle and absolute timeouts are enforced server-side.
- [ ] Logout and revoke-all remove server state.
- [ ] State-changing routes are CSRF-protected.
