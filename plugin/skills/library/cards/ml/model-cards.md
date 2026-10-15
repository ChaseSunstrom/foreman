---
name: model-cards
title: Model cards
area: ml
tags: [model-card, documentation, evaluation, bias, limitations, governance]
detect: [file:MODEL_CARD.md, file:modelcard.md]
related: [llm-evals, mlflow, hf-datasets, data-labeling]
---
Document each released model: intended use, data, metrics by slice, limitations and risks, kept in the repo and checked in CI.

## Verify
- `pytest -q tests/test_model_card.py`: required sections exist and metrics match the latest eval output.
- `python -m evals.run --suite dev --out metrics.json`: the numbers the card cites come from this file.
- `grep -n "<" MODEL_CARD.md`: no unfilled template placeholders ship.

## Test first
```python
import json, re
from pathlib import Path

def test_card_cites_current_accuracy():
    card = Path("MODEL_CARD.md").read_text()
    acc = json.load(open("metrics.json"))["accuracy"]
    assert f"{acc:.3f}" in card
    assert all(h in card for h in ["## Intended use", "## Limitations", "## Training data"])
```

## Do
- Include: model name and version, owner, intended and out-of-scope uses, architecture, training and evaluation data, metrics, limitations, ethical considerations and contact.
- Report metrics on named datasets with sample sizes and the date, and break them down by relevant slices (language, region, demographic, input type).
- Generate metric tables from the eval output file, not by hand.
- State the data provenance, licences, collection period, known gaps and personal-data handling.
- Describe failure modes with concrete examples and recommended mitigations or human review points.
- Record the training recipe: base model, seeds, hyperparameters, hardware and code commit.
- Version the card with the model; update it in the same change as retraining.
- Include licence, usage restrictions and how to report issues.

## Avoid
- A single aggregate metric: hides weak slices. Report per-slice results.
- Hand-typed numbers: they drift from reality. Generate from artefacts.
- Vague limitations such as "may be biased": give specific observed gaps and untested areas.
- Evaluation on training data or a leaked set: inflated claims. State the split and check overlap.
- Omitting out-of-scope uses: invites misuse. List them.
- Stale cards after retraining: add a CI check tying the card to the model version.

## Review
- [ ] Required sections complete.
- [ ] Metrics reproduce from the committed eval.
- [ ] Slice results and sample sizes included.
- [ ] Data provenance and licences stated.
- [ ] Limitations are specific.
