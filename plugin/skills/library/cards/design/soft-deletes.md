---
name: soft-deletes
title: Soft deletes
area: design
tags: [soft-delete, database, deleted-at, retention, unique-constraints, restore]
detect: []
related: [data-retention, audit-trails, multi-tenancy, zero-downtime-migrations, event-sourcing]
---
Mark rows deleted with a timestamp instead of removing them, and make every query, index and constraint respect that mark.

## Verify
- `pytest -q -k "delete or restore"`: hidden by default, restorable, unique reuse works.
- `psql -c "\d TABLE"`: partial unique indexes carry `WHERE deleted_at IS NULL`.
- `git grep -nE "deleted_at|is_deleted" -- src`: filtering lives in one place (default scope or view), not scattered.

## Test first
A deleted row disappears from reads, frees its unique value, and restores.
```python
def test_soft_delete_hides_frees_unique_and_restores(db):
    u = create_user(db, email="a@x.io")
    delete_user(db, u.id)
    assert get_user(db, u.id) is None
    assert list_users(db) == []
    u2 = create_user(db, email="a@x.io")            # unique value reusable
    assert u2.id != u.id
    with pytest.raises(Conflict):
        restore_user(db, u.id)                       # email now taken
    delete_user(db, u2.id); restore_user(db, u.id)
    assert get_user(db, u.id).email == "a@x.io"
```

## Do
- Use `deleted_at timestamptz null` (plus `deleted_by` if needed), not a boolean, so you know when.
- Centralise filtering: an ORM default scope, a view, or row-level security. Provide an explicit `with_deleted` opt-out.
- Make unique indexes partial: `CREATE UNIQUE INDEX ... WHERE deleted_at IS NULL`.
- Decide cascade rules per relation: children soft-delete with the parent, or are hidden through the join.
- Add a purge job that hard-deletes after the retention window, and a real erasure path for privacy requests.
- Index so live-row queries stay fast (partial indexes on the live set).
- Define restore semantics and conflicts up front.

## Avoid
- Filtering by hand in each query: one miss leaks deleted data. Use a scope or view.
- Full unique constraint on a soft-deleted column: reuse fails. Use a partial unique index.
- Treating soft delete as erasure: personal data stays. Purge or anonymise for privacy deletes.
- Foreign keys pointing at hidden rows: orphan-like reads. Cascade or check on write.
- Forgetting aggregate counts, search indexes and caches: they still include deleted rows. Update or filter them too.

## Review
- [ ] One default filter mechanism with explicit opt-out.
- [ ] Unique constraints are partial.
- [ ] Purge and privacy erasure exist.
- [ ] Search, caches and counts exclude deleted rows.
