---
id: T-2499
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmnight.py, plugin/lib/fmoutcomes.py, plugin/tests/test_night.py, plugin/tests/test_outcomes.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-01T19:05:34Z
updated: 2026-11-02T00:35:04Z
base: 867388844522f6b544bc3bae172feed0fa1073ad
base_tree: 80b1a6446b24887aebd587356fcdbff225ef4b12
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T00:26:39Z
plan0_scope: [plugin/lib/fmnight.py, plugin/lib/fmoutcomes.py, plugin/tests/test_night.py, plugin/tests/test_outcomes.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Bets settle with no session: the night tick runs fmoutcomes.maintain; the digest names the kind whose Brier trails its base rate most
## Raw request
> FEATURE: bets settle with no session: fm night's tick runs fmoutcomes.maintain, and the nightly digest names the bet kind whose Brier trails its base rate most, once 20 are scored
> DONE-WHEN: a tick with due bets writes their outcome rows; the digest line names the worst kind or says too few scored
## Interpretation
Reading 1: fm night's tick calls fmoutcomes.maintain so due outcome rows are written (and the bar check runs) on nights with no fm task finish; fm digest's ledger line adds the bet kind whose stated Brier is furthest above its base-rate Brier, once 20 are scored, else says too few. Reading 2: a separate nightly report file for the ledger. Reading 1 fits: the digest already carries the ledger line and the tick already runs per-project steps in their own try.
## Assumptions (confidence)
## Acceptance criteria
- [x] a tick with a due bet writes its outcome row (fm outcomes --judgment shows it scored) without any fm task finish — verify with `python3 plugin/tests/run.py test_night`
- [x] fm digest's ledger line names the kind whose stated Brier trails its base rate most once 20 are scored, and says too few before — verify with `python3 plugin/tests/run.py test_outcomes`
## Non-goals
## Approach (options → choice → why)
1) the tick gains a try-wrapped fmoutcomes.maintain(p) step beside the shadow pass; ledger_lines appends 'trails most: KIND (Brier stated S vs base B, n N)' from per-kind Briers over rows with a base, kinds under 5 rows skipped; fails if: per-kind counts stay tiny (then it says too few). 2) use what exists: fm task finish already runs maintain; fails if: days pass with no close, the very gap. 3) do less: only the tick step, no digest line; fails if: the request names the worst kind. Choice 1 (80%): one try-wrapped call in the tick and one clause in an existing line.
## Risks and rollback
Risk: maintain also runs the bar check, so a bar can rise overnight; it moves only on signals Foreman didn't author (survival, CI), as it does at a close. Risk: a slow outcomes() pass lengthens the tick; maintain returns at once when no ledger exists. Rollback: revert the commit; no state format changes.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/lib/fmcore.py, plugin/tests/test_guard.py; past FIXes T-0921, T-0980, T-0985, T-0986, T-0987.
## Execution prompt
## Steps
1. [x] red tests: test_night (a settled-but-unwritten choice bet; tick; its outcome row exists) and test_outcomes (seeded 20+ scored rows across two kinds; ledger_lines names the worse one; under 20 says too few)
2. [x] fmnight.tick: maintain step in its own try (a note on failure); fmoutcomes.ledger_lines: the trails-most clause; MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_night.NightTick test_outcomes.CalibrationTrails` → ✗ exit 1 · Ran 16 tests in 1.7s (2 classes, 16 at a time; slowest: NightTick 1s, CalibrationTrails 0s) / FAILED (2 classes: test_night.NightTick, test_outcomes.CalibrationTrails) [ran] [tree 2c27d1e90df4] [world 2f1906870a] (2026-11-02T00:26:54Z)
- (step 1) `python3 plugin/tests/run.py test_night.NightTick test_outcomes.CalibrationTrails` → exit 0 · Ran 16 tests in 1.7s (2 classes, 16 at a time; slowest: NightTick 1s, CalibrationTrails 0s) / OK [ran] [tree f6feff5c14c9] [world 2f1906870a] (2026-11-02T00:27:33Z)
- (step 2) `python3 plugin/tests/run.py test_night test_outcomes test_mcp` → exit 0 · Ran 125 tests in 14.5s (42 classes, 16 at a time; slowest: Survival 14s, ModelRouter 9s, CalibrationLedgerBets 9s) / OK [ran] [tree f6feff5c14c9] [world 2f1906870a] (2026-11-02T00:27:48Z)
- (ac 1) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 40 tests in 7.1s (12 classes, 16 at a time; slowest: Night 7s, NightInstall 2s, NightGuards 2s) / OK [ran] [tree 3e053b4a2e73] [world 2f1906870a] (2026-11-02T00:34:23Z)
- (ac 2) `python3 plugin/tests/run.py test_outcomes` → exit 0 · Ran 56 tests in 12.8s (15 classes, 16 at a time; slowest: Survival 13s, ModelRouter 8s, CalibrationLedgerBets 8s) / OK [ran] [tree 3e053b4a2e73] [world 2f1906870a] (2026-11-02T00:34:23Z)
- (audit intent) `self-review: the tick's new step is try-wrapped like its neighbours (a failure is a note, the tick goes on); maintain returns at once with no ledger; _trails compares per-kind stated Brier with the base rate's over rows with a base (5+ per kind) and only once 20 are scored; the digest line names it or says none trails; the too-few path is unchanged` → bets settle when no session closes a task, and the digest names the weakest kind of judgment so the user knows where stated numbers mislead [tree 3e053b4a2e73] (2026-11-02T00:34:23Z)
- (audit edge) `self-review: the tick's new step is try-wrapped like its neighbours (a failure is a note, the tick goes on); maintain returns at once with no ledger; _trails compares per-kind stated Brier with the base rate's over rows with a base (5+ per kind) and only once 20 are scored; the digest line names it or says none trails; the too-few path is unchanged` → a kind with under 5 based rows is skipped; equal Briers don't trail; a maintain that raises leaves a 'calibration:' note and the tick's other steps run [tree 3e053b4a2e73] (2026-11-02T00:34:23Z)
## Log
- 2026-11-01T19:05:34Z created
- 2026-11-02T00:01:11Z planned from capture
- 2026-11-02T00:01:17Z set approved=True
- 2026-11-02T00:26:38Z focused
- 2026-11-02T00:26:39Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T00:35:01Z done
- 2026-11-02T00:35:04Z committed 9925ea55 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- T-2500 [FEATURE M, planned, 2 steps] Bets carry their harness; fm outcomes --judgment --by-harness splits buckets and Brier by it
- T-2498 [FEATURE M, done, 3 steps] Interim calibration reads and reliability bins: fm outcomes --judgment adds a 7-day… — lesson: When a score needs a month to settle, sh…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- the similar finished task took 3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_night.py, plugin/tests/test_outcomes.py
## Preflight
Changed in scope since this was planned (2026-11-01): CHANGELOG.md, MASTER.md, plugin/lib/fmoutcomes.py, plugin/tests/test_outcomes.py; re-ground the plan against them before editing
## Lessons
- A score that waits on a session to settle stalls exactly when nobody is working; settle it on the clock
## Plan gaps
- failed first: step 1 red tests: test_night (a settled-but-unwritten choice bet; tick; its outcome row exists) and test_o…
## Files touched
- plugin/tests/test_night.py
- plugin/tests/test_outcomes.py
- plugin/lib/fmnight.py
- plugin/lib/fmoutcomes.py
- MASTER.md
- CHANGELOG.md
