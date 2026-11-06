---
id: T-3447
type: FIX
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T15:19:24Z
updated: 2026-11-06T16:07:54Z
---
# A test fm call that times out leaves its gate's bash and run.py orphaned (ppid 1,…
## Raw request
> FIX: a test fm call that times out leaves its gate's bash and run.py orphaned (ppid 1, deleted cwd) still polling the slot pool until FM_RUN_DEADLINE: core.run_command and the forkcli worker each start a new session, so the kill misses the grandchildren; kill the whole process group on timeout
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
- 2026-11-06T15:19:24Z created
- 2026-11-06T16:07:54Z steer: T-3442 (landed) removes the slot-pool polling part: a nested run.py now sees FOREMAN_SLOT and takes no slot. Left: orphans run on to FM_RUN_DEADLINE when a test's fm call is killed, since run_command's bash is in its own session; the fix is a parent-gone check in run.py (ppid changed → exit), not a wider killpg
## Follow-ups captured
