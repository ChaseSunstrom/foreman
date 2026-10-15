---
name: coverage
title: Test coverage
area: testing
tags: [coverage, branch, thresholds, reports, ci, diff-coverage]
detect: [dep:coverage, dep:pytest-cov, dep:c8, dep:nyc, dep:istanbul, file:.coveragerc, file:codecov.yml, file:.nycrc*]
related: [mutation-testing, unit-test-design, test-pyramid, regression-tests]
---
Coverage shows which code never ran under test; use branch coverage and per-diff checks to find gaps, never as a measure of quality.

## Verify
- `pytest --cov=src --cov-branch --cov-report=term-missing`: branch coverage with missing line numbers.
- `go test -coverprofile=c.out ./... && go tool cover -func=c.out`: per-function coverage in Go.
- `npx vitest run --coverage` (or `npx jest --coverage`): JS/TS coverage report.
- `cargo llvm-cov --summary-only`: Rust coverage (needs cargo-llvm-cov).

## Test first
For an uncovered branch, write the test that drives it and asserts its outcome.
```python
# term-missing: payment.py 41-44 (declined card branch) uncovered
def test_declined_card_marks_order_failed(gateway):
    gateway.decline_next()
    order = checkout(cart(), gateway)
    assert order.status == "failed"
```
Coverage config lives in `.coveragerc`, `pyproject.toml`, `package.json` or `vitest.config.*`.

## Do
- Enable branch coverage; line coverage misses untaken `else` and short-circuit paths.
- Open the missing-lines report for changed files and write behavior tests for those lines.
- Enforce a floor in CI (`--cov-fail-under=N`, Jest `coverageThreshold`) and a diff-coverage rule for new code.
- Exclude generated code, vendor and boilerplate explicitly in config, with a reason.
- Merge coverage across parallel shards and test types before judging the number.
- Track the trend, and fail a PR that drops coverage substantially.
- Pair with mutation testing on critical code to check assertion strength.

## Avoid
- Writing assertion-free tests that only execute code to raise the number: coverage rises, protection does not. Assert outcomes.
- Targeting 100%: pushes tests of trivial lines and `# pragma: no cover` abuse. Set a floor, review gaps.
- Reading line coverage of a branch-heavy function as safe: enable branch mode.
- Excluding files to pass the gate: hides risk. Exclude only generated or vendored code.
- Measuring only unit tests and ignoring that integration tests cover wiring: merge reports.
- Per-shard thresholds: each shard looks low. Combine, then check.

## Review
- [ ] Branch coverage is on.
- [ ] Threshold and diff-coverage gates run in CI.
- [ ] Exclusions are listed with reasons.
- [ ] New tests assert outcomes, not just execution.
- [ ] Shard reports are merged before the gate.
