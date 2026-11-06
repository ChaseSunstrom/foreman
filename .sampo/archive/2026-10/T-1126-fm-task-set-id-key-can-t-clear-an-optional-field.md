---
id: T-1126
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T07:10:17Z
updated: 2026-10-16T07:20:42Z
---
# Fm task set ID key= can't clear an optional field (cost_cap=, confidence=, predict_*=): an
## Raw request
> fm task set ID key= can't clear an optional field (cost_cap=, confidence=, predict_*=): an empty value is rejected, so a cap can only be replaced, never removed; empty clears optional fields
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
- 2026-10-16T07:10:17Z created
- 2026-10-16T07:20:42Z dropped: folded into T-1083: fm task set ID key= clears confidence, cost_cap and predict_* (CLEARABLE)
## Follow-ups captured
