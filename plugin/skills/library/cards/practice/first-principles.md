---
name: first-principles
title: First principles
area: practice
tags: [reasoning, design, constraints, assumptions, simplification]
detect: []
related: [assumption-mapping, approach-comparison, scope-cutting, spikes]
---
Strip a problem to facts and hard constraints, then rebuild the solution from those instead of copying how it is usually done.

## Verify
- `fm research list`: the fact sheet or reasoning note is saved.
- `grep -n "constraint\|fact" <note>`: replace with your note path; both lists exist and each fact has a source.
- `git diff --stat`: the resulting design is smaller or simpler than the convention it replaced, or the note says why not.

## Test first
Separate facts from habits in writing, and make each fact checkable.
```markdown
Goal: <outcome, not mechanism>
Facts (each with source/command): 1. ... 2. ...
Hard constraints (physics, contract, law, budget): ...
Inherited assumptions (habits we may drop): ...
Pass = every fact has a source, and >= 1 inherited assumption was tested or dropped.
```

## Do
- State the goal as an outcome ("users see results in under 1 s"), not a mechanism ("add a cache").
- List what is verifiably true: measured numbers, API contracts, limits. Run the command that shows each.
- List inherited assumptions ("we always use a queue") and ask for each: what breaks if it is false?
- Derive the minimum design that satisfies facts and hard constraints; compare it with the conventional design.
- Check the derived design against the facts with a small calculation or prototype.
- Keep the conventional option in the comparison; it wins when it earns it.

## Avoid
- Calling opinions facts: attach a source or a measurement or move it to assumptions.
- Reinventing a solved problem for its own sake: first-principles is for challenging a constraint, not for avoiding libraries; check the standard option.
- Skipping numbers: estimate magnitudes (rows, requests, bytes) before designing.
- Deriving in your head only: write the chain down so it can be reviewed.
- Ignoring hard constraints you cannot change: list them first so you do not design against them.

## Review
- [ ] Goal is an outcome.
- [ ] Facts are sourced; assumptions are labelled.
- [ ] At least one convention was challenged with a test or number.
- [ ] The derived design was compared with the conventional one.
- [ ] Hard constraints are respected in the result.
