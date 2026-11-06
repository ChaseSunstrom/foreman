---
id: T-2142
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T10:40:19Z
updated: 2026-10-31T04:44:59Z
inferred_deps: [T-2137]
inferred_why: T-2137: notices fire on verdict changes
---
# Goal notices fire only on state transitions (item done, verdict change, a typed wait),…
## Raw request
> Goal notices fire only on state transitions (item done, verdict change, a typed wait), never per stop (Mission 4 inbox)
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
- 2026-10-30T10:40:19Z created
- 2026-10-31T04:44:59Z dropped: already holds: the only goal notice on Stop is _goal_gate (T-2137), which fires on a done claim against a stopped verdict and is keyed once per cause set and session (fmhooks.py:3659), so it repeats only when the causes change; the goal line itself is printed at SessionStart, not per stop
## Follow-ups captured
