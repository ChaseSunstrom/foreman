---
id: T-1594
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T19:41:04Z
updated: 2026-10-22T20:29:17Z
---
# Fmrelease.py:177` — `subprocess.run(..., text=True)` has no `errors=`, so undecodable sent
## Raw request
> fmrelease.py:177` — `subprocess.run(..., text=True)` has no `errors=`, so undecodable sentinel output raises in a pool thread and aborts the whole canary
> (noticed by an agent; research T-1518-review)
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
- 2026-10-22T19:41:04Z created
- 2026-10-22T20:29:17Z dropped: done in T-1518: the canary passes errors=replace
## Follow-ups captured
