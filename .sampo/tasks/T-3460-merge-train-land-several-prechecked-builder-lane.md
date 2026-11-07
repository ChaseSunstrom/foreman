---
id: T-3460
type: PERFORMANCE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T16:16:26Z
updated: 2026-11-06T16:24:13Z
---
# Merge train: land several prechecked builder lanes back to back, then run the close…
## Raw request
> Merge train: land several prechecked builder lanes back to back, then run the close gates once on the combined tree and close each (T-3120's gates reuse), bisecting only on red: ~60 finished lanes wait on one-at-a-time landings of 4-11 min each
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
- 2026-11-06T16:16:26Z created
- 2026-11-06T16:24:13Z dropped: duplicate of T-3380: sampo lane train already lands N lanes through one gate run (bisecting a red set); the landing pipeline now uses it
## Follow-ups captured
