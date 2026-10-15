---
name: rag
title: Retrieval-augmented generation
area: ml
tags: [rag, llm, retrieval, embeddings, chunking, reranking]
detect: []
related: [qdrant, chroma, llamaindex, langchain, llm-evals, anthropic-sdk]
---
RAG pipelines: ingest, chunk, embed, retrieve, optionally rerank, then answer from cited context, with retrieval measured on its own.

## Verify
- `pytest -q tests/retrieval`: recall at k on a labeled query set meets the threshold.
- `python -m evals.run --suite rag`: answer faithfulness and citation checks pass (your own harness).
- `python -c "from mypkg.ingest import chunk; print(max(len(c) for c in chunk(open('sample.txt').read())))"`: chunks respect the size limit.

## Test first
Label queries with the document that should answer them. Test retrieval alone, before the LLM.
```python
from mypkg.rag import retrieve

QUERIES = [("how do I reset my password", "doc-auth-12"),
           ("refund window", "doc-billing-3")]

def test_recall_at_5():
    hits = sum(any(r.doc_id == want for r in retrieve(q, k=5)) for q, want in QUERIES)
    assert hits / len(QUERIES) >= 0.9
```

## Do
- Chunk on structure first (headings, paragraphs), then by size with modest overlap. Keep title and source in each chunk's metadata.
- Use one embedding model for documents and queries, record its name with the index, and re-embed everything when it changes.
- Combine dense search with keyword (BM25) search and merge results when queries contain exact terms or ids.
- Retrieve wide (20 to 50), rerank, then pass only the top few to the model.
- Filter by metadata (tenant, permissions, date) in the query itself, not after generation.
- Instruct the model to answer only from the provided context, cite chunk ids, and say when the context is insufficient.
- Put documents in a stable, cacheable prefix when many questions hit the same context.
- Make ingestion idempotent with stable chunk ids, so re-runs update rather than duplicate.

## Avoid
- Judging only the final answer: retrieval failures and generation failures look the same. Measure recall and faithfulness separately.
- Mixing embedding models or distance metrics between index and query: nonsense neighbors. Pin both.
- Huge chunks or tiny fragments: diluted or context-free matches. Tune size on the recall set.
- Skipping access control at retrieval: leaks other users' documents. Filter by permission on every query.
- Treating retrieved text as trusted instructions: prompt injection. Delimit it and tell the model it is data.
- Stuffing every retrieved chunk into the prompt: cost and distraction. Rerank and cap.
- Never refreshing the index: stale answers. Schedule re-ingestion and delete removed documents.

## Review
- [ ] Retrieval recall is measured on a labeled set, separate from answer quality.
- [ ] Embedding model and metric are recorded and consistent.
- [ ] Permission and tenant filters apply inside the query.
- [ ] Answers cite sources and handle "not found".
- [ ] Ingestion is idempotent and removes deleted documents.
