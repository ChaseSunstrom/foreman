---
id: T-3408
type: FIX
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T08:45:32Z
updated: 2026-11-06T08:45:32Z
---
# The user's rule no longer holds: Never interrupt the user mid-run: no AskUserQuestion and no fm ask permission p…
## Raw request
> [steer-check dccfa0a1@19cf45dc02be] fm genesis steer (T-2350): the user's rule `Never interrupt the user mid-run: no AskUserQuestion and no fm ask permission p…` has the check `fm outcomes --questions --none --since 2026-11-04T00:02:00Z`, and at commit 19cf45dc02be it fails: exit 1: 1 AskUserQuestion call(s) since 2026-11-04T00:02:00Z: 1 question(s), 1 took the default, 0 another …. Fix what broke the rule; the rule stands until the user's own steer reverses it.
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
- 2026-11-06T08:45:32Z created
## Follow-ups captured
