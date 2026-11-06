---
id: T-0878
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-15T14:52:27Z
updated: 2026-10-15T14:52:41Z
done_in: T-0859
---
# Catch it earlier: the guard had no notion of an idempotent re-init; every git init counted
## Raw request
> T-0859 (Guard: a bare git init in a folder that's already a repo isn't a tree write over core (3 f) wasn't caught before it shipped: the guard had no notion of an idempotent re-init; every git init counted as a write to its folder
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
- 2026-10-15T14:52:27Z created
- 2026-10-15T14:52:41Z done in T-0859: the guard now knows an idempotent re-init (T-0859)
## Follow-ups captured
