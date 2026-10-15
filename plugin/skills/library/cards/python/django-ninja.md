---
name: django-ninja
title: Django Ninja
area: python
tags: [python, django, api, pydantic, openapi, rest]
detect: [dep:django-ninja]
related: [django, django-orm, pydantic, fastapi, django-rest-framework]
---
Django Ninja: FastAPI-style typed Django APIs with Pydantic schemas, routers and generated OpenAPI.

## Verify
- `python manage.py check`: URL conf and the `NinjaAPI` instance load.
- `python manage.py export_openapi_schema --api config.api.api`: the schema builds (replace the dotted path to your `NinjaAPI`).
- `pytest -q`: endpoints through `ninja.testing.TestClient`.
- `python manage.py makemigrations --check --dry-run`: schema changes carry migrations.

## Test first
```python
import pytest
from ninja.testing import TestClient
from app.api import router

@pytest.mark.django_db
def test_create_rejects_blank_title():
    client = TestClient(router)
    r = client.post("/items", json={"title": ""})
    assert r.status_code == 422
```
`TestClient` skips the URL layer and middleware. For auth and middleware tests, use Django's `Client` against the real URLs.

## Do
- Declare `Schema` classes (subclass `ninja.Schema`) for input and output. Pass `response={200: ItemOut, 404: ErrorOut}`.
- Use `ModelSchema` with `class Meta: model = Item; fields = [...]`. List `fields` explicitly, never `"__all__"`.
- Split into `Router()` instances and attach with `api.add_router("/items/", router)`.
- Set `auth=` on the router or `NinjaAPI(auth=...)`. Use `HttpBearer` or `APIKeyHeader` subclasses with `authenticate(request, token)`.
- Use `Query[FilterSchema]` and `ninja.pagination.paginate` for lists.
- Register `@api.exception_handler(DomainError)` and return `api.create_response(request, {...}, status=409)`.
- Use `async def` views with Django async ORM (`aget`, `async for`).

## Avoid
- Returning querysets with lazy relations from async views: use `select_related` and await evaluation. Sync ORM in async raises `SynchronousOnlyOperation`.
- Two `NinjaAPI` instances with the same `urls_namespace`: Django raises a namespace clash. Give each a `urls_namespace`.
- Forgetting `auth` on a router: endpoints are public by default.
- Pydantic v1 idioms (`orm_mode`, `.dict()`): use `from_attributes`-style config and `.model_dump()` on Pydantic v2 builds.
- `ModelSchema` exposing password hashes or internal flags: use `fields` or `exclude` deliberately.
- Mutating state in `GET` handlers.

## Review
- [ ] Every endpoint has a typed response, with error codes listed in `response=`.
- [ ] Auth is set at router or API level and the public endpoints are an explicit exception.
- [ ] No sync ORM calls inside `async def`.
- [ ] List endpoints are paginated and avoid N+1 (`select_related`, `prefetch_related`).
- [ ] Schemas expose an explicit field list.
