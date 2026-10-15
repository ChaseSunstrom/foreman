---
name: chroma
title: Chroma
area: ml
tags: [vector-database, embeddings, search, python, rag, chroma]
detect: [dep:chromadb, dep:langchain-chroma, dep:llama-index-vector-stores-chroma]
related: [rag, qdrant, langchain, llamaindex]
---
Chroma embedded vector store: persistent clients, collections with an embedding function, add and query with metadata filters.

## Verify
- `python -c "import chromadb; print(chromadb.__version__)"`: installed version.
- `pytest -q`: collection and query tests pass using an ephemeral client.
- `python -c "import chromadb; c=chromadb.EphemeralClient(); print(c.heartbeat())"`: the client starts in memory.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Use an ephemeral client and supply embeddings yourself so the test needs no model download.
```python
import chromadb

def test_where_filter_and_ids():
    c = chromadb.EphemeralClient()
    col = c.get_or_create_collection("t", metadata={"hnsw:space": "cosine"})
    col.add(ids=["a", "b"], embeddings=[[1, 0], [1, 0.1]],
            metadatas=[{"tenant": "x"}, {"tenant": "y"}], documents=["da", "db"])
    r = col.query(query_embeddings=[[1, 0]], n_results=2, where={"tenant": "y"})
    assert r["ids"][0] == ["b"]
```

## Do
- Use `PersistentClient(path=...)` for local durable data, `EphemeralClient` for tests, `HttpClient` for a server.
- Pass the same embedding function every time you open a collection, or supply embeddings explicitly.
- Choose the distance at creation (`hnsw:space` or the configuration API): the default is L2, set cosine for text embeddings.
- Use deterministic ids and `upsert` to make ingestion repeatable.
- Store source and tenant in metadata, and filter with `where` and `where_document`.
- Batch adds below the client's maximum batch size.
- Read results as lists per query: `ids[0]`, `distances[0]`, `documents[0]`.
- Use `include=[...]` to fetch only the fields you need.

## Avoid
- Changing the embedding model for an existing collection: dimensions or semantics mismatch. Create a new collection and re-embed.
- Assuming the default distance is cosine: it is L2, so scores mislead. Set it at creation.
- `add` with an existing id: ignored or duplicated. Use `upsert`.
- Treating `distances` as similarities: lower is closer. Convert before thresholding.
- Sharing one `PersistentClient` path between several processes: corruption risk. Use the server mode.
- Metadata values that are lists or nested dicts: unsupported. Flatten to str, int, float or bool.
- The removed legacy `Client(Settings(chroma_db_impl=...))` setup: use the current client constructors.

## Review
- [ ] Distance and embedding function are fixed and recorded with the collection.
- [ ] Ids are stable and ingestion uses upsert.
- [ ] Metadata is flat and filters are tested.
- [ ] Persistence path is owned by one process.
- [ ] Tests use the ephemeral client and explicit embeddings.
