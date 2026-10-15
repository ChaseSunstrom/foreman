---
name: reranking
title: Reranking
area: ml
tags: [reranking, retrieval, cross-encoder, rag, hybrid-search, ranking]
detect: [dep:rank-bm25, dep:flashrank]
related: [rag, embeddings, chunking, llm-evals]
---
Rerank a wide first-stage candidate set with a cross-encoder or LLM scorer so only the best passages reach the model.

## Verify
- `pytest -q tests/test_rerank.py`: ordering, top-k cut and ties behave on fixed inputs.
- `python -m evals.retrieval --rerank on --k 5`: nDCG or recall@5 beats the first-stage baseline.
- `python -m evals.latency --rerank`: p95 added latency stays within budget.

## Test first
```python
from app.rerank import rerank

def test_relevant_doc_moves_to_top():
    docs = ["cats are mammals", "reset password steps", "weather today"]
    out = rerank("how do I reset my password", docs, top_k=2)
    assert out[0] == "reset password steps" and len(out) == 2
```

## Do
- Retrieve generously (for example 50 to 100 candidates) with dense, BM25 or both fused, then rerank down to 3 to 10.
- Fuse hybrid lists with reciprocal rank fusion before reranking; do not mix raw scores from different scorers.
- Score query and passage pairs together with a cross-encoder; batch pairs and cap passage length.
- For an LLM reranker, ask for a structured score per id and validate the output; keep it deterministic.
- Measure with a labelled set: compare recall@k and nDCG with and without the reranker.
- Cache scores by query and document hash; set a latency budget and a fallback to first-stage order on timeout.
- Keep the candidate count and cutoff as config, tuned on the eval.

## Avoid
- Reranking only 5 candidates: the right passage was never retrieved. Widen stage one.
- Comparing scores across queries or models: only the order within a query is meaningful. Rank, do not threshold, unless calibrated.
- Truncating passages mid-sentence to fit: score loss. Chunk sensibly first.
- Adding a reranker with no eval: latency and cost with unknown gain. Measure.
- LLM reranker over unbounded candidates: cost explosion. Cap and batch.
- Tuning the cutoff on the test set: hold out.

## Review
- [ ] Candidate and final k are config values tied to eval results.
- [ ] Improvement over baseline demonstrated.
- [ ] Latency budget and timeout fallback exist.
- [ ] Hybrid lists fused by rank, not raw score.
- [ ] Inputs length-capped.
