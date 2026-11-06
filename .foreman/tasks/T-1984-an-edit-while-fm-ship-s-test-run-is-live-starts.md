---
id: T-1984
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T13:23:04Z
updated: 2026-10-29T13:33:15Z
done_in: T-1987
---
# An edit while fm ship's test run is live starts an ambient run beside it (fmambient.after_
## Raw request
> FIX: an edit while fm ship's test run is live starts an ambient run beside it (fmambient.after_edit checks only gates_running), two suites at once; skip it then, and have fm ship start one afterward when the tree changed during its run (as T-1973 does for fm check)
> DONE-WHEN: an edit during a live ship_testing marker starts no ambient run :: python3 plugin/tests/run.py test_ambient
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
- 2026-10-29T13:23:04Z created
- 2026-10-29T13:23:09Z batched into T-1987
- 2026-10-29T13:33:15Z done in T-1987 (batch)
## Follow-ups captured
