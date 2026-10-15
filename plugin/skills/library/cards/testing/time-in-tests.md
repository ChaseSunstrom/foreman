---
name: time-in-tests
title: Time in tests
area: testing
tags: [testing, time, clock, timezone, timers, flaky, determinism]
detect: []
related: [flaky-tests, async-tests, randomness-in-tests, test-isolation]
---
Make time an input: inject a clock, freeze or advance it in tests, pin the timezone, and never wait on the real one.

## Verify
- `TZ=UTC pytest -q && TZ=Pacific/Auckland pytest -q`: results do not depend on the machine's timezone.
- `TZ=America/Los_Angeles npx jest`: the same check for Jest.
- `TZ=Asia/Kolkata go test ./...`: Go suites under a half-hour-offset zone.
- `grep -rnE "sleep\(|Thread\.sleep|setTimeout\(" tests/`: finds real-time waits that should be a fake clock.

## Test first
Write the boundary case with a frozen clock, then make the code take the clock as input.
```python
from freezegun import freeze_time

@freeze_time("2024-03-10T01:59:59Z")
def test_token_expires_exactly_at_ttl():
    t = issue_token(ttl_seconds=1)
    assert not is_expired(t)
    with freeze_time("2024-03-10T02:00:00Z"):
        assert is_expired(t)
```
Jest equivalent: `jest.useFakeTimers().setSystemTime(new Date("2024-03-10T01:59:59Z"))`. Go: pass a `func() time.Time` or a clock interface.

## Do
- Inject `now` (a parameter, a clock object or a `func() time.Time`) so production code never calls the global clock in logic.
- Freeze time for point-in-time logic; advance fake timers (`jest.advanceTimersByTime`, `clock.tick`) for timeouts, retries and debounce.
- Test the boundaries: exactly at expiry, one tick before and after, midnight, month end, leap day, year rollover.
- Test DST transitions with real zone names, never fixed offsets: the skipped hour and the repeated hour.
- Store and compare instants in UTC; test the display conversion separately.
- Set the timezone explicitly in the test run (`TZ`) and run CI under a second zone.
- Restore real timers after each test (`useRealTimers`, context-manager freeze).

## Avoid
- `sleep(2)` to wait for expiry: slow and racy. Advance a fake clock.
- `datetime.now()` or `Date.now()` inside logic: untestable. Take the clock as a dependency.
- Asserting equality with the current time (`== now()`): flaky by milliseconds. Freeze, or assert within a delta.
- Tests that pass only in the developer's timezone: fix `TZ` and use zoned types.
- Fake timers left on after a test: later tests hang. Reset in teardown.
- Fake timers with real promises and I/O unadvanced: deadlock. Flush microtasks (`await jest.runAllTimersAsync()`).

## Review
- [ ] Production logic receives time as input.
- [ ] Boundary and DST cases are covered.
- [ ] The suite passes under at least two timezones.
- [ ] No real sleeps; timers restored in teardown.
- [ ] Instants are UTC internally.
