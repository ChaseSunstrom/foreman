---
name: tenacity
title: tenacity
area: python
tags: [python, retry, backoff, resilience, async, reliability]
detect: [dep:tenacity]
related: [httpx, asyncio, pytest-mock, celery]
---
tenacity: declarative retries with stop, wait and retry conditions, for sync and async code.

## Verify
- `pytest -q`: retry behaviour tests with the sleep patched out.
- `ruff check .`: unused imports and bare excepts near retried code.
- `python -c "import tenacity; print(tenacity.__name__)"`: the library resolves (not the unrelated `retrying`).

## Test first
Patch the waiting so tests are instant, then count attempts.
```python
import pytest
from tenacity import retry, stop_after_attempt, wait_none, retry_if_exception_type

calls = {"n": 0}

@retry(stop=stop_after_attempt(3), wait=wait_none(), retry=retry_if_exception_type(ConnectionError), reraise=True)
def flaky():
    calls["n"] += 1
    raise ConnectionError

def test_gives_up_after_three():
    with pytest.raises(ConnectionError):
        flaky()
    assert calls["n"] == 3
```
In real code, inspect `fn.retry.statistics`, and swap the waiter in tests with `fn.retry_with(wait=wait_none())`.

## Do
- Always bound retries: `stop=stop_after_attempt(5) | stop_after_delay(30)`.
- Use `wait=wait_exponential(multiplier=0.5, max=10) + wait_random(0, 1)`, or `wait_random_exponential(multiplier=1, max=60)`, so clients do not retry in lockstep.
- Retry only transient failures: `retry=retry_if_exception_type((httpx.TransportError, TimeoutError))`, or `retry_if_exception(predicate)` on status 429 and 5xx.
- Set `reraise=True` to raise the original exception rather than `RetryError`.
- Log with `before_sleep=before_sleep_log(logger, logging.WARNING)`.
- Use the same decorator on `async def`. Tenacity awaits with `asyncio.sleep`.
- Use `Retrying(...)` or `AsyncRetrying(...)` in a `for attempt in ...: with attempt:` loop to retry a block, not a function.
- Make retried operations idempotent or guard with an idempotency key.

## Avoid
- `@retry` with no arguments: retries forever, immediately, on every exception. Add stop, wait and a type filter.
- `retry_if_exception_type(Exception)` for everything: retries programming errors and bad input (4xx). Narrow it.
- Retrying non-idempotent writes (payments, sends): duplicates. Add idempotency keys or do not retry.
- Nested retries (client retry inside worker retry): multiplicative attempts. Retry at one layer.
- Real sleeps in tests: slow suites. Use `wait_none()` or patch `tenacity.nap.time.sleep`.
- Swallowing the final failure with `retry_error_callback` and returning a default silently: hides outages. Log or raise.

## Review
- [ ] Every retry has stop, wait with jitter and an exception filter.
- [ ] Retried calls are idempotent.
- [ ] Final failure surfaces with the original exception and a log line.
- [ ] Tests assert attempt counts without sleeping.
