---
name: elasticsearch
title: Elasticsearch / OpenSearch
area: data
tags: [search, elasticsearch, opensearch, mappings, analyzers, indexing]
detect: [dep:elasticsearch, dep:@elastic/elasticsearch, dep:opensearch-py, dep:@opensearch-project/opensearch, dep:elasticsearch-java, dep:olivere/elastic, dep:Elastic.Clients.Elasticsearch]
related: [kafka, query-tuning, etl-pipelines]
---
Elasticsearch/OpenSearch: explicit mappings, bulk indexing, aliases for reindexing, filters over scoring where possible.

## Verify
- `curl -s "$ES/_cluster/health?pretty"`: status is green or an understood yellow.
- `curl -s "$ES/index/_mapping?pretty"`: field types match what the code sends.
- `curl -s "$ES/index/_search?pretty" -H 'Content-Type: application/json' -d '{"query":{...},"explain":true}'`: why a hit scored as it did.
- `curl -s -X POST "$ES/index/_analyze?pretty" -H 'Content-Type: application/json' -d '{"analyzer":"standard","text":"..."}'`: tokens an analyzer produces.

## Test first
Run a real node in a container; create the index from the same mapping code as production.
```python
def test_search_matches_prefix(es):
    es.index(index="t", id=1, document={"name": "Widget"}, refresh=True)
    r = es.search(index="t", query={"match": {"name": "widg*"}})
    assert r["hits"]["total"]["value"] == 1
```
Fails until the analyzer/mapping supports the lookup. Use `refresh=True` in tests only.

## Do
- Define mappings explicitly (`dynamic: strict` or `false`); use `keyword` for exact match/aggregation and `text` for full text.
- Put non-scoring conditions in `bool.filter` so they cache.
- Index with the bulk API and check per-item errors in the response.
- Serve reads through an alias; reindex into a new versioned index and swap the alias atomically.
- Paginate deep results with `search_after` plus a point-in-time, not `from`/`size`.
- Set shard count deliberately; avoid many tiny shards.
- Use `_source` filtering to return only needed fields.

## Avoid
- Dynamic mapping on user-supplied JSON: mapping explosion and wrong types. Set `dynamic: strict`.
- Aggregating or sorting on `text` fields: errors or fielddata blowup. Use a `keyword` subfield.
- `from + size` beyond `index.max_result_window`: fails or is slow. Use `search_after`.
- Treating it as the system of record: no transactions. Keep the source in a database and reindex from it.
- Ignoring bulk response `errors: true`: silent partial failures. Iterate items.
- `refresh=true` on every write in production: kills indexing throughput. Rely on the refresh interval.
- Changing a field's type in place: not allowed. Reindex.

## Review
- [ ] Mapping is explicit and reviewed; analyzers fit the language.
- [ ] Bulk results are checked for per-item errors.
- [ ] Reads go through an alias; a reindex path exists.
- [ ] Filters are in filter context; deep pagination uses search_after.
- [ ] Source-of-truth data exists elsewhere.
