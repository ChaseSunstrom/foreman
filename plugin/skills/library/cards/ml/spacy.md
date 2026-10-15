---
name: spacy
title: spaCy
area: ml
tags: [spacy, nlp, ner, pipelines, tokenization, training]
detect: [dep:spacy, file:config.cfg]
related: [transformers, data-labeling, hf-datasets, sklearn-pipelines]
---
spaCy NLP pipelines: load models once, batch with nlp.pipe, train from a config with held-out evaluation.

## Verify
- `python -m spacy validate`: installed models are compatible with the spaCy version.
- `python -m spacy debug data config.cfg`: training data statistics and format problems.
- `python -m spacy evaluate model-best data/dev.spacy`: precision, recall and F-score on the dev set.
- `pytest -q tests/test_nlp.py`: pipeline outputs on fixture sentences.

## Test first
```python
import spacy

def test_ner_finds_org():
    nlp = spacy.load("models/model-best")
    doc = nlp("Acme Corp hired Dana in Paris.")
    assert ("Acme Corp", "ORG") in [(e.text, e.label_) for e in doc.ents]
```

## Do
- Load with `spacy.load(name)` once at startup and exclude unused components (`exclude=["parser"]`) for speed.
- Process many texts with `nlp.pipe(texts, batch_size=..., n_process=...)`, not a Python loop of calls.
- Train via `python -m spacy train config.cfg`; generate the config with `spacy init config` and keep it in version control.
- Convert annotations to `DocBin` `.spacy` files; use separate train and dev sets split by source document.
- Evaluate per label and examine errors; add rules with `EntityRuler` or `Matcher` for high-precision cases.
- Pin the spaCy version and model package; models are tied to the library version.
- Set seeds in the config and record the config used for every model.
- Add a transformer component only when a measured gain justifies the cost.

## Avoid
- Calling `nlp(text)` one text at a time in a loop: slow. Use `nlp.pipe`.
- Loading the model inside a request handler: seconds per call. Load once.
- Overlapping entity spans in training data: errors or dropped labels. Check with `debug data`.
- Evaluating on training documents or near duplicates: inflated scores. Hold out by source.
- Using a small model's vectors for similarity: weak vectors. Use a model with real vectors or embeddings.
- Mixing model and library versions: load errors or silent differences. Run `spacy validate`.

## Review
- [ ] Model loaded once; unused components excluded.
- [ ] Batch processing with `nlp.pipe`.
- [ ] Config and versions pinned in the repo.
- [ ] Dev split is independent; per-label scores reviewed.
- [ ] Rules complement the statistical model where needed.
