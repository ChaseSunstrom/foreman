---
id: T-1978
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T11:46:57Z
updated: 2026-10-29T12:25:19Z
done_in: T-1980
---
# Fm ship's test suite runs in its scratch tree with no marker, so a full fm check started m
## Raw request
> FIX: fm ship's test suite runs in its scratch tree with no marker, so a full fm check started meanwhile runs a second suite beside it (the T-1964/T-1971 rule covers only this tree), and a ship started during a full check does the same. fm ship marks its test run (meta ship_testing: pid, scratch root) and waits for a live full check or ambient run here first; a full fm check on another tree waits for a live ship test run (at most 10 minutes, saying so). The ship's own fm check in its scratch tree does not wait for itself (fmrelease ship, fmcli _cmd_check).
> DONE-WHEN: a full fm check started during fm ship's test run waits for it and says so; the ship marks and clears its run :: python3 plugin/tests/run.py test_ship test_ambient
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
- 2026-10-29T11:46:57Z created
- 2026-10-29T12:10:05Z batched into T-1980
- 2026-10-29T12:25:19Z done in T-1980 (batch)
## Follow-ups captured
