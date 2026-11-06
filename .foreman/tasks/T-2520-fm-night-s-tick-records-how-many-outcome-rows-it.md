---
id: T-2520
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmoutcomes.py, plugin/lib/fmnight.py, plugin/tests/test_night.py, plugin/tests/test_judgment.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T00:49:21Z
updated: 2026-11-02T01:17:46Z
base: 180aef8bb05fcc688f5b9f50e4149d7ac197f45a
base_tree: 5bae01a91c476d9b66120207b628fba51d6458be
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T01:09:58Z
plan0_scope: [plugin/lib/fmoutcomes.py, plugin/lib/fmnight.py, plugin/tests/test_night.py, plugin/tests/test_judgment.py, CHANGELOG.md]
verified: strong
---
# fm night's tick records how many bets it settled
## Raw request
> fm night's tick records how many outcome rows its fmoutcomes.maintain step wrote (a 'settled' count in the tick's result and its night_tick event when nonzero), so 'bets settle with no session' is measured, not assumed (gen-2 Mission 2 critique)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fmoutcomes.maintain returns the outcome rows it wrote (settle's count; 0 with no ledger or on an error); the tick's result carries settled, its night_tick event is written when settled > 0 and carries it, and its printed line says 'N bet(s) settled' — verify with `python3 plugin/tests/run.py test_night test_judgment`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: maintain returns 1 after a ci_verdict settles a ship bet (and 0 the second time); a tick with maintain mocked to return 2 has res['settled'] == 2 and a night_tick event with settled 2
2. [x] maintain returns settle()'s count; tick stores res['settled'], logs it in night_tick (the condition gains settled), prints it; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment.ShipBets test_night.NightTick` → ✗ exit 1 · Ran 15 tests in 1.6s (2 classes, 16 at a time; slowest: NightTick 1s, ShipBets 0s) / FAILED (2 classes: test_night.NightTick, test_judgment.ShipBets) [ran] [tree 36765546e0e2] [world 2f1906870a] (2026-11-02T01:10:06Z)
- (step 1) `python3 plugin/tests/run.py test_judgment.ShipBets test_night.NightTick` → exit 0 · Ran 15 tests in 1.7s (2 classes, 16 at a time; slowest: NightTick 1s, ShipBets 0s) / OK [ran] [tree 9b9d95e59bea] [world 2f1906870a] (2026-11-02T01:10:47Z)
- (step 2) `python3 plugin/tests/run.py test_night test_judgment test_outcomes` → exit 0 · Ran 159 tests in 15.2s (46 classes, 16 at a time; slowest: Survival 15s, DoorPark 10s, CalibrationLedgerBets 10s) / OK [ran] [tree 9b9d95e59bea] [world 2f1906870a] (2026-11-02T01:11:02Z)
- (ac 1) `python3 plugin/tests/run.py test_night test_judgment` → exit 0 · Ran 101 tests in 8.8s (30 classes, 16 at a time; slowest: DoorPark 9s, Night 7s, DoorGate 4s) / OK [ran] [tree 0cf2d720f984] [world 2f1906870a] (2026-11-02T01:17:14Z)
- (audit edge) `self-review: maintain returns settle()'s count (0 with no ledger or on any error, which it still swallows); its other callers (fm task finish, ci-watch) ignore the value as before; the tick stores res['settled'], writes night_tick when it is nonzero (with the count) and prints 'N bet(s) settled'` → a second maintain writes 0; a maintain that raises is caught in maintain (0) and the tick's own try notes an import failure; a quiet night writes no event, as before [tree 0cf2d720f984] (2026-11-02T01:17:14Z)
- (audit self) `self-review: maintain returns settle()'s count (0 with no ledger or on any error, which it still swallows); its other callers (fm task finish, ci-watch) ignore the value as before; the tick stores res['settled'], writes night_tick when it is nonzero (with the count) and prints 'N bet(s) settled'` → no findings [tree 0cf2d720f984] (2026-11-02T01:17:14Z)
## Log
- 2026-11-02T00:49:21Z created
- 2026-11-02T00:52:37Z planned from capture
- 2026-11-02T01:09:57Z focused
- 2026-11-02T01:09:58Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T01:17:43Z done
- 2026-11-02T01:17:46Z committed e913482a (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2499 [FEATURE M, done, 2 steps] Bets settle with no session: the night tick runs fmoutcomes.maintain; the digest names the kind whose Brier trails its base rate most —…
- T-2357 [FEATURE M, done, 3 steps] Installs are queued for one yes: night and tick timers staged, asked once, installed only after the user's yes (Mission 8, #11) — lesso…
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- decision 2026-11-01: [revisited: finish round 1 completely] [cites: user steer 2026-10-31: (2) Finish round 1 completely, in order: Mission 4's remaining work, then writ…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_night.py, plugin/tests/test_outcomes.py
## Lessons
- A background step that changes state should leave a count of what it changed, or nobody can tell it ran
## Plan gaps
- failed first: step 1 red tests: maintain returns 1 after a ci_verdict settles a ship bet (and 0 the second time); a tick…
## Files touched
- plugin/tests/test_judgment.py
- plugin/tests/test_night.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmnight.py
- CHANGELOG.md
