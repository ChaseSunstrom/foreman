---
name: pytest-asyncio
title: pytest-asyncio
area: python
tags: [python, testing, asyncio, pytest, fixtures, event-loop]
detect: [dep:pytest-asyncio]
related: [pytest, asyncio, httpx, fastapi, pytest-mock]
---
pytest-asyncio: run coroutine tests and async fixtures on a managed event loop, with explicit mode and loop scope.

## Verify
- `pytest -q`: async tests run (an un-run coroutine shows as a skipped or warned test).
- `pytest -q -W error::RuntimeWarning`: "coroutine was never awaited" becomes a failure.
- `pytest --collect-only -q`: async tests are collected under the expected names.
- `pytest -q -p no:randomly -x`: ordering-independent failures stand out when you bisect.

## Test first
Set the mode once in `pyproject.toml` under `[tool.pytest.ini_options]`: `asyncio_mode = "auto"`. Then:
```python
import asyncio
import pytest

@pytest.fixture
async def queue():
    q = asyncio.Queue()
    yield q

async def test_get_times_out(queue):
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(queue.get(), timeout=0.05)
```
In `strict` mode (the default) mark tests with `@pytest.mark.asyncio` and fixtures with `@pytest_asyncio.fixture`.

## Do
- Pick the mode deliberately: `asyncio_mode = "auto"` for async-only suites, `strict` when mixing with anyio or other plugins.
- Declare async fixtures with `@pytest_asyncio.fixture` in strict mode.
- Share a loop with `@pytest.mark.asyncio(loop_scope="module")` and `@pytest_asyncio.fixture(loop_scope="module")`. Set the default with `asyncio_default_fixture_loop_scope = "function"` in the ini options.
- Use `async with` and `yield` in fixtures so connections and clients close on teardown.
- Bound waits with `asyncio.wait_for` or `asyncio.timeout` so a hang fails fast.
- Drive ASGI apps with `httpx.AsyncClient(transport=ASGITransport(app=app))`.
- Patch coroutines with `AsyncMock`, and assert with `assert_awaited_once_with`.

## Avoid
- Overriding the `event_loop` fixture: removed in recent releases. Use `loop_scope` and `asyncio_default_fixture_loop_scope`.
- An `async def` test with no marker in strict mode: it never runs and warns. Add the marker or enable auto mode.
- A session-scoped async fixture with function-loop tests: "attached to a different loop" errors. Match the `loop_scope` values.
- `asyncio.run()` inside a test: fails under a running loop. `await` the coroutine.
- `time.sleep` or sync I/O in async tests: blocks the loop. Use `asyncio.sleep` and async clients.
- Leaving tasks pending at test end: warnings and leaks. Await or cancel them in teardown.

## Review
- [ ] `asyncio_mode` and default loop scope are set in config.
- [ ] Every async fixture releases its resources after `yield`.
- [ ] No test relies on shared loop state it did not declare.
- [ ] Waits have timeouts and no real sleeps stand in for synchronization.
