---
name: postgres-full-text-search
title: PostgreSQL full-text search
area: data
tags: [postgres, search, tsvector, gin, ranking, trigram]
detect: []
related: [postgres, postgres-indexes, elasticsearch, meilisearch]
---
Built-in search with tsvector, GIN and ranking; trigram for fuzzy and prefix matching.

## Verify
- `psql -c "EXPLAIN ANALYZE SELECT id FROM docs WHERE search @@ websearch_to_tsquery('english','fast index')"`: the GIN index is used.
- `psql -c "SELECT to_tsvector('english','The running dogs')"`: shows stemming and stop-word removal.
- `psql -c "SELECT * FROM pg_extension WHERE extname = 'pg_trgm'"`: trigram extension installed when fuzzy search is needed.

## Test first
Assert on stemming, ranking and user-input safety.
```python
def test_search_stems_and_survives_garbage(db):
    db.execute("INSERT INTO docs(body) VALUES ('running dogs'),('cats')")
    assert db.execute("SELECT count(*) FROM docs WHERE search @@ websearch_to_tsquery('english','dog')").fetchone()[0] == 1
    db.execute("SELECT count(*) FROM docs WHERE search @@ websearch_to_tsquery('english','\") & (| !')")  # no error
```

## Do
- Store a generated column: `search tsvector GENERATED ALWAYS AS (setweight(to_tsvector('english', title),'A') || setweight(to_tsvector('english', body),'B')) STORED`, with `CREATE INDEX ON docs USING gin (search)`.
- Use `websearch_to_tsquery` for raw user input; it never raises on syntax.
- Rank with `ts_rank_cd(search, query)` and order by it, with a LIMIT.
- Pass the regconfig explicitly in both the vector and the query, so the index expression matches.
- Highlight with `ts_headline` on the top results only, not the whole match set.
- Fuzzy or prefix: `CREATE INDEX ON t USING gin (name gin_trgm_ops)` and `name % 'term'` or `ILIKE '%term%'`.
- Prefix terms in tsquery: `to_tsquery('english','pre:*')`.

## Avoid
- `to_tsquery` on raw user input: syntax errors and injection-like failures. Use `websearch_to_tsquery` or `plainto_tsquery`.
- `to_tsvector(col)` without a config: depends on `default_text_search_config`, and cannot be used in an index expression. Always name the config.
- Computing `to_tsvector` per row at query time with no index: seq scan. Store and index it.
- Ranking the entire result set before limiting: very slow on common words. Filter first, rank the top.
- Using `LIKE '%x%'` for search at scale: use trigram GIN.
- Expecting typo tolerance from tsvector: it has none; use pg_trgm or a search engine.

## Review
- [ ] Query and index use the same language config.
- [ ] User input goes through `websearch_to_tsquery`.
- [ ] EXPLAIN shows a GIN bitmap scan.
- [ ] Weights and ranking checked against sample queries.
- [ ] Scale ceiling noted; an external engine considered past it.
