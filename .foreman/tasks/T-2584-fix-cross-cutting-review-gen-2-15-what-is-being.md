---
id: T-2584
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:29Z
updated: 2026-11-02T09:15:06Z
trigger: genesis-review
trigger_key: 1b59a7559284a4a9
done_in: T-2594
---
# Survival and the track record count a close as held or lost only once its 30-day window has ended; closes still in the window are shown apart
## Raw request
> FIX: cross-cutting review gen-2 #15 (what is being measured wrong): Only 157 closes are decided, yet "held" in the track record (546 of 568) counts the 1542 unsettled as held and the 4% is taken over all 1699. [Survival (30 days): of 1699 closes, 66 lost (4%), 91 survived the window, 1542 settling]
> genesis-review 2:15
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] _survival marks window_done; the survival line takes the lost rate over closes whose window has ended and names the closes still in it (with the losses already seen among them); the track record's 'held' counts only settled holds, as 'X of Y settled held, Z settling' — verify with `python3 plugin/tests/run.py test_outcomes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red tests in test_outcomes (a settling close isn't held; the rate's denominator is window-done closes)  <- CURRENT
2. [ ] window_done in _survival; survival_lines and track/_row use it
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-02T08:23:29Z created
- 2026-11-02T08:50:27Z planned from capture
- 2026-11-02T09:02:39Z batched into T-2594
- 2026-11-02T09:15:06Z done in T-2594 (batch)
## Follow-ups captured
