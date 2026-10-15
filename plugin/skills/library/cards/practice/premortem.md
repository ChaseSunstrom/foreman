---
name: premortem
title: Premortem
area: practice
tags: [risk, planning, failure, mitigation, review]
detect: []
related: [red-team-review, assumption-mapping, kill-criteria, second-opinions]
---
Assume the work already failed, list the specific reasons, then change the plan or add a check for each of the top few.

## Verify
- `fm second plan ID`: a model outside your context lists objections and a verdict for the brief.
- `fm second debate ID --role pre-mortem`: the premortem role run as a separate voice, if you want one more read.
- `git diff --stat`: the plan or tests changed after the premortem; if nothing changed, it did not count.

## Test first
Write failures as testable statements, each with the check that would catch it.
```markdown
It is two weeks later and this failed. Top causes:
1. <cause> | likelihood H/M/L | impact H/M/L | early signal: <observable> | guard: <test or step>
2. ...
Pass = each of the top 3 maps to a new test, step or kill criterion in the brief.
```

## Do
- Frame it in the past tense ("it failed because") so people stop defending the plan.
- Generate 8-10 causes across categories: wrong problem, wrong assumption, integration, data, scale, people, time.
- Rank by likelihood times impact; keep the top 3-5 and drop the rest with a line.
- For each kept cause, write an early signal you can observe cheaply and a guard.
- Put guards in the plan: a step, a failing test, a rollback, or a kill criterion.
- Re-read the list at the midpoint and delete causes that are now ruled out.

## Avoid
- Generic risks ("scope creep", "bugs"): rewrite to name the component and the mechanism or delete.
- A premortem nobody acts on: every top item must change the plan or be explicitly accepted with a reason.
- Listing only technical causes: include wrong-requirement and wrong-metric causes.
- Doing it after building: run it before the first edit, while the plan is still cheap to change.
- Taking the model's list as truth: spot-check two causes against the code.

## Review
- [ ] Causes are specific, with a mechanism.
- [ ] Top items have an observable early signal.
- [ ] Each top item changed the plan, or an acceptance reason is written.
- [ ] At least one cause challenges the goal itself.
- [ ] The list was revisited at least once during the work.
