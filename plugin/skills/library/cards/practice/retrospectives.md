---
name: retrospectives
title: Retrospectives
area: practice
tags: [retro, reflection, lessons, process, learning]
detect: []
related: [friction-logging, decision-records, self-improvement-loops, five-whys]
---
After a task or phase, record what happened against the plan, the cause of each gap, and at least one concrete change that sticks.

## Verify
- `fm decide --list`: decisions from the work are recorded.
- `fm task finish --help`: shows `--lesson`, which records the lesson with the task.
- `git log --oneline -5`: the change the retro chose (a test, a check, a rule) is committed, not just promised.

## Test first
A retro passes only if it ends in an artifact.
```markdown
Planned: <criteria and estimate>   Actual: <what shipped, time/steps, surprises>
Gaps (3 max): 1. <gap> | cause (five-whys, evidence) | change: <file/test/rule/check>
Keep: <what worked, one line>
Pass = each gap names a change that exists in the repo or as a captured task with an id.
```

## Do
- Compare plan to outcome with facts: criteria met, steps added, blocks, retries, time.
- Pick at most three gaps; ask why for each until you reach something controllable.
- Pair each gap with a change that is checkable: a test, a lint, a gate, a checklist line, a doc fix.
- Implement the cheap changes now; capture the rest as tasks.
- Record durable learnings as lessons, and choices as decisions, each one sentence with the evidence.
- Note what worked, so it is repeated.
- Read the last retro first; check whether its changes held.

## Avoid
- A retro with no change: end with a committed artifact or a task id, or the retro did not happen.
- Blame or mood: describe events and mechanisms.
- Ten action items: keep three; the rest are noise that nobody does.
- Lessons that restate the obvious ("test more"): make them specific ("add a fixture for X in Y").
- Skipping the retro after a smooth task: record what made it smooth.

## Review
- [ ] Plan versus actual is stated with facts.
- [ ] No more than three gaps, each with a cause.
- [ ] Each gap has a change or a captured task.
- [ ] Lessons are specific and recorded.
- [ ] The previous retro's changes were checked.
