---
name: api-keys
title: API keys
area: security
tags: [security, api-keys, authentication, hashing, scopes, rotation]
detect: []
related: [secrets-management, rate-limiting, key-rotation, audit-logging, authorization]
---
Issuing API keys: random, prefixed, hashed at rest, scoped, expiring, revocable, shown once.

## Verify
- `pytest -q -k api_key`: hashing, scope and revocation tests pass.
- `git grep -nE "api_key *= *['\"][A-Za-z0-9]{16,}" -- ':!*test*'`: no literal keys in source.
- `gitleaks detect --source . --no-banner`: no leaked keys in the working tree and history.

## Test first
The database must never hold a usable key.
```python
def test_key_is_stored_hashed_and_scoped(client, db, admin):
    r = client.post("/keys", json={"scopes": ["read"]}, headers=admin)
    key = r.json()["key"]
    assert key.startswith("sk_live_")
    assert key not in str(db.dump("api_keys"))
    ro = {"Authorization": f"Bearer {key}"}
    assert client.get("/items", headers=ro).status_code == 200
    assert client.delete("/items/1", headers=ro).status_code == 403
```

## Do
- Generate 32 random bytes from a CSPRNG and encode them. Add a readable prefix (`sk_live_`) so scanners can detect leaks.
- Store a SHA-256 of the key (it is high entropy, so a slow hash is unnecessary) plus the prefix and last four characters for display. Show the full key once.
- Look up by an id or prefix segment, then compare hashes with a constant-time check.
- Attach scopes, an owner, an optional expiry and a last-used timestamp to each key.
- Let owners list, revoke and rotate keys. Support two active keys per client for zero-downtime rotation.
- Send keys only in headers over TLS, never in URLs, which land in logs.
- Rate limit per key and log key id (never key value) on every use.
- Register the prefix with secret scanning.

## Avoid
- Storing keys in plaintext "so support can see them": store hashes and let users regenerate.
- Using `==` to compare tokens: timing leaks. Use `hmac.compare_digest` or the equivalent.
- One all-powerful key per account: issue scoped, per-integration keys.
- Keys in query strings: they are logged by proxies. Use the Authorization header.
- Keys that never expire or have no revoke: add expiry and a kill switch.
- Logging full request headers: redact Authorization.

## Review
- [ ] Only a hash is stored and the full key appears once at creation.
- [ ] Scopes are enforced server-side on every route.
- [ ] Revocation takes effect immediately, including caches.
- [ ] Keys have a prefix, an owner and last-used tracking.
- [ ] Logs and error reports contain no key values.
