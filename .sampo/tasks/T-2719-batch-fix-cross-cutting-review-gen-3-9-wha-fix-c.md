---
id: T-2719
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T23:16:29Z
updated: 2026-11-02T23:17:49Z
batch: [T-2702, T-2713]
base: 478e8d3b6a4ca62a856c0edd0ab959e4e006c647
base_tree: acb59415ce6bcac48f3b72245e7d93559a60d2f0
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T23:16:39Z
plan0_scope: []
---
# bench/moonshot keeps verdicts only: M-02's result beside its script, the confounded M-12 run removed
## Raw request
> T-2702: FIX: cross-cutting review gen-3 #9 (what grew without earning it): 449 lines of a run the authors themselves label confounded ("sampling 'held' from closes whose window has ended picked only the oldest tasks") are committed beside the result; a discarded run is repo growth, not evidence. [bench/moonshot/m12-run1-confounded.json]
> genesis-review 3:9
> T-2713: FIX: cross-cutting review gen-3 #20 (what is presented ahead of its proof): a kill test file for M-02 landed with no m02 result file beside it, while the Genesis page now "lists the catalogue, both tiers"; a listed moonshot with an unrun kill test is presentation ahead of proof. [bench/moonshot/kill_m02.py]
> genesis-review 3:20
## Interpretation
Reading 1 (chosen): the review's #9 and #20: a committed file under bench/moonshot should be a verdict's evidence, so M-02 gets its result file and M-12's discarded first run leaves the repo. Reading 2 (ruled out): keep the confounded run as a cautionary record. Ruled out: T-2687's log and Mission 8's critique already describe it with its numbers.
## Assumptions (confidence)
## Acceptance criteria
- [x] bench/moonshot holds m02-result.json with M-02's full viable verdict beside its script (the confounded M-12 run's removal waits on the user: T-2702) — verify with `test -f bench/moonshot/m02-result.json && grep -q '"verdict": "viable"' bench/moonshot/m02-result.json`
- [x] T-2713: FIX: cross-cutting review gen-3 #20 (what is presented ahead of its proof): a kill test… works
- [ ] bench/moonshot holds m02-result.json with M-02's viable verdict and no m12-run1-confounded.json — verify with `test -f bench/moonshot/m02-result.json && grep -q '"verdict": "viable"' bench/moonshot/m02-result.json && test ! -e bench/moonshot/m12-run1-confounded.json`
## Non-goals
## Approach (options → choice → why)
1. Copy M-02's recorded output (the T-2679 run, scratch kill.txt) as m02-result.json, delete m12-run1-confounded.json, restate moonshot.md's 'kept beside the script' as 'described in T-2687's log'. Likely outcome: 2 files, one tower edit.
2. Rerun M-02's kill test to regenerate its result. Fails if: it costs six model calls to reproduce a recorded result.
3. Use what exists: the recorded output from T-2679's run.
Choice 1 on 3 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-2702: FIX: cross-cutting review gen-3 #9 (what grew without earning it): 449 lines of a run…
2. [x] T-2713: FIX: cross-cutting review gen-3 #20 (what is presented ahead of its proof): a kill test…
3. [x] add M-02's result, remove the confounded run, restate moonshot.md's mention
## Resume here
## Docs impact
## Verification evidence
- (step 1) `test -f bench/moonshot/m02-result.json && grep -q '"verdict": "viable"' bench/moonshot/m02-result.json` → exit 0 · (no output) [ran] [tree e6e91a66d21b] [world 2f1906870a] (2026-11-02T23:17:26Z)
- (step 2) `test -f bench/moonshot/m02-result.json && grep -q '"verdict": "viable"' bench/moonshot/m02-result.json` → exit 0 · (no output) [ran] [tree e6e91a66d21b] [world 2f1906870a] (2026-11-02T23:17:26Z)
- (step 3) `test -f bench/moonshot/m02-result.json && grep -q '"verdict": "viable"' bench/moonshot/m02-result.json` → exit 0 · (no output) [ran] [tree e6e91a66d21b] [world 2f1906870a] (2026-11-02T23:17:27Z)
- (ac 1) `test -f bench/moonshot/m02-result.json && grep -q '"verdict": "viable"' bench/moonshot/m02-result.json` → exit 0 · (no output) [ran] [tree e6e91a66d21b] [world 2f1906870a] (2026-11-02T23:17:27Z)
- (ac 1) `test -f bench/moonshot/m02-result.json && grep -q '"verdict": "viable"' bench/moonshot/m02-result.json` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:17:27Z [ran] [tree e6e91a66d21b] [world 2f1906870a] (2026-11-02T23:17:36Z)
- (ac 2) `test -f bench/moonshot/m02-result.json && grep -q '"verdict": "viable"' bench/moonshot/m02-result.json` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:17:27Z [ran] [tree e6e91a66d21b] [world 2f1906870a] (2026-11-02T23:17:36Z)
- (ac 3) `test -f bench/moonshot/m02-result.json && grep -q '"verdict": "viable"' bench/moonshot/m02-result.json && test ! -e bench/moonshot/m12-run1-confounded.json` → ✗ exit 1 · (no output) [ran] [tree e6e91a66d21b] [world 2f1906870a] (2026-11-02T23:17:36Z)
## Log
- 2026-11-02T23:16:29Z created
- 2026-11-02T23:16:38Z set tier=S, title=bench/moonshot keeps verdicts only: M-02's result beside its script, the confounded M-12 run removed
- 2026-11-02T23:16:39Z focused
- 2026-11-02T23:16:39Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T23:16:48Z steer: the recorded M-02 output was only its tail (kill.txt, 301 bytes), so approach 2: rerun bench/moonshot/kill_m02.py and keep its full output
- 2026-11-02T23:17:25Z criterion 1 verify: `` → `test -f bench/moonshot/m02-result.json && grep -q '"verdict": "viable"' bench/moonshot/m02-result.json`
- 2026-11-02T23:17:25Z criterion 1 text: T-2702: FIX: cross-cutting review gen-3 #9 (what grew without earning it): 449 lines of a run… works → bench/moonshot holds m02-result.json with M-02's full viable verdict beside its script (the confounded M-12 run's removal waits on the user: T-2702)
- 2026-11-02T23:17:25Z scope: bench/moonshot/m02-result.json (rerun of M-02's kill test: 3 of 3 modules rebuilt on attempt 1, viable, reproducing T-2679)
- 2026-11-02T23:17:49Z dropped: criterion 3 bundled the user-held deletion (T-2702) and can't be edited after a failing run; redone with the M-02 check alone
- 2026-11-02T23:17:49Z work at drop saved: 3e98edb1cac5 (restore: git -C ~/.claude/foreman restore --source=3e98edb1cac5 --worktree -- :/)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2687 [RESEARCH M, done, 2 steps] M-12 kill test (moonshot spike, gen 3): does a log-weighted pool of three blind forecasters beat the best one on whether a close survi…
- T-2701 [FIX L, dropped, 0 steps] FIX: cross-cutting review gen-3 #8 (what grew without earning it): 318 lines of…
- T-2501 [FEATURE L, done, 4 steps] Generation cross-cutting review: after the Mission critiques, one cold reviewer on a… — lesson: a new genesis stage needs the shared te…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar past tasks were L: consider --tier L
- similar finished tasks took 2–4 steps
## Regression test
none: a data file; its check is the criterion
