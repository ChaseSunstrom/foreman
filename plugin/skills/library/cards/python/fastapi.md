---
name: fastapi
title: FastAPI
area: python
tags: [python, web, api, async, pydantic, openapi]
detect: [dep:fastapi]
related: [pydantic, sqlalchemy, pytest, httpx, uv, ruff]
---
FastAPI services: typed path operations, Pydantic v2 models, dependency injection, generated OpenAPI.

## Verify
- `ruff check . && ruff format --check .`: lint and format.
- `pyright` (or `mypy .`): types, including response models.
- `pytest -q`: the suite, through the ASGI app in process with no server.
- `python -c "import app.main as m; m.app.openapi()"`: the schema still builds (catches bad models at import).

## Test first
Drive the app in process. Override dependencies rather than patching modules.
```python
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.deps import get_db

@pytest.mark.anyio
async def test_create_item_rejects_blank_name(fake_db):
    app.dependency_overrides[get_db] = lambda: fake_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
        r = await c.post("/items", json={"name": ""})
    assert r.status_code == 422
```
For sync tests, `fastapi.testclient.TestClient(app)` works.

## Do
- Keep separate request, response and DB models (`ItemIn`, `ItemOut`, ORM `Item`). Set `response_model` so internal fields never leak.
- Get sessions, the current user and settings through `Depends`. Use `yield` dependencies for cleanup and commit or roll back in one place.
- Load settings with `pydantic-settings`. Build clients once in `lifespan`, not per request.
- Use `async def` only when everything awaited inside is async. Use plain `def` for blocking libraries (FastAPI runs those in a threadpool).
- Raise `HTTPException` with a stable `detail` shape. Register exception handlers for domain errors.
- Split the app into routers (`APIRouter(prefix=..., tags=[...])`) and include them in `main.py`.

## Avoid
- Blocking calls (`requests`, sync DB drivers, `time.sleep`) inside `async def`: they stall the event loop for every request. Use `httpx.AsyncClient` or an async driver, or make the handler `def`.
- Returning ORM objects without a response model: lazy loads fire after the session closes, and private columns leak. Use `model_config = ConfigDict(from_attributes=True)` on the out model.
- Pydantic v1 idioms in a v2 codebase: `orm_mode`, `.dict()`, `@validator`. Use `from_attributes`, `.model_dump()`, `@field_validator`.
- A module-level `Session()` or client shared across requests: a race under load. Make it per request via a dependency.
- `dependency_overrides` left set between tests: clear it in a fixture teardown.
- CORS `allow_origins=["*"]` together with `allow_credentials=True`: browsers reject it, and it signals an unreviewed policy.

## Review
- [ ] Every route has a response model or explicit response class, and status codes match the semantics (201 on create, 204 with no body).
- [ ] No blocking I/O inside `async def` handlers or dependencies.
- [ ] Auth comes from a dependency on the router or route, not ad hoc checks in handler bodies.
- [ ] Validation errors return 422 with field paths, and domain errors map to 4xx by explicit handlers.
- [ ] Tests override dependencies (DB, auth, clock) and cover at least one failure path per route.
