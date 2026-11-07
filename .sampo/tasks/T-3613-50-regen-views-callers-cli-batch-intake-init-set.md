---
id: T-3613
type: PERFORMANCE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T04:34:06Z
updated: 2026-11-07T04:34:06Z
---
# ~50 regen_views callers (cli batch/intake/init/_settle_batch, doctor, eco, find, rune,…
## Raw request
> PERF: ~50 regen_views callers (cli batch/intake/init/_settle_batch, doctor, eco, find, rune, serve, sync, tidy, grants, incident …) still regenerate the views under the project lock; T-3558/T-3582 moved mutate, focus, capture, task new and the prompt/session hooks to export_mirror under it + regen_views(mirror=False) after it: sample /proc/locks under 8 lanes and move the ones that show (found in T-3582)
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
- 2026-11-07T04:34:06Z created
## Follow-ups captured
