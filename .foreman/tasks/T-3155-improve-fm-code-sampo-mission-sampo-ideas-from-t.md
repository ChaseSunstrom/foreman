---
id: T-3155
type: RESEARCH
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-05T05:57:59Z
updated: 2026-11-05T06:00:28Z
friction_at: 2026-11-05T05:57:59Z
---
# Improve fm code: sampo mission + sampo ideas from the user's friction
## Raw request
> fm code run killed
> (the user's friction with fm code: run fm mission --request on it, then sampo ideas, then a build round)
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
- 2026-11-05T05:57:59Z created
- 2026-11-05T05:57:59Z run friction: killed: a run was left unfinished (killed outright)
- 2026-11-05T06:00:28Z dropped: folded into T-3117: the local lane runs fm code on real S tasks and reads each killed or failed run from its journal; a mission/ideas round on one 'run killed' line has no source to ground (only searches for it are on record)
## Follow-ups captured
