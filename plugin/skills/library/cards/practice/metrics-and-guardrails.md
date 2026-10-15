---
name: metrics-and-guardrails
title: Metrics and guardrails
area: practice
tags: [metrics, measurement, guardrails, goals, regression]
detect: []
related: [experiment-design, eval-driven-development, kill-criteria, self-improvement-loops]
---
Pick one target metric you can compute by command, plus guardrail metrics that must not regress, so progress is a number and not an impression.

## Verify
- `fm check`: gates (the guardrails) pass on the current tree.
- `fm bench --help`: replay-based comparison for before/after numbers.
- `git log --oneline -5`: each commit that claims an improvement has the before and after numbers in its message or the task log.

## Test first
Define each metric as a command and its direction before changing anything.
```markdown
Target:    p95 latency   | cmd: `./bench.sh | tail -1` | now: 480 ms | goal: <= 300 ms
Guardrail: tests         | cmd: `pytest -q`            | must stay green
Guardrail: peak RSS      | cmd: `./rss.sh`             | must be <= 1.1 x baseline
Guardrail: binary size   | cmd: `du -b dist/app`       | must be <= +5%
Pass = baseline recorded for all four before the first edit.
```

## Do
- Choose one target metric tied to the outcome; list 2-3 guardrails covering correctness, cost and a neighbouring quality.
- Make every metric a command with a number as output; save the command in the brief.
- Record the baseline first, on the same input, with the spread across runs.
- Set the goal and the guardrail limits as numbers, with a reason.
- Re-measure all of them at the end and write the table of before and after.
- Prefer a rate or a percentile to an average that hides tails.
- Pair every efficiency metric with a quality metric.

## Avoid
- A metric you can only eyeball: build the command or choose another.
- Optimising a proxy until it detaches from the goal (line coverage with no assertions): add a guardrail that checks the real behaviour, such as a mutation or an end-to-end test.
- Guardrails checked only at the end: run them after each major step.
- Moving the goal after seeing results: log any change with the reason.
- Reporting only the winning metric: show all of them, including those that worsened.

## Review
- [ ] One target and at least two guardrails, each a command.
- [ ] Baseline recorded before editing.
- [ ] Limits are numeric.
- [ ] Final table shows before and after for every metric.
- [ ] Any regression is explained or fixed.
