---
id: T-3557
type: FIX
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T00:43:06Z
updated: 2026-11-07T00:43:06Z
---
# SessionStart loses its whole context when the project lock stays busy past its retry…
## Raw request
> FIX: SessionStart loses its whole context when the project lock stays busy past its retry (the heartbeat block raises LockTimeout out of session_start): skip only the heartbeat writes and still inject the session context (found in T-3535)
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
- 2026-11-07T00:43:06Z created
## Follow-ups captured
