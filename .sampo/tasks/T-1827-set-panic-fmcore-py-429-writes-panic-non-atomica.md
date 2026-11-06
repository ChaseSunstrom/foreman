---
id: T-1827
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T08:44:01Z
updated: 2026-10-28T09:33:28Z
---
# Set_panic` (fmcore.py:429) writes PANIC non-atomically, and `panicked(hard=True)` can read
## Raw request
> set_panic` (fmcore.py:429) writes PANIC non-atomically, and `panicked(hard=True)` can read an empty file mid-write. That is benign now. Use `write_atomic` if the flag ever carries more
> (noticed by an agent; research T-1821-review)
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
- 2026-10-28T08:44:01Z created
- 2026-10-28T09:33:28Z dropped: already built: set_panic writes PANIC with write_atomic (fmcore.py:427)
## Follow-ups captured
