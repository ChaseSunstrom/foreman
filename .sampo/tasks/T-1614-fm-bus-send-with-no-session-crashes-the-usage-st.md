---
id: T-1614
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T20:54:23Z
updated: 2026-10-22T21:07:59Z
---
# Fm bus send with no session crashes: the usage string in fmbus.py cmd_bus has unescaped qu
## Raw request
> fm bus send with no session crashes: the usage string in fmbus.py cmd_bus has unescaped quotes around <text>
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
- 2026-10-22T20:54:23Z created
- 2026-10-22T21:07:59Z dropped: fixed in T-1543 (fmbus cmd_bus usage quoting, with a test in test_bus.py)
## Follow-ups captured
