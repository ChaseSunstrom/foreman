---
name: circuit-breaker
title: Circuit breaker
area: design
tags: [resilience, circuit-breaker, fault-tolerance, timeouts, fallback, dependencies]
detect: []
related: [timeouts, retries-backoff, bulkheads, backpressure, health-checks]
---
Stop calling a failing dependency after a failure threshold, fail fast, and probe for recovery with a half-open state.

## Verify
- `pytest -q -k breaker`: transitions and probe behaviour.
- `go test -race -count=1 ./...`: the state machine is safe under concurrent callers (Go stacks).
- `git grep -nE "requests\.(get|post)|http\.Get\(" -- src`: remote calls go through the breaker wrapper.

## Test first
Drive the breaker with a fake clock and a failing callee. Assert the call count, not just the error.
```python
def test_opens_then_half_open_probe(clock):
    calls = []
    def boom(): calls.append(1); raise IOError
    cb = Breaker(failures=3, reset_after=30, clock=clock)
    for _ in range(3):
        with pytest.raises(IOError): cb.call(boom)
    with pytest.raises(CircuitOpen): cb.call(boom)
    assert len(calls) == 3                 # open: callee not touched
    clock.advance(31)
    with pytest.raises(IOError): cb.call(boom)   # one probe
    with pytest.raises(CircuitOpen): cb.call(boom)
    assert len(calls) == 4
```

## Do
- States: closed, open, half-open. Trip on consecutive failures or an error rate over a window with a minimum request count.
- Count timeouts and 5xx as failures. Do not count 4xx caller errors.
- Allow one (or few) probe in half-open; success closes, failure reopens with the timer reset.
- One breaker per dependency (or per host), not one global.
- Pair with a timeout on every call and a defined fallback: cached value, default, or a clear error.
- Emit state-change metrics and logs.

## Avoid
- Breaker without a timeout: hung calls never count as failures. Add a per-call timeout.
- Retrying inside an open breaker, or retries outside it that hammer: retry inside, breaker outside, honouring `CircuitOpen`.
- Tripping on tiny samples (1 of 2): require a minimum volume.
- Letting every request probe in half-open: a thundering herd. Limit probes.
- Wall-clock time in tests: inject a clock.

## Review
- [ ] Per-dependency breaker with timeout.
- [ ] 4xx not counted as failure.
- [ ] Half-open admits limited probes.
- [ ] Open state returns a deliberate fallback or error.
- [ ] State changes are observable.
