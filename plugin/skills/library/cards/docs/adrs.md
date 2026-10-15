---
name: adrs
title: Architecture decision records
area: docs
tags: [adr, architecture, decisions, docs, design, tradeoffs]
detect: [file:docs/adr/*.md, file:docs/decisions/*.md, file:doc/adr/*.md]
related: [docs-as-code, technical-writing, diagrams-as-code, changelogs]
---
ADRs: one short, numbered, immutable file per significant decision, recording context, options, the choice and its consequences.

## Verify
- `ls docs/adr | sort`: files are numbered consecutively with no gaps or duplicates (adjust the directory to the repo).
- `grep -L "^## Status\|^Status:" docs/adr/*.md`: lists records with no status line.
- `grep -rn "Status: *Superseded" docs/adr`: every superseded record names the record that replaces it.
- `npx markdownlint-cli2 "docs/adr/*.md"`: markdown lints (when the repo uses markdownlint).

## Test first
Write the decision question and the options before choosing. If you cannot list two real alternatives, it may not need an ADR.
```md
# 0007. Use Postgres advisory locks for job claiming
Status: Proposed
## Context
Workers double-claim jobs under load. Constraint: one database, no new infra.
## Options
1. Advisory locks. 2. SELECT FOR UPDATE SKIP LOCKED. 3. External queue.
```
Fill Decision and Consequences only after the options are written down.

## Do
- Use one file per decision, named `NNNN-short-title.md`, with a number that is never reused.
- Use a fixed template: Title, Status, Context, Options considered, Decision, Consequences.
- State the forces in Context: constraints, requirements, deadlines, what hurts today.
- List real alternatives with the reason each was rejected, including doing nothing.
- Write the Decision as one active sentence ("We will use X"), and list consequences, good and bad.
- Treat accepted records as immutable. To change one, add a new ADR and mark the old one Superseded by it, linking both ways.
- Commit the ADR in the same pull request as the change it explains, and link it from the code or docs it affects.
- Keep it to one page. Link to spikes, benchmarks and diagrams instead of pasting them.

## Avoid
- Editing an accepted ADR to reflect a new decision: history disappears. Supersede it with a new record.
- Writing the ADR after the fact with no alternatives: it reads as justification. Capture options while deciding.
- Recording trivial choices (formatter settings): noise buries the important ones. Reserve ADRs for hard-to-reverse or cross-cutting decisions.
- Omitting consequences: readers cannot see the cost. State downsides and follow-up work.
- Vague titles ("Database"): unfindable. Name the choice made.
- Keeping ADRs in a wiki away from the code: they rot. Keep them in the repo.

## Review
- [ ] Number is unique and sequential, and status is present.
- [ ] Context states constraints, and at least two options have reasons.
- [ ] Decision is one clear sentence, and consequences list costs as well as benefits.
- [ ] Superseded records link to their replacements both ways.
- [ ] The ADR landed in the same change as the work.
