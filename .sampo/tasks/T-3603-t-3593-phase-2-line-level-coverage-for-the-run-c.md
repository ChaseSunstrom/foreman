---
id: T-3603
type: PERFORMANCE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-07T04:13:13Z
updated: 2026-11-07T04:13:13Z
---
# T-3593 phase 2: line-level coverage for the run cache: runcover.py records files, so an…
## Raw request
> T-3593 phase 2: line-level coverage for the run cache: runcover.py records files, so an edit to core.py (read by ~90% of classes) or cli.py (~45%) reruns nearly every class that touches them; record the functions each class ran (sys.monitoring PY_START, disabled after the first hit) and map a change's diff hunks to functions, so only classes that ran an edited function rerun
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
- 2026-11-07T04:13:13Z created
## Follow-ups captured
