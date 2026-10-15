---
name: value-effort-scoring
title: Value and effort scoring
area: practice
tags: [prioritisation, scoring, ranking, roadmap, planning]
detect: []
related: [scope-cutting, grounding-ideas, ideation-to-briefs, approach-comparison]
---
Rank candidate work by value, effort, confidence and risk using evidence-based numbers, so the order is defensible and checkable.

## Verify
- `fm queue`: the queue order matches the scored order, or the note says why not.
- `fm research list`: the scoring table is saved with its inputs.
- `fm cost`: where cost matters, the effort estimates can be compared with what similar tasks cost.

## Test first
Fix the scale and a rule that would reorder the list before scoring.
```markdown
Value 1-5 (users or failures affected, with number), Effort 1-5 (files/steps), Confidence 1-5, Risk 1-5
Score = (value x confidence) / (effort + risk)
Check: re-score the top item with confidence lowered by one; if it drops below #3, mark it unstable.
Pass = top 3 each cite one measured input and none is unstable.
```

## Do
- Define each scale in a line with anchors (effort 1 = one file under 30 lines; 5 = cross-cutting).
- Take value inputs from data: logs, error counts, usage, tickets, or the stated user need.
- Estimate effort from a concrete file or step list from grounding, not gut feel.
- Score confidence separately; low confidence moves the item toward a spike, not down the list.
- Sort, then sanity-check the top and bottom by asking whether you would be surprised.
- Break ties by reversibility, then by what unblocks others.
- Re-score after any spike or refuted assumption.

## Avoid
- False precision (scores to two decimals): use 1-5 and treat near ties as ties.
- Scoring ideas nobody grounded: effort without file evidence is fiction; ground first.
- One composite number hiding a veto: a critical security or data-loss item skips the ranking.
- Value as "sounds nice": cite who benefits and how many, or lower the confidence.
- Ranking once and never updating: re-run when new evidence lands.

## Review
- [ ] Scales are anchored and written down.
- [ ] Top items cite measured inputs.
- [ ] Confidence is scored apart from value.
- [ ] Vetoes (security, data loss) were applied before ranking.
- [ ] The resulting order is what was queued.
