---
name: llm-evals
title: LLM evals
area: ml
tags: [llm, evaluation, testing, regression, judge, datasets]
detect: [dep:promptfoo, dep:deepeval, dep:ragas, dep:inspect-ai, dep:braintrust]
related: [anthropic-sdk, rag, tool-use, prompt-caching]
---
Evals for LLM features: a versioned dataset, deterministic checks first, a calibrated judge second, and a regression gate in CI.

## Verify
- `pytest -q tests/evals`: the offline eval suite runs against recorded or fake outputs and enforces thresholds.
- `python -m evals.run --dataset evals/cases.jsonl --report out.json`: the harness scores every case and writes a report (your own entry point).
- `python -c "import json; [json.loads(l) for l in open('evals/cases.jsonl')]"`: the dataset file parses line by line.

## Test first
Write the failing case before changing the prompt: input, expected property, and a scorer that returns a number.
```python
import json
from mypkg.evals import score_case, load_cases

def test_golden_cases_meet_threshold(model_under_test):
    cases = load_cases("evals/cases.jsonl")
    scores = [score_case(c, model_under_test(c["input"])) for c in cases]
    assert sum(scores) / len(scores) >= 0.9
    assert all(s == 1 for c, s in zip(cases, scores) if c.get("must_pass"))
```

## Do
- Store cases as JSONL with an id, input, expected property or reference, tags and a `must_pass` flag. Version the file in git.
- Prefer deterministic scorers: exact match, regex, JSON schema validation, tool-call equality, unit tests on generated code.
- Use a model judge only for open-ended quality. Give it a rubric with a bounded scale, ask for reasoning before the score, and use a different or stronger model than the one under test.
- Calibrate the judge against 20 or more human-labeled cases and track agreement.
- Include failures from production, adversarial and refusal cases, and empty or very long inputs.
- Run each case several times at the production temperature and report the pass rate, not one sample.
- Record model id, prompt hash and dataset version with every run, and gate merges on a no-regression threshold.
- Keep a held-out set you do not tune prompts against.

## Avoid
- Judging with the same model and a vague "rate 1 to 10" prompt: self-preference and noisy scores. Use a rubric, a pairwise or binary check, and a separate judge.
- Tuning the prompt on the whole dataset: overfits. Split a held-out set.
- One sample per case: variance reads as signal. Repeat and aggregate.
- Evals only on happy paths: misses refusals and injection. Add adversarial cases.
- Live API calls in the default unit test run: slow, costly, flaky. Mark them separately and cache outputs.
- Reporting a single average: hides regressions on key slices. Report by tag.
- Checking that output "looks right": no regression protection. Assert a measurable property.

## Review
- [ ] Dataset is versioned with must-pass cases and held-out split.
- [ ] Deterministic checks come first, and the judge is calibrated.
- [ ] Runs record model, prompt and dataset versions.
- [ ] CI fails on regression against the baseline.
- [ ] Results are broken down by slice, not only averaged.
