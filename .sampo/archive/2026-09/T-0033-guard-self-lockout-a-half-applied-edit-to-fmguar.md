---
id: T-0033
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-09-26T17:08:33Z
updated: 2026-09-26T17:34:43Z
---
# Guard self-lockout: a half-applied edit to fmguard.py (a helper used before it was defined
## Raw request
> Guard self-lockout: a half-applied edit to fmguard.py (a helper used before it was defined) made every Edit/Write and quoted-path interpreter command fail closed; recovery needed an argv-path python edit. Fall back to the committed guard (git show HEAD:plugin/lib/fmguard.py) when the working copy raises, still fail-closed if that fails too; and/or define-before-use in one edit
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
- 2026-09-26T17:08:33Z created
- 2026-09-26T17:34:43Z dropped: done in T-0018 round 4 (638e1c2): committed-guard fallback
## Follow-ups captured
