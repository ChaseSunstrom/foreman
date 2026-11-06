---
id: T-2654
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T20:00:11Z
---
# fm tidy --verbs: list verbs with no use in 60 days and a one-line retire proposal (c21:…
## Raw request
> FEATURE: fm tidy --verbs: list verbs with no use in 60 days and a one-line retire proposal (c21: Slimming and lifecycle; value 3, effort M, risk med)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
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
- 2026-11-02T19:21:26Z created
- 2026-11-02T20:00:11Z dropped: mostly built: fm usage --prune (fmcost.py:1480, T-0468) lists verbs unused in the window and files a CLEAN capture; the remainder (60 days, under fm tidy) isn't worth a task
## Follow-ups captured
