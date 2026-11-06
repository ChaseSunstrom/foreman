---
id: T-1593
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T19:31:17Z
updated: 2026-10-22T20:29:17Z
---
# _interpreter_reads` is called without the `fm --run` strip at depth > 0; no test covers th
## Raw request
> _interpreter_reads` is called without the `fm --run` strip at depth > 0; no test covers the join-under-home case with a cwd inside home
> (noticed by an agent; research T-1585-rereview)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T19:31:17Z created
- 2026-10-22T20:29:17Z dropped: covered in T-1585: _interp_code strips fm --run at every depth; the cwd-inside-home join has a test
## Follow-ups captured
