---
id: T-1826
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T08:32:47Z
updated: 2026-10-28T08:35:39Z
---
# _sessions` in plugin/lib/fmcost.py (lines 687-730) now has a dict-literal line over 150 ch
## Raw request
> _sessions` in plugin/lib/fmcost.py (lines 687-730) now has a dict-literal line over 150 characters (line 714) and mixes pricing logic into the row-building loop; worth splitting out a `_price_row` he…
> (noticed by an agent; research T-1820-review)
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
- 2026-10-28T08:32:47Z created
- 2026-10-28T08:35:39Z dropped: wrapped line 718 inside T-1820 (split now iterates SPLIT directly); a _price_row helper isn't needed: fmcost.weighted() is the pricing helper
## Follow-ups captured
