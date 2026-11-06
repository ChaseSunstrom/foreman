---
id: T-2475
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-01T15:45:20Z
updated: 2026-11-01T17:56:30Z
done_in: T-2493
---
# A mistyped flag's 'did you mean' suggests only the typed command's own flags (fm night --print-timer suggested --print, which fm night doesn't take)
## Raw request
> FIX: a mistyped flag's 'did you mean' suggests a flag from any command (fm night --print-timer suggested --print, which fm night doesn't take); suggest only the typed command's own flags
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm night --print-timer suggests none of another command's flags; fm check --evidance still suggests --evidence — verify with `python3 plugin/tests/run.py test_gate_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red test, then match flags of the typed subcommand only  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-01T15:45:20Z created
- 2026-11-01T16:56:56Z planned from capture
- 2026-11-01T17:47:17Z batched into T-2493
- 2026-11-01T17:56:30Z done in T-2493 (batch)
## Follow-ups captured
