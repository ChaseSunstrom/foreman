---
id: T-1973
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T11:31:47Z
updated: 2026-10-29T11:43:21Z
done_in: T-1974
---
# An edit made while full gates run gets no ambient run (T-1965) and no pass (T-1963), and n
## Raw request
> FIX: An edit made while full gates run gets no ambient run (T-1965) and no pass (T-1963), and nothing tests it until the next fm check. When a full fm check ends and the tree changed during it, it starts one ambient run for those edits (fmcli _cmd_check → fmambient.after_edit).
> DONE-WHEN: a full check whose tree changed mid-run starts an ambient run afterward :: python3 plugin/tests/run.py test_ambient
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
- 2026-10-29T11:31:53Z set tier=S
- 2026-10-29T11:32:47Z batched into T-1974
- 2026-10-29T11:43:21Z done in T-1974 (batch)
## Follow-ups captured
