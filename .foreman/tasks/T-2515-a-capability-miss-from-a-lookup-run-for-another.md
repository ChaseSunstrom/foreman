---
id: T-2515
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T23:16:24Z
updated: 2026-11-01T23:30:42Z
---
# A capability miss from a lookup run for another task (bc in a T-2380 count while T-2498…
## Raw request
> A capability miss from a lookup run for another task (bc in a T-2380 count while T-2498 was active) blocked T-2498's close; the paired fix that did the count without bc didn't clear it (fix_paired needs the tool present). Consider: a miss whose paired fix passed without the tool is cleared, as the gate's design allows a fallback, without weakening the gate for a check that was dropped
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
- 2026-11-01T23:16:24Z created
- 2026-11-01T23:30:42Z dropped: by design: clearing a miss on any passing paired fix would weaken the evidence gate (plain pytest would clear a missing coverage tool); the gate's own fallback route (fm ask ID system --later --fallback, then a passing step run) cleared T-2498 in two commands, and the queued request leaves the user's list when the task closes
## Follow-ups captured
