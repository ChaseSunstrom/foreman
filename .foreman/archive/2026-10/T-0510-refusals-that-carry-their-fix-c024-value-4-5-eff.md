---
id: T-0510
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
# Refusals that carry their fix (C024, value 4/5, effort M, risk low)
## Raw request
> SECURITY: Refusals that carry their fix (C024, value 4/5, effort M, risk low)
>   first version: Audit refusal messages so each names the allowed form (fixture test that every block reason has an 'instead/use' clause), and add a repeated-refusal counter in the hook that escalates to fm ask or task block after 3 identical blocks. Never rewrites and runs commands itself.
>   what it is: Every guard refusal says what is allowed instead, rewrites the command, and stops loops of repeated refusals.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
