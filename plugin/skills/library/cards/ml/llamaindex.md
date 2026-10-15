---
name: llamaindex
title: LlamaIndex
area: ml
tags: [python, llm, rag, indexing, query-engine, agents]
detect: [dep:llama-index, dep:llama-index-core, dep:llama-index-llms-anthropic]
related: [rag, langchain, qdrant, chroma, llm-evals]
---
LlamaIndex data apps: documents to nodes, vector indexes, retrievers and query engines, with global Settings for the LLM and embeddings.

## Verify
- `python -c "import llama_index.core as li; print(li.__version__)"`: the core package imports.
- `pytest -q`: ingestion and retrieval tests pass with mock models.
- `pip check`: integration packages are compatible with core.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Use `MockLLM` and `MockEmbedding` so the pipeline runs offline, and assert on retrieved nodes.
```python
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.embeddings import MockEmbedding
from llama_index.core.llms import MockLLM

def test_retriever_returns_source_nodes():
    Settings.llm = MockLLM()
    Settings.embed_model = MockEmbedding(embed_dim=8)
    idx = VectorStoreIndex.from_documents([Document(text="alpha", metadata={"src": "a"})])
    nodes = idx.as_retriever(similarity_top_k=1).retrieve("alpha")
    assert nodes[0].node.metadata["src"] == "a"
```

## Do
- Import from `llama_index.core`, and install each integration as its own package (`llama-index-llms-...`, `llama-index-vector-stores-...`).
- Configure `Settings.llm` and `Settings.embed_model` once at startup.
- Pick the node parser deliberately (`SentenceSplitter` with `chunk_size` and `chunk_overlap`), and attach metadata to documents.
- Use an external vector store with `StorageContext` for anything beyond a demo, and `persist` or reload instead of re-embedding.
- Build an `IngestionPipeline` with a docstore so reruns skip unchanged documents.
- Check `response.source_nodes` for citations and scores. Add a reranker postprocessor when top-k is noisy.
- Use metadata filters for tenants and permissions.

## Avoid
- `from llama_index import ...` and `ServiceContext`: removed in the modular layout. Use `llama_index.core` and `Settings`.
- Relying on the default OpenAI LLM and embeddings when you meant another provider: silent key errors or wrong models. Set `Settings` explicitly.
- Re-embedding on each app start: slow and costly. Persist the index or use a vector store.
- Changing the embedding model against an existing index: mismatched vectors. Rebuild.
- Trusting retrieved text as instructions: prompt injection. Treat nodes as data.
- Ignoring `source_nodes`: answers cannot be audited. Surface them.
- Tests using a real LLM: flaky. Use `MockLLM` and `MockEmbedding`.

## Review
- [ ] Settings for LLM and embeddings are explicit.
- [ ] Index persistence and incremental ingestion are in place.
- [ ] Chunking parameters were checked against retrieval quality.
- [ ] Sources are returned with answers and filtered by permission.
- [ ] Tests run offline with mock models.
