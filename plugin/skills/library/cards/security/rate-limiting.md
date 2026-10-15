---
name: rate-limiting
title: Rate limiting and abuse control
area: security
tags: [security, rate-limit, throttling, brute-force, dos, api]
detect: [dep:slowapi, dep:flask-limiter, dep:express-rate-limit, dep:django-ratelimit, dep:rate-limiter-flexible, dep:github.com/ulule/limiter/v3, dep:@nestjs/throttler]
related: [password-hashing, sessions, authorization, ssrf, upload-security]
---
Rate limiting: throttle per account and per IP on login, reset, signup and expensive endpoints, with a shared store and a correct client identity.

## Verify
- `pytest -q tests/security/test_rate_limit.py`: the limit trips, returns 429 with `Retry-After`, and resets.
- `for i in $(seq 1 20); do curl -s -o /dev/null -w "%{http_code}\n" -X POST localhost:8000/login -d "u=a&p=b"; done | sort | uniq -c`: some responses are 429 after the limit.
- `curl -si -X POST localhost:8000/login -d "u=a&p=b" -H "X-Forwarded-For: 1.2.3.4" | head -1`: spoofing a forwarded header does not reset the count.

## Test first
```python
def test_login_is_throttled_per_account(client):
    codes = [client.post("/login", json={"email": "a@x.io", "password": f"bad{i}"}).status_code
             for i in range(12)]
    assert codes[-1] == 429

def test_limit_response_has_retry_after(client):
    for i in range(12):
        r = client.post("/login", json={"email": "b@x.io", "password": "bad"})
    assert r.status_code == 429 and "retry-after" in r.headers
```

## Do
- Key limits on the right identity: the account name or email for login, the authenticated user for APIs, the IP as an extra layer.
- Use stricter buckets for credential endpoints (login, reset, OTP verify, signup) than for reads.
- Store counters in Redis or the gateway so limits hold across processes and restarts.
- Return `429 Too Many Requests` with `Retry-After`, and the same body whether the account exists or not.
- Add exponential backoff or temporary lockout with a CAPTCHA step for repeated failures. Avoid permanent lockout, which becomes a denial-of-service tool.
- Get the client IP only from a proxy you trust (configure trusted proxy count or `X-Forwarded-For` parsing explicitly).
- Bound cost beyond request count: payload size, query complexity, pagination size, concurrent jobs.
- Limit at the edge (gateway or CDN) and again in the app for sensitive routes.

## Avoid
- In-memory counters in a multi-instance deploy: each process counts separately, so the real limit is multiplied. Use a shared store.
- Trusting `X-Forwarded-For` from the client: an attacker rotates it per request. Accept it only from your proxy.
- Limiting only by IP: botnets and NAT sharing both defeat it. Combine with an account key.
- Locking accounts permanently after N failures: attackers lock victims out. Use timed backoff.
- Different error messages for locked, unknown and wrong-password: they enumerate accounts. Return one response.
- Only fixed-window counters at the boundary: bursts of double the limit pass. Use sliding window or token bucket.
- Rate limiting after the expensive work (hashing, DB, third-party calls): put it first.

## Review
- [ ] Credential and expensive endpoints have their own limits.
- [ ] Counters are shared across instances.
- [ ] Client identity is derived safely.
- [ ] 429 includes `Retry-After` and leaks nothing about accounts.
- [ ] A test proves the limit trips.
