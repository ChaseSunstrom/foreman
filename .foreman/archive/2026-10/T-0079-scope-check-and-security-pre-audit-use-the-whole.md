---
id: T-0079
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-09-30T11:28:09Z
updated: 2026-10-03T04:32:42Z
done_in: T-0078
---
# Scope check and security pre-audit use the whole uncommitted tree, so in a never-committed
## Raw request
> scope check and security pre-audit use the whole uncommitted tree, so in a never-committed repo every task needs a scope log and an adversary lens for lockfiles it didn't touch; compare against files changed since the task was focused — evidence: T-0055..T-0066 each needed 'scope: other uncommitted paths belong to earlier tasks'
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
- 2026-09-30T11:28:09Z created
- 2026-10-03T04:32:42Z done in T-0078: same fix: scope and pre-audit diff from the focus snapshot
## Follow-ups captured
