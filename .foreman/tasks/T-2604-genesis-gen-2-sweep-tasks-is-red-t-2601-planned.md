---
id: T-2604
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T10:54:32Z
updated: 2026-11-02T10:57:55Z
genesis_sweep: 2:tasks
---
# Genesis gen-2 sweep: tasks is red — T-2601 planned
## Raw request
> fm genesis sweep 2: ✗ tasks: T-2601 planned
> Done when the rerun's tasks line is ✓.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the sweep's tasks line is ✓ — verify with `fm genesis sweep 2`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] fix what the sweep's tasks line names, then rerun fm genesis sweep 2  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-02T10:54:32Z created
- 2026-11-02T10:57:55Z dropped: no work of its own: the sweep's tasks row clears when the open tasks (T-2600, T-2603, T-2601) close, which are queued; the sweep reruns after them
## Follow-ups captured
## Regression test
The sweep's tasks row: every fm genesis sweep reruns it, so this can't come back unseen.
