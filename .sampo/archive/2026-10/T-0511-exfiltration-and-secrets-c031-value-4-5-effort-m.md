---
id: T-0511
type: SECURITY
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:33Z
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
- 2026-10-09T14:30:18Z created
- 2026-10-09T14:30:33Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
