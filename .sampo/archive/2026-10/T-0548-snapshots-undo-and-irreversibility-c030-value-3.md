---
id: T-0548
type: SECURITY
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:41Z
---
# Snapshots, undo and irreversibility (C030, value 3/5, effort M, risk med)
## Raw request
> SECURITY: Snapshots, undo and irreversibility (C030, value 3/5, effort M, risk med)
>   first version: First version: before a destructive-category grant is used, record git stash-create/HEAD sha in the task log and name restorable vs irreversible in the ask text. No effect ledger yet.
>   what it is: Snapshot before risky actions, classify what git can restore, keep an effect ledger and budget irreversible steps.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 9 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:41Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
