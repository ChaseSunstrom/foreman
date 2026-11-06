---
id: T-2692
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T23:08:42Z
updated: 2026-11-02T23:13:00Z
---
# fm ship reads the publish grant at the start and again at push time from whatever task…
## Raw request
> fm ship reads the publish grant at the start and again at push time from whatever task is active then: focusing another task while a ship runs makes the push refuse after the full suite passed; pass the start's granted task into _push
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
- 2026-11-02T23:08:42Z created
- 2026-11-02T23:13:00Z dropped: premise false: fm ship takes its granted task at the start and spends by that id (fmrelease.ship → _push_main(p, b.id) → _spend), so focusing another task mid-ship can't refuse the push; only fm release --push re-reads the active task, by design, since a release resumes across steps
## Follow-ups captured
