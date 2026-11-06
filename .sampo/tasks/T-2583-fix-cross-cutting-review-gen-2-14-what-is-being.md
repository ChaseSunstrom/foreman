---
id: T-2583
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
trigger_key: efee027b99f16af2
done_in: T-2594
---
# A Genesis review finding is grounded by a short number quoted with its words ('landed 57%'), not only by a path or a 3+ digit number
## Raw request
> FIX: cross-cutting review gen-2 #14 (what is being measured wrong): A review finding now needs a number of 3+ digits, so the 57% landing rate, the 4% survival loss and the 0/6 long-horizon score can ground nothing; the rule excludes the numbers a reviewer most needs. [f95fac52]
> genesis-review 2:14
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a ground of 8+ characters holding a digit and a letter, found verbatim in the inputs, grounds a finding ('briefs of 8-16k landed 57%', '4% lost'); a bare '57%' or '10' still grounds nothing; paths and 3+ digit numbers as before; REVIEW_CHILD asks for the number with its words — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red test beside T-2506's  <- CURRENT
2. [ ] widen path_or_number at fmgenesis.py:3449 and reword REVIEW_CHILD
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-02T08:23:29Z created
- 2026-11-02T08:49:36Z planned from capture
- 2026-11-02T09:02:39Z batched into T-2594
- 2026-11-02T09:15:06Z done in T-2594 (batch)
## Follow-ups captured
