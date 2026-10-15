---
name: bulkheads
title: Bulkheads
area: design
tags: [resilience, isolation, bulkhead, concurrency, pools, fault-tolerance]
detect: []
related: [circuit-breaker, backpressure, timeouts, rate-limiter-algorithms, concurrency]
---
Give each dependency or tenant its own bounded pool so one slow consumer cannot exhaust shared threads, connections or memory.

## Verify
- `pytest -q -k bulkhead`: saturating one pool leaves the other serving.
- `go test -race -count=1 ./...`: semaphores and counters are race free (Go stacks).
- `git grep -nE "Semaphore|ThreadPoolExecutor|max_connections|MaxOpenConns" -- src`: each pool has an explicit size.

## Test first
Saturate one compartment and prove the other still answers, and that overflow is rejected fast.
```python
def test_slow_dependency_does_not_starve_others():
    bh = {"search": Bulkhead(max_concurrent=2, queue=0),
          "billing": Bulkhead(max_concurrent=2, queue=0)}
    release = threading.Event()
    for _ in range(2):
        bh["search"].submit(release.wait)          # hold both slots
    with pytest.raises(BulkheadFull):
        bh["search"].submit(lambda: 1)             # rejected, not queued
    assert bh["billing"].submit(lambda: 42).result(1) == 42
    release.set()
```

## Do
- Size each compartment from measured latency and target throughput (concurrency is roughly rate times latency); document the number.
- Prefer a semaphore with a short or zero queue and fail-fast rejection over unbounded queues.
- Separate pools per downstream service, per priority class, and per tenant tier. Keep health checks and admin endpoints on their own pool.
- Use separate DB or HTTP connection pools where one dependency is much slower.
- Expose in-use, queued and rejected counts as metrics.
- Combine with timeouts so slots are always released.

## Avoid
- One shared executor for all outbound calls: one slow API blocks everything. Split by dependency.
- Unbounded queues in front of a pool: they convert overload into latency and memory growth. Bound and reject.
- Slots held without a timeout: a hang leaks capacity. Wrap in a deadline and release in `finally`.
- Pools sized by guess: record the sizing basis and revisit.
- Rejecting without telling callers: return a retryable 503 with `Retry-After` where appropriate.

## Review
- [ ] Every outbound dependency has its own bounded pool.
- [ ] Overflow rejects fast with a defined error.
- [ ] Release happens in `finally`, with timeouts.
- [ ] Rejections and saturation are measured.
