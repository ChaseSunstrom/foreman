---
name: retries-backoff
title: Retries and backoff
area: design
tags: [retries, backoff, jitter, timeouts, circuit-breaker, resilience]
detect: [dep:tenacity, dep:backoff, dep:retry, dep:p-retry, dep:cenkalti/backoff, dep:resilience4j-retry, dep:polly, dep:Polly, dep:failsafe]
related: [idempotency, error-handling, microservices, background-jobs, websockets]
---
Bounded retries with exponential backoff and jitter, only for transient and idempotent failures, inside an overall deadline.

## Verify
- `pytest -q tests/resilience`: retry counts, delays and give-up behavior are asserted with a fake clock.
- `grep -rnE "while True:|for \{" src | grep -i retry`: hand-rolled unbounded retry loops are visible (review each).
- `grep -rn "timeout" src/clients | wc -l`: every outbound client sets timeouts (compare with the client count).

## Test first
Inject a flaky dependency and a fake sleeper, and assert attempts, delays and the final error.
```python
def test_retries_transient_then_succeeds(sleeps):
    calls = iter([TimeoutError, TimeoutError, "ok"])
    def op():
        v = next(calls)
        if isinstance(v, type): raise v()
        return v
    assert call_with_retry(op, attempts=4, base=0.1, sleep=sleeps.append) == "ok"
    assert len(sleeps) == 2 and all(0 <= s <= 0.4 for s in sleeps)

def test_does_not_retry_validation_error():
    with pytest.raises(ValueError):
        call_with_retry(lambda: (_ for _ in ()).throw(ValueError()), attempts=4)
```

## Do
- Retry only transient failures: timeouts, connection resets, 429, 502, 503, 504. Respect `Retry-After`.
- Retry only idempotent operations, or those protected by an idempotency key.
- Use exponential backoff with full jitter: `sleep = random(0, min(cap, base * 2**attempt))`.
- Cap attempts (3-5) and the total elapsed time, and fit the retries inside the caller's deadline.
- Set connect and read timeouts on every call, since retries multiply the wait.
- Add a circuit breaker or concurrency limit for a dependency that keeps failing, so you stop sending traffic.
- Retry at one layer only (usually the outermost client), not at each layer of the stack.
- Record attempts, the final error and the retry reason in logs and metrics.

## Avoid
- Retrying on every exception: 400s, auth failures and bugs will never succeed. Whitelist transient errors.
- Fixed-interval or no-delay retries: synchronized clients create a retry storm. Use jittered exponential backoff.
- Unlimited attempts: one dead dependency holds workers forever. Cap count and total time.
- Retrying non-idempotent writes without a key: duplicate charges or records. Add an idempotency key first.
- Stacked retries (client x SDK x gateway): 3 x 3 x 3 = 27 requests. Retry in one place and disable the others.
- Retrying inside a transaction or while holding a lock: it extends contention. Retry outside it.
- `time.sleep` in async code: it blocks the loop. Use `await asyncio.sleep`.

## Review
- [ ] Only listed transient errors are retried, and idempotency is confirmed.
- [ ] Backoff has jitter, a cap on attempts and a total deadline.
- [ ] Every outbound call has its own timeout.
- [ ] There is exactly one retrying layer per call path.
- [ ] Tests use a fake clock, with no real sleeps.
