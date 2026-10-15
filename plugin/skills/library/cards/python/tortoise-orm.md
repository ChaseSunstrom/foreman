---
name: tortoise-orm
title: Tortoise ORM
area: python
tags: [python, orm, async, asyncio, database, aerich]
detect: [dep:tortoise-orm, dep:aerich]
related: [asyncio, fastapi, pytest-asyncio, pydantic]
---
Tortoise ORM: async-native models with explicit connection lifecycle, prefetching and Aerich migrations.

## Verify
- `pytest -q`: async tests against an in-memory SQLite database.
- `aerich migrate --name check && aerich upgrade`: Aerich generates and applies a migration (needs `aerich init` first).
- `pyright` (or `mypy .`): model field types.
- `python -c "import app.models"`: model modules import with no relation errors.

## Test first
```python
import pytest
from tortoise import Tortoise
from app.models import User

@pytest.fixture
async def db():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

@pytest.mark.asyncio
async def test_username_unique(db):
    await User.create(username="a")
    with pytest.raises(Exception):
        await User.create(username="a")
```
Use pytest-asyncio auto mode or async fixtures with the marker as shown. Tortoise also ships `tortoise.contrib.test`.

## Do
- Define models as `class User(Model): id = fields.IntField(primary_key=True)` (older code uses `pk=True`) and set `class Meta: table = "users"`.
- Call `await Tortoise.init(config=...)` once at startup and `await Tortoise.close_connections()` at shutdown. With FastAPI use `register_tortoise` or lifespan.
- Reference models in `ForeignKeyField("models.User", related_name="posts")`: the `"app.Model"` string uses the app label, not the module path.
- Prefetch with `.prefetch_related("posts")` and `.select_related("owner")`.
- Use `F()` expressions with `.update()`, and `in_transaction()` for multi-step writes.
- Use `Model.filter(...).first()`, `.exists()` and `.count()`. Use `bulk_create` for batches.
- Generate Pydantic models with `pydantic_model_creator` and call `Tortoise.init_models` first when relations exist.

## Avoid
- Forgetting `await` on a queryset: you get a QuerySet object, not rows.
- Accessing `obj.posts` without prefetch: returns a manager that needs `await obj.posts.all()` or a prior `fetch_related`.
- `generate_schemas()` in production in place of Aerich migrations: no schema history.
- Missing modules in `Tortoise.init` or `TORTOISE_ORM["apps"]`: relations fail with a "no model" error. Include `aerich.models` for Aerich.
- Sharing sync code paths that call the ORM from threads: Tortoise needs the event loop that opened the connection.
- Skipping `close_connections()` in tests: "event loop closed" and hanging runs.

## Review
- [ ] Startup initializes and shutdown closes connections.
- [ ] Every queryset is awaited or iterated with `async for`.
- [ ] Relations are prefetched where lists are returned.
- [ ] Schema changes have an Aerich migration committed.
- [ ] Tests build and tear down schemas per test or per session deliberately.
