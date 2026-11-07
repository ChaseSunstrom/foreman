---
id: T-3485
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T18:37:52Z
updated: 2026-11-06T18:37:52Z
inferred_deps: [T-3483, T-3484]
inferred_why: T-3483: named in its request; T-3484: registry maps the failure classes the loop produces
group: local-model exam loop
---
# T-3483 part 2: a class-to-scaffold registry: each louhi FAILURE_CLASSES entry maps to its scaffold and closing task (loop → planner handback, plan_refused → refusal text in the repair prompt, budget → think off, false_done → verify before close), status open/building/closed
## Raw request
> T-3483 part 2: a class-to-scaffold registry: each louhi FAILURE_CLASSES entry maps to its scaffold and closing task (loop → planner handback, plan_refused → refusal text in the repair prompt, budget → think off, false_done → verify before close), status open/building/closed
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] every FAILURE_CLASSES entry has a registry row or an explicit unmapped — verify with `python3 plugin/tests/run.py test_louhi`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test, then the change  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T18:37:52Z created
## Follow-ups captured
