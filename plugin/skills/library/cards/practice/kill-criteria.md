---
name: kill-criteria
title: Kill criteria
area: practice
tags: [stopping, decision, risk, scope, discipline]
detect: []
related: [spikes, premortem, experiment-design, scope-cutting, assumption-mapping]
---
Write down, before starting, the observations that mean stop or change course, and check them at fixed points.

## Verify
- `fm queue`: the brief contains the kill criteria and a checkpoint step that evaluates them.
- `fm decide --list`: a stop, pivot or continue decision was logged at each checkpoint.
- `fm checkpoint --help`: shows how to save a resume point before a risky step.

## Test first
Make each criterion measurable and attach the check that reads it.
```markdown
Kill if any:
- Spike shows p95 > 500 ms with the simplest design (check: `bench.sh`)
- More than 3 failed attempts on one step (fm rule: block and diagnose)
- Needs a schema change outside the approved scope (check: `git diff --stat -- migrations/`)
Checkpoints: after the spike, at 50% of steps, before merge.
Pass = every criterion names a command or an observable count.
```

## Do
- Write 2-4 criteria when planning, covering results, effort and scope drift.
- Make each one a number or a yes/no that a command or a diff can show.
- Set the checkpoints in the plan as steps, so they get run.
- When a criterion fires, stop, record the decision with `fm decide`, and choose: pivot, shrink, or drop.
- Prefer a defined fallback ("ship the smaller version") written alongside the criterion.
- After stopping, capture what was learned so the effort is not wasted.

## Avoid
- Vague criteria ("if it gets too hard"): replace with a count, a time, or a measured threshold.
- Moving the threshold when it fires: changing it requires a logged reason made before seeing the result.
- Sunk-cost continuation: a fired criterion forces a recorded decision, not a quiet carry-on.
- Criteria with no checkpoint: if no step reads it, it never fires.
- Treating a kill as failure: a clean stop with a recorded finding counts as a result.

## Review
- [ ] Criteria are measurable and written before work began.
- [ ] Each has a check and a scheduled checkpoint.
- [ ] A fallback exists for each.
- [ ] Any fired criterion led to a logged decision.
- [ ] No threshold was changed after the fact without a reason.
