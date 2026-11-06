---
id: T-1098
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T04:43:14Z
updated: 2026-10-16T05:36:47Z
---
# - Pre-existing: the roll opens the ledger in text mode and can raise `UnicodeDecodeError`
## Raw request
> - Pre-existing: the roll opens the ledger in text mode and can raise `UnicodeDecodeError` on a bad byte (`fmtidy.py:256`)
> (noticed by an agent; research T-1065-review)
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
- 2026-10-16T04:43:14Z created
- 2026-10-16T05:36:47Z dropped: done by T-1099: the roll reads bytes now
## Follow-ups captured
