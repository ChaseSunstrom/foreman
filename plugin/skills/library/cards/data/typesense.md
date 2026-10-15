---
name: typesense
title: Typesense
area: data
tags: [typesense, search, collections, schema, typo-tolerance, scoped-keys]
detect: [dep:typesense, dep:typesense-python]
related: [meilisearch, elasticsearch, postgres-full-text-search]
---
Typesense collections: explicit schemas, import with action, query_by weights, scoped keys, aliases for reindexing.

## Verify
- `curl -s localhost:8108/health`: returns ok true.
- `curl -s localhost:8108/collections/products -H "X-TYPESENSE-API-KEY: $KEY"`: the schema, num_documents and field facets and types.
- `curl -s "localhost:8108/collections/products/documents/search?q=shoe&query_by=name&filter_by=price:<100" -H "X-TYPESENSE-API-KEY: $KEY"`: query and filter behave.
- `curl -s localhost:8108/aliases -H "X-TYPESENSE-API-KEY: $KEY"`: aliases point at the live collection.

## Test first
Create a throwaway collection and test search semantics.
```python
def test_filter_and_typo(client):
    client.collections.create({"name": "t", "fields": [
        {"name": "name", "type": "string"}, {"name": "price", "type": "int32"}]})
    client.collections["t"].documents.import_([{"name": "sneaker", "price": 50}], {"action": "upsert"})
    r = client.collections["t"].documents.search({"q": "sneker", "query_by": "name", "filter_by": "price:<100"})
    assert r["found"] == 1
```

## Do
- Define the schema explicitly; mark fields `facet: true`, `sort_by`-able numeric fields and `optional: true` where needed.
- Import with the bulk endpoint and `action=upsert` (or `emplace`) in JSONL batches; check the per-line success results.
- Use `query_by` with several fields and `query_by_weights` to rank; set `num_typos` and `prefix` per need.
- Reindex without downtime: build a new versioned collection, then repoint an alias with `PUT /aliases/products`.
- Generate scoped search keys with an embedded `filter_by` for per-tenant access, from a parent search-only key.
- Keep the admin key on the server only.
- Use `sort_by` with a tie-breaker and `_text_match` when combining relevance and business signals.
- Use a cluster of 3 nodes for production high availability.

## Avoid
- Assuming import fails loudly: the response is a line per document, and bad documents are reported there with HTTP 200. Parse the results.
- Using the admin API key in the browser: use a search-only or scoped key.
- Auto-schema (`.*` fields) in production: wrong inferred types. Declare the types.
- Changing a field type in place: unsupported. Create a new collection and swap the alias.
- Filtering on a field that was not indexed (`index: false`): no results or error. Keep it indexed.
- Querying fields that are not in `query_by`: no matches.
- A single node for critical search: downtime during restarts.

## Review
- [ ] Explicit schema with correct types and facets.
- [ ] Import results inspected for failures.
- [ ] Reindex flow uses versioned collections and aliases.
- [ ] Client-side keys are scoped.
- [ ] Source of truth lives elsewhere and is replayable.
