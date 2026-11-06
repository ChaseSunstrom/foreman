---
id: T-0726
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T17:20:35Z
updated: 2026-10-09T17:30:47Z
done_in: T-0729
---
# Fm capture prints 'Dropped before: T-0260 (Evidence quality…)' for unrelated requests (4 t
## Raw request
> fm capture prints 'Dropped before: T-0260 (Evidence quality…)' for unrelated requests (4 times today: audit diffs, lane locks, commit retry): the re-ask match fires on T-0260's huge batch request text; cap or skip batch-shell requests in the match
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
- 2026-10-09T17:20:35Z created
- 2026-10-09T17:27:26Z batched into T-0729
- 2026-10-09T17:30:47Z done in T-0729 (batch)
## Follow-ups captured
