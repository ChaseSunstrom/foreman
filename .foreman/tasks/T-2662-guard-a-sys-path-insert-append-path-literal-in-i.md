---
id: T-2662
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-02T20:15:11Z
updated: 2026-11-02T20:30:28Z
done_in: T-2665
---
# Guard: a sys.path.insert/append path literal in interpreter code counts as a write…
## Raw request
> Guard: a sys.path.insert/append path literal in interpreter code counts as a write target (_quoted_paths, fmguard.py:2256); skip constants that are arguments of sys.path calls; replay the full blocked command from the guard ledger first
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
- 2026-11-02T20:15:11Z created
- 2026-11-02T20:23:36Z batched into T-2665
- 2026-11-02T20:30:28Z done in T-2665 (batch)
## Follow-ups captured
