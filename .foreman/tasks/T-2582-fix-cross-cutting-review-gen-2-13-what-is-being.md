---
id: T-2582
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:28Z
updated: 2026-11-02T09:15:06Z
trigger: genesis-review
trigger_key: 1026b024a355f191
done_in: T-2594
---
# The model-versus-rule exam line says the model arm wasn't run (no night answers booked) instead of scoring it 0/0
## Raw request
> FIX: cross-cutting review gen-2 #13 (what is being measured wrong): The model-versus-rule exam has a rule side and no model side; an exam that can report 0/0 on the arm it exists to score is not scoring that arm. [model dedupe: rule 1/2, model 0/0; model intake-tier: rule 24/36, model 0/0]
> genesis-review 2:13
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a model_replay use with model_n 0 reads 'model not run: no night answers booked (a model backend and a night pass)' in the exam summary, never 'model 0/0'; a use with answers prints its score as before — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red test on the summary line  <- CURRENT
2. [ ] branch on model_n in fmgenesis's exam summary
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-02T08:23:28Z created
- 2026-11-02T08:48:39Z planned from capture
- 2026-11-02T09:02:39Z batched into T-2594
- 2026-11-02T09:15:06Z done in T-2594 (batch)
## Follow-ups captured
