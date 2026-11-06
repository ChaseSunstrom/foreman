---
id: T-2638
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T19:56:08Z
---
# fm prove --coverage: report which changed hunks the proof command actually executed…
## Raw request
> FEATURE: fm prove --coverage: report which changed hunks the proof command actually executed (c05: Review aids and proof kinds for diffs; value 4, effort M, risk med)
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
- 2026-11-02T19:56:08Z dropped: built: fm task prove --hunks (T-0271) reverts each hunk of the task's diff and runs the check, naming hunks no check notices; the recon's grep looked in fmprove.py only
## Follow-ups captured
