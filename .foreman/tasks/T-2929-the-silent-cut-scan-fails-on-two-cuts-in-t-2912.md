---
id: T-2929
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T08:21:19Z
updated: 2026-11-04T08:22:27Z
base: b7e2edca7480003b5461247eca29ba760022d3f9
base_tree: c30e4f359a56222978a326a38814a30bd435916e
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T08:21:21Z
plan0_scope: []
verified: strong
---
# The silent-cut scan fails on two cuts in T-2912's local-arm prompt (foresight.py: an ask's files cut at 4, the standing rules at 10): say how many each leaves out
## Raw request
> The silent-cut scan fails on two cuts in T-2912's local-arm prompt (foresight.py: an ask's files cut at 4, the standing rules at 10): say how many each leaves out
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the silent-cut scan passes — verify with `python3 plugin/tests/run.py test_left_out test_foresight`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] joinmore for both cuts
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_left_out` → ✗ exit 1 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: LeftOut 0s) / FAILED (1 classes: test_left_out.LeftOut) [ran] [tree c30e4f359a56] [world 2f1906870a] (2026-11-04T08:21:24Z)
- (step 1) `python3 plugin/tests/run.py test_left_out test_foresight` → exit 0 · Ran 42 tests in 7.9s (10 classes, 16 at a time; slowest: PredictionBook 8s, LocalArm 2s, DraftAhead 2s) / OK [ran] [tree d4d5851c8d7f] [world 2f1906870a] (2026-11-04T08:21:40Z)
- (ac 1) `python3 plugin/tests/run.py test_left_out test_foresight` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T08:21:40Z [ran] [tree d4d5851c8d7f] [world 2f1906870a] (2026-11-04T08:21:49Z)
- (audit edge) `test_left_out red before, green after with test_foresight` → under the cut the prompt reads as before; over it the model sees how many files or rules were left out [tree d4d5851c8d7f] (2026-11-04T08:21:49Z)
- (audit intent) `test_left_out red before, green after with test_foresight` → the full check is green again after T-2912's merge [tree d4d5851c8d7f] (2026-11-04T08:21:49Z)
- (audit self) `test_left_out red before, green after with test_foresight` → no findings [tree d4d5851c8d7f] (2026-11-04T08:21:49Z)
## Log
- 2026-11-04T08:21:19Z created
- 2026-11-04T08:21:20Z focused
- 2026-11-04T08:21:21Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T08:22:25Z done
- 2026-11-04T08:22:27Z committed 6936e68f (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2673 [FIX S, done, 3 steps] every list fm cuts at N says how many it left out and the flag that shows them: one helper in fmcore for the fmcli sites that cut silently
- T-2912 [FEATURE M, planned, 4 steps] A local-model arm for the next-request prediction: the 27B reads the user's recent asks, the open queue and the standing steers and …
- research mission-20261102-155156: Request: Genesis gen-3 Mission 7: #3 Anticipation (gen-0.md #3), per the standing mandate 'Genesis: build Foreman into a self-directing…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: pending T-2184] Standing rule: a capability whose free arm beats th…
## Regression test
none new: test_left_out is the regression test; it was red on this tree (recorded as step 1's first run, exit 1) and is green now
## Why not caught
the T-2912 lane's affected tests didn't include test_left_out
## Lessons
- a prompt is a reader too: a cut list in it says how many it left out, as the scan requires
## Plan gaps
- failed first: step 1 joinmore for both cuts
## Files touched
- plugin/lib/sampo/foresight.py
