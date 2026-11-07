---
id: T-3069
type: FIX
tier: S
status: done
priority: low
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/foresight.py, plugin/lib/sampo/outcomes.py, plugin/lib/sampo/triggers.py, plugin/tests/test_foresight.py]
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:13Z
updated: 2026-11-06T16:29:48Z
trigger: genesis-review
trigger_key: 43e2306442479bcc
base: 74e8d98a05b695ab98f8b23f241802a3b888d156
base_tree: b7d8030fca78b8467da6a2281643f125211b127f
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T12:46:41Z
plan0_scope: []
builder_returned: 2026-11-06T13:16:49Z
lane_stop: merged 2026-11-06T14:07:50Z
verified: strong
unproven: [meaning]
lane_verified: 4fa15eda56c663f17991a74339e383aea8fdb8e1
---
# The next-request predictor is shown as leading only when its lead over the naive guess is significant on replay, not three rows
## Raw request
> FIX: cross-cutting review gen-4 #13 (what is being measured wrong): The next-request predictor ties the naive guess on replay (paths 0.088 vs 0.086) yet ships as a scored arm "shown only when it leads"; three rows over naive is noise, not a lead. [259/376 (naive 256)]
> genesis-review 4:13
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the predictor's arm counts as leading only when a paired test over the replay (its hits against the naive guess's, case by case) gives p < 0.05 and the lead is at least 2 points; 259 against 256 of 376 (today) reads 'level with naive', and the self-running line and any surface that shows it say so — verify with `python3 plugin/tests/run.py test_foresight test_exam`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: 259 vs 256 of 376 is level; a clear lead (300 vs 256) leads
2. [x] the paired test where the arm's lead is decided
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_foresight.PairedLead` → exit 0 · Ran 2 tests in 61.7s (1 jobs, 16 at a time; slowest: PairedLead 0s) / OK [ran] [tree 98fa22150a64] [world 2f1906870a] (2026-11-06T12:48:26Z)
- (step 2) `python3 plugin/tests/run.py test_foresight test_exam` → ✗ exit 1 · Ran 161 tests in 222.3s (84 jobs, 16 at a time; slowest: JudgmentKinds 71s, LeanKindGateHookDelay 63s, LeanKindGateSessionLine 58s) / FAILED (1 classes: test_foresight.DraftAhead) [ran] [tree 98fa22150a64] [world 2f1906870a] (2026-11-06T12:52:10Z)
- (step 2) `python3 plugin/tests/run.py test_foresight.DraftAhead test_foresight.PairedLead test_foresight.PredictionBook test_foresight.LocalArm` → exit 0 · Ran 17 tests in 42.6s (12 jobs, 16 at a time; slowest: PredictionBook.test_predictions_report_hit_rates_beside_the_baseline_and_mute_a_kind_that_trails_it 3s, LocalArm 2s, DraftAhead 2s) / OK [ran] [tree cfead9c02b04] [world 2f1906870a] (2026-11-06T12:53:40Z)
- (step 2) `python3 plugin/tests/run.py test_foresight test_exam` → exit 0 · Ran 162 tests in 219.8s (105 jobs, 16 at a time; slowest: LeanKindGateHookDelay 61s, LeanKindGateSessionLine 47s, LeanKindGateGuardAllow 45s) / OK [ran] [tree 13ee5801c89b] [world 2f1906870a] (2026-11-06T13:16:25Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 6e5108b3f12c] (2026-11-06T14:07:53Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight test_exam` → exit 0 · Ran 162 tests in 257.5s (103 jobs, 16 at a time; slowest: LeanKindGateHookDelay 57s, LeanKindGateSessionLine 51s, LeanKindGateGuardAllow 49s) / OK [ran] [tree 6e5108b3f12c] [world 2f1906870a] (2026-11-06T14:12:15Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 6e5108b3f12c] (2026-11-06T14:12:15Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 6e5108b3f12c] (2026-11-06T14:12:15Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 6e5108b3f12c] (2026-11-06T14:12:15Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 6e5108b3f12c] (2026-11-06T14:12:15Z)
## Log
- 2026-11-05T00:31:13Z created
- 2026-11-05T04:43:37Z planned from capture
- 2026-11-05T04:43:38Z set approved=True
- 2026-11-05T04:43:38Z blocked: approved; waits for a builder slot
- 2026-11-06T03:52:38Z unblocked
- 2026-11-06T12:46:40Z focused
- 2026-11-06T12:46:41Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T14:07:50Z merged worktree-agent-aa05b259e10228de1 (4 file(s))
- 2026-11-06T14:07:50Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa05b259e10228de1
- 2026-11-06T14:07:51Z focused
- 2026-11-06T14:07:53Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/foresight.py', 'plugin/lib/sampo/outcomes.py', 'plugin/lib/sampo/triggers.py', 'plugin/tests/test_foresight.py']
- 2026-11-06T14:07:53Z scope: widened at merge to the reviewed lane's own diff (4fa15eda5), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T14:15:25Z done
- 2026-11-06T14:15:31Z committed c53e668e2 (1 file)
- 2026-11-06T16:29:48Z verified: the full suite is green on 1078ed22d, which contains 4fa15eda5
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3133 [FIX M, planned, 6 steps] Batch: FIX: cross-cutting review gen-4 #5 (wha…; FIX: cross-cutting review gen-4 #12 (wh…; FIX: cross-cutting review ge…
- T-3070 [FIX L, dropped, 0 steps] FIX: cross-cutting review gen-4 #14 (what is being measured wrong): Live hook p95 is 315…
- T-3134 [FIX M, planned, 4 steps] Batch: FIX: cross-cutting review gen-4 #8 (wha…; FIX: cross-cutting review gen-4 #11 (wh…; FIX: cross-cutting review ge…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 2 the paired test where the arm's lead is decided
## Files touched
- .fm-scratch/e.json
- plugin/lib/sampo/foresight.py
- .fm-scratch/e2.json
- plugin/lib/sampo/outcomes.py
- plugin/lib/sampo/triggers.py
- plugin/tests/test_foresight.py
- .fm-scratch/e3.json
- .fm-scratch/e4.json
- CHANGELOG.md
