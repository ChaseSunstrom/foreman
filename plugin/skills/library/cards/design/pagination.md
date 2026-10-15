---
name: pagination
title: Pagination
area: design
tags: [pagination, cursor, keyset, offset, sorting, api]
detect: []
related: [rest-api-design, graphql-schema, caching, openapi]
---
List endpoints with bounded pages, deterministic order and keyset cursors for large or changing data.

## Verify
- `curl -s 'localhost:8080/items?limit=2' | jq '{n: (.items|length), next: .next_cursor}'`: a page returns at most `limit` items and a cursor.
- `curl -s 'localhost:8080/items?limit=100000' | jq '.items|length'`: the request is clamped or rejected at the maximum.
- `psql -c "explain select * from items where (created_at, id) < ('2026-01-01', 10) order by created_at desc, id desc limit 20"`: the plan uses an index, with no sort or full scan.

## Test first
Walk every page and assert no gaps or duplicates, including inserts mid-walk.
```python
def test_paging_covers_all_rows_once(client, make_items):
    make_items(25)
    seen, cursor = [], None
    while True:
        r = client.get("/items", params={"limit": 10, **({"cursor": cursor} if cursor else {})}).json()
        seen += [i["id"] for i in r["items"]]
        cursor = r.get("next_cursor")
        if not cursor: break
    assert len(seen) == len(set(seen)) == 25
```

## Do
- Always apply a default limit and a hard maximum, and echo them in docs.
- Sort by a unique, stable key: `ORDER BY created_at DESC, id DESC`. Add the ID as a tiebreaker.
- Use keyset (seek) pagination: `WHERE (created_at, id) < (:c, :i)`, and back it with a composite index in the same order.
- Return an opaque cursor (base64 of the last key plus a sort or filter fingerprint). Clients must not parse it.
- Fetch `limit + 1` rows to decide `has_next` without a count query.
- Offer total counts only when needed, as a separate or estimated field, since `COUNT(*)` on large tables is slow.
- Reject a cursor that doesn't match the current sort or filters with 400.
- Allow offset only for small, static sets, and cap the offset.

## Avoid
- `OFFSET` on big tables: cost grows with the offset, and inserts or deletes shift rows so items repeat or vanish. Use keyset.
- Sorting by a non-unique column alone (`created_at`): ties split across pages unpredictably. Add the ID.
- Cursors that are raw IDs with the sort left implicit: they break when order changes. Encode the sort keys.
- A different filter on page two than on page one: results are inconsistent. Bind filters into the cursor.
- Unbounded `limit` from the client: a single request can pull the whole table. Clamp it.
- Computing `COUNT(*)` on every page request: use `has_next` or a cached approximate count.
- `NULL` sort keys in a keyset comparison: they compare unknown. Use `NULLS LAST` handling or a non-null key.

## Review
- [ ] Default and maximum limits are enforced and tested.
- [ ] Order is total (tiebreaker included) and supported by an index.
- [ ] The cursor is opaque, bound to sort and filters, and validated.
- [ ] A walk test proves no gaps or duplicates, including a mid-walk insert.
- [ ] No hidden total-count query on the hot path.
