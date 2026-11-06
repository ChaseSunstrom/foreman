---
id: T-2611
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmoutcomes.py, plugin/lib/fmrelease.py, plugin/tests/test_judgment.py, CHANGELOG.md, plugin/skills/playbooks/references/release/ship-to-main.md]
depends_on: []
source: genesis
created: 2026-11-02T13:14:27Z
updated: 2026-11-02T13:56:21Z
base: 221357ee3caadb14c01de43343fb0478517587da
base_tree: 2bf1546fc7acfd8aecd9af2ad0805144a8848942
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T13:39:21Z
plan0_scope: [plugin/lib/fmoutcomes.py, plugin/lib/fmrelease.py, plugin/tests/test_judgment.py, CHANGELOG.md, plugin/skills/playbooks/references/release/ship-to-main.md]
verified: strong
---
# fm ship --chance names the ship record when the chance sits 15+ points from 20+ settled ship bets
## Raw request
> FEATURE: fm ship --chance N names the ship record in one line when N sits 15+ points from the held share of 20+ settled ship bets, like the plan's base-rate note (T-2497); CHANGELOG and release/ship-to-main.md say it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a ship chance 15+ points from the held share of 20+ settled ship bets prints one record line; within 15, or under 20 settled, prints none — verify with `python3 plugin/tests/run.py test_judgment.ShipNote`
- [x] fm ship prints the line after its Ship bet line — verify with `python3 plugin/tests/run.py test_judgment.ShipNote`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: test_judgment.ShipNote
2. [x] fmoutcomes.ship_note and its print in fmrelease after the Ship bet line
3. [x] docs: CHANGELOG, ship-to-main.md
## Resume here
## Docs impact
CHANGELOG (Unreleased entry); playbooks/references/release/ship-to-main.md (the record line after the ship bet).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment.ShipNote test_ship.Ship` → ✗ exit 1 · Ran 39 tests in 28.9s (2 classes, 16 at a time; slowest: Ship 29s, ShipNote 1s) / FAILED (2 classes: test_ship.Ship, test_judgment.ShipNote) [ran] [tree 0971975885f0] [world 2f1906870a] (2026-11-02T13:40:33Z)
- (step 2) `python3 plugin/tests/run.py test_judgment test_ship test_outcomes` → ✗ exit 1 · Ran 169 tests in 30.7s (39 classes, 16 at a time; slowest: Ship 30s, Survival 14s, DoorPark 10s) / FAILED (1 classes: test_judgment.ShipNote) [ran] [tree a3d39287c3d3] [world 2f1906870a] (2026-11-02T13:41:04Z)
- (step 2) `python3 plugin/tests/run.py test_judgment test_ship test_outcomes` → exit 0 · Ran 169 tests in 30.5s (39 classes, 16 at a time; slowest: Ship 30s, Survival 14s, DoorPark 10s) / OK [ran] [tree f9da1113e647] [world 2f1906870a] (2026-11-02T13:41:46Z)
- (audit edge) `self (S: no reviewer pass in economy mode)` → the just-booked bet is pending, so it never counts toward its own record; under 20 settled or within 15 points prints nothing; a bad chance can't reach here (ship refuses it before any push); scored() errors return '' so a note never fails a ship that already landed [tree 80e2251b21d2] (2026-11-02T13:42:01Z)
- (step 3) `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 80e2251b21d2] [world 2f1906870a] (2026-11-02T13:42:15Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment.ShipNote` → exit 0 · Ran 3 tests in 0.9s (1 classes, 16 at a time; slowest: ShipNote 1s) / OK [ran] [tree 80e2251b21d2] [world 2f1906870a] (2026-11-02T13:48:16Z)
- (ac 2) `python3 plugin/tests/run.py test_judgment.ShipNote` → exit 0 · Ran 3 tests in 0.9s (1 classes, 16 at a time; slowest: ShipNote 1s) / OK [ran] [tree 80e2251b21d2] [world 2f1906870a] (2026-11-02T13:48:16Z)
- (step 1) `python3 plugin/tests/run.py test_judgment.ShipNote test_ship.Ship` → exit 0 · Ran 39 tests in 29.0s (2 classes, 16 at a time; slowest: Ship 29s, ShipNote 1s) / OK [ran] [tree 80e2251b21d2] [world 2f1906870a] (2026-11-02T13:48:16Z)
- (audit edge) `self (S: no reviewer pass in economy mode); the e2e ship test shows the line after the bet` → the just-booked bet is pending so it never counts toward its own record; under 20 settled or within 15 points prints nothing; errors return '' [tree 80e2251b21d2] (2026-11-02T13:48:16Z)
- (audit self) `self (S: no reviewer pass in economy mode); the e2e ship test shows the line after the bet` → no findings [tree 80e2251b21d2] (2026-11-02T13:48:16Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 80e2251b21d2] [world 2f1906870a] (2026-11-02T13:50:39Z)
## Log
- 2026-11-02T13:14:27Z created
- 2026-11-02T13:14:39Z set tier=S
- 2026-11-02T13:25:02Z planned from capture
- 2026-11-02T13:39:20Z focused
- 2026-11-02T13:39:21Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T13:41:46Z scope: test_ship.Ship gains the end-to-end check that fm ship prints the record line after its bet
- 2026-11-02T13:49:42Z done
- 2026-11-02T13:49:45Z committed 71981f46 (6 files)
- 2026-11-02T13:50:39Z guard authorization added: publish
- 2026-11-02T13:56:21Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2610 [FIX M, done, 3 steps] Calibration reads compare like with like: a close or a task or choice bet counts once its 30-day window finished — lesson: When one read of…
- T-2499 [FEATURE M, done, 2 steps] Bets settle with no session: the night tick runs fmoutcomes.maintain; the digest names the kind whose Brier trails its base rate most —…
- T-2496 [FEATURE M, done, 3 steps] Ship bets: fm ship --chance NN records a write-once "ship" bet keyed by the pushed… — lesson: the fastest honest score for a stated con…
- decision 2026-11-02: [costly] Release 1.2.51: its push step conflicted because fm ship cherry-picks left foreman/build and main with diverged histories (merge base 2026-…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_board_surfaces.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_cost.py, plugin/test…
## Lessons
- A fixture that fakes commit shas must vary the characters the code keys on: ship bets key on the first 12, so f'{i:040x}' wrote one bet, not twenty
## Plan gaps
- failed first: step 1 red: test_judgment.ShipNote
- failed first: step 2 fmoutcomes.ship_note and its print in fmrelease after the Ship bet line
## Files touched
- plugin/tests/test_judgment.py
- plugin/tests/test_ship.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
- plugin/skills/playbooks/references/release/ship-to-main.md
