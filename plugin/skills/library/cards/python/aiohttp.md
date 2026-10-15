---
name: aiohttp
title: aiohttp
area: python
tags: [python, async, http, client, server, websocket]
detect: [dep:aiohttp]
related: [asyncio, httpx, pytest, pydantic]
---
aiohttp as HTTP client (`ClientSession`) and as an async web server (`web.Application`, handlers, middlewares, websockets).

## Verify
- `pytest -q`: the suite; with `pytest-aiohttp` use its `aiohttp_client` fixture.
- `python -X dev -W error::ResourceWarning -m pytest -q`: unclosed sessions and connectors surface as errors.
- `python -c "import app.main"`: the app module imports and routes register.
- `ruff check . && pyright`: lint and types.

## Test first
Use `pytest-aiohttp`; the client drives the app in process.
```python
from aiohttp import web

async def hello(request):
    return web.json_response({"ok": True})

async def test_hello(aiohttp_client):
    app = web.Application()
    app.router.add_get("/", hello)
    client = await aiohttp_client(app)
    r = await client.get("/")
    assert r.status == 200 and await r.json() == {"ok": True}
```
Tests that mock outbound calls patch the session or use a local `aiohttp_server`.

## Do
- Create one `ClientSession` per app and share it; open it in `cleanup_ctx` and close it on shutdown.
- Set `aiohttp.ClientTimeout(total=..., connect=...)` on the session; the default total is long.
- Use `async with session.get(url) as resp:` and call `resp.raise_for_status()` before reading the body.
- Stream large bodies with `resp.content.iter_chunked(n)` instead of `await resp.read()`.
- Store shared state on `app["key"]` using `web.AppKey` for typing; use `request.app[key]` in handlers.
- Write middlewares as `@web.middleware async def mw(request, handler)` and return the handler's response.
- Cancel and await background tasks in a `cleanup_ctx` teardown.

## Avoid
- `ClientSession()` created per request: leaks connectors and loses pooling. Share one.
- Using the session outside a running loop, or creating it at import: warns or breaks. Create it inside a coroutine or `cleanup_ctx`.
- Blocking calls (`requests`, `time.sleep`, sync DB) in handlers: freezes every connection. Use `await asyncio.to_thread(...)` or async libraries.
- `app.on_startup`/`on_cleanup` signal lists for resources needing paired teardown: use `cleanup_ctx` generators.
- `web.run_app` handlers that return a dict: it must return a `web.Response`. Use `web.json_response`.
- Forgetting `await resp.release()` or leaving a response unread outside `async with`: connections stay checked out.
- `ssl=False` to silence cert errors: disables verification. Fix the trust store or pass an `ssl.SSLContext`.

## Review
- [ ] One shared `ClientSession` with explicit timeouts, closed on shutdown.
- [ ] Every client response is read inside `async with` and its status checked.
- [ ] No blocking calls on the event loop; background tasks are tracked and cancelled.
- [ ] Middlewares always return a response and re-raise `web.HTTPException` they do not handle.
- [ ] Tests run with `ResourceWarning` as errors.
