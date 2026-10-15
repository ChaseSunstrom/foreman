---
name: freezegun
title: freezegun
area: python
tags: [python, testing, time, datetime, mocking, pytest]
detect: [dep:freezegun, dep:time-machine, dep:pytest-freezer]
related: [pytest, pytest-mock, factory-boy, asyncio]
---
freezegun: freeze or step the clock in tests so time-based logic is deterministic. time-machine is the faster alternative.

## Verify
- `pytest -q`: time-dependent tests pass at any wall-clock time.
- `faketime '2030-01-01 00:00:00' pytest -q` (libfaketime, if installed): the suite does not depend on the real date.
- `pytest -q -k expir`: iterate on the time-sensitive tests.

## Test first
```python
from datetime import datetime, timedelta
from freezegun import freeze_time
from app.tokens import issue, is_valid

def test_token_expires_after_one_hour():
    with freeze_time("2024-03-01 12:00:00") as clock:
        t = issue(ttl=timedelta(hours=1))
        clock.tick(timedelta(minutes=59))
        assert is_valid(t)
        clock.tick(timedelta(minutes=2))
        assert not is_valid(t)
```

## Do
- Use the decorator or context manager: `@freeze_time("2024-03-01")` or `with freeze_time(...) as clock`. Move time with `clock.tick(delta)` or `clock.move_to(...)`.
- Use `auto_tick_seconds=1` when code loops on the clock.
- Code under test should read time through `datetime.now(timezone.utc)` and not cache it at import.
- Freeze in UTC and pass aware datetimes. Test the timezone path with an explicit `tz_offset=`.
- Prefer injecting a clock parameter in new code and use freezegun for legacy code.
- For async and speed, `time-machine` (`time_machine.travel(dt, tick=False)`) patches at the C level and is much faster on big suites.
- Add `ignore=["sqlalchemy"]` (a module list) when a library breaks under frozen time. Set `freezegun.configure(extend_ignore_list=[...])` once in `conftest.py`.

## Avoid
- `from datetime import datetime` in a module imported before freezing and then expecting the class to be patched everywhere: freezegun patches module attributes it finds, but values stored earlier (`default=datetime.now()` evaluated at import) stay real. Call `now()` at use time.
- Freezing inside a fixture shared by many tests without stopping: leaks the date to later tests. Use a context manager or yield and `stop()`.
- Frozen time with real network or DB timeouts: sockets and connection pools wait forever. Narrow the frozen block.
- Comparing naive and aware datetimes after freezing: `TypeError`. Use aware values throughout.
- Using `time.sleep` in a frozen test to move time: it returns at once. Use `tick`.
- Asserting on `datetime.now()` equality from two calls without `tick` semantics: frozen time makes them equal, which can hide ordering bugs.

## Review
- [ ] No test depends on the real current date or `sleep`.
- [ ] Freeze scope is narrow and cleaned up.
- [ ] Naive and aware datetimes are not mixed.
- [ ] Code reads the clock at call time, not import time.
