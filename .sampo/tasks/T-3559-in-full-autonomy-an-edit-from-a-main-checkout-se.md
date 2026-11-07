---
id: T-3559
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T00:45:21Z
updated: 2026-11-07T00:45:21Z
---
# In full autonomy, an edit from a main-checkout session into a .claude/worktrees/X path…
## Raw request
> In full autonomy, an edit from a main-checkout session into a .claude/worktrees/X path with no active task runs _first_brief (hooks.py ~2137, lane_hint is empty when p.lane is unset), making a new task in the main checkout for a lane's edit — against fmguard.py ~305's 'never a new one in the main checkout': when the refused path is inside a lane, skip _first_brief and give the lane hint (T-3534 review)
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
- 2026-11-07T00:45:21Z created
## Follow-ups captured
