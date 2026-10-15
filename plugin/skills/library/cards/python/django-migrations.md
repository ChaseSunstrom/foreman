---
name: django-migrations
title: Django migrations
area: python
tags: [python, django, migrations, schema, database, deploy]
detect: [file:*/migrations/0001_initial.py]
related: [django, django-orm, alembic]
---
Django schema migrations: generated, reviewed, reversible, and safe to deploy against a live database.

## Verify
- `python manage.py makemigrations --check --dry-run`: no model change lacks a migration (fails CI on drift).
- `python manage.py migrate --plan`: shows the exact operations pending.
- `python manage.py sqlmigrate APP 0007`: the SQL a migration will run (look for table rewrites and locks).
- `python manage.py migrate APP 0006 && python manage.py migrate`: the migration reverses and reapplies.
- `python manage.py showmigrations`: applied state and a single linear history.

## Test first
Check the data step on a fresh database. With `django-test-migrations`:
```python
def test_backfill_slug(migrator):
    old = migrator.apply_initial_migration(("blog", "0004_post"))
    Post = old.apps.get_model("blog", "Post")
    Post.objects.create(title="Hello World")
    new = migrator.apply_tested_migration(("blog", "0005_backfill_slug"))
    assert new.apps.get_model("blog", "Post").objects.get().slug == "hello-world"
```
Without that package, assert `makemigrations --check` in CI and test the backfill function directly.

## Do
- Commit migrations with the model change. Read the generated file before committing.
- Split schema from data: one migration adds a nullable column, a `RunPython` migration backfills, a later one adds `NOT NULL`.
- Give every `RunPython` a reverse (`migrations.RunPython.noop` when truly nothing to undo). Use `apps.get_model(...)` inside it.
- Add indexes on big tables with `AddIndexConcurrently` (PostgreSQL, `atomic = False` on the migration).
- Rename in steps (add new, dual-write, backfill, switch reads, drop old) across deploys.
- Resolve merge conflicts with `python manage.py makemigrations --merge`, then review.
- Squash only old, fully-applied migrations with `squashmigrations`.

## Avoid
- Importing real models in `RunPython`: later model changes break old migrations. Use `apps.get_model`.
- Editing or deleting an applied migration: other databases diverge. Add a new one.
- Adding a `NOT NULL` column without a default on a big table: long lock or failure. Add nullable, backfill, then tighten.
- `RunSQL` with no `reverse_sql`: irreversible. Provide it or `migrations.RunSQL.noop`.
- Running `migrate` before the new code is deployed when the migration drops or renames something old code reads: deploy in the order add, deploy, remove.
- Ignoring `makemigrations` output that asks "was X renamed?": answering no drops and recreates the column and its data.

## Review
- [ ] `sqlmigrate` output has no full-table rewrite or long lock on large tables.
- [ ] Data migrations are idempotent, batched and reversible.
- [ ] No migration edits an already-applied file.
- [ ] Destructive operations (`RemoveField`, `DeleteModel`) land a deploy after code stops using them.
- [ ] One leaf node per app in the migration graph.
