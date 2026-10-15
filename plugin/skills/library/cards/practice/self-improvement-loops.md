---
name: self-improvement-loops
title: Self-improvement loops
area: practice
tags: [improvement, loop, feedback, evals, iteration]
detect: []
related: [friction-logging, retrospectives, recursive-improvement, eval-driven-development]
---
Improve your own process in bounded rounds: measure, change one thing, re-measure, keep or revert, and record the result.

## Verify
- `fm friction --brief`: the evidence the next round starts from.
- `fm bench --help`: replay finished work to compare a change before adopting it.
- `git log --oneline -5`: each kept change is its own commit with its measurement; reverted ones are not there.

## Test first
State the round's hypothesis and the measurement before touching anything.
```markdown
Round N. Problem: <observed, with count or example>
Change: <one thing>
Measure: <command or counter>, baseline = <number>
Keep if: metric improves >= X and nothing guarded regresses. Else revert.
Pass = baseline is recorded and the keep rule is written before the change.
```

## Do
- Start each round from recorded evidence (friction notes, failed runs, repeated manual steps), not from a hunch.
- Pick the one problem with the most recurrence and the cheapest fix.
- Make one change per round so the effect is attributable.
- Gate it: run the project's checks plus the metric; keep only on a measured gain.
- Record the outcome, kept or reverted, with numbers; reverted rounds are findings.
- Cap rounds (a budget or count) and stop when a round finds nothing worth changing.
- Hold a standing guardrail set so improvements in one area cannot quietly break another.

## Avoid
- Changing several things per round: you cannot attribute the gain; split it.
- Improvement without a measure: "feels better" is not a result; define the counter.
- Self-grading with no external check: use tests, a replay or a second model.
- Unbounded loops: set a round cap and a dry-round stop rule.
- Rewriting your own rules or guard without approval: protected files need the user's grant; capture and ask.

## Review
- [ ] Each round began from evidence.
- [ ] One change, one measurement, one keep-or-revert decision.
- [ ] Reverts and negatives were recorded.
- [ ] Guardrails were rerun.
- [ ] The loop has a cap and a stop rule.
