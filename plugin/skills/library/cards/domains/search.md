---
name: search
title: Search
area: domains
tags: [search, elasticsearch, full-text, relevance, indexing, typesense]
detect: [dep:@elastic/elasticsearch, dep:elasticsearch, dep:meilisearch, dep:typesense, dep:algoliasearch, dep:@opensearch-project/opensearch, dep:opensearch-py, dep:lunr, dep:minisearch, dep:fuse.js]
related: [unicode, i18n, postgis, web-scraping]
---
Search features: choose the engine to fit scale, index what users query, analyze text per language, and test relevance with judged queries.

## Verify
- `psql -c "select to_tsvector('english','running dogs') @@ websearch_to_tsquery('english','run dog')"`: Postgres full-text stemming works (returns t).
- `curl -s localhost:9200/_cluster/health?pretty`: Elasticsearch or OpenSearch status is green or yellow.
- `curl -s localhost:7700/health`: Meilisearch is up.
- The relevance test suite: judged queries return expected documents at the top.

## Test first
Keep a small judged-query set; each query must return its expected hit in the top results.
```python
JUDGED = [
    ("blu sweater", "sku-123"),        # typo tolerance
    ("jackets women", "sku-777"),      # word order
    ("ß", "sku-straße"),               # folding
    ("iphone 15 case", "sku-case-15"), # numbers
]

import pytest
@pytest.mark.parametrize("query,expected", JUDGED)
def test_expected_hit_in_top_3(search, query, expected):
    ids = [h["id"] for h in search(query, limit=3)]
    assert expected in ids
```

## Do
- Start with the database: Postgres `tsvector` with a GIN index (and `pg_trgm` for fuzzy) covers many apps; add a search engine when you need facets, typo tolerance or scale.
- Treat the engine as a derived index: the database stays the source of truth; reindex from it, using an alias swap for zero-downtime rebuilds.
- Update the index through a queue or change events; handle deletes, and monitor lag.
- Choose analyzers per language (stemming, stopwords, ASCII folding); use separate fields for exact, stemmed and ngram matches with boosts.
- Define mappings explicitly: `keyword` for filters and facets, `text` for searching; disable dynamic mapping on production indexes.
- Paginate with `search_after` or cursors, not deep `from + size`.
- Apply authorization as filters inside the query so users never see forbidden docs.
- Log queries and zero-result searches; tune synonyms and ranking from them.
- Highlight snippets with escaped output.

## Avoid
- `LIKE '%term%'` on large tables: full scans. Use full-text or trigram indexes.
- Dynamic mapping in production: field type explosions and wrong types. Set mappings.
- Treating the search index as primary storage: loses data on rebuild. Keep the DB authoritative.
- Deep pagination (`from` of 10000 or more): slow and capped. Use cursors.
- Filtering permissions after the query: leaks counts and breaks pagination. Filter in the query.
- Passing raw user input to query syntax (`query_string`): errors and expensive wildcards. Use `match`, `simple_query_string` or the engine's safe API.
- Changing analyzers in place: existing documents keep old tokens. Reindex into a new index.
- Tuning relevance by anecdote: regressions. Use the judged set.
- Sending admin or write keys to the browser (Algolia, Typesense): use search-only scoped keys.

## Review
- [ ] Mappings and analyzers are explicit and match the languages served.
- [ ] Reindex path exists, tested, and zero-downtime.
- [ ] Permission filters are part of every query.
- [ ] Judged-query tests cover typos, numbers, accents and zero results.
- [ ] Only search-only keys reach clients.
