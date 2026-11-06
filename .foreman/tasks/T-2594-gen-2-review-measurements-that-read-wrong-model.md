---
id: T-2594
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T09:02:39Z
updated: 2026-11-02T09:21:57Z
batch: [T-2582, T-2583, T-2584]
base: 7272d2c05e38706ac143151d4493e3cb8b151088
base_tree: 0a007bfc73d014d85fb79d791c040cb38536df17
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T09:03:01Z
plan0_scope: []
verified: strong
---
# Gen-2 review: measurements that read wrong (model arm 0/0, short-number grounds, settling closes counted held)
## Raw request
> T-2582: FIX: cross-cutting review gen-2 #13 (what is being measured wrong): The model-versus-rule exam has a rule side and no model side; an exam that can report 0/0 on the arm it exists to score is not scoring that arm. [model dedupe: rule 1/2, model 0/0; model intake-tier: rule 24/36, model 0/0]
> genesis-review 2:13
> T-2583: FIX: cross-cutting review gen-2 #14 (what is being measured wrong): A review finding now needs a number of 3+ digits, so the 57% landing rate, the 4% survival loss and the 0/6 long-horizon score can ground nothing; the rule excludes the numbers a reviewer most needs. [f95fac52]
> genesis-review 2:14
> T-2584: FIX: cross-cutting review gen-2 #15 (what is being measured wrong): Only 157 closes are decided, yet "held" in the track record (546 of 568) counts the 1542 unsettled as held and the 4% is taken over all 1699. [Survival (30 days): of 1699 closes, 66 lost (4%), 91 survived the window, 1542 settling]
> genesis-review 2:15
## Interpretation
Reading 1 (chosen): three display and counting fixes the gen-2 review grounded, each in its own function: fmgenesis._exam_tail (model arm), the review's ground rule and REVIEW_CHILD, fmoutcomes survival and track. Reading 2: rework the measurements themselves (run the model arm, rebuild survival). Rejected: the model arm needs a backend the user hasn't set, and survival's data is right, only its counting reads wrong.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-2582: a model_replay use with model_n 0 reads 'model not run: no night answers booked (a model backend and a night pass)' in the exam summary, never 'model 0/0'; a use with answers prints its score as before — verify with `python3 plugin/tests/run.py test_genesis`
- [x] T-2583: a ground of 8+ characters holding a digit and a letter, found verbatim in the inputs, grounds a finding ('briefs of 8-16k landed 57%', '4% lost'); a bare '57%' or '10' still grounds nothing; paths and 3+ digit numbers as before; REVIEW_CHILD asks for the number with its words — verify with `python3 plugin/tests/run.py test_genesis`
- [x] T-2584: _survival marks window_done; the survival line takes the lost rate over closes whose window has ended and names the closes still in it (with the losses already seen among them); the track record's 'held' counts only settled holds, as 'X of Y settled held, Z settling' — verify with `python3 plugin/tests/run.py test_outcomes`
## Non-goals
## Approach (options → choice → why)
1) Fix each where it is printed or counted: model_n 0 says 'not run'; a ground of 7+ characters with a 3-letter word and a digit counts; held and the loss rate count only closes whose 30-day window ended. Likely outcome: three honest lines, nothing else moves. Fails if: the ground rule lets a vague phrase through (it must still occur verbatim in the inputs). 2) use what exists: the review already drops ungrounded findings; just reword REVIEW_CHILD to ask for the number with its words, no code change. Fails if: the parser still rejects '57%'-style grounds the prompt asks for. 3) do less: drop the model_replay line and the survival percentage entirely. Fails if: the scorecard loses the only rule-versus-model record and the only loss figure. Choice 1 (85%): each fix sits in one function with a test beside its existing one.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-2582: red test on the summary line
2. [x] T-2582: branch on model_n in fmgenesis's exam summary
3. [x] T-2583: red test beside T-2506's
4. [x] T-2583: widen path_or_number at fmgenesis.py:3449 and reword REVIEW_CHILD
5. [x] T-2584: red tests in test_outcomes (a settling close isn't held; the rate's denominator is window-done closes)
6. [x] T-2584: window_done in _survival; survival_lines and track/_row use it
## Resume here
## Docs impact
CHANGELOG (Unreleased). No MASTER change: the same functions, honest counts.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis test_outcomes` → ✗ exit 1 · Ran 270 tests in 18.6s (40 classes, 16 at a time; slowest: Survival 15s, GenerationReview 15s, GenesisRead 13s) / FAILED (3 classes: test_genesis.GenesisDraft, test_genesis.GenerationReview, test_outc [ran] [tree 47f289803353] [world 2f1906870a] (2026-11-02T09:03:34Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes test_genesis` → exit 0 · Ran 270 tests in 19.3s (40 classes, 16 at a time; slowest: Survival 16s, GenerationReview 16s, GenesisRead 14s) / OK [ran] [tree 716e02a71526] [world 2f1906870a] (2026-11-02T09:06:17Z)
- (step 3) `python3 plugin/tests/run.py test_outcomes test_genesis` → exit 0 · Ran 270 tests in 18.9s (40 classes, 16 at a time; slowest: Survival 15s, GenerationReview 15s, GenesisRead 13s) / OK [ran] [tree 716e02a71526] [world 2f1906870a] (2026-11-02T09:06:36Z)
- (step 4) `python3 plugin/tests/run.py test_outcomes test_genesis` → exit 0 · Ran 270 tests in 19.0s (40 classes, 16 at a time; slowest: Survival 15s, GenerationReview 15s, GenesisRead 13s) / OK [ran] [tree 716e02a71526] [world 2f1906870a] (2026-11-02T09:06:55Z)
- `python3 plugin/tests/run.py test_outcomes.TrackRecord test_outcomes.Survival test_genesis.GenerationReview test_genesis.GenesisDraft` → ✗ exit 1 · Ran 43 tests in 13.3s (4 classes, 16 at a time; slowest: Survival 12s, GenerationReview 9s, GenesisDraft 5s) / FAILED (4 classes: test_genesis.GenesisDraft, test_genesis.GenerationReview, test_outcome (start tree + this task's tests) [ran] [tree 6c06d2c01180] [world 2f1906870a] (2026-11-02T09:12:53Z)
- `python3 plugin/tests/run.py test_outcomes.TrackRecord test_outcomes.Survival test_genesis.GenerationReview test_genesis.GenesisDraft` → exit 0 · Ran 43 tests in 12.3s (4 classes, 16 at a time; slowest: Survival 12s, GenerationReview 12s, GenesisDraft 5s) / OK [ran] [tree 6c06d2c01180] [world 2f1906870a] (2026-11-02T09:12:53Z)
- (step 5) `python3 plugin/tests/run.py test_outcomes` → exit 0 · Ran 59 tests in 12.7s (16 classes, 16 at a time; slowest: Survival 12s, ModelRouter 8s, CalibrationLedgerBets 8s) / OK [ran] [tree 6c06d2c01180] [world 2f1906870a] (2026-11-02T09:13:30Z)
- (step 6) `python3 plugin/tests/run.py test_outcomes` → exit 0 · Ran 59 tests in 12.7s (16 classes, 16 at a time; slowest: Survival 12s, ModelRouter 8s, CalibrationLedgerBets 8s) / OK [ran] [tree 6c06d2c01180] [world 2f1906870a] (2026-11-02T09:13:43Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 211 tests in 15.2s (24 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 12s, GenesisRead 11s) / OK [ran] [tree 6c06d2c01180] [world 2f1906870a] (2026-11-02T09:14:32Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 211 tests in 15.2s (24 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 12s, GenesisRead 11s) / OK [ran] [tree 6c06d2c01180] [world 2f1906870a] (2026-11-02T09:14:32Z)
- (ac 3) `python3 plugin/tests/run.py test_outcomes` → exit 0 · Ran 59 tests in 12.7s (16 classes, 16 at a time; slowest: Survival 12s, ModelRouter 8s, CalibrationLedgerBets 8s) / OK [ran] [tree 6c06d2c01180] [world 2f1906870a] (2026-11-02T09:14:32Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_outcomes` → exit 0 · Ran 270 tests in 18.7s (40 classes, 16 at a time; slowest: Survival 15s, GenerationReview 15s, GenesisRead 13s) / OK [ran] [tree 6c06d2c01180] [world 2f1906870a] (2026-11-02T09:14:32Z)
- (audit intent) `self-review of the three members: _exam_tail branches on model_n; the ground rule adds one alternative and the prompt names it; _survival stamps window_done and survival_lines/track/_row count only finished windows; existing tests updated to the honest wording; full gate green` → model 0/0 reads 'not run' (test); 'landed 57%' grounds while '57%' and 'gen 10' don't (test); a fresh close is neither held nor in the loss rate (two tests) [tree 6c06d2c01180] (2026-11-02T09:14:32Z)
- (audit edge) `self-review of the three members: _exam_tail branches on model_n; the ground rule adds one alternative and the prompt names it; _survival stamps window_done and survival_lines/track/_row count only finished windows; existing tests updated to the honest wording; full gate green` → a ground still has to occur verbatim in the inputs, so the wider rule can't admit invented text; an unknown-time close has no window_done and counts as still in the window; a reverted or fixed-later close is decided at once and counts as settled [tree 6c06d2c01180] (2026-11-02T09:14:32Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 773b6e126ee1] [world 2f1906870a] (2026-11-02T09:17:05Z)
## Log
- 2026-11-02T09:02:39Z created
- 2026-11-02T09:03:00Z steer: T-2583's criterion says 8+ characters but its own example '4% lost' has 7; the rule is 7+ characters with a word of 3+ letters and a digit, which keeps 'gen 10' (6) out
- 2026-11-02T09:03:00Z set approved=True
- 2026-11-02T09:03:00Z focused
- 2026-11-02T09:03:01Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T09:06:56Z scope: plugin/lib/fmgenesis.py, plugin/lib/fmoutcomes.py and their tests — the three members' own functions
- 2026-11-02T09:15:05Z done
- 2026-11-02T09:15:08Z committed a60940fd (5 files)
- 2026-11-02T09:17:05Z guard authorization added: publish
- 2026-11-02T09:21:57Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2583 [FIX S, planned, 2 steps] A Genesis review finding is grounded by a short number quoted with its words ('landed 57%'), not only by a path or a 3+ digit number
- T-2584 [FIX S, planned, 2 steps] Survival and the track record count a close as held or lost only once its 30-day window has ended; closes still in the window are shown …
- T-2582 [FIX S, planned, 2 steps] The model-versus-rule exam line says the model arm wasn't run (no night answers booked) instead of scoring it 0/0
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Why not caught
each line had a test pinning its wording (model 2/3, the 40% survival line, '2 of 2 held'), but none fed the edge case the review found: no answers, a short number, a close still in its window
## Lessons
- A rate whose events arrive at different times (losses mid-window, survivals at its end) needs a denominator of finished windows, or recent work inflates one side
## Plan gaps
- failed first: step 1 T-2582: red test on the summary line
## Files touched
- plugin/tests/test_genesis.py
- plugin/tests/test_outcomes.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmoutcomes.py
- CHANGELOG.md
