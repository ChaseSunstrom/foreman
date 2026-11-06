---
id: T-3094
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T02:06:48Z
updated: 2026-11-05T02:59:05Z
---
# test_docs.MapShards says MASTER.md's File map and Operations moved into docs/map shards,…
## Raw request
> test_docs.MapShards says MASTER.md's File map and Operations moved into docs/map shards, but MASTER.md still holds both sections (:51, :381): check whether the test pins a stale layout or MASTER.md kept a copy (T-2907 scout)
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
- 2026-11-05T02:06:48Z created
- 2026-11-05T02:59:05Z dropped: premise false: test_docs passes (MapShards included); MASTER.md's File map (:51) and Operations (:381) are index lines, each the first words of an entry and a link to the docs/map shard that holds it whole (files-*, ops-*), which is the layout the test pins
## Follow-ups captured
