---
name: test-observability
title: Test observability
area: testing
tags: [testing, ci, reporting, flaky, junit, traces, diagnostics]
detect: []
related: [flaky-tests, test-sharding, e2e-strategy, coverage]
---
Make failures self-explanatory and suite health measurable: structured reports, artifacts on failure, flake and duration tracking.

## Verify
- `pytest -q --junitxml=out/junit.xml --durations=10`: a JUnit report for CI and the ten slowest tests (pytest).
- `npx jest --ci --reporters=default --reporters=jest-junit`: a machine-readable report (needs jest-junit).
- `go test -json ./... > out/test.json`: structured events per test for tooling (Go).
- `npx playwright test --trace on-first-retry`: a trace is captured for retried failures (Playwright).
- `ls out/`: the report and artifacts exist after a failing run.

## Test first
Prove the failure message is diagnosable by making a test fail on purpose and reading what CI would show.
```python
def test_order_total_mismatch_is_explained():
    order = place_order(items=[("pen", 2)], coupon="TENOFF")
    assert order.total == 18, (
        f"total={order.total} lines={order.lines} coupon={order.coupon_applied}"
    )
```
If the message needs a debugger to interpret, improve it before merging.

## Do
- Emit JUnit or JSON from every CI run and upload it as an artifact; publish the summary in the PR.
- Include context in assertion messages: inputs, actual and expected, relevant ids.
- Capture failure artifacts: screenshots, traces, videos, server logs, DB dumps, request and response bodies.
- Log the seed, the timezone, the commit sha and the environment at the start of the run.
- Track per-test duration and failure rate over time; list the slowest and the flakiest weekly.
- Tag flaky tests with an owner and a ticket, quarantine them to a separate non-blocking job, and set a deadline to fix.
- Correlate test runs with service logs through a request or test id header.
- Fail the build on tests that print errors to stderr only if that is the policy, and make that policy explicit.

## Avoid
- Retrying failures silently: flakes are hidden and trend upward. Record every retry as a signal.
- `assert x` with no message on complex state: a bare failure is a dead end. Add context or use richer assertions.
- Discarding artifacts when CI is green and when it is red: no way to debug. Keep failure artifacts at least.
- Quarantining forever: the suite loses coverage. Give each quarantine an owner and expiry.
- Ignoring duration drift: slow suites get skipped. Track and budget it.
- Printing secrets in test logs: leaks into CI artifacts. Redact tokens and keys.

## Review
- [ ] CI publishes a structured report and failure artifacts.
- [ ] Assertion messages carry context.
- [ ] Seed, timezone and sha are logged per run.
- [ ] Flaky tests have an owner and deadline.
- [ ] Durations and flake rates are tracked.
