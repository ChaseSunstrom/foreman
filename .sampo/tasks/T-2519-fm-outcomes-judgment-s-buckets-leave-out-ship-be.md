---
id: T-2519
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmoutcomes.py, plugin/tests/test_judgment.py, plugin/tests/test_outcomes.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T00:48:43Z
updated: 2026-11-02T01:00:18Z
base: 7210d0c7144aefe378bad660e80774afb12fdf1a
base_tree: ec348f9d99c8d1b5519255e5aa3dfb571896806d
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T00:49:35Z
plan0_scope: [plugin/lib/fmoutcomes.py, plugin/tests/test_judgment.py, plugin/tests/test_outcomes.py, CHANGELOG.md]
verified: strong
---
# fm outcomes --judgment's buckets show ship bets (kept out of the bars and routes)
## Raw request
> fm outcomes --judgment's buckets leave out ship bets: KINDS (fmoutcomes) has no 'ship', so tables() skips the 4 settled ship bets (85, 75, 85, 85: all held) though they count in 'scored 5'; add ship to the tables (it stays out of the bars and the routes, as T-2496 meant), so the user sees the one bet kind with outside outcomes so far
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm outcomes --judgment --json's kinds table has a ship row once a ship bet is scored; ship bets still never move a bar or a route — verify with `python3 plugin/tests/run.py test_judgment test_outcomes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a scored ship bet (seeded) shows in ledger_data's kinds as ship, and bar_rows/routes ignore it
2. [x] fmoutcomes: 'ship' in the kinds the tables read (KINDS or a TABLE_KINDS), the bars and routes unchanged; Why not caught; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment.ShipBets` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: ShipBets 0s) / FAILED (1 classes: test_judgment.ShipBets) [ran] [tree 5c8e485545a7] [world 2f1906870a] (2026-11-02T00:49:55Z)
- (step 1) `python3 plugin/tests/run.py test_judgment.ShipBets` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: ShipBets 0s) / OK [ran] [tree 344a5b1ebdde] [world 2f1906870a] (2026-11-02T00:50:25Z)
- (step 2) `python3 plugin/tests/run.py test_judgment test_outcomes test_mcp test_site` → exit 0 · Ran 183 tests in 29.7s (68 classes, 16 at a time; slowest: Survival 29s, DoorPark 20s, CalibrationLedgerBets 20s) / OK [ran] [tree 344a5b1ebdde] [world 2f1906870a] (2026-11-02T00:50:56Z)
- `python3 plugin/tests/run.py test_judgment.ShipBets` → ✗ exit 1 · Ran 1 tests in 2.5s (1 classes, 16 at a time; slowest: ShipBets 0s) / FAILED (1 classes: test_judgment.ShipBets) (start tree + this task's tests) [ran] [tree 344a5b1ebdde] [world 2f1906870a] (2026-11-02T00:51:00Z)
- `python3 plugin/tests/run.py test_judgment.ShipBets` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: ShipBets 0s) / OK [ran] [tree 344a5b1ebdde] [world 2f1906870a] (2026-11-02T00:51:00Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment test_outcomes` → exit 0 · Ran 119 tests in 14.1s (34 classes, 16 at a time; slowest: Survival 14s, DoorPark 9s, ModelRouter 9s) / OK [ran] [tree d21c4fd418e5] [world 2f1906870a] (2026-11-02T00:59:47Z)
- (audit edge) `self-review: 'ship' joins KINDS, which only tables() and _trails read; bar_rows filters by source and kind on its own and the test asserts it still returns [] for ship rows; routes read stated vs base per tier/type pair, which ship rows carry none of; the real table now shows 4 ship bets held` → no ship bets → no ship row; a pending ship bet isn't in the table (scored rows only); bars unchanged [tree d21c4fd418e5] (2026-11-02T00:59:47Z)
- (audit self) `self-review: 'ship' joins KINDS, which only tables() and _trails read; bar_rows filters by source and kind on its own and the test asserts it still returns [] for ship rows; routes read stated vs base per tier/type pair, which ship rows carry none of; the real table now shows 4 ship bets held` → no findings [tree d21c4fd418e5] (2026-11-02T00:59:47Z)
## Log
- 2026-11-02T00:48:43Z created
- 2026-11-02T00:49:33Z planned from capture
- 2026-11-02T00:49:34Z focused
- 2026-11-02T00:49:35Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T00:51:10Z scope: CHANGELOG.md entry
- 2026-11-02T01:00:15Z done
- 2026-11-02T01:00:18Z committed 8549dbc9 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2498 [FEATURE M, done, 3 steps] Interim calibration reads and reliability bins: fm outcomes --judgment adds a 7-day… — lesson: When a score needs a month to settle, sh…
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- T-2496 [FEATURE M, done, 3 steps] Ship bets: fm ship --chance NN records a write-once "ship" bet keyed by the pushed… — lesson: the fastest honest score for a stated con…
- decision 2026-10-30: [revisited: weakness-finding uses signals] [cites: user steer 2026-10-30] [check: python3 plugin/tests/run.py test_exam.ExamAuthors] Standing rule: …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_outcomes.py
## Why not caught
T-2496's test checked a ship bet's verdict and that it moves no bar, never the --judgment table a user reads; KINDS (the tables' list) predates the ship kind.
## Lessons
- When a new kind of record is added, check every list that enumerates kinds; a kind missing from one list is silently invisible there
## Plan gaps
- failed first: step 1 red test: a scored ship bet (seeded) shows in ledger_data's kinds as ship, and bar_rows/routes igno…
## Files touched
- plugin/tests/test_judgment.py
- plugin/lib/fmoutcomes.py
- CHANGELOG.md
