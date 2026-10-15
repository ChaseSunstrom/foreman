---
name: chunking
title: Chunking
area: ml
tags: [chunking, rag, retrieval, splitting, tokens, documents]
detect: []
related: [rag, embeddings, reranking, llamaindex, langchain]
---
Split documents into retrievable chunks that respect structure, fit the embedding model and keep enough context to be answerable.

## Verify
- `pytest -q tests/test_chunk.py`: size limits, overlap and no-lost-text properties pass.
- `python -m evals.retrieval --chunk-size 400 --k 5`: recall for the chosen size on a labelled set.
- `python -m app.chunk --stats data/docs`: token-length distribution has no chunk over the model limit.

## Test first
Assert the invariants, not exact splits.
```python
from app.chunk import chunk

def test_no_text_lost_and_size_capped():
    text = ("Sentence one. " * 300).strip()
    parts = chunk(text, max_tokens=100, overlap=10)
    assert all(count_tokens(p) <= 100 for p in parts)
    assert all(w in " ".join(parts) for w in ["Sentence", "one."])
```

## Do
- Split on structure first (headings, paragraphs, code blocks, table rows), then by sentences, then by tokens as a last resort.
- Measure size in tokens of the embedding model's tokenizer, not characters.
- Use modest overlap (about 10 to 15 percent) only where structure cannot be respected.
- Attach metadata to each chunk: source, section path, page, offsets; prepend the title or section path to the embedded text.
- Keep tables, lists and code blocks whole where possible; split tables by row groups with the header repeated.
- Choose size by retrieval eval; try two or three sizes and keep the best.
- Make chunk ids deterministic (hash of source and span) so re-indexing upserts rather than duplicates.

## Avoid
- Fixed 1000-character splits through sentences, code and tables: broken meaning. Split on structure.
- Chunks above the embedder's token limit: silent truncation. Enforce the cap.
- Tiny chunks without context: pronouns lose referents. Add section titles or parent context.
- Large chunks that dilute the embedding: the match is vague. Test smaller sizes.
- Dropping metadata: no citations or filtering later. Store it.
- Re-chunking without re-embedding and replacing old vectors: stale entries remain. Version the index.

## Review
- [ ] Chunk size, overlap and splitter recorded as config.
- [ ] Token cap enforced against the real tokenizer.
- [ ] Metadata and deterministic ids present.
- [ ] Tables and code handled specially.
- [ ] Size chosen from an eval, not by default.
