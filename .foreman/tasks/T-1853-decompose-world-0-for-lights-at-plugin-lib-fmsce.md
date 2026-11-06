---
id: T-1853
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T17:51:35Z
updated: 2026-10-28T17:51:40Z
---
# _decompose(world)[0]` for lights at plugin/lib/fmscene.py:782 is just `world[12:15]` with
## Raw request
> _decompose(world)[0]` for lights at plugin/lib/fmscene.py:782 is just `world[12:15]` with rounding. It does needless work and can raise on overflow
> (noticed by an agent; research T-1847-review)
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
- 2026-10-28T17:51:35Z created
- 2026-10-28T17:51:40Z dropped: already fixed in T-1847 impl2: lights use _tidy(world[12:15])
## Follow-ups captured
