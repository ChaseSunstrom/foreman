---
name: django-orm
title: Django ORM
area: python
tags: [python, django, orm, queryset, sql, performance]
detect: [dep:Django, file:manage.py]
related: [django, django-migrations, django-rest-framework, pytest]
---
Django ORM querysets: lazy evaluation, N+1 control, atomic writes, F and Q expressions, constraints.

## Verify
- `python manage.py check`: models and settings load without system-check errors.
- `python manage.py makemigrations --check --dry-run`: model changes have matching migrations.
- `pytest -q --reuse-db` (or `python manage.py test`): the suite against a real test database.
- `pytest -q --ds=config.settings` : settings module resolves under pytest-django (replace the module path).

## Test first
Assert the query count so N+1 regressions fail.
```python
import pytest
from app.models import Author

@pytest.mark.django_db
def test_author_list_uses_two_queries(django_assert_num_queries, client):
    Author.objects.bulk_create([Author(name=f"a{i}") for i in range(5)])
    with django_assert_num_queries(2):
        r = client.get("/authors/")
    assert r.status_code == 200
```
`django_assert_num_queries` comes from pytest-django. In `TestCase`, use `assertNumQueries`.

## Do
- Fetch related rows up front: `select_related` for FK and one-to-one (JOIN), `prefetch_related` for reverse FK and M2M (second query). Use `Prefetch(..., queryset=...)` to filter.
- Update in the database with `F()`: `Item.objects.filter(pk=pk).update(stock=F("stock") - 1)`. No read-modify-write in Python.
- Wrap multi-row writes in `transaction.atomic()`. Lock with `select_for_update()` inside it.
- Use `bulk_create`, `bulk_update(objs, fields)` and `.update()` for batches. Use `.iterator(chunk_size=...)` for large reads.
- Enforce rules in `Meta.constraints` (`UniqueConstraint`, `CheckConstraint`) and `Meta.indexes`, not only in `clean()`.
- Use `.only()`, `.values_list()` and `.exists()` instead of loading whole rows or `len(qs)`.
- Use `get_or_create` / `update_or_create` with a unique constraint backing them.

## Avoid
- Accessing `obj.related.x` in a loop: one query per row. Add `select_related` or `prefetch_related`.
- `if qs:` or `len(qs)` to test emptiness or count: loads everything. Use `.exists()` and `.count()`.
- Assuming `bulk_create` or `.update()` call `save()` or send signals: they do not. Move that logic or loop deliberately.
- Raw SQL via f-strings: injectable. Use `raw(sql, params)` or `cursor.execute(sql, params)`.
- `null=True` on `CharField`: two empty values. Use `blank=True, default=""`.
- Catching `IntegrityError` inside `atomic()` without a nested `atomic()`: the outer transaction is already broken.
- `Model.objects.get()` without handling `DoesNotExist` and `MultipleObjectsReturned`; use `get_object_or_404` in views.

## Review
- [ ] Every list view or serializer has `select_related` / `prefetch_related` and a query-count test.
- [ ] Counters and balances change through `F()` or `select_for_update`, not Python arithmetic.
- [ ] Uniqueness and check rules exist as DB constraints with migrations.
- [ ] No raw SQL built by string formatting.
- [ ] Multi-step writes are inside `transaction.atomic()`.
