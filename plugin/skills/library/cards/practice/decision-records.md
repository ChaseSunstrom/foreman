---
name: decision-records
title: Decision records
area: practice
tags: [decisions, adr, documentation, tradeoffs, history]
detect: []
related: [approach-comparison, retrospectives, second-opinions, kill-criteria]
---
Record each non-trivial choice with its reason, the rejected options and a revisit trigger, so it is not reopened or forgotten.

## Verify
- `fm decide --list`: the entry exists with its date and reason.
- `fm decide --help`: shows `--why`, `--rejected`, `--kind`, `--revisit` and `--cites`.
- `git log --oneline -5`: the change that implements the decision references it in the message or task log.

## Test first
A decision record is complete when each field answers a future reader's question.
```markdown
Decision: use SQLite, not Postgres, for the cache.
Why: single node, < 50 MB, no concurrent writers (measured: `du -h cache.db`).
Rejected: Postgres (ops cost), files (no query).
Kind: reversible.
Revisit: when writers > 1 or size > 1 GB.
Pass = reason cites evidence, >= 1 rejected option, revisit trigger set.
```

## Do
- Record at the moment of choosing, in one command: `fm decide "<what>" --why "<reason>" --rejected "<options>"`.
- Cite evidence in the reason: a measurement, a file, a constraint.
- Mark the kind (reversible, costly, outward); costly and outward choices go in the final report.
- Add a revisit trigger (`--revisit`) tied to a date or a path or a condition.
- Link a reversal to the decision it replaces (`--reverses`).
- Keep records short: one decision per entry, a few lines.
- Check the log before deciding: a previous decision may already cover it.

## Avoid
- Recording after the fact from memory: the reason drifts; record while evidence is in hand.
- "Because it is best": give the reason as a number, constraint or comparison.
- Omitting rejected options: they are what stops the argument from reopening.
- Recording every trivial choice: reserve entries for choices someone would question later.
- Silent reversal: a reversal needs its own record linking the old one.

## Review
- [ ] Reason cites evidence.
- [ ] Rejected options are listed.
- [ ] Kind and revisit trigger are set.
- [ ] Implementation points to the record.
- [ ] Existing decisions were checked first.
