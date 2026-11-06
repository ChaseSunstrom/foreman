---
id: T-2573
type: FIX
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:22Z
updated: 2026-11-02T08:25:38Z
trigger: genesis-review
trigger_key: b47a242c1410b79f
---
# FIX: cross-cutting review gen-2 #4 (what got worse): Both friction trends moved the…
## Raw request
> FIX: cross-cutting review gen-2 #4 (what got worse): Both friction trends moved the wrong way this window while guard blocks fell by 0.1. [failed tool calls 0.6 → 0.7 · drive stops 0 → 0.2]
> genesis-review 2:4
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
- 2026-11-02T08:23:22Z created
- 2026-11-02T08:25:38Z dropped: review.md marks it dismissed: one window's 0.1 moves in two friction trends with no named cause; fm friction keeps watching and files a trend that holds
## Follow-ups captured
