---
name: httpx
title: HTTPX
area: python
tags: [python, http, client, async, httpx, testing]
detect: [dep:httpx]
related: [asyncio, aiohttp, fastapi, pytest, pydantic]
---
HTTPX: sync and async HTTP client with timeouts, connection pooling, HTTP/2, transports and ASGI/WSGI testing.

## Verify
- `python -c "import httpx; print(httpx.__version__)"`: the installed version.
- `pytest -q`: tests using `httpx.MockTransport` or `respx`.
- `python -X dev -W error::ResourceWarning -m pytest -q`: unclosed clients surface as errors.
- `python -c "import httpx; print(httpx.get('https://example.com', timeout=5).status_code)"`: a real call works with a bounded timeout (skip offline).

## Test first
Inject a `MockTransport` so no network is touched.
```python
import httpx
from app.api import fetch_user

def test_fetch_user_raises_on_404():
    def handler(request):
        return httpx.Response(404, json={"detail": "nope"})
    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://t")
    with pytest.raises(httpx.HTTPStatusError):
        fetch_user(client, 7)
```
For apps, `httpx.ASGITransport(app=app)` drives an ASGI app in process.

## Do
- Reuse one `httpx.Client` or `httpx.AsyncClient` for many requests, used as a context manager or closed on shutdown.
- Set `timeout=httpx.Timeout(10.0, connect=5.0)` explicitly.
- Call `response.raise_for_status()` and catch `httpx.HTTPStatusError` and `httpx.RequestError` separately.
- Pass `params=`, `json=`, `data=` and `files=` rather than building URLs and bodies by hand.
- Configure base URL, headers and auth once on the client (`base_url=`, `headers=`, `auth=`).
- Retry transient failures with `httpx.HTTPTransport(retries=N)` (connection errors only) or a library such as tenacity for status retries.
- Stream large bodies with `with client.stream("GET", url) as r: for chunk in r.iter_bytes(): ...`.
- Inject the client into functions so tests can pass a mock transport.

## Avoid
- Module-level `httpx.get(...)` in hot paths: new connection each call. Use a shared client.
- Relying on the default timeout in code that has no deadline of its own: it is 5 seconds, not infinite, but too short or too long varies. State it.
- Forgetting `follow_redirects=True`: unlike `requests`, HTTPX does not follow redirects by default.
- Using a sync `Client` inside `async def`: blocks the loop. Use `AsyncClient` with `await`.
- Sharing one `AsyncClient` across different event loops: errors on closed loops. Create it inside the running loop.
- `verify=False` to bypass TLS errors: no certificate checks. Provide the CA bundle via `verify="path"` or an `ssl.SSLContext`.
- Reading `response.text` after streaming without `read()`: raises `ResponseNotRead`.

## Review
- [ ] One client per process or task group, always closed.
- [ ] Every call has a timeout and checked status.
- [ ] Both `HTTPStatusError` and `RequestError` paths are handled and tested.
- [ ] Redirect and TLS behavior is explicit; `verify` is never disabled.
- [ ] Tests use `MockTransport` or `respx`, no live network.
