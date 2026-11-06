---
id: T-2785
type: FIX
tier: M
status: dropped
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-11-03T05:12:56Z
updated: 2026-11-03T05:14:02Z
trigger: baseline
trigger_key: 28b7465959df8ea6
baseline: true
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_left_out.LeftOut.test_no_silent_cut_in_fmcli. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
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
- 2026-11-03T05:12:56Z created
- 2026-11-03T05:14:02Z dropped: fixed in T-2774's second commit 55acec05 (joinmore says how many were left out); it was that lane's own red, caught by its behaviour lock
## Follow-ups captured
