---
id: T-0441
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T16:27:38Z
done_in: T-0672
---
# Exfiltration and secrets (C031, value 4/5, effort M, risk med)
## Raw request
> SECURITY: Exfiltration and secrets (C031, value 4/5, effort M, risk med)
>   first version: Extend fm secrets into a done-gate check on the task diff and outbound-looking commands (curl/scp of files matching secret patterns) already refused by guard; skip honeytokens. Strictly adds refusals.
>   what it is: Scan outbound data, redact secrets at write time, plant honeytokens and label information flow between projects.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:17Z created
- 2026-10-09T15:40:13Z batched into T-0672
- 2026-10-09T16:27:38Z done in T-0672 (batch)
## Follow-ups captured
