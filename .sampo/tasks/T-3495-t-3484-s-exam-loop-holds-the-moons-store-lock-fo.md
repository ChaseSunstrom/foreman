---
id: T-3495
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-06T18:57:34Z
updated: 2026-11-06T18:57:34Z
inferred_deps: [T-3484]
inferred_why: T-3484: named in its request
group: local-model exam loop
---
# T-3484's exam loop holds the moons store lock for a whole round (its criterion said to…
## Raw request
> T-3484's exam loop holds the moons store lock for a whole round (its criterion said to skip while moons holds it, written before the recon); after T-3487 lands, rounds take T-3487's exam lock instead, so the loop runs beside sampo moons grow --keep and keeps the GPU busy
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
- 2026-11-06T18:57:34Z created
## Follow-ups captured
