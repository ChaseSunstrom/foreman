---
id: T-0611
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:20:23Z
updated: 2026-10-09T19:54:54Z
done_in: T-0686
---
# Hypothesis tournament (I050, value 4/5, effort M, risk low)
## Raw request
> FEATURE: Hypothesis tournament (I050, value 4/5, effort M, risk low)
>   first version: Replace the flat 3-attempt block with an escalation ladder in fm next (repeat -> fm-debugger -> differential table -> block), keyed on hypothesis ledger state and failure frontier. First step: derive stuck state from attempts + hypotheses and emit the next rung.
>   what it is: Ranks hypotheses by cost-to-test, picks probes that split them, and escalates through a ladder when stuck.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 13 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T15:20:23Z created
- 2026-10-09T15:40:16Z batched into T-0686
- 2026-10-09T19:54:54Z done in T-0686 (batch)
## Follow-ups captured
