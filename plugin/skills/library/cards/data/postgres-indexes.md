---
name: postgres-indexes
title: PostgreSQL indexes
area: data
tags: [postgres, index, btree, explain, gin, partial, performance]
detect: []
related: [postgres, query-tuning, postgres-jsonb, postgres-locking]
---
Choose, build and prove PostgreSQL indexes with EXPLAIN (ANALYZE, BUFFERS) instead of guessing.

## Verify
- `psql -c "EXPLAIN (ANALYZE, BUFFERS) <query>"`: the plan uses the new index and shows real row counts and buffer hits.
- `psql -c "SELECT indexrelname, idx_scan FROM pg_stat_user_indexes ORDER BY idx_scan"`: unused indexes (idx_scan = 0) that only cost writes.
- `psql -c "SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid"`: a failed CREATE INDEX CONCURRENTLY left an invalid index.
- `psql -c "SELECT pg_size_pretty(pg_relation_size('idx_name'))"`: index size, to spot bloat.

## Test first
Fail on the plan, not the result. Seed realistic volume (100k+ rows) and ANALYZE, otherwise the planner picks a seq scan anyway.
```python
def test_orders_by_customer_uses_index(db):
    db.execute("INSERT INTO orders SELECT g, g % 1000, now() FROM generate_series(1,200000) g")
    db.execute("ANALYZE orders")
    plan = "\n".join(r[0] for r in db.execute(
        "EXPLAIN SELECT * FROM orders WHERE customer_id = 7 ORDER BY created_at DESC LIMIT 20"))
    assert "Seq Scan" not in plan
```

## Do
- Order composite columns equality first, then range or sort: `(customer_id, created_at DESC)` serves the filter and the ORDER BY.
- Use partial indexes for hot subsets: `CREATE INDEX ON jobs (run_at) WHERE status = 'queued'`. The query must repeat the predicate.
- Use covering indexes with `INCLUDE (col)` to get index-only scans; keep the visibility map fresh with autovacuum.
- Use `CREATE INDEX CONCURRENTLY` on live tables, outside a transaction block, and drop failed ones before retrying.
- Index every foreign key column you join or delete through.
- Expression indexes must match the query expression exactly: `ON users (lower(email))`.
- Choose the type deliberately: btree default, GIN for arrays, jsonb and tsvector, BRIN for huge append-only ordered data, GiST for ranges.

## Avoid
- Plain `CREATE INDEX` on a busy table: it blocks writes. Use `CONCURRENTLY`.
- Indexing low-cardinality booleans alone: planner ignores it. Use a partial index.
- `WHERE lower(email) = ...` against a plain index: no match. Add the expression index.
- Leading `LIKE '%x'` with btree: use `pg_trgm` GIN or a reversed expression index. Non-C collations also need `text_pattern_ops` for prefix LIKE.
- Redundant prefixes: `(a)` next to `(a, b)`. Drop the shorter one.
- Judging plans on an empty dev table or after no ANALYZE.

## Review
- [ ] Each new index has an EXPLAIN showing it is chosen, in the PR.
- [ ] Created CONCURRENTLY, in its own migration without a transaction.
- [ ] Column order matches equality, range, sort of the real query.
- [ ] No duplicate or prefix-redundant indexes added.
- [ ] Write-heavy tables: index count and size justified.
