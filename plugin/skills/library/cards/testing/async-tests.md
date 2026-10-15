---
name: async-tests
title: Async tests
area: testing
tags: [testing, async, promises, await, events, timeouts, flaky]
detect: []
related: [flaky-tests, time-in-tests, concurrency-tests, http-mocking]
---
Test asynchronous code by awaiting completion or a condition, never by sleeping, and make every missed await fail loudly.

## Verify
- `pytest -q` with `pytest-asyncio` or `anyio` marks: coroutine tests actually run (a skipped-coroutine warning means they did not).
- `pytest -W error::RuntimeWarning -q`: a never-awaited coroutine fails the run.
- `npx jest --detectOpenHandles`: leaked timers or sockets after tests are reported (Jest).
- `go test -race -count=20 ./...`: repeated, race-checked runs expose timing-dependent failures (Go).

## Test first
Await the result and assert the failure path, with a bounded timeout.
```python
import asyncio, pytest

@pytest.mark.anyio
async def test_fetch_times_out():
    async def slow(): await asyncio.sleep(10)
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow(), timeout=0.05)
```
```js
test("rejects on bad input", async () => {
  await expect(load("")).rejects.toThrow("empty");
});
```

## Do
- Declare the test async and `await` the call, or `return` the promise; use `await expect(p).rejects` for errors.
- Wait for a condition: `waitFor`, `vi.waitFor`, `asyncio.Event`, `Eventually` with a timeout and short poll, not a fixed sleep.
- Use fake timers or a fake clock for timeouts, retries and debounce, and flush pending promises after advancing.
- Put a timeout on every wait so a hang fails in seconds instead of stalling CI.
- Await cleanup (closing servers, cancelling tasks) in teardown; assert no tasks remain pending.
- Use channels, `sync.WaitGroup` or an event signal to wait for goroutines or callbacks to finish (Go).
- Test cancellation and error propagation, not only the happy path.

## Avoid
- `sleep(1)` to let background work finish: slow and racy. Wait on the event or condition.
- Forgetting `await`: the test passes before the assertion runs. Enable the unawaited-coroutine warnings as errors and lint for floating promises.
- Callback-style tests without `done` or a returned promise: they end early. Wrap in a promise.
- Unbounded waits: a bug hangs CI. Always give a timeout.
- Shared event loop state or tasks left running between tests: bleed-through. Isolate and cancel in teardown.
- Mixing real timers with fake timers mid-test: confusing hangs. Choose one.

## Review
- [ ] Every async call in a test is awaited or returned.
- [ ] No fixed sleeps; conditional waits have timeouts.
- [ ] Rejection, timeout and cancellation paths are tested.
- [ ] Teardown awaits cleanup; no leaked tasks or handles.
- [ ] Unawaited-coroutine warnings are errors.
