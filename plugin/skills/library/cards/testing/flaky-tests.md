---
name: flaky-tests
title: Flaky tests
area: testing
tags: [flaky, nondeterminism, retries, quarantine, race, ci]
detect: []
related: [e2e-strategy, integration-testing, test-sharding, unit-test-design]
---
A flaky test passes and fails on the same code; reproduce it, find the nondeterminism, fix the cause, and quarantine only as a short-term bridge.

## Verify
- `pytest -q --count=50 -x path::test` (pytest-repeat): a suspect test survives 50 repeats.
- `go test -run TestX -count=200 -race ./pkg`: repeated and race-detected in Go.
- `npx playwright test --repeat-each=20 spec.ts`: repeated browser runs.
- `pytest -q -p randomly` (pytest-randomly) or `go test -shuffle=on ./...`: order dependence shows up under shuffling.

## Test first
Make the failure deterministic before fixing: force the bad interleaving or time.
```python
def test_token_expires_exactly_at_boundary(fake_clock):
    t = issue_token(ttl=60, clock=fake_clock)
    fake_clock.advance(60)
    assert t.is_expired(clock=fake_clock)   # flaked on real clock ticks
```
A flaky test fix needs a reproducing loop run (repeat count plus seed) recorded in the task.

## Do
- Capture the seed, order, worker and logs of a failed run; rerun with the same seed and `-x`.
- Classify the cause: time, ordering, shared state, concurrency, network, resource limits, randomness.
- Inject a clock and seeded RNG; freeze time rather than sleeping.
- Replace sleeps with waits on an observable condition with a timeout.
- Isolate state per test: temp dirs, unique ports (bind to port 0), unique DB names.
- Run the race detector or thread sanitizer for concurrent code.
- Quarantine with a tracking issue and an owner and a deadline; keep running it so it is not forgotten.

## Avoid
- Blanket automatic retries: they hide real races and double CI time. Fix the cause; allow at most one retry and report it.
- `sleep` to "give it time": fails under load. Wait on the condition.
- Deleting the test: you lose the coverage and the bug remains. Quarantine and fix.
- Asserting unordered collections in order (sets, map iteration, parallel results): sort or compare as sets.
- Shared global state, singletons or env vars mutated across tests: reset in fixtures.
- Real network or external services in unit and integration tests: stub or contain them.

## Review
- [ ] Root cause is named, not "timing".
- [ ] The fix passes a high repeat count and shuffled order.
- [ ] No new sleep or retry was added to mask it.
- [ ] Quarantined tests have an owner and a deadline.
- [ ] Clock, RNG and ports are injected or isolated.
