---
name: litestar
title: Litestar
area: python
tags: [python, web, asgi, litestar, async, openapi]
detect: [dep:litestar, dep:litestar-*]
related: [pydantic, sqlalchemy, pytest, httpx, fastapi]
---
Litestar ASGI apps: controllers, route handlers, dependency injection with `Provide`, DTOs, plugins, generated OpenAPI.

## Verify
- `litestar --app app.main:app routes`: the app imports and routes register.
- `litestar --app app.main:app schema openapi --output openapi.json`: the OpenAPI schema builds.
- `pytest -q`: the suite using Litestar's test clients.
- `pyright` (or `mypy .`): handler signatures and DTO types check.

## Test first
Use `litestar.testing.TestClient` (sync) or `AsyncTestClient`.
```python
from litestar.testing import TestClient
from app.main import app

def test_create_item_requires_name():
    with TestClient(app=app) as client:
        r = client.post("/items", json={})
    assert r.status_code == 400
```

## Do
- Type every handler parameter and return value; Litestar derives validation and the schema from them.
- Group handlers in `Controller` classes and attach them to a `Router` with a `path`.
- Provide dependencies with `dependencies={"db": Provide(get_db)}` at app, router, controller or handler level; use async generators for cleanup.
- Use DTOs (`DataclassDTO`, `PydanticDTO`, `SQLAlchemyDTO`) with `DTOConfig(exclude=...)` to control what crosses the wire.
- Register plugins (`SQLAlchemyPlugin`) for session lifecycle instead of hand-rolled middleware.
- Mark blocking handlers `sync_to_thread=True`.
- Set `debug` from config, and guards (`guards=[...]`) for authorization.

## Avoid
- Returning ORM models directly with no DTO: lazy-loads fire after the session closes and internal fields leak. Add a return DTO.
- FastAPI idioms (`Depends`, `APIRouter`, `HTTPException`): they do not exist here. Use `Provide`, `Router`, and `litestar.exceptions.HTTPException`.
- Sync handlers that block with no `sync_to_thread`: Litestar warns and blocks the loop. Set the flag or go async.
- Untyped dependency or handler arguments: they are treated as query parameters or fail at startup. Annotate them.
- `debug=True` in deployed config: tracebacks reach clients.
- A dependency that is not in a reachable layer's `dependencies` mapping: handlers fail with a `ImproperlyConfiguredException` at startup. Check the layer.

## Review
- [ ] Handlers are fully typed and their DTOs expose only intended fields.
- [ ] Authorization is by guards on the router or controller, not inline checks.
- [ ] Sessions and clients come from `Provide` or a plugin, one per request.
- [ ] Blocking calls are in `sync_to_thread` handlers or awaited async drivers.
- [ ] Tests use the test client and cover a validation failure and an authorization failure.
