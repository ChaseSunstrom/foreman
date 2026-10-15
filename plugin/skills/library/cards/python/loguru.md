---
name: loguru
title: Loguru
area: python
tags: [python, logging, observability, structured, debugging, stdlib]
detect: [dep:loguru]
related: [pytest, fastapi, asyncio]
---
Loguru: one global logger with sinks, lazy formatting, bound context and exception capture.

## Verify
- `python -c "from loguru import logger; logger.info('ok {}', 1)"`: the logger works and prints to stderr.
- `pytest -q`: tests that capture logs through a sink or `caplog` bridge.
- `grep -rn "logger.add(" src`: sinks are configured in one place only.

## Test first
Loguru bypasses stdlib logging, so capture with a sink.
```python
import pytest
from loguru import logger
from app.jobs import run

@pytest.fixture
def logs():
    out = []
    hid = logger.add(out.append, format="{level}|{message}", level="DEBUG")
    yield out
    logger.remove(hid)

def test_failure_is_logged_at_error(logs):
    run(bad=True)
    assert any(m.startswith("ERROR|") for m in logs)
```
Stdlib `caplog` sees nothing unless you add a propagating sink: `logger.add(PropagateHandler(), format="{message}")`.

## Do
- Configure once at startup: `logger.remove()` then `logger.add(sys.stderr, level="INFO")`. Libraries should not call `add`.
- Use brace formatting with args: `logger.info("user {} paid {}", uid, amt)`. Do not pre-format with f-strings.
- Add context with `logger.bind(request_id=rid)` or `with logger.contextualize(request_id=rid):`, and show it with `{extra[request_id]}` in the format.
- Log exceptions with `logger.exception("failed")` inside `except`, or decorate with `@logger.catch`.
- Write files with rotation: `logger.add("app.log", rotation="10 MB", retention="7 days", compression="zip")`.
- Use `serialize=True` for JSON lines output.
- Use `enqueue=True` for multiprocess or async-safe file sinks.
- Use `logger.opt(lazy=True).debug("x {}", lambda: expensive())` for costly values.
- Route stdlib logging into loguru with an `InterceptHandler` registered through `logging.basicConfig(handlers=[...], level=0)`.

## Avoid
- Logging secrets or full request bodies: they land in files. Redact before binding.
- `diagnose=True` in production sinks: tracebacks print variable values, leaking secrets. Set `diagnose=False`, `backtrace=False`.
- f-strings in log calls: formats even when filtered, and braces in data raise `KeyError`. Use `{}` placeholders with args.
- Adding a sink at import time in library code or per request: duplicate lines. Configure once in the entry point.
- Forgetting `logger.remove(id)` in tests: handlers pile up. Remove in teardown.
- `enqueue=False` file sinks shared across processes: interleaved or lost writes. Use `enqueue=True`.

## Review
- [ ] One configuration site with levels from settings.
- [ ] No secrets in messages or `extra`, and `diagnose` is off outside development.
- [ ] Request or job context is bound, not re-passed by hand.
- [ ] File sinks have rotation and retention.
