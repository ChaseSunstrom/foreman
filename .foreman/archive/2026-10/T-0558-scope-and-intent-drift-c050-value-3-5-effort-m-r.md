---
id: T-0558
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:42Z
---
# Scope and intent drift (C050, value 3/5, effort M, risk low)
## Raw request
> FEATURE: Scope and intent drift (C050, value 3/5, effort M, risk low)
>   first version: Derive tier from the diff at done (files, lines, core paths) and flag a mismatch with the declared tier; reuse the existing scope check. Skip the effort ledger.
>   what it is: Detect drift between brief, diff and vetoes, derive tier from the diff and keep sessions on intent.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:42Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
