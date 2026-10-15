---
name: test-sharding
title: Test sharding and parallelism
area: testing
tags: [sharding, parallel, ci, xdist, timing, isolation]
detect: [dep:pytest-xdist, dep:pytest-split, dep:knapsack, dep:parallel_tests, file:.github/workflows/*.yml]
related: [flaky-tests, e2e-strategy, integration-testing, coverage]
---
Split a suite across workers or CI machines using timing data, which only works if tests are isolated and results merge afterward.

## Verify
- `pytest -n auto -q`: runs in parallel with xdist; compare results with the serial run.
- `npx playwright test --shard=1/4`: runs one quarter of the Playwright suite.
- `npx jest --shard=1/3`: runs one third of a Jest suite.
- `go test -p 4 -parallel 4 ./...`: package and test parallelism in Go.

## Test first
Isolation is the failing check: run the suite in parallel and shuffled; any failure is shared state.
```python
@pytest.fixture
def db_name(worker_id):            # xdist fixture: "gw0", "gw1" or "master"
    return f"test_{worker_id}"
def test_users_table_is_private_to_worker(db_name):
    conn = connect(db_name)
    assert conn.execute("select count(*) from users").scalar() == 0
```
Config lives in `pytest.ini`/`pyproject.toml`, `playwright.config.*` or the CI workflow matrix.

## Do
- Make every test independent first; sharding exposes order and shared-state bugs.
- Give each worker its own database or schema, temp directory, and port (bind to port 0).
- Balance shards by recorded duration (pytest-split, Playwright and CI timing), not file count.
- Use a CI matrix with `fail-fast: false` so one shard failing does not hide others.
- Merge coverage and test reports from all shards before gating (Playwright `blob` reporter then `merge-reports`).
- Mark inherently serial tests and run them in a separate job.
- Keep per-shard setup cached (dependencies, browsers, build artifacts).

## Avoid
- Sharding before fixing shared state: new random failures. Isolate then shard.
- Splitting by file count with uneven durations: one slow shard sets the total time. Split by timing.
- Per-shard coverage thresholds: each looks low. Merge, then check.
- Shared database or fixed ports across workers: collisions. Use per-worker resources.
- `fail-fast` on the CI matrix: first failure cancels others, hiding extra failures. Disable it.
- Assuming a shard order: tests relying on another file's side effects break. Remove the dependency.

## Review
- [ ] Suite passes serially, in parallel and shuffled.
- [ ] Each worker owns its database, directories and ports.
- [ ] Shards are balanced from timing data.
- [ ] Reports and coverage merge before gating.
- [ ] Serial-only tests are isolated into their own job.
