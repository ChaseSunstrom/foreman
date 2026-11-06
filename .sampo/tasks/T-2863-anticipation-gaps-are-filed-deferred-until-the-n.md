---
id: T-2863
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T00:35:03Z
updated: 2026-11-04T00:42:53Z
base: 1c5eb344c911a84b9724807e0daca40447bf4038
base_tree: e18b060ef90e0fe5d58acfd93b56d3e8150e3635
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T00:35:05Z
plan0_scope: []
verified: strong
---
# Anticipation gaps are filed deferred until the next generation's seal, so the drive never offers them as work
## Raw request
> Anticipation gaps are filed deferred until the next generation's seal, so the drive never offers them as work
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a missed steer files its gap deferred with the reason, and the next seal still closes it — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: the gap test expects deferred, then score_steer defers the new capture
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 216 tests in 44.0s (24 classes, 16 at a time; slowest: GenesisRead 41s, GenerationReview 38s, GenesisCheck 34s) / FAILED (1 classes: test_genesis.SealedPrediction) (start tree + this task's tests) [ran] [tree dad2a77fdca9] [world 2f1906870a] (2026-11-04T00:36:26Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 216 tests in 29.3s (24 classes, 16 at a time; slowest: GenesisRead 29s, GenerationReview 26s, GenesisCheck 23s) / FAILED (1 classes: test_genesis.SealedPrediction) [ran] [tree dad2a77fdca9] [world 2f1906870a] (2026-11-04T00:36:26Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 216 tests in 31.3s (24 classes, 16 at a time; slowest: GenesisRead 31s, GenerationReview 29s, GenesisCheck 25s) / OK [ran] [tree 24de4078f505] [world 2f1906870a] (2026-11-04T00:39:27Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 216 tests in 35.1s (24 classes, 16 at a time; slowest: GenesisRead 33s, GenerationReview 29s, ProofBeforePresentation 27s) / FAILED (1 classes: test_genesis.SealedPrediction) (start tree + this task's tests) [ran] [tree 24de4078f505] [world 2f1906870a] (2026-11-04T00:40:36Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 216 tests in 32.4s (24 classes, 16 at a time; slowest: GenesisRead 32s, GenerationReview 29s, GenesisCheck 25s) / OK [ran] [tree 24de4078f505] [world 2f1906870a] (2026-11-04T00:40:36Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T00:40:36Z [ran] [tree 24de4078f505] [world 2f1906870a] (2026-11-04T00:40:41Z)
- (audit edge) `self-review: score_steer defers only a gap it just captured (new, still captured), logs why, and _close_gaps still closes any open gap at the next seal (the same test seals gen-2 and sees done)` → a held or muted trigger returns no brief (guarded); a deduped repeat (new False) is left as it is [tree 24de4078f505] (2026-11-04T00:40:41Z)
- (audit self) `self-review: score_steer defers only a gap it just captured (new, still captured), logs why, and _close_gaps still closes any open gap at the next seal (the same test seals gen-2 and sees done)` → no findings [tree 24de4078f505] (2026-11-04T00:40:41Z)
## Log
- 2026-11-04T00:35:03Z created
- 2026-11-04T00:35:04Z focused
- 2026-11-04T00:35:05Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T00:42:51Z done
- 2026-11-04T00:42:53Z committed 8d812586 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2774 [CLEAN M, done, 3 steps] Rune's anticipation gaps are consumed, not dropped: the next generation's predict action lists the last generation's missed steers, and s…
- T-2806 [FEATURE M, blocked, 0 steps] FEATURE: anticipation gap (#3): the user's steer wasn't among gen-4's sealed…
- T-2505 [FEATURE L, done, 4 steps] Find what nobody thought of: each generation writes a sealed prediction of the user's… — lesson: fmgenesis is large enough that a short…
- decision 2026-11-01: [revisited: T-2450 (the secrets finder reads a date as a credential)] [cites: user steer 2026-10-31: finish round 1 completely, in order; no new mai…
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–4 steps
## Why not caught
T-2774 filed gaps as inbox captures; the drive offers every capture as work, 13 times in one evening with the trigger at 0.00 precision
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/sampo/rune.py
