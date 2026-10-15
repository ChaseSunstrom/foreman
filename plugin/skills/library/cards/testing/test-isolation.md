---
name: test-isolation
title: Test isolation
area: testing
tags: [testing, isolation, state, flaky, order, parallel, fixtures]
detect: []
related: [flaky-tests, test-fixtures, database-tests, test-sharding, unit-test-design]
---
Each test builds its own world and leaves none behind, so any test passes alone, in any order, and in parallel.

## Verify
- `pytest -p no:randomly path/to/test.py::test_name`: the single test passes alone (Python).
- `pytest -p randomly -q` (with pytest-randomly installed): random order still passes.
- `npx jest --randomize` (or `--runInBand` versus default): order and parallelism do not matter (Jest).
- `go test -shuffle=on -count=3 ./...`: shuffled, repeated runs pass (Go).
- `go test -race ./...`: no shared-memory races between tests.

## Test first
Reproduce the leak first: write the pair that fails only when run in order.
```python
_cache = {}

def test_a_populates():
    _cache["k"] = 1
    assert _cache["k"] == 1

def test_b_expects_clean():
    assert "k" not in _cache   # fails after test_a: shared module state
```
The fix is a fixture that creates and discards the state per test, then the pair passes in both orders.

## Do
- Create state in a fixture or setup function per test, with teardown that always runs.
- Give every test its own temp directory, database schema or transaction, and port (port 0 and read it back).
- Generate unique ids and names per test (a counter or UUID) so parallel tests never collide.
- Reset or inject singletons, caches, env vars and the clock; restore them in teardown.
- Keep fixtures function-scoped by default; widen scope only for immutable, expensive resources.
- Run the suite shuffled and in parallel in CI regularly to surface hidden coupling.
- Make each test assert only its own data, not totals over shared tables.

## Avoid
- Module-level mutable globals used by tests: order-dependent results. Build them in fixtures.
- A test that relies on another test's inserts: it fails alone. Arrange its data inside itself.
- Assertions like `count == 3` on a shared table: parallel runs break it. Filter by the test's own ids.
- Setting `os.environ` or monkeypatching without restore: leaks into later tests. Use `monkeypatch` or `t.Setenv`.
- Fixed ports and file names (`/tmp/out.txt`): collisions in parallel. Use temp dirs and ephemeral ports.
- Fixing flakiness with retries or `--runInBand`: the coupling stays. Find and remove the shared state.

## Review
- [ ] Each test passes alone, shuffled and in parallel.
- [ ] Setup and teardown are per test; teardown runs on failure.
- [ ] No fixed ports, paths, ids or shared tables.
- [ ] Globals, env and clock are restored.
- [ ] Assertions concern only the test's own data.
