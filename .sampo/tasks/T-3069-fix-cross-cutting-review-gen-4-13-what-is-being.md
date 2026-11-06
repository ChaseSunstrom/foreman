---
id: T-3069
type: FIX
tier: S
status: planned
priority: low
scope: []
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:13Z
updated: 2026-11-06T03:52:38Z
trigger: genesis-review
trigger_key: 43e2306442479bcc
---
# The next-request predictor is shown as leading only when its lead over the naive guess is significant on replay, not three rows
## Raw request
> FIX: cross-cutting review gen-4 #13 (what is being measured wrong): The next-request predictor ties the naive guess on replay (paths 0.088 vs 0.086) yet ships as a scored arm "shown only when it leads"; three rows over naive is noise, not a lead. [259/376 (naive 256)]
> genesis-review 4:13
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the predictor's arm counts as leading only when a paired test over the replay (its hits against the naive guess's, case by case) gives p < 0.05 and the lead is at least 2 points; 259 against 256 of 376 (today) reads 'level with naive', and the self-running line and any surface that shows it say so — verify with `python3 plugin/tests/run.py test_foresight test_exam`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test: 259 vs 256 of 376 is level; a clear lead (300 vs 256) leads  <- CURRENT
2. [ ] the paired test where the arm's lead is decided
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T00:31:13Z created
- 2026-11-05T04:43:37Z planned from capture
- 2026-11-05T04:43:38Z set approved=True
- 2026-11-05T04:43:38Z blocked: approved; waits for a builder slot
- 2026-11-06T03:52:38Z unblocked
## Follow-ups captured
