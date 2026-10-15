---
name: approach-comparison
title: Approach comparison
area: practice
tags: [planning, design, tradeoffs, options, decision]
detect: []
related: [decision-records, spikes, first-principles, value-effort-scoring, second-opinions]
---
Choose between three or more real approaches against criteria written before scoring, and record why the losers lost.

## Verify
- `fm decide --list`: the choice and its rejected options are in the decision log.
- `fm queue`: the chosen approach turned into steps in the brief.
- `git log --oneline -5`: later commits follow the chosen approach, not a silent alternative.

## Test first
Fix the criteria and a kill threshold before naming favourites.
```markdown
Need: <one sentence>
Criteria (weights 1-3): correctness risk, effort, reversibility, fits existing code, runtime cost
Options: A <do nothing/extend what exists>, B <the obvious one>, C <the different one>
Rule: an option that fails a hard constraint is out, not low-scored.
Pass = winner beats runner-up on >= 2 weighted criteria and the margin is stated.
```

## Do
- Always include "extend what exists" or "do nothing" as an option; it sets the baseline.
- Write each option as a one-paragraph sketch with the first file you would touch.
- Score against the criteria in a small table; keep scores as words (low/med/high) with a reason per cell.
- Name the riskiest assumption of the winner and what would make you switch.
- Prefer reversible choices when scores are close.
- Record with `fm decide "<choice>" --why "<reason>" --rejected "<options>"`.
- For L-tier work, get a read from another model: `fm second plan ID`.

## Avoid
- Straw options (two bad, one favourite): each option needs a believable case for it; write it.
- Scoring after deciding: the criteria are written first or the table is theatre.
- Averaging numbers across unlike criteria: hard constraints eliminate; only the rest are scored.
- Comparing by features instead of failure modes: ask how each one breaks.
- Skipping the record: unrecorded choices are re-litigated next session.

## Review
- [ ] At least three options, one being the baseline.
- [ ] Criteria predate the scores.
- [ ] The winner's biggest risk and a switch trigger are written down.
- [ ] Rejected options and reasons are in the decision log.
- [ ] The plan steps match the chosen option.
