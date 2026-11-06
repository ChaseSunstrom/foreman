---
id: T-1960
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T10:15:48Z
updated: 2026-10-29T10:26:35Z
done_in: T-1962
---
# Fm ship --check [shas] exits 0 when the remote's main holds those commits' changes (by pat
## Raw request
> FEATURE: fm ship --check [shas] exits 0 when the remote's main holds those commits' changes (by patch, as the default pick does) and 1 naming the ones it lacks, so a ship task verifies without a git log -n3 | grep that a later ship pushes out of view
> DONE-WHEN: fm ship --check exits 0 after a ship and 1 before it, without the publish grant
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
- 2026-10-29T10:15:48Z created
- 2026-10-29T10:17:49Z batched into T-1962
- 2026-10-29T10:26:35Z done in T-1962 (batch)
## Follow-ups captured
