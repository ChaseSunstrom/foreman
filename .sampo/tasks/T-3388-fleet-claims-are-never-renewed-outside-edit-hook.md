---
id: T-3388
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:54:33Z
updated: 2026-11-06T06:54:33Z
---
# Fleet claims are never renewed outside edit hooks: claims.renew has no caller in…
## Raw request
> FEATURE: fleet claims are never renewed outside edit hooks: claims.renew has no caller in plugin/lib, so a task claim lapses after 30 min of Bash-only work and a tower claim mid-job; wire renewal into SessionStart/Stop and long-job heartbeats, and release on finish (T-3330, T-3333 reviews)
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
- 2026-11-06T06:54:33Z created
## Follow-ups captured
