---
name: experiment-design
title: Experiment design
area: practice
tags: [experiment, hypothesis, measurement, benchmark, validation]
detect: []
related: [metrics-and-guardrails, spikes, eval-driven-development, scientific-debugging]
---
Test a change with a stated hypothesis, a baseline, one varied factor and a pre-set success threshold, so the result can say no.

## Verify
- `fm bench --help`: replay and compare tooling for before/after runs of finished tasks.
- `git stash list; git log --oneline -3`: the baseline commit is identifiable and the variant is a separate commit or branch.
- `fm research list`: hypothesis, method, numbers and conclusion are saved together.

## Test first
Write the hypothesis and threshold before running the variant.
```markdown
Hypothesis: replacing the regex parser with the stdlib parser cuts p50 parse time >= 20% on corpus C.
Baseline: commit <sha>, 5 runs, median.
Variant: only the parser changes.
Metric: `python bench.py` median ms. Guardrail: tests pass, memory <= +10%.
Decision: >= 20% and guardrails hold -> adopt; else revert.
```

## Do
- State a hypothesis that can be wrong, with a numeric threshold.
- Measure the baseline first, on the same machine, with the same input, several runs; keep the raw numbers.
- Change one thing; if two things must change, say so and accept that the result is joint.
- Fix input and seed; record the command so anyone can rerun it.
- Repeat runs to see noise; if the noise is larger than the effect, the result is inconclusive, and you say so.
- Decide by the pre-set rule; log the outcome with `fm decide` including the numbers.
- Run guardrail metrics alongside the target metric.

## Avoid
- Choosing the threshold after seeing numbers: write it first.
- A single run: take at least 3-5 and report the spread.
- Measuring a different workload in the variant: pin the corpus and config.
- Cherry-picking the one run that supports the hypothesis: report the median and range.
- Dropping a negative result: save it; it prevents repeating the experiment.

## Review
- [ ] Hypothesis and threshold were written before the variant ran.
- [ ] Baseline and variant used identical inputs and commands.
- [ ] Multiple runs with the spread reported.
- [ ] Guardrails were measured.
- [ ] The decision follows the rule and is logged, including if negative.
