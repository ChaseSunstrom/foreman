---
id: T-1475
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T16:18:18Z
updated: 2026-10-22T17:32:25Z
---
# Fm check`/`fm code` leave a dump file on every run past 15 minutes. Whether that noise is
## Raw request
> fm check`/`fm code` leave a dump file on every run past 15 minutes. Whether that noise is wanted is a separate decision
> (noticed by an agent; research T-1405-review)
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
- 2026-10-22T16:18:18Z created
- 2026-10-22T17:32:25Z dropped: kept as is: the dump fires after 30 min (not 15), an empty one is removed, and fm tidy prunes stacks older than 14 days; a run that long is worth a clue
## Follow-ups captured
