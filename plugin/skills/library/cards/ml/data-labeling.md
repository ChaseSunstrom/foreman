---
name: data-labeling
title: Data labeling
area: ml
tags: [labeling, annotation, agreement, quality, guidelines, active-learning]
detect: [dep:label-studio, dep:cleanlab, dep:argilla, dep:doccano]
related: [llm-evals, yolo, spacy, model-cards, hf-datasets]
---
Produce reliable labels with written guidelines, measured inter-annotator agreement, a gold set and audit loops.

## Verify
- `pytest -q tests/test_labels.py`: schema, class set, duplicates and empty fields are valid.
- `python -m tools.agreement --file labels.jsonl`: agreement (Cohen or Krippendorff alpha) per class and overall.
- `python -m tools.audit --sample 100`: a reviewed sample reports the label error rate.

## Test first
```python
import json

def test_labels_valid_and_unique():
    rows = [json.loads(l) for l in open("labels.jsonl")]
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids))
    assert all(r["label"] in {"pos", "neg", "unsure"} for r in rows)
```

## Do
- Write guidelines with definitions, decision rules, edge cases and examples; version them.
- Pilot on a small batch, compute agreement, resolve disagreements and refine the guidelines before scaling.
- Have at least two annotators on a sampled overlap; adjudicate conflicts and record who decided.
- Keep a gold set labelled by experts and use it to monitor annotator quality.
- Allow an explicit "unsure" or "other" label and track its rate.
- Split train, dev and test by source before labelling extras, and never let test items be relabelled from model predictions.
- Use model pre-labels only with review, and measure the anchoring effect by comparing to blind labels on a sample.
- Search for noisy labels (confident-learning tools or disagreement with a model) and send them to review.
- Store raw annotations, annotator ids, timestamps and guideline version.

## Avoid
- Scaling before measuring agreement: low agreement means the task is ill-defined. Fix the guidelines first.
- Majority vote hiding systematic disagreement: inspect per-class confusions.
- Using LLM labels as ground truth for the test set: circular evaluation. Use human gold labels.
- Duplicates across splits: leakage. Deduplicate before splitting.
- Throwing away annotator disagreement: it carries signal on ambiguous items. Keep raw annotations.
- Paying per item with no quality checks: speed beats care. Use gold checks.

## Review
- [ ] Guidelines versioned with examples.
- [ ] Agreement measured and acceptable.
- [ ] Gold set and audit sample used.
- [ ] No duplicates across splits.
- [ ] Raw annotations and metadata stored.
