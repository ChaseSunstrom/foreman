---
id: T-3244
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T20:57:49Z
updated: 2026-11-05T21:03:55Z
---
# Guard over-refusal: pgrep -fc '[f]m ui --json' (a bracketed pattern that can't match its…
## Raw request
> Guard over-refusal: pgrep -fc '[f]m ui --json' (a bracketed pattern that can't match its own command line) is refused as matching its own shell; the message itself recommends bracketing one letter
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
- 2026-11-05T20:57:49Z created
- 2026-11-05T21:03:55Z dropped: not a bug: the refused command also held the literal text 'fm ui --json' in an echo, so the bracketed pattern really matched its own shell; the guard's existing test covers the truly bracketed form (test_hooks: while pgrep -f "[f]m check")
## Follow-ups captured
