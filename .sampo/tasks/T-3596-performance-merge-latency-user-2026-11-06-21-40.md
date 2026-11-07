---
id: T-3596
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T03:35:57Z
updated: 2026-11-07T03:35:57Z
---
# PERFORMANCE merge latency (user 2026-11-06 21:40: why is merging still so slow): a…
## Raw request
> PERFORMANCE merge latency (user 2026-11-06 21:40: why is merging still so slow): a 12-lane train ran 20:22 → ~21:37 before landing, ~50 min of it pre-check probes (each lane's affected tests on base+lane, 3 at a time) before the ~20 min gate, then ~12 serial closes; fast-tracked fixes built after it started wait for all of that. Cut: probes run only coverage-selected tests (T-3593) and are skipped when the lane already has green evidence on a base with the same code tree; probe lanes while the previous batch closes (T-3589); measure probe, gate and close minutes per batch in the train's report
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
- 2026-11-07T03:35:57Z created
## Follow-ups captured
