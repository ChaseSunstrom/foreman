---
name: recursive-improvement
title: Recursive improvement
area: practice
tags: [improvement, iteration, brainstorm, review, rounds]
detect: []
related: [self-improvement-loops, brainstorming-lenses, grounding-ideas, retrospectives]
---
Run rounds of build, review what shipped, and brainstorm on top of it, stopping when a round produces nothing new worth doing.

## Verify
- `fm queue`: the next round's items exist and trace to the previous round's review.
- `git log --oneline -10`: each round is a distinct set of commits.
- `fm ideas --help`: `--rounds`, `--dry`, `--seen` and `--deepen` support repeated, deduplicated idea passes.
- `fm research list`: each round's ideas and review notes are saved.

## Test first
Set the round budget and the stop rule before round one.
```markdown
Goal: <what better means, with a metric or checklist>
Round = build -> review shipped work -> brainstorm next items -> ground -> score.
Stop when: a round's review finds no defect AND brainstorm yields no grounded item above the cut line, or the cap (N rounds) is reached.
Pass = every round has a saved review and a recorded stop-or-continue decision.
```

## Do
- Each round: finish the highest-value items, then review the shipped diff with fresh eyes (a second read) before ideating.
- Seed the next brainstorm with what shipped and what the review found, and pass the previous ideas as `seen` so they are not repeated.
- Ground every new idea in files or commands before scoring (see grounding-ideas).
- Re-score the backlog each round; evidence from shipped work changes confidence.
- Fix defects found in the review before adding features.
- Record a stop-or-continue decision at the end of each round with the reason.
- Keep a hard cap on rounds and on spend.

## Avoid
- Adding features while the last round's bugs are open: fix first.
- Brainstorming without reviewing: the best ideas are in the flaws of what just shipped.
- Repeating old ideas under new words: dedupe against the saved list.
- Growing scope each round without a goal check: re-read the goal and cut what does not serve it.
- Never stopping: the dry-round rule and cap are mandatory.

## Review
- [ ] Each round has a saved review.
- [ ] New ideas were grounded and deduped.
- [ ] Defects were fixed before new features.
- [ ] A stop-or-continue decision is recorded per round.
- [ ] The cap was respected.
