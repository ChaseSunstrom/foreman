---
id: T-3532
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T21:51:51Z
updated: 2026-11-06T22:07:15Z
---
# A merge train's left-out line names only the gate command ('its merge turns the gates…
## Raw request
> FIX: a merge train's left-out line names only the gate command ('its merge turns the gates red: python3 plugin/tests/run.py'), not the failing classes, so finding why T-3163 and T-3316 were left out on 2026-11-06 needed a fresh 20-30 min full run per lane: name the failing classes (and the gate's last lines) in the left-out reason and on the lane's brief
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
- 2026-11-06T21:51:51Z created
- 2026-11-06T22:07:15Z dropped: folded into the affected-gate task filed just now (its step 2)
## Follow-ups captured
