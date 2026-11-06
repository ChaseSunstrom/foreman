---
id: T-1368
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T06:28:42Z
updated: 2026-10-21T13:37:43Z
---
# Canary after Foreman 1.2.47: ✗ foreman-4a056f: Sentinel: 8 past check(s) from 10 finished
## Raw request
> Canary after Foreman 1.2.47: ✗ foreman-4a056f: Sentinel: 8 past check(s) from 10 finished task(s); 3 failing now; 1 with side effects skipped
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
- 2026-10-21T06:28:42Z created
- 2026-10-21T13:37:43Z dropped: transient: fm sentinel rerun here shows 0 failing now; the canary ran while the release's own checks loaded the machine
## Follow-ups captured
