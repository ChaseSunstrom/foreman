---
name: timeouts
title: Timeouts and deadlines
area: design
tags: [timeouts, deadlines, resilience, networking, cancellation, latency]
detect: []
related: [retries-backoff, circuit-breaker, bulkheads, backpressure, health-checks]
---
Every network or lock wait has an explicit timeout, and a request-level deadline shrinks as it travels downstream.

## Verify
- `pytest -q -k timeout`: slow-dependency tests finish within bound.
- `git grep -nE "requests\.(get|post|put|delete)\(" -- src | grep -v timeout`: calls without a timeout argument.
- `curl --max-time 2 -sS URL`: manual probe that a slow endpoint is cut off.

## Test first
A hung dependency must fail within the budget and release resources.
```python
def test_call_fails_within_deadline_and_cleans_up(slow_server):
    slow_server.delay = 30
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        fetch_profile("u1", deadline=0.5)
    assert time.monotonic() - start < 1.0
    assert slow_server.open_connections == 0

def test_downstream_gets_remaining_budget(spy):
    handle(request(deadline=1.0))
    assert spy.downstream_timeout <= 0.8      # parent budget minus work done so far
```

## Do
- Set connect, read and total timeouts separately on every HTTP client, DB driver, queue client and lock acquisition. Libraries often default to none.
- Propagate a deadline (absolute time or remaining budget) via context or headers (`context.Context` in Go, gRPC deadlines); each hop uses what remains.
- Choose values from observed latency: just above p99 for the dependency, under the caller's own timeout. Outer timeouts must exceed inner ones times attempts.
- Cancel the underlying work on timeout (close the request, cancel the task) so it does not keep consuming resources.
- Budget retries inside the deadline: attempts times timeout plus backoff must fit.
- Set DB statement and lock timeouts (`statement_timeout`, `lock_timeout` in Postgres).
- Surface timeouts as distinct, retryable errors (504 or 503) and metric them.

## Avoid
- No timeout on `requests`, `fetch`, `http.Client{}`: one hung peer stalls a worker forever. Set them explicitly.
- Same timeout at every layer: the outer fires first and the inner work continues. Make them nested and shrinking.
- Timing out without cancelling: zombie work. Propagate cancellation.
- Retrying on timeout against a non-idempotent call: duplicates. Use idempotency keys.
- Huge timeouts "to be safe": they hold connections through an outage. Keep them tight.

## Review
- [ ] Every remote call and lock wait has a timeout.
- [ ] Deadline propagates and shrinks per hop.
- [ ] Cancellation actually frees resources.
- [ ] Retry budget fits within the deadline.
