---
id: T-1951
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T09:50:32Z
updated: 2026-10-29T09:58:08Z
done_in: T-1953
---
# Fm ship reports a failure when writing refs/foreman/shipped fails after a successful push;
## Raw request
> FIX: fm ship reports a failure when writing refs/foreman/shipped fails after a successful push; the push landed, so it should warn and still print the shipped line
> DONE-WHEN: a failed update-ref after the push exits 0 with a warning
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
- 2026-10-29T09:50:32Z created
- 2026-10-29T09:50:36Z set tier=S
- 2026-10-29T09:50:45Z batched into T-1953
- 2026-10-29T09:58:08Z done in T-1953 (batch)
## Follow-ups captured
