---
name: asyncio
title: asyncio
area: python
tags: [python, async, asyncio, concurrency, tasks, event-loop]
detect: [ext:.py]
related: [aiohttp, httpx, pytest, fastapi]
---
asyncio: coroutines, tasks, `TaskGroup`, timeouts, cancellation, and mixing blocking code with the event loop.

## Verify
- `python -X dev script.py`: debug mode warns about never-awaited coroutines, slow callbacks and unclosed resources.
- `python -W error -X dev -m pytest -q`: those warnings fail tests.
- `pytest -q`: async tests, with pytest-asyncio or anyio installed.
- `python -c "import asyncio; print(asyncio.TaskGroup)"`: `TaskGroup` and `asyncio.timeout` exist (3.11 and newer).

## Test first
Mark async tests and bound them with a timeout so a hang fails.
```python
import asyncio, pytest
from app.fetch import fetch_all

@pytest.mark.asyncio
async def test_fetch_all_cancels_siblings_on_error(fake_client):
    with pytest.raises(ExceptionGroup):
        async with asyncio.timeout(2):
            await fetch_all(fake_client, ["ok", "boom"])
```
Use `@pytest.mark.anyio` instead when the project uses anyio.

## Do
- Start the loop once at the top with `asyncio.run(main())`.
- Run concurrent work in `async with asyncio.TaskGroup() as tg: tg.create_task(...)`; handle failures with `except*`.
- Bound waits with `async with asyncio.timeout(seconds):`.
- Limit concurrency with `asyncio.Semaphore(n)` around outbound calls.
- Push blocking or CPU work off the loop with `await asyncio.to_thread(fn, ...)` or a process pool.
- Keep a reference to every task you create with `create_task`, and cancel and await them on shutdown.
- Re-raise `asyncio.CancelledError` after cleanup; use `try/finally` for resources.
- Share state with `asyncio.Queue` and `asyncio.Lock` rather than globals.

## Avoid
- Calling a coroutine without `await`: it never runs ("coroutine was never awaited"). Await it or schedule it.
- Fire-and-forget `asyncio.create_task(...)` with no stored reference: the task can be garbage-collected mid-run. Keep it in a set.
- `time.sleep`, `requests`, sync DB or file-heavy calls inside `async def`: they freeze all tasks. Use `asyncio.sleep` or `to_thread`.
- `asyncio.run()` inside a running loop (notebooks, handlers): `RuntimeError`. `await` instead, or use a thread.
- `asyncio.get_event_loop()` to start a loop, and `loop.run_until_complete` in new code: deprecated paths. Use `asyncio.run`.
- `gather(...)` without `return_exceptions` and no cleanup: a failure leaves siblings running. Use `TaskGroup`.
- Swallowing `CancelledError` with a bare `except:` or `except Exception` on old Python: shutdown hangs.

## Review
- [ ] Every created task is awaited, cancelled or tracked; none are orphaned.
- [ ] Every external wait has a timeout and concurrency is bounded.
- [ ] No blocking calls on the loop; blocking work uses `to_thread`.
- [ ] `CancelledError` propagates and cleanup is in `finally`.
- [ ] Tests run in dev mode with warnings as errors.
