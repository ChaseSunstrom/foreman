---
name: rate-limiter-algorithms
title: Rate limiter algorithms
area: design
tags: [rate-limiting, token-bucket, sliding-window, throttling, redis, api]
detect: []
related: [backpressure, api-gateway-pattern, bulkheads, idempotency, timeouts]
---
Pick token bucket, leaky bucket, fixed window or sliding window deliberately, and make the check-and-decrement atomic.

## Verify
- `pytest -q -k limiter`: burst, refill and boundary tests with a fake clock.
- `go test -race -count=1 ./...`: concurrent callers cannot exceed the limit (Go stacks).
- `git grep -nE "time\.(time|monotonic)\(\)|time\.Now\(\)" -- src/limiter`: the limiter takes an injected clock, not a hidden one.

## Test first
Pin burst size and refill with a fake clock; then hammer from threads.
```python
def test_token_bucket_burst_then_refill(clock):
    rl = TokenBucket(rate=1, burst=3, clock=clock)   # 1 token/s, capacity 3
    assert [rl.allow("k") for _ in range(4)] == [True, True, True, False]
    clock.advance(2)
    assert [rl.allow("k") for _ in range(3)] == [True, True, False]

def test_never_exceeds_limit_concurrently(clock):
    rl = TokenBucket(rate=0, burst=50, clock=clock)
    with ThreadPoolExecutor(16) as ex:
        ok = sum(ex.map(lambda _: rl.allow("k"), range(500)))
    assert ok == 50
```

## Do
- Token bucket: allows bursts, steady rate; the default for APIs. Leaky bucket: smooths output. Sliding window: accurate, costs more. Fixed window: cheap, but allows 2x at boundaries.
- Key by the right identity (API key, user, tenant, IP as last resort) and add a global ceiling.
- Make read-modify-write atomic: a lock in process, a Lua script or atomic command in Redis. Never get then set.
- Store tokens plus last-refill timestamp and compute refill lazily; no timer per key.
- Return 429 with `Retry-After`, and `RateLimit` style headers if you publish limits.
- Decide fail-open or fail-closed when the store is down, and test it.
- Expire idle keys.

## Avoid
- Non-atomic get/set in a shared store: concurrent requests overshoot. Use a script or atomic increment.
- Fixed window only: bursts at the edge double the limit. Use sliding or token bucket.
- Trusting `X-Forwarded-For` blindly: spoofable. Use the trusted proxy hop.
- Per-instance limits behind a load balancer: limit is multiplied by N. Share state or divide the limit.
- Unbounded key cardinality: memory leak. Set TTLs.

## Review
- [ ] Algorithm chosen and the burst behaviour documented.
- [ ] Check-and-decrement is atomic.
- [ ] Store-outage behaviour decided and tested.
- [ ] 429 carries `Retry-After`.
