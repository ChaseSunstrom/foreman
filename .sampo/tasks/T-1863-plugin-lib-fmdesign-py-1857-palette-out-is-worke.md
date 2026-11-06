---
id: T-1863
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T20:58:51Z
updated: 2026-10-28T20:59:14Z
---
# Plugin/lib/fmdesign.py:1857` `palette --out` is worker-allowed and writes arbitrary paths
## Raw request
> plugin/lib/fmdesign.py:1857` `palette --out` is worker-allowed and writes arbitrary paths (the same flaw as the first finding, but from T-1714)
> (noticed by an agent; research T-1652-review)
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
- 2026-10-28T20:58:51Z created
- 2026-10-28T20:59:14Z dropped: fixed in T-1652: palette --out is refused for workers with tokens --out
## Follow-ups captured
