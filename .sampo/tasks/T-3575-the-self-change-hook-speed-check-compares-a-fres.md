---
id: T-3575
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T02:26:44Z
updated: 2026-11-07T02:26:44Z
---
# The self-change hook-speed check compares a fresh lane bench against a base bench it…
## Raw request
> The self-change hook-speed check compares a fresh lane bench against a base bench it cached earlier (often at a quieter time), so load noise reads as a regression (T-3551: SessionStart p95 97 → 294 ms recorded; interleaved reruns showed no change, 70-77 ms p50 on fork point, lane and build alike). Run base and lane benches interleaved in the same window, or scale by load, before flagging a regression
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
- 2026-11-07T02:26:44Z created
## Follow-ups captured
