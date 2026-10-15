---
name: postgres-jsonb
title: PostgreSQL jsonb
area: data
tags: [postgres, jsonb, gin, json, schema, query]
detect: []
related: [postgres, postgres-indexes, sql-migrations]
---
Store and query semi-structured data in jsonb without losing indexes, types or integrity.

## Verify
- `psql -c "EXPLAIN (ANALYZE) SELECT id FROM events WHERE payload @> '{\"type\":\"click\"}'"`: containment uses the GIN index.
- `psql -c "SELECT jsonb_typeof(payload->'age'), count(*) FROM users GROUP BY 1"`: a field has one consistent type.
- `psql -c "\d+ events"`: indexes and CHECK constraints present.

## Test first
Write the query test with mixed-type and missing-key rows.
```python
def test_filter_handles_missing_and_string_numbers(db):
    db.execute("INSERT INTO t(doc) VALUES ('{\"n\":5}'),('{}'),('{\"n\":\"5\"}')")
    rows = db.execute("SELECT count(*) FROM t WHERE (doc->>'n')::int = 5").fetchone()
    assert rows[0] == 2
```

## Do
- Promote fields you filter, join or constrain on to real columns; keep jsonb for the variable remainder.
- Use `->` for jsonb and `->>` for text; cast explicitly: `(doc->>'n')::numeric`.
- Index with `USING gin (doc jsonb_path_ops)` for `@>` only (smaller, faster), or default `jsonb_ops` when you need `?` key tests.
- For one hot key use an expression btree: `CREATE INDEX ON t ((doc->>'status'))`.
- Update in place with `jsonb_set(doc, '{a,b}', '1'::jsonb, true)` and `doc || '{"k":1}'`.
- Validate shape with a CHECK constraint (`jsonb_typeof(doc->'tags') = 'array'`) or app-side schema.
- Use `jsonb_path_exists` or `@@` with jsonpath for complex predicates.

## Avoid
- `json` instead of `jsonb`: no indexing, keeps duplicates and whitespace. Use jsonb.
- Querying `doc->>'k' = 'v'` against a GIN index: it does not match. Use `doc @> '{"k":"v"}'` or an expression index.
- Whole-document rewrites for one key under concurrency: the last writer wins and TOAST rewrites are heavy. Use `jsonb_set` or a column.
- Unbounded arrays inside one document: row bloat, write amplification. Use a child table.
- Casting without guarding type: `::int` on a string value errors the whole query. Filter with `jsonb_typeof` first.
- Storing big blobs and indexing everything: GIN write cost and size explode.

## Review
- [ ] Filtered fields have a matching index form (GIN containment or expression index) shown in EXPLAIN.
- [ ] Frequently joined or unique fields are columns, not json keys.
- [ ] Casts guarded against missing or mistyped keys.
- [ ] Documents have a bounded size.
- [ ] Schema expectations enforced by CHECK or validation at write.
