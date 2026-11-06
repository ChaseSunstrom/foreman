---
id: T-1971
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T11:31:47Z
updated: 2026-10-29T11:43:21Z
done_in: T-1974
---
# A second full fm check started while another runs on the same tree overwrites its gates_ru
## Raw request
> FIX: A second full fm check started while another runs on the same tree overwrites its gates_running marker and runs a second suite beside it; whichever ends first clears the marker for both. fm check now waits (at most 10 minutes, saying so) for another live full check on this tree, then reuses its cached pass when the tree is unchanged, and clears the marker only when it is its own (fmcli _cmd_check).
> DONE-WHEN: a full fm check started beside a live one waits for it and says so; the marker is cleared only by its owner :: python3 plugin/tests/run.py test_ambient test_close_gates
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
- 2026-10-29T11:31:47Z created
- 2026-10-29T11:32:47Z batched into T-1974
- 2026-10-29T11:43:21Z done in T-1974 (batch)
## Follow-ups captured
