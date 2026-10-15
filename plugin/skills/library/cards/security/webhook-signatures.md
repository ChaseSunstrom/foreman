---
name: webhook-signatures
title: Webhook signature verification
area: security
tags: [security, webhooks, hmac, signatures, replay, api]
detect: []
related: [crypto-usage, ssrf, rate-limiting, csrf, secrets-management]
---
Webhooks: verify an HMAC over the raw body in constant time, reject stale timestamps, dedupe event ids, and respond fast.

## Verify
- `pytest -q tests/security/test_webhooks.py`: tampered, unsigned, stale and replayed requests are refused.
- `curl -s -o /dev/null -w "%{http_code}\n" -X POST localhost:8000/webhooks/provider -d '{"id":"evt_1"}'`: an unsigned request returns 401 or 400.
- `grep -rnE "(signature|digest).*==|==.*(signature|digest)" src/`: no plain equality on signatures.

## Test first
```python
import hmac, hashlib, time, json
def sign(body: bytes, ts: int, secret=b"whsec_test"):
    return hmac.new(secret, f"{ts}.".encode() + body, hashlib.sha256).hexdigest()

def test_unsigned_and_tampered_are_rejected(client):
    body = json.dumps({"id": "evt_1"}).encode()
    ts = int(time.time())
    assert client.post("/webhooks/p", data=body).status_code == 401
    r = client.post("/webhooks/p", data=body + b" ",
                    headers={"X-Timestamp": str(ts), "X-Signature": sign(body, ts)})
    assert r.status_code == 401

def test_old_timestamp_and_replay_are_rejected(client):
    body = b'{"id":"evt_2"}'
    old = int(time.time()) - 3600
    r = client.post("/webhooks/p", data=body,
                    headers={"X-Timestamp": str(old), "X-Signature": sign(body, old)})
    assert r.status_code == 401
```

## Do
- Read the raw request bytes before any JSON parsing, and compute `HMAC-SHA256(secret, timestamp + "." + raw_body)` in the format the provider documents.
- Compare with `hmac.compare_digest`, `crypto.timingSafeEqual` or `hmac.Equal`.
- Reject timestamps outside a window of a few minutes, to block replays of captured requests.
- Store processed event ids (unique constraint) and make handlers idempotent, so retries and replays are harmless.
- Prefer the provider's official verification helper from its SDK when one exists.
- Keep the signing secret in the secret store, one per endpoint, and support two active secrets during rotation.
- Return 2xx quickly and process asynchronously through a queue, and use `401` or `400` for bad signatures without detail.
- Exempt only the webhook route from CSRF and session checks, and apply rate limits to it.

## Avoid
- Verifying a re-serialized JSON body: whitespace and key order change the digest, so you either fail good requests or invite hacks. Use the raw bytes.
- `signature == expected`: a timing side channel. Use constant-time compare.
- Skipping verification "in staging" with an environment flag that leaks to production: use test secrets, not a bypass.
- Trusting the payload's own fields (account id, amount) without verifying the signature first: parse after verification.
- Ignoring timestamps: a captured valid request can be replayed forever. Enforce the window and event-id dedupe.
- Returning detailed verification errors: they help attackers tune forgeries. Return a plain 401.
- Using a shared secret across all customers or environments: one leak breaks all. Scope per endpoint.

## Review
- [ ] Raw body is used and signature compare is constant-time.
- [ ] Timestamp window and event-id dedupe are enforced.
- [ ] Handlers are idempotent and respond quickly.
- [ ] Secrets are stored securely and rotatable.
- [ ] Tests cover unsigned, tampered, stale and replayed requests.
