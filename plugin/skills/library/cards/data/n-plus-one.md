---
name: n-plus-one
title: N+1 queries
area: data
tags: [orm, performance, queries, eager-loading, batching, dataloader]
detect: []
related: [query-tuning, postgres, mysql, sql-migrations]
---
Detect and remove N+1 query patterns by counting queries in a test, then batching with joins, eager loading or a loader.

## Verify
- `pytest -q tests/test_query_counts.py`: the query-count assertions pass for list endpoints.
- `rg -n "for .* in .*:\s*$" -A3 app | rg "\.get\(|\.execute\(|\.query\(|\.first\("`: loops that run a query per item (candidates to review).
- `psql "$DATABASE_URL" -c "SELECT query, calls FROM pg_stat_statements ORDER BY calls DESC LIMIT 10;"`: one statement called thousands of times is the signature.
- `rails test` with the `bullet` gem enabled, or Django's `assertNumQueries`: framework-level detection that raises on N+1.

## Test first
Assert a query count independent of the number of rows.
```python
def test_list_orders_query_count(client, django_assert_num_queries):
    make_orders(users=1, per_user=1); make_orders(users=20, per_user=3)
    with django_assert_num_queries(2):   # orders + prefetched items
        client.get("/orders")
```
SQLAlchemy: count via a `before_cursor_execute` listener. The same test with 1 row and 60 rows must report the same count.

## Do
- Fix it where the data is loaded: eager load relations the view needs (`select_related`/`prefetch_related`, `joinedload`/`selectinload`, `include`/`with`, `.Include()`).
- Use `selectinload`-style batching (`WHERE id IN (...)`) for collections and joins for single-valued relations.
- Fetch only needed columns for lists (`only`, `load_only`, `select`).
- In GraphQL, batch per-field lookups with a DataLoader (one batch per tick) keyed by id.
- Replace per-item existence or count checks with one aggregate query grouped by key.
- Add query-count tests to list and detail endpoints, and keep them in CI.
- Write in bulk too: `bulk_create`, `insertMany`, `executemany`, a single `INSERT ... VALUES` with many rows.

## Avoid
- Accessing a lazy relation inside a template or serializer loop: one query per row. Prefetch in the query.
- A global "always eager load everything" setting: heavy joins and row explosion. Load per use case.
- Joining two collections in one query: cartesian row multiplication. Use separate `IN` batches.
- Calling `.count()` or `.exists()` inside a loop: one query each. Annotate or aggregate once.
- Fixing with a cache around the loop: hides the pattern and breaks on a cold cache. Batch the query.
- Measuring only latency on a small dataset: N+1 looks fast with 5 rows. Assert counts, not time.
- `IN` lists of unbounded size: parameter limits. Chunk the ids.

## Review
- [ ] List endpoints have a query-count test that is flat as rows grow.
- [ ] Relations used by serializers or templates are loaded explicitly.
- [ ] Counts, sums and existence checks are aggregated in SQL.
- [ ] Bulk writes replace per-row inserts and updates.
- [ ] `IN` batches are chunked.
