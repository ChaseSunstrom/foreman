---
id: T-3611
type: FEATURE
tier: L
status: captured
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-07T04:30:01Z
updated: 2026-11-07T04:30:01Z
---
# The guard blocks every systemd-run (fmguard.py ~5411), so agents can't run a measurement…
## Raw request
> FEATURE: the guard blocks every systemd-run (fmguard.py ~5411), so agents can't run a measurement under a CPU cap (systemd-run --user --scope -p CPUQuota=...); allow only the foreground --user --scope form with resource-control -p keys, and teach _strip_wrappers (~1521) to check the inner command (systemd-run --user --scope -- rm -rf ~ must still block; --on-calendar, no --scope, -M, --system stay blocked) (self-improvement pass; loosens the guard: review it security-first)
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
- 2026-11-07T04:30:01Z created
## Follow-ups captured
