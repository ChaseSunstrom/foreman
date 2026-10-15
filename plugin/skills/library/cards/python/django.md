---
name: django
title: Django
area: python
tags: [python, web, orm, django, migrations, templates]
detect: [dep:django, dep:Django, file:manage.py]
related: [django-rest-framework, pytest, celery, ruff, uv]
---
Django projects: models and migrations, views, forms, the ORM, settings per environment, the built-in test runner or pytest-django.

## Verify
- `python manage.py check --deploy`: settings audit (DEBUG, SECRET_KEY, HTTPS flags, cookies).
- `python manage.py makemigrations --check --dry-run`: models and migrations agree, nothing unwritten.
- `python manage.py migrate --plan`: what would run, in order.
- `python manage.py test` (or `pytest` with pytest-django): the suite against a throwaway test database.

## Test first
Use `TestCase` (transaction-wrapped) and the test client. Tests live in `app/tests/` or `tests.py`.
```python
from django.test import TestCase
from django.urls import reverse

class OrderListTests(TestCase):
    def test_other_users_orders_hidden(self):
        self.client.force_login(self.make_user("a"))
        r = self.client.get(reverse("orders:list"))
        self.assertNotContains(r, "order-of-b")
```
For N+1 regressions use `with self.assertNumQueries(2):`.

## Do
- Write a migration for every model change and commit it. Split schema and data migrations (`RunPython` with a reverse function).
- Use `select_related` for FK/one-to-one and `prefetch_related` for reverse/M2M on every list view.
- Subclass `AbstractUser` and set `AUTH_USER_MODEL` before the first migration.
- Read secrets and `DEBUG` from the environment; keep one settings module per environment or one module driven by env.
- Wrap multi-write views in `transaction.atomic()`. Use `F()` expressions and `update_fields` for concurrent counters.
- Put `db_index`, `UniqueConstraint` and `CheckConstraint` in `Meta.constraints`, not only in forms.
- Enqueue work from `transaction.on_commit`, not before the commit.

## Avoid
- `DEBUG = True` or a hardcoded `SECRET_KEY` in deployable settings: `check --deploy` flags it. Read from env.
- `ALLOWED_HOSTS = ["*"]` in production: host-header attacks. List real hosts.
- `.raw()` or `.extra()` with f-strings: SQL injection. Use ORM expressions or parameters.
- `Model.objects.get()` without handling `DoesNotExist`/`MultipleObjectsReturned`: use `get_object_or_404` or `.filter().first()`.
- `@csrf_exempt` to silence a 403: send the token (`X-CSRFToken`) instead.
- Editing an applied migration: others have run it. Add a new one.
- `len(qs)` or `if qs:` to test existence: use `.exists()` and `.count()`.

## Review
- [ ] Every model change has a committed migration and `makemigrations --check` is clean.
- [ ] List views use `select_related`/`prefetch_related`; a query-count test guards hot ones.
- [ ] Views check permissions (`LoginRequiredMixin`, `permission_required`) and filter querysets by owner.
- [ ] No secrets or `DEBUG=True` in committed settings; `check --deploy` passes.
- [ ] Migrations that touch big tables avoid locking operations in a single step.
