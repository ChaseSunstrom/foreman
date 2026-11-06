---
id: T-2067
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-30T00:29:09Z
updated: 2026-10-30T00:30:16Z
---
# Ambient tests note embeds the evidence command, so each one differs and escapes…
## Raw request
> Ambient tests note embeds the evidence command, so each one differs and escapes _said_once (28x): say the full line once per step, repeats only the short 'affected tests pass again' (fmambient.py ~122)
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
- 2026-10-30T00:29:09Z created
- 2026-10-30T00:30:16Z dropped: the ambient note fires only on a fail/pass flip, so each is a new event, not a repeat; ~250 chars per flip
## Follow-ups captured
