---
id: T-1883
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T00:12:08Z
updated: 2026-10-29T00:12:24Z
done_in: T-1873
---
# Gallery()` catches only OSError and ValueError per tile (fmscene.py:128), so one corrupt l
## Raw request
> gallery()` catches only OSError and ValueError per tile (fmscene.py:128), so one corrupt look card or ledger entry that raises KeyError or TypeError takes down the whole index. A per-tile `except Exc…
> (noticed by an agent; research T-1873-review)
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
- 2026-10-29T00:12:08Z created
- 2026-10-29T00:12:24Z done in T-1873
## Follow-ups captured
