---
name: recommendations
title: Recommendations
area: domains
tags: [recommendations, ranking, cold-start, collaborative-filtering, evaluation, diversity]
detect: [dep:implicit, dep:lightfm]
related: [ab-testing, search-autocomplete, analytics-events, search]
---
Recommenders: start with popularity and co-occurrence, evaluate offline with time splits, handle cold start, filter seen items, then A/B test.

## Verify
- `pytest -q tests/test_recs.py`: candidate, filter and metric tests pass.
- `python -m app.recs.evaluate --split time`: offline recall@k or NDCG on a temporal split (your own script; it must not use a random split).
- `pytest -q -k "cold_start or seen"`: new users and already-seen items behave.

## Test first
Never recommend what the user already has, and never fail for a new user.
```python
from app.recs import recommend

def test_excludes_owned_and_falls_back_for_new_user(store):
    store.interactions = {"u1": ["a", "b"]}
    store.popular = ["a", "c", "d"]
    assert recommend(store, "u1", k=2) == ["c", "d"]
    assert recommend(store, "new", k=2) == ["a", "c"]     # popularity fallback
    assert len(set(recommend(store, "u1", k=2))) == 2     # no duplicates
```

## Do
- Ship a baseline first: popular items, recent items, or item-to-item co-occurrence counts. Beat it before adding models.
- Two stages: cheap candidate generation (hundreds), then a ranker; apply business rules after.
- Log impressions, not only clicks, so you can compute click-through and train unbiased.
- Evaluate with a time-based split per user; metrics: recall@k, NDCG, coverage, and diversity.
- Filter seen, purchased, out-of-stock and blocked items every time.
- Handle cold start: content features, onboarding picks, and popularity within segment.
- Add exploration (a small random slice) so the model can learn about unshown items.
- Precompute per-user lists on a schedule and cache; fall back if stale or missing.
- Provide a "why" signal when possible, and an opt-out.

## Avoid
- Random train/test splits: leak the future. Split by time.
- Training only on clicked items: feedback loop and popularity bias. Log impressions and explore.
- Recommending near-duplicates (all one brand or series): rerank for diversity.
- Treating implicit zeros as dislikes: missing is unknown. Use implicit-feedback methods and confidence weights.
- Shipping on offline metrics alone: confirm with an online experiment.
- Recomputing at request time with heavy models: latency. Precompute or ANN-index.

## Review
- [ ] Baseline exists and is compared against.
- [ ] Offline eval is time-split.
- [ ] Seen and unavailable items are filtered.
- [ ] Cold-start path tested.
- [ ] Impressions are logged for later training.
