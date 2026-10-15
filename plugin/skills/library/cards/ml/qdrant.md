---
name: qdrant
title: Qdrant
area: ml
tags: [vector-database, embeddings, search, python, rag, qdrant]
detect: [dep:qdrant-client, dep:@qdrant/js-client-rest, dep:llama-index-vector-stores-qdrant, dep:langchain-qdrant]
related: [rag, chroma, llamaindex, langchain]
---
Qdrant vector search: collections with a fixed vector size and distance, points with payloads, filtered queries and payload indexes.

## Verify
- `python -c "from qdrant_client import QdrantClient; c=QdrantClient(':memory:'); print(c.get_collections())"`: the client works with the in-memory mode used in tests.
- `pytest -q`: collection, upsert and search tests pass.
- `curl -s localhost:6333/collections`: a running server answers and lists collections.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Use `QdrantClient(":memory:")` with tiny hand-made vectors, so nearest neighbors are known.
```python
from qdrant_client import QdrantClient, models

def test_filter_restricts_results():
    c = QdrantClient(":memory:")
    c.create_collection("t", vectors_config=models.VectorParams(size=2, distance=models.Distance.COSINE))
    c.upsert("t", points=[
        models.PointStruct(id=1, vector=[1, 0], payload={"tenant": "a"}),
        models.PointStruct(id=2, vector=[1, 0.1], payload={"tenant": "b"})])
    f = models.Filter(must=[models.FieldCondition(key="tenant", match=models.MatchValue(value="b"))])
    hits = c.query_points("t", query=[1, 0], query_filter=f, limit=3).points
    assert [h.id for h in hits] == [2]
```

## Do
- Set `VectorParams(size=..., distance=...)` to match the embedding model. Use `COSINE` for normalized text embeddings.
- Use stable point ids (an int or a UUID derived from the content) so upserts are idempotent.
- Store source, tenant and timestamps in the payload, and create payload indexes (`create_payload_index`) on fields you filter by.
- Upsert in batches, and use `query_points` for search in current clients.
- Apply tenant and permission filters in every query.
- Use named vectors for several embeddings per point, and sparse vectors for hybrid search.
- Enable scalar or binary quantization only after checking recall on a labeled set.
- Set an API key and TLS on any non-local server.

## Avoid
- Creating a collection whose size differs from the embedding output: upserts fail. Read the size from the model.
- `recreate_collection` in app startup: deletes data. Check `collection_exists` and create only when missing.
- Filtering on unindexed payload fields at scale: slow scans. Create payload indexes.
- Random UUIDs as ids on each ingest run: duplicates pile up. Derive ids from content.
- The old `search` call in new code: deprecated in favor of `query_points`. Use the latter.
- Exposing port 6333 without an API key: open read and write access. Configure auth and network limits.
- Judging quantization or HNSW tweaks by eye: recall can drop silently. Measure.

## Review
- [ ] Collection size and distance match the embedding model.
- [ ] Ids are deterministic and upserts are idempotent.
- [ ] Filtered fields have payload indexes.
- [ ] Tenant filters are in every query path.
- [ ] Tests use the in-memory client.
