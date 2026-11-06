---
id: T-3305
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T03:58:54Z
updated: 2026-11-06T03:58:54Z
---
# test_lanes leaks 'sleep 3600' children into its fm-lanes temp work dirs: they outlive…
## Raw request
> test_lanes leaks 'sleep 3600' children into its fm-lanes temp work dirs: they outlive the test (ppid 1, 40 min old, cwd deleted) on 2026-11-06; the fixture should start them in their own group and kill the group in tearDown, and run.py could sweep a class's process group after it ends
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
- 2026-11-06T03:58:54Z created
## Follow-ups captured
