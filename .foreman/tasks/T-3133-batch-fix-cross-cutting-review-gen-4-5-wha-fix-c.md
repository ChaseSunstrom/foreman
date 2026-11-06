---
id: T-3133
type: FIX
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-05T04:18:02Z
updated: 2026-11-06T03:52:46Z
batch: [T-3061, T-3068, T-3071, T-3072, T-3074, T-3075]
---
# Batch: FIX: cross-cutting review gen-4 #5 (wha…; FIX: cross-cutting review gen-4 #12 (wh…; FIX: cross-cutting review ge…
## Raw request
> T-3061: FIX: cross-cutting review gen-4 #5 (what got worse): s32-015 went 3/3 at gen 2, 2/3 with 2 false alarms at gen 3, 3/3 at gen 4 on the same 3 scenarios; the smoke signal flaps and the generation ships on it anyway. [fully closed 2 of 3]
> genesis-review 4:5
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
> T-3068: FIX: cross-cutting review gen-4 #12 (what is being measured wrong): The retrieval decider's 0.77 is on the 92% it answers, compared against 0.60 for majority on all 200 briefs; abstentions are dropped from the numerator but not the baseline. [0.77 on type]
> genesis-review 4:12
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
> T-3071: FIX: cross-cutting review gen-4 #15 (what is being measured wrong): A majority baseline of 0.12 on tier is impossible for any class that is actually a majority; the Jeff LoRA result is on one held-out project with a baseline that cannot be right. [0.64 on tier against 0.12]
> genesis-review 4:15
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
> T-3072: FIX: cross-cutting review gen-4 #16 (what is presented ahead of its proof): CHANGELOG claims the 12B went from 0 to 3 of 8 fixed once served 32k with reasoning off; the exam line for gpu-gemma12-32k shows fixed 0/3, and jarvis-nothink fixed 0/3. [0 to 3 of 8]
> genesis-review 4:16
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
> T-3074: FIX: cross-cutting review gen-4 #18 (what is presented ahead of its proof): Small-model cards are presented as "about 1 in 6 passes" with "the first long grow is running"; the only landed number is 400 calls and 0 kept. [400 calls, 0 kept]
> genesis-review 4:18
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
> T-3075: FIX: cross-cutting review gen-4 #19 (what is presented ahead of its proof): Loop-break shipped against loops ending 4 of 10 scenarios, and the next smith exam (s0-001, gpu-qwen4-32k) is found 1/8, fixed 1/8, closed by missing-tool; no line shows loops fell. [4 of 10 scenarios]
> genesis-review 4:19
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
## Interpretation
Reading 1: do T-3061, T-3068, T-3071, T-3072, T-3074, T-3075 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-3133. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670). Reading 2: each one alone; ruled out because one plan read and one gate run serve them all cheaper.
## Assumptions (confidence)
## Acceptance criteria
- [ ] T-3061: a generation ships only on a smoke signal that held: s32-015's three runs (3/3, 2/3 with 2 false alarms, 3/3) read as flapping, and the generation's line says so instead of passing — verify with `python3 plugin/tests/run.py test_smoke`
- [ ] T-3068: the retrieval decider is scored on all briefs with an abstention counted wrong (or shown as its own column), so its accuracy and the majority's share one denominator — verify with `python3 plugin/tests/run.py test_louhi_models`
- [ ] T-3071: the majority baseline is the share of the held-out project's own most common class (never below 1/k), and a one-project result is labelled one project — verify with `python3 plugin/tests/run.py test_louhi_models`
- [ ] T-3072, T-3074, T-3075: each CHANGELOG and research claim names its measured number and run (the 12B's fixed count from its exam lines, the cards' kept counts from the store, loop-break's before and after on the same scenarios) or says unproven; a check flags a numeric claim with no run cited — verify with `python3 plugin/tests/run.py test_docs`
- [ ] T-3074: the cards claim states the store's kept counts (5,031 on 2026-11-05: 1,894 general, 3,137 UI) and the admit rate measured, not 'about 1 in 6' — verify with `grep -q '3,137' ~/.claude/foreman/CHANGELOG.md`
- [ ] T-3075: the loop-break claim states loops before and after on the same scenarios and model, or says unproven until that run exists — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] T-3061: FIX: cross-cutting review gen-4 #5 (what got worse): s32-015 went 3/3 at gen 2, 2/3 with…  <- CURRENT
2. [ ] T-3068: FIX: cross-cutting review gen-4 #12 (what is being measured wrong): The retrieval…
3. [ ] T-3071: FIX: cross-cutting review gen-4 #15 (what is being measured wrong): A majority baseline…
4. [ ] T-3072: FIX: cross-cutting review gen-4 #16 (what is presented ahead of its proof): CHANGELOG…
5. [ ] T-3074: FIX: cross-cutting review gen-4 #18 (what is presented ahead of its proof): Small-model…
6. [ ] T-3075: FIX: cross-cutting review gen-4 #19 (what is presented ahead of its proof): Loop-break…
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T04:18:02Z created
- 2026-11-05T04:18:14Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_smoke`
- 2026-11-05T04:18:14Z criterion 1 text: T-3061: FIX: cross-cutting review gen-4 #5 (what got worse): s32-015 went 3/3 at gen 2, 2/3 with… works → T-3061: a generation ships only on a smoke signal that held: s32-015's three runs (3/3, 2/3 with 2 false alarms, 3/3) read as flapping, and the generation's line says so instead of passing
- 2026-11-05T04:18:15Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_louhi_models`
- 2026-11-05T04:18:15Z criterion 2 text: T-3068: FIX: cross-cutting review gen-4 #12 (what is being measured wrong): The retrieval… works → T-3068: the retrieval decider is scored on all briefs with an abstention counted wrong (or shown as its own column), so its accuracy and the majority's share one denominator
- 2026-11-05T04:18:16Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_louhi_models`
- 2026-11-05T04:18:16Z criterion 3 text: T-3071: FIX: cross-cutting review gen-4 #15 (what is being measured wrong): A majority baseline… works → T-3071: the majority baseline is the share of the held-out project's own most common class (never below 1/k), and a one-project result is labelled one project
- 2026-11-05T04:18:17Z criterion 4 verify: `` → `python3 plugin/tests/run.py test_docs`
- 2026-11-05T04:18:17Z criterion 4 text: T-3072: FIX: cross-cutting review gen-4 #16 (what is presented ahead of its proof): CHANGELOG… works → T-3072, T-3074, T-3075: each CHANGELOG and research claim names its measured number and run (the 12B's fixed count from its exam lines, the cards' kept counts from the store, loop-break's before and after on the same scenarios) or says unproven; a check flags a numeric claim with no run cited
- 2026-11-05T04:18:36Z criterion 5 verify: `` → `grep -q '3,137' ~/.claude/foreman/CHANGELOG.md`
- 2026-11-05T04:18:36Z criterion 5 text: T-3074: FIX: cross-cutting review gen-4 #18 (what is presented ahead of its proof): Small-model… works → T-3074: the cards claim states the store's kept counts (5,031 on 2026-11-05: 1,894 general, 3,137 UI) and the admit rate measured, not 'about 1 in 6'
- 2026-11-05T04:18:39Z criterion 6 verify: `` → `python3 plugin/tests/run.py test_docs`
- 2026-11-05T04:18:39Z criterion 6 text: T-3075: FIX: cross-cutting review gen-4 #19 (what is presented ahead of its proof): Loop-break… works → T-3075: the loop-break claim states loops before and after on the same scenarios and model, or says unproven until that run exists
- 2026-11-05T04:18:40Z set tier=M
- 2026-11-05T04:18:40Z set approved=True
- 2026-11-05T04:18:41Z blocked: approved batch; waits for a builder slot
- 2026-11-06T03:52:46Z unblocked
## Follow-ups captured
