---
name: eval-driven-development
title: Eval-driven development
area: practice
tags: [evals, testing, ml, regression, quality]
detect: []
related: [metrics-and-guardrails, experiment-design, self-improvement-loops, recursive-improvement]
---
Write the eval cases and pass criteria first, run them as a baseline, then change the system until they pass without regressing the rest.

## Verify
- `fm evals inbox`: candidate eval cases from past failures are waiting or consumed.
- `fm evals add --help`: how a failure becomes a saved eval case.
- `fm bench --help`: replays finished tasks against a candidate to compare before adopting.
- The eval command exits 0 on the final tree and failed on the baseline.

## Test first
The eval is the test: cases, expected behaviour and a pass bar, committed before the change.
```python
CASES = [
    ("empty input", "", "refuses with message"),
    ("typo in name", "gt status", "suggests 'git status'"),
]
def test_eval_pass_rate():
    got = [judge(run(i), want) for _, i, want in CASES]
    assert sum(got) / len(got) >= 0.9, got
```
Run it first and record the baseline pass rate.

## Do
- Draw cases from real failures and edge cases; each case has an input and an observable expectation.
- Prefer deterministic checks (exact output, schema, test) over a judge; use a judge only for prose and pin its rubric.
- Split the set: cases you tune against, and held-out cases you look at only at the end.
- Record baseline, then change one thing, rerun, compare the whole table not only the target case.
- Add every new failure found in practice as a case, so it cannot return.
- Save eval results with the commit; fix the seed and the model where behaviour varies, and repeat runs to see noise.

## Avoid
- Evals written after the change to fit its output: write them first.
- Tuning on the held-out set: it stops being an eval; refresh it with new cases.
- A single aggregate score hiding regressions: report per-case and per-category.
- Judge prompts that praise anything: include failing examples in the rubric and check it rejects them.
- Too few cases to detect the effect: add cases or accept an inconclusive result.

## Review
- [ ] Cases and pass bar were committed before the change.
- [ ] Baseline numbers are recorded.
- [ ] Held-out cases stayed untouched during tuning.
- [ ] Per-case results show no hidden regression.
- [ ] New failures became new cases.
