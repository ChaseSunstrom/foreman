---
id: T-2423
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmoutcomes.py, plugin/tests/test_judgment.py, plugin/tests/test_outcomes.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-31T15:27:45Z
updated: 2026-11-02T01:38:07Z
base: e913482a2b28b51c587ed230ae46fbe43b5c4684
base_tree: 0cf2d720f984f6005dd48c7ddf57ea8768760ae4
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T01:17:52Z
plan0_scope: [plugin/lib/fmoutcomes.py, plugin/tests/test_judgment.py, plugin/tests/test_outcomes.py, CHANGELOG.md]
verified: strong
---
# The base rate counts held the way the bet scorer does: a correction or a smoke failure isn't a miss
## Raw request
> the base rate counts "smoke failed after" as a miss, but the survival score does not, so the Brier comparison is slightly biased
> (noticed by an agent; research T-2337-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] base_rate counts a close as held unless its first finish failed or a revert or later fix undid it (the scorer's survival misses); a task whose fate is 'smoke failed after' or 'corrected' counts held in the base rate, as it does for its bet — verify with `python3 plugin/tests/run.py test_judgment test_outcomes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: outs of 4 closes (held, smoke failed after, corrected, fixed later) give base_rate 75, not 25
2. [x] fmoutcomes.base_rate: held = first finish clean and fate not in (reverted, fixed later); Why not caught; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment.BaseRateHeld` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: BaseRateHeld 0s) / FAILED (1 classes: test_judgment.BaseRateHeld) [ran] [tree c95fedfd4acc] [world 2f1906870a] (2026-11-02T01:17:57Z)
- (step 1) `python3 plugin/tests/run.py test_judgment.BaseRateHeld` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: BaseRateHeld 0s) / OK [ran] [tree 501696fc8fb0] [world 2f1906870a] (2026-11-02T01:18:22Z)
- (step 2) `python3 plugin/tests/run.py test_judgment test_outcomes` → exit 0 · Ran 120 tests in 14.0s (35 classes, 16 at a time; slowest: Survival 14s, DoorPark 9s, ModelRouter 9s) / OK [ran] [tree 501696fc8fb0] [world 2f1906870a] (2026-11-02T01:18:36Z)
- `python3 plugin/tests/run.py test_judgment.BaseRateHeld` → ✗ exit 1 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: BaseRateHeld 0s) / FAILED (1 classes: test_judgment.BaseRateHeld) (start tree + this task's tests) [ran] [tree 501696fc8fb0] [world 2f1906870a] (2026-11-02T01:18:39Z)
- `python3 plugin/tests/run.py test_judgment.BaseRateHeld` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: BaseRateHeld 0s) / OK [ran] [tree 501696fc8fb0] [world 2f1906870a] (2026-11-02T01:18:39Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment test_outcomes` → exit 0 · Ran 120 tests in 13.9s (35 classes, 16 at a time; slowest: Survival 14s, DoorPark 9s, ModelRouter 9s) / OK [ran] [tree 31f5b4151fa0] [world 2f1906870a] (2026-11-02T01:24:50Z)
- (audit edge) `self-review: base_rate's held is now 'first finish clean and fate not in (reverted, fixed later)', the scorer's survival misses; corrected and smoke-failed fates count held, as they do for bets; the pool and the LEDGER_MIN fallback are unchanged` → a failed first finish still misses; reverted and fixed later miss; corrected and smoke failed after hold [tree 31f5b4151fa0] (2026-11-02T01:24:50Z)
- (audit self) `self-review: base_rate's held is now 'first finish clean and fate not in (reverted, fixed later)', the scorer's survival misses; corrected and smoke-failed fates count held, as they do for bets; the pool and the LEDGER_MIN fallback are unchanged` → no findings [tree 31f5b4151fa0] (2026-11-02T01:24:50Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 505d26a77d24] [world 2f1906870a] (2026-11-02T01:26:00Z)
## Log
- 2026-10-31T15:27:45Z created
- 2026-11-02T01:03:31Z planned from capture
- 2026-11-02T01:17:51Z focused
- 2026-11-02T01:17:52Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T01:18:39Z scope: CHANGELOG.md entry
- 2026-11-02T01:25:19Z done
- 2026-11-02T01:25:21Z committed e995cf90 (3 files)
- 2026-11-02T01:26:00Z guard authorization added: publish
- 2026-11-02T01:38:07Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- T-2337 [FEATURE M, done, 4 steps] Calibration ledger (Mission 5, #8): every stated confidence is a write-once bet scored later by signals Foreman didn't author, beside a…
- T-2499 [FEATURE M, done, 2 steps] Bets settle with no session: the night tick runs fmoutcomes.maintain; the digest names the kind whose Brier trails its base rate most —…
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Long-horizon tier is the deciding end-of-run score for every ca…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_outcomes.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, plugin/lib/fmoutcomes.py, plugin/tests/test_judgment.py, plugin/tests/test_outcomes.py; re-ground the plan against them before editing
## Why not caught
base_rate's tests seeded held and fixed-later fates only; the scorer's survival rule lives in _survival and _verdicts, and nothing compared the two definitions of held.
## Lessons
- Two numbers that are compared must be counted by one definition; a forecast scored by another rule than its baseline is biased by construction
## Plan gaps
- failed first: step 1 red test: outs of 4 closes (held, smoke failed after, corrected, fixed later) give base_rate 75, no…
## Files touched
- plugin/tests/test_judgment.py
- plugin/lib/fmoutcomes.py
- CHANGELOG.md
