---
id: T-2200
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T19:24:27Z
updated: 2026-10-30T19:24:34Z
---
# fmfind._files on a copy without .git falls back to a walk, so a cold re-find may list…
## Raw request
> fmfind._files on a copy without .git falls back to a walk, so a cold re-find may list files differently: the difference can only turn a proof into a lead
> (noticed by an agent; research T-2122-review)
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
- 2026-10-30T19:24:27Z created
- 2026-10-30T19:24:34Z dropped: not a defect: the cold re-find compares one finding by kind, file, line and symbol; a different file listing on the copy can only turn a proof into a lead, never a lead into a proof
## Follow-ups captured
