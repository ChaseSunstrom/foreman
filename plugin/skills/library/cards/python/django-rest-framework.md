---
name: django-rest-framework
title: Django REST framework
area: python
tags: [python, django, rest, api, serializers, viewsets]
detect: [dep:djangorestframework]
related: [django, pytest, celery, pydantic]
---
DRF APIs on Django: serializers, viewsets and routers, permissions, pagination, filtering, throttling.

## Verify
- `python manage.py check`: settings and installed apps load, including `REST_FRAMEWORK`.
- `python manage.py makemigrations --check --dry-run`: no model drift behind the serializers.
- `pytest -q` (or `python manage.py test`): the suite through `APIClient`.
- `python manage.py spectacular --validate --fail-on-warn`: the schema builds, only when drf-spectacular is installed.

## Test first
Use `rest_framework.test.APIClient` and authenticate with `force_authenticate`.
```python
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_cannot_read_other_users_note(user, other_note):
    c = APIClient()
    c.force_authenticate(user)
    r = c.get(f"/api/notes/{other_note.pk}/")
    assert r.status_code == 404
```

## Do
- Set `DEFAULT_PERMISSION_CLASSES` to `IsAuthenticated` globally and loosen per view.
- Override `get_queryset` to scope by `request.user`; use object permissions for the rest.
- Declare `fields` explicitly on every `ModelSerializer`, and mark server-set fields `read_only`.
- Put cross-field rules in `validate()` and per-field rules in `validate_<field>`.
- Set `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE` so list endpoints are bounded.
- Use `select_related`/`prefetch_related` in `get_queryset`; nested serializers cause N+1 otherwise.
- Use `@action(detail=True, methods=[...])` for non-CRUD verbs instead of extra views.
- Set `DEFAULT_THROTTLE_CLASSES` and rates on login and expensive endpoints.

## Avoid
- `fields = "__all__"` or `exclude`: new model columns leak and become writable. List fields.
- Trusting `request.data` for ownership (`owner` in the body): set it in `perform_create` with `serializer.save(owner=request.user)`.
- `AllowAny` left on a viewset: pairs with an unfiltered queryset to expose every row.
- Overriding `create()` to do a multi-step write with no `transaction.atomic()`: partial rows on failure.
- Writable nested serializers with no custom `create`/`update`: DRF raises, or silently drops data. Write them explicitly.
- Returning `Response(serializer.data)` after `is_valid()` without `raise_exception=True`: errors never reach the client as 400.
- `SerializerMethodField` that queries per row: annotate the queryset instead.

## Review
- [ ] Each viewset has explicit `permission_classes` and a scoped `get_queryset`.
- [ ] No serializer uses `__all__`; read-only and write-only fields are deliberate.
- [ ] List endpoints are paginated and query counts do not grow with page size.
- [ ] Tests cover 401, 403, 404-for-foreign-object and a 400 validation case.
- [ ] Authentication classes match the client (session needs CSRF; token or JWT does not).
