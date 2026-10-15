---
name: embeddings
title: Embeddings
area: ml
tags: [embeddings, vectors, similarity, retrieval, normalization, search]
detect: [dep:sentence-transformers, dep:voyageai, dep:faiss-cpu, dep:faiss-gpu]
related: [rag, reranking, chunking, qdrant, chroma]
---
Text embeddings for search and clustering: pick the model by eval, normalise consistently, and version the index with the model.

## Verify
- `pytest -q tests/test_embed.py`: dimension, normalisation and determinism checks pass.
- `python -m evals.retrieval --k 10`: recall@10 and MRR on a labelled query set meet the baseline.
- `python -c "from app.embed import dim; print(dim())"`: index dimension matches the model in use.

## Test first
Test the property retrieval depends on.
```python
import numpy as np
from app.embed import embed

def test_vectors_are_unit_norm_and_paraphrase_is_closer():
    a, b, c = embed(["reset my password", "I forgot my password", "pizza recipe"])
    assert abs(np.linalg.norm(a) - 1) < 1e-3
    assert a @ b > a @ c
```

## Do
- Choose the model with a retrieval eval on your own queries and documents, not a leaderboard.
- Use the model's query and document modes or prefixes when it defines them; apply the same ones at index and query time.
- Normalise to unit length and use cosine or inner product consistently with the index metric.
- Store model name, dimension and chunking params with the index; re-embed everything when any changes.
- Batch requests and cache by content hash to avoid paying twice.
- Truncate or chunk to the model's max tokens explicitly instead of letting it clip silently.
- Use float32 for the index; consider lower dimensions or quantisation only after measuring recall.

## Avoid
- Mixing vectors from two models in one index: distances are meaningless. Version and rebuild.
- Euclidean index with unnormalised vectors when the model expects cosine: wrong ranking. Normalise or switch metric.
- Skipping the query prefix the model needs: recall drops quietly. Follow the model's usage.
- Embedding huge documents whole: the tail is dropped. Chunk first.
- Judging quality by a handful of queries: build a labelled set.
- Embedding private text through a third-party API without checking policy.

## Review
- [ ] Model chosen by eval; recall metric recorded.
- [ ] Same model, prefix and normalisation at index and query time.
- [ ] Index stores model and dimension metadata.
- [ ] Inputs fit the token limit.
- [ ] Embeddings cached by content hash.
