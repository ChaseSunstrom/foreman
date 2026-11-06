---
id: T-1945
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T09:31:56Z
updated: 2026-10-29T09:49:28Z
done_in: T-1948
---
# Fm ship remembers the last commit it shipped (a ref under refs/foreman/) and its default p
## Raw request
> FEATURE: fm ship remembers the last commit it shipped (a ref under refs/foreman/) and its default picks start after it (git cherry's limit), so commits that reached main through a merge under other patches no longer block a plain fm ship
> DONE-WHEN: after one ship, a plain fm ship skips everything up to the shipped commit even when git cherry still lists it
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
- 2026-10-29T09:31:56Z created
- 2026-10-29T09:32:02Z set tier=S
- 2026-10-29T09:39:17Z batched into T-1948
- 2026-10-29T09:49:28Z done in T-1948 (batch)
## Follow-ups captured
