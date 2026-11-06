---
id: T-1168
type: CLEAN
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:47:19Z
---
# Retire deferred "Later from T-..." briefs into one dated parking file with `fm tidy --appl
## Raw request
> CLEAN: Retire deferred "Later from T-..." briefs into one dated parking file with `fm tidy --apply`, so mission packs stop listing them.
> DONE-WHEN: after `fm tidy --apply` on a fixture with three deferred "Later from" briefs they are gone from the queue, their titles are in one parking file with a date, and no text is lost
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
- 2026-10-16T10:45:53Z created
- 2026-10-16T11:47:19Z dropped: replaced by a triage instead of a parking file: 5 built and 2 obsolete deferred briefs dropped with evidence, 4 re-queued (T-0792, T-0275, T-0829, T-0787), 11 stay deferred on named external needs (evidence, Claude Code events, the user's plugin yes)
## Follow-ups captured
