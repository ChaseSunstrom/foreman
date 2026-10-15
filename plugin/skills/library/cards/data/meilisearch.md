---
name: meilisearch
title: Meilisearch
area: data
tags: [meilisearch, search, index, ranking, typo-tolerance, tenant-tokens]
detect: [dep:meilisearch, dep:meilisearch-python]
related: [typesense, elasticsearch, postgres-full-text-search]
---
Meilisearch indexes: settings before documents, async task checking, filterable attributes and key scoping.

## Verify
- `curl -s localhost:7700/health`: returns status available.
- `curl -s localhost:7700/tasks?statuses=failed -H "Authorization: Bearer $KEY"`: no failed tasks; writes are asynchronous.
- `curl -s localhost:7700/indexes/products/settings -H "Authorization: Bearer $KEY"`: filterable, sortable and searchable attributes as intended.
- `curl -s -X POST localhost:7700/indexes/products/search -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' -d '{"q":"shoe","filter":"brand = nike"}'`: the filter works.

## Test first
Wait for tasks before asserting; writes return a task, not a result.
```python
def test_filter_and_typo_tolerance(client):
    idx = client.index("t")
    client.wait_for_task(idx.update_filterable_attributes(["brand"]).task_uid)
    client.wait_for_task(idx.add_documents([{"id": 1, "name": "sneaker", "brand": "nike"}]).task_uid)
    hits = idx.search("sneker", {"filter": "brand = nike"})["hits"]
    assert [h["id"] for h in hits] == [1]
```

## Do
- Configure settings (`filterableAttributes`, `sortableAttributes`, `searchableAttributes`, `rankingRules`, `synonyms`) before bulk importing, so indexing happens once.
- Set the primary key explicitly when creating the index.
- Add documents in large batches; poll `GET /tasks/{uid}` until succeeded.
- Keep documents small and flat; index only the fields you search or display.
- Use a search-only API key in clients and the master key only on the server; mint scoped keys with `indexes` and `actions`.
- Use tenant tokens (signed JWT with search rules) to enforce per-tenant filters on a public frontend.
- Use `attributesToRetrieve` and `attributesToHighlight` to shrink responses; paginate with `limit` and `offset` or `page`.
- Treat the database as source of truth and reindex from it; Meilisearch is a derived index.

## Avoid
- Filtering on an attribute not in `filterableAttributes`: error. Add it, and expect a reindex.
- Asserting right after `add_documents`: the task is queued. Wait for completion.
- Exposing the master key in browser code: full admin. Use search keys or tenant tokens.
- Changing settings after loading millions of documents repeatedly: each change triggers a reindex. Batch settings changes.
- Updating one document per request: task queue floods. Batch.
- Using it as the primary datastore: no transactions. Keep the source in a database.
- Putting huge text blobs into every document: index size and latency. Trim.

## Review
- [ ] Settings set up front and under version control.
- [ ] Tasks are awaited or monitored for failure.
- [ ] Browser clients use only search or tenant keys.
- [ ] Sync from the source of truth is replayable.
- [ ] Batches used for writes.
