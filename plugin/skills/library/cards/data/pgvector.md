---
name: pgvector
title: pgvector
area: data
tags: [pgvector, postgres, embeddings, vector-search, hnsw, ivfflat]
detect: [dep:pgvector, dep:pgvector-python, dep:pgvector-node, dep:pgvector-go, dep:pgvector-rust, dep:Pgvector, dep:langchain-postgres]
related: [postgres, query-tuning, sql-migrations]
---
pgvector: embeddings in Postgres with a fixed dimension, the right distance operator, and an index that matches it.

## Verify
- `psql "$DATABASE_URL" -c "SELECT extname, extversion FROM pg_extension WHERE extname='vector';"`: extension is installed.
- `psql "$DATABASE_URL" -c "\d+ items"`: vector column dimension and the index (hnsw or ivfflat) with its operator class.
- `psql "$DATABASE_URL" -c "EXPLAIN (ANALYZE) SELECT id FROM items ORDER BY embedding <=> '[...]' LIMIT 5;"`: the plan uses the vector index, not a seq scan.
- `psql "$DATABASE_URL" -c "SHOW hnsw.ef_search;"`: query-time recall setting.

## Test first
Insert known vectors and assert nearest-neighbor order.
```python
def test_nearest_is_closest(db):
    db.execute("insert into items(id, embedding) values (1,'[1,0,0]'),(2,'[0,1,0]')")
    row = db.execute("select id from items order by embedding <=> '[0.9,0.1,0]' limit 1").fetchone()
    assert row[0] == 1
```

## Do
- `CREATE EXTENSION vector;` then `embedding vector(1536)` with the exact dimension of your model.
- Pick the operator for the metric: `<->` L2, `<=>` cosine, `<#>` negative inner product, and an index operator class to match (`vector_cosine_ops`).
- Use HNSW for most cases: `CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);` or IVFFlat after loading data, with `lists` sized to rows.
- Raise recall at query time with `SET hnsw.ef_search` (or `ivfflat.probes`).
- Combine with filters carefully: add a B-tree on the filter column or partition, and check the plan.
- Register types with the driver (`pgvector.psycopg.register_vector`, `pgvector.asyncpg`) and pass vectors as typed values.
- Normalize embeddings when using inner product; store the model name and version beside each vector.

## Avoid
- Operator and index class mismatch (query `<=>` with an `vector_l2_ops` index): the index is ignored and it seq-scans. Match them.
- Dimension mismatch on insert (new embedding model): errors or garbage. Use a new column and backfill.
- Building IVFFlat before loading data: poor clusters. Build after data exists.
- Expecting exact results from an ANN index: recall is approximate. Tune `ef_search`, or verify with an unindexed query.
- Filtering after a top-K ANN search and getting fewer than K rows: raise the limit or use iterative scan settings where supported.
- String-building vector literals into SQL: bind a parameter.
- Embeddings in a table row with huge unrelated columns: bloat. Store vectors in a side table.

## Review
- [ ] Column dimension equals the model's output size.
- [ ] Distance operator and index operator class agree; EXPLAIN uses the index.
- [ ] Recall was measured against exact search on a sample.
- [ ] Embedding model identity is recorded for re-embedding.
- [ ] Filters plus vector queries are tested together.
