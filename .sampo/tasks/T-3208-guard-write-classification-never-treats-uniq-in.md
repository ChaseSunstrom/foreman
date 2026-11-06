---
id: T-3208
type: SECURITY
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T13:54:49Z
updated: 2026-11-05T13:54:49Z
group: guard bypasses and over-refusals
---
# Guard: write classification never treats 'uniq IN OUT' (or 'uniq -- - -x') as a write to…
## Raw request
> guard: write classification never treats 'uniq IN OUT' (or 'uniq -- - -x') as a write to OUT, and read_only (fmguard ~2671) skips operands starting with '-'; found by T-2261's adversary review
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
- 2026-11-05T13:54:49Z created
## Follow-ups captured
