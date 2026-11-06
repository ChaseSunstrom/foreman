---
id: T-0204
type: PERFORMANCE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-04T04:07:02Z
updated: 2026-10-04T04:12:07Z
---
# Fm replay: skip session logs unchanged since the last accepted run so the guard gate isn't
## Raw request
> fm replay: skip session logs unchanged since the last accepted run so the guard gate isn't 7s each time (fmreplay.py:18-33 rereads 14 days)
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
- 2026-10-04T04:07:02Z created
- 2026-10-04T04:12:07Z dropped: premise false: measured corpus read 0.14 s vs guard verdicts 6.5 s on 5000 commands; the gate runs only when fmguard.py changes, when every verdict must be recomputed anyway
## Follow-ups captured
