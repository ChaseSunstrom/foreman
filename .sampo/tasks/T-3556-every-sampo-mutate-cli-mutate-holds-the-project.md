---
id: T-3556
type: PERFORMANCE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T00:43:05Z
updated: 2026-11-07T00:43:05Z
---
# Every sampo mutate (cli.mutate) holds the project lock across regen_views (state_dict…
## Raw request
> PERF: every sampo mutate (cli.mutate) holds the project lock across regen_views (state_dict re-reads all ~2,345 briefs: 0.26 s of a 0.30 s mutate idle, 0.3-1.3 s sampled from /proc/locks under builder load), so hooks queue behind plain task set/ac/step calls; move the regen out of the project lock under its own views lock (mind sync off's mirror removal, which relies on the project lock excluding exports, and view write ordering) (found in T-3535)
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
- 2026-11-07T00:43:05Z created
## Follow-ups captured
