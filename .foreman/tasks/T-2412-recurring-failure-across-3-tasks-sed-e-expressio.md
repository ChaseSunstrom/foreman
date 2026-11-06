---
id: T-2412
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T14:45:32Z
updated: 2026-10-31T17:43:20Z
---
# Recurring failure across 3 tasks: sed: -e expression #0, char 0: unknown command: ','
## Raw request
> Recurring failure across 3 tasks: sed: -e expression #0, char 0: unknown command: ','
> recurring-failure a1a26ae6860f
> (hit in T-0108, T-0245, T-1243: find the cause and fix it once; fm recall and fm whyred help)
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
- 2026-10-31T14:45:32Z created
- 2026-10-31T17:43:20Z dropped: not a Foreman fault: three old sessions' own mistyped sed expressions (T-0108, T-0245, T-1243, last 2026-10); no code path emits it, and the Edit-not-sed rule covers the habit
## Follow-ups captured
