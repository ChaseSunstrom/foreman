---
id: T-3486
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T18:37:53Z
updated: 2026-11-06T18:37:54Z
inferred_deps: [T-3483, T-3485]
inferred_why: T-3483: named in its request; T-3485: re-measure gate checks closures the registry tracks
group: local-model exam loop
---
# T-3483 part 3: a re-measure gate: a paired before/after on the same scenarios (callcards.sign_test) marks a failure class closed only at p<0.05 and n>=30; n=8 is inconclusive
## Raw request
> T-3483 part 3: a re-measure gate: a paired before/after on the same scenarios (callcards.sign_test) marks a failure class closed only at p<0.05 and n>=30; n=8 is inconclusive
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] real-effect fixture rows give closed and n=8 rows give inconclusive — verify with `python3 plugin/tests/run.py test_louhi`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test, then the change  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T18:37:53Z created
## Follow-ups captured
