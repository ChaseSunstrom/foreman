---
id: T-3525
type: PERFORMANCE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:26:12Z
updated: 2026-11-06T19:26:12Z
inferred_deps: [T-3042, T-3514]
inferred_why: T-3042: named in its request; T-3514: named in its request
group: moons grow throughput
---
# Moons grow --keep 10000 can't reach its target: 34 kept an hour (1,041 to 1,369 in 9.5…
## Raw request
> PERFORMANCE: moons grow --keep 10000 can't reach its target: 34 kept an hour (1,041 to 1,369 in 9.5 h, 4% of 33,439 generated) puts 10,000 about 250 h away; find the stage that drops most (T-3514 names it), raise yield or parallel local calls so 10,000 kept lands within a day, measured on a 1 h window before and after (T-3042 step 4)
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
- 2026-11-06T19:26:12Z created
## Follow-ups captured
