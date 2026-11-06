---
id: T-3331
type: FEATURE
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_lanes.py]
depends_on: []
source: followup
created: 2026-11-06T04:31:59Z
updated: 2026-11-06T04:32:00Z
---
# Fleet: a lane per session: a second live session in the same checkout gets its own lane worktree, so its edits are its own task's
## Raw request
> Fleet: a lane per session: a second live session in the same checkout gets its own lane worktree, so its edits are its own task's
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] when a session starts while another live session holds the main checkout's focus, it is told to work in a new lane (sampo lane new + EnterWorktree) and its edits there are credited to its lane's task, never the other session's — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] test with two session ids, red  <- CURRENT
2. [ ] SessionStart: detect the live focus holder (hooks.py:322-330, 382) and route
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:31:59Z created
## Follow-ups captured
