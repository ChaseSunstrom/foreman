---
name: ab-testing
title: A/B testing
area: domains
tags: [experiments, ab-testing, bucketing, statistics, feature-flags, srm]
detect: [dep:@growthbook/growthbook, dep:growthbook]
related: [analytics-events, recommendations, gdpr]
---
Experiments: deterministic sticky bucketing, exposure logging, a pre-set sample size, and a sample-ratio check before reading results.

## Verify
- `pytest -q tests/test_experiments.py`: bucketing, exposure and stats tests pass.
- `python -c "from app.exp import bucket; print(bucket('exp1','u1'))"`: assignment is stable across calls and processes.
- `pytest -q -k srm`: the sample-ratio-mismatch check flags a skewed split.

## Test first
Assignment must be sticky, independent across experiments, and near the target split.
```python
from app.exp import bucket

def test_bucketing_is_sticky_independent_and_balanced():
    ids = [f"u{i}" for i in range(20000)]
    a = [bucket("exp1", u) for u in ids]
    assert a == [bucket("exp1", u) for u in ids]            # sticky
    assert abs(a.count("B") / len(a) - 0.5) < 0.02          # balanced
    b = [bucket("exp2", u) for u in ids]
    both = sum(x == "B" and y == "B" for x, y in zip(a, b)) / len(ids)
    assert abs(both - 0.25) < 0.02                          # independent
```

## Do
- Bucket by hash of `experiment_key + unit_id` (user id, or anonymous id before login) into 0 to 9999; map ranges to variants. No stored randomness.
- Log an exposure event the first time a user actually sees the variant, with experiment key and variant; analyze exposed users only.
- Fix before launch: primary metric, minimum detectable effect, sample size or duration, and guardrail metrics.
- Run full weekly cycles; do not stop early on a good-looking p-value, or use a sequential method built for peeking.
- Run a sample ratio mismatch check (chi-square on counts vs planned split) first; a mismatch invalidates the result.
- Use the same unit for assignment and analysis; keep mutually exclusive experiments in layers.
- Make kill switches: a flag that forces control.
- Record the config version and start time with each result.

## Avoid
- `random()` per request: users flip variants. Hash a stable id.
- Reusing one hash salt for all experiments: correlated assignment. Include the experiment key.
- Counting all visitors rather than exposed ones: dilutes effect. Analyze exposure.
- Checking the dashboard daily and stopping at p<0.05: inflates false positives. Pre-commit or use sequential tests.
- Testing many metrics and reporting the one that won: correct for multiplicity or declare one primary.
- Changing allocation mid-test without handling: Simpson's paradox. Restart or analyze by period.

## Review
- [ ] Hypothesis, metric and sample size recorded before launch.
- [ ] Assignment is deterministic and tested.
- [ ] Exposure is logged at render time.
- [ ] SRM checked.
- [ ] Cleanup removes losing code paths and the flag.
