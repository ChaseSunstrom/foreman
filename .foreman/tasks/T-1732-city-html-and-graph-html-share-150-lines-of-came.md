---
id: T-1732
type: CLEAN
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-23T03:36:21Z
updated: 2026-10-23T06:00:27Z
---
# City.html and graph.html share ~150 lines of camera, input and survival JS: one shared inl
## Raw request
> city.html and graph.html share ~150 lines of camera, input and survival JS: one shared inlined scene kit both pages fill, so they can't drift
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
- 2026-10-23T03:36:21Z created
- 2026-10-23T06:00:27Z dropped: deferred by decision: test_showpieces asserts the copied survival block is identical in city.html and graph.html (T-1654 review), so drift already fails a test; extracting a shared fill would touch both pages' browser-tested scenes for no behaviour change, and usage is ahead of pace. Revisit when a third scene page is added.
## Follow-ups captured
