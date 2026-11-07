---
id: T-3586
type: PERFORMANCE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T03:07:54Z
updated: 2026-11-07T03:07:54Z
---
# After T-3577 lands, active_brief_fast can skip open non-active briefs by T-3573's…
## Raw request
> PERFORMANCE: after T-3577 lands, active_brief_fast can skip open non-active briefs by T-3573's briefs-open.json keys directly (T-3573 widened briefs-closed.json to every non-active brief instead, leaving active_brief_fast's text untouched to avoid a merge clash); also move the ~40 ledger_tail(p, 3000-50000) readers that filter one or two kinds (cost.py, night.py, cli.py, outcomes.py, contract.py) to ledger_tail(p, n, kinds=...) or ledger_events(kinds), which T-3573 made cheap
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
- 2026-11-07T03:07:54Z created
## Follow-ups captured
