---
id: T-2610
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmoutcomes.py, plugin/tests/test_outcomes.py, CHANGELOG.md, MASTER.md, plugin/skills/intake/references/planning.md]
depends_on: []
source: genesis
created: 2026-11-02T13:14:27Z
updated: 2026-11-02T13:39:10Z
base: c5fbfafc89afb22d0f5e09cbf7bc0d6474737ccb
base_tree: fbf742c28bdb03555013ddc688bdd42e75f8a0ec
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-02T13:16:33Z
plan0_scope: [plugin/lib/fmoutcomes.py, plugin/tests/test_outcomes.py, CHANGELOG.md, MASTER.md, plugin/skills/intake/references/planning.md]
verified: strong
---
# Calibration reads compare like with like: a close or a task or choice bet counts once its 30-day window finished
## Raw request
> FIX: calibration reads compare like with like: fmoutcomes.track, tables, brier, the trails clause, the bar check (bar_rows) and base_rate count a close or a task or choice bet only once its 30-day window finished (window_done), as survival_lines does since T-2584; misses inside open windows are named apart ("N lost in open windows, not scored yet"); MASTER, CHANGELOG and intake/references/planning.md say it
## Interpretation
Reading 1 (chosen): every read that turns closes or task and choice bets into a held share must count a close only once its 30-day window has finished, because a miss lands mid-window and a hold only after it; today fm outcomes' track record says FEATURE M held 21 of 43 while finished windows held 95%. Reading 2: only the research bar check matters (it is the read that changes behavior), and the display lines may stay; rejected because the track record is shown at every fm focus and the plan's base-rate note reads base_rate, so a biased display steers judgment too.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm outcomes' track record counts a close as held or not only once its window finished — verify with `python3 plugin/tests/run.py test_outcomes.CensoredReads`
- [x] a task or choice bet missed inside an open window is pending in the ledger's buckets, Briers and bar check, and named in an open-windows line — verify with `python3 plugin/tests/run.py test_outcomes.CensoredReads`
- [x] base_rate pools only closes whose window finished, or whose window is unknown — verify with `python3 plugin/tests/run.py test_outcomes.CensoredReads`
- [x] the existing outcome and judgment tests still pass — verify with `python3 plugin/tests/run.py test_outcomes test_judgment test_planning`
## Non-goals
## Approach (options → choice → why)
1) scored() marks a task or choice bet whose task's window is still open as pending (outcome None) and keeps the would-be grade as early; every reader (tables, brier, routes, trails, bar_rows, the trial grader, --by harness) then skips it with no change of its own; track and base_rate gate on window_done; ledger_data counts early misses for an open-windows line. Outcome: one filter where all readers route; grade rows stay write-once. Fails if: a reader reads grade rows directly instead of scored() (only settle does, and it should). 2) use what exists: show the interim read (T-2498) beside the biased numbers as the honest one. Fails if: the bar check and focus line still read the biased rows. 3) do less: stop settling task and choice bets until their window ends. Fails if: a revert mid-window is evidence that should be written at once, and grade rows already written stay. Choice 1 (85%): the root-cause filter at the one function every reader calls.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: test_outcomes.CensoredReads for the track record, the ledger and base_rate
2. [x] fix: scored() marks open-window task and choice bets pending with early; track and base_rate gate on window_done; open-windows line in ledger_lines and --judgment
3. [x] docs: CHANGELOG, MASTER (fmoutcomes), planning.md calibration section
## Resume here
## Docs impact
CHANGELOG (Unreleased entry); MASTER.md fmoutcomes line (T-2610 note); plugin/skills/intake/references/planning.md Confidence paragraph. No site page: the Judgment page reads ledger_data, so it shows the corrected numbers unchanged.
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_outcomes.CensoredReads 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|KeyError|TypeError)" | head -10` → ✗ exit 1 · FAILED (failures=3, errors=1) / FAILED (1 classes: test_outcomes.CensoredReads) [ran] [tree e0e653361754] [world 2f1906870a] (2026-11-02T13:16:54Z)
- (ac 2) `python3 plugin/tests/run.py test_outcomes.CensoredReads 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|KeyError|TypeError)" | head -10` → ✗ exit 1 · FAILED (failures=3, errors=1) / FAILED (1 classes: test_outcomes.CensoredReads) [ran] [tree e0e653361754] [world 2f1906870a] (2026-11-02T13:16:54Z)
- (ac 3) `python3 plugin/tests/run.py test_outcomes.CensoredReads 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|KeyError|TypeError)" | head -10` → ✗ exit 1 · FAILED (failures=3, errors=1) / FAILED (1 classes: test_outcomes.CensoredReads) [ran] [tree e0e653361754] [world 2f1906870a] (2026-11-02T13:16:54Z)
- (step 1) `python3 plugin/tests/run.py test_outcomes.CensoredReads` → ✗ exit 1 · Ran 4 tests in 2.0s (1 classes, 16 at a time; slowest: CensoredReads 2s) / FAILED (1 classes: test_outcomes.CensoredReads) [ran] [tree 235e34a3347c] [world 2f1906870a] (2026-11-02T13:17:14Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes test_judgment test_planning test_trials test_cost` → ✗ exit 1 · Ran 182 tests in 15.7s (56 classes, 16 at a time; slowest: Survival 15s, DoorPark 11s, CalibrationLedgerBets 10s) / FAILED (1 classes: test_outcomes.CalibrationLedgerBets) [ran] [tree 1bb9677d8ffc] [world 2f1906870a] (2026-11-02T13:18:24Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes test_judgment test_planning test_trials test_cost` → exit 0 · Ran 182 tests in 15.6s (56 classes, 16 at a time; slowest: Survival 15s, DoorPark 11s, CalibrationLedgerBets 10s) / OK [ran] [tree 24838428d6b0] [world 2f1906870a] (2026-11-02T13:19:13Z)
- (step 3) `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 4fd4a77f5df5] [world 2f1906870a] (2026-11-02T13:20:05Z)
- `python3 plugin/tests/run.py test_outcomes.CensoredReads` → ✗ exit 1 · Ran 6 tests in 3.7s (1 classes, 16 at a time; slowest: CensoredReads 2s) / FAILED (1 classes: test_outcomes.CensoredReads) (start tree + this task's tests) [ran] [tree 57a0e22d7d9e] [world 2f1906870a] (2026-11-02T13:21:49Z)
- `python3 plugin/tests/run.py test_outcomes.CensoredReads` → exit 0 · Ran 6 tests in 2.8s (1 classes, 16 at a time; slowest: CensoredReads 3s) / OK [ran] [tree 57a0e22d7d9e] [world 2f1906870a] (2026-11-02T13:21:49Z)
- (audit intent) `self (subagents held by the budget guard)` → matches the brief: track, buckets, Briers, trails, bar check, routes, the trial grader and base_rate all count a close or a task or choice bet only once its window finished; live read FEATURE M 21 of 43 -> 21 of 22 held, the choice bucket's +84 became 5 open-window misses [tree 0704e9948734] (2026-11-02T13:25:13Z)
- (audit edge) `self` → one finding, fixed: a brier trial due at 30 days would see no settled after-move bets and propose revert; it now stays pending until due + 30 days. Rows with no window on record (seeded, reopened, unknown close) count as before; grade rows are still written at once, so a finished window reads the early grade [tree 0704e9948734] (2026-11-02T13:25:13Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes test_judgment test_planning test_trials test_cost test_metacog` → exit 0 · Ran 186 tests in 16.9s (59 classes, 16 at a time; slowest: Survival 17s, DoorPark 12s, CalibrationLedgerBets 11s) / OK [ran] [tree 2bf1546fc7ac] [world 2f1906870a] (2026-11-02T13:31:37Z)
- (audit intent) `self (subagents held by the budget guard)` → matches the brief: track, buckets, Briers, trails, bar check, routes, the trial grader and base_rate count a close or a task or choice bet only once its window finished; live read FEATURE M 21 of 43 -> 21 of 22 held; the choice bucket's +84 became 5 open-window misses [tree 2bf1546fc7ac] (2026-11-02T13:31:44Z)
- (audit edge) `self` → one finding, fixed: a brier trial due at 30 days saw no settled after-move bets and proposed revert; it now waits until due + 30 days. Two tests encoded the old behavior or a timing race (seeded rows landing either side of the trial's second) and now read past the windows. Rows with no window on record count as before; grade rows are still written at once [tree 2bf1546fc7ac] (2026-11-02T13:31:44Z)
- `python3 plugin/tests/run.py test_outcomes.CensoredReads test_outcomes.CalibrationBars` → ✗ exit 1 · Ran 20 tests in 5.7s (2 classes, 16 at a time; slowest: CalibrationBars 4s, CensoredReads 2s) / FAILED (2 classes: test_outcomes.CalibrationBars, test_outcomes.CensoredReads) (start tree + this task's tests) [ran] [tree 2bf1546fc7ac] [world 2f1906870a] (2026-11-02T13:37:06Z)
- `python3 plugin/tests/run.py test_outcomes.CensoredReads test_outcomes.CalibrationBars` → exit 0 · Ran 20 tests in 4.5s (2 classes, 16 at a time; slowest: CalibrationBars 4s, CensoredReads 2s) / OK [ran] [tree 2bf1546fc7ac] [world 2f1906870a] (2026-11-02T13:37:06Z)
- (ac 1) `python3 plugin/tests/run.py test_outcomes.CensoredReads` → exit 0 · Ran 6 tests in 2.8s (1 classes, 16 at a time; slowest: CensoredReads 3s) / OK [ran] [tree 2bf1546fc7ac] [world 2f1906870a] (2026-11-02T13:37:32Z)
- (ac 2) `python3 plugin/tests/run.py test_outcomes.CensoredReads` → exit 0 · Ran 6 tests in 2.8s (1 classes, 16 at a time; slowest: CensoredReads 3s) / OK [ran] [tree 2bf1546fc7ac] [world 2f1906870a] (2026-11-02T13:37:32Z)
- (ac 3) `python3 plugin/tests/run.py test_outcomes.CensoredReads` → exit 0 · Ran 6 tests in 2.8s (1 classes, 16 at a time; slowest: CensoredReads 3s) / OK [ran] [tree 2bf1546fc7ac] [world 2f1906870a] (2026-11-02T13:37:32Z)
- (ac 4) `python3 plugin/tests/run.py test_outcomes test_judgment test_planning` → exit 0 · Ran 149 tests in 14.7s (47 classes, 16 at a time; slowest: Survival 14s, DoorPark 10s, ModelRouter 10s) / OK [ran] [tree 2bf1546fc7ac] [world 2f1906870a] (2026-11-02T13:37:32Z)
- (audit intent) `self-review over the diff (subagents held by the budget guard); one edge finding fixed inline (brier trial waits for windows)` → every read of the record counts a close or a task or choice bet once its window finished; live: FEATURE M 21 of 43 -> 21 of 22 held, choice +84 -> 5 named open-window misses [tree 2bf1546fc7ac] (2026-11-02T13:37:32Z)
- (audit edge) `self-review over the diff (subagents held by the budget guard); one edge finding fixed inline (brier trial waits for windows)` → a brier trial due at 30 days now waits until due + 30 days instead of proposing revert on no scored bets; rows with no window on record count as before; grade rows still written at once [tree 2bf1546fc7ac] (2026-11-02T13:37:32Z)
## Log
- 2026-11-02T13:14:27Z created
- 2026-11-02T13:16:29Z planned from capture
- 2026-11-02T13:16:32Z set approved=True
- 2026-11-02T13:16:33Z focused
- 2026-11-02T13:16:33Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-02T13:20:05Z scope: interim read gains early losses (same censoring, mirror direction); _survival's lost rows carry days_left for it
- 2026-11-02T13:23:27Z scope: fmtrials.grade keeps a brier trial pending while the bets since the move are inside their windows (capped at due + 30 days); without it the read change would propose a revert for 'no scored bets'
- 2026-11-02T13:31:14Z scope: test_metacog.Calibrate's digest expectation encoded the old early count (1 of 20 scored); now 0 scored, 2 pending, plus the open-windows line
- 2026-11-02T13:39:07Z done
- 2026-11-02T13:39:10Z committed 221357ee (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- T-2498 [FEATURE M, done, 3 steps] Interim calibration reads and reliability bins: fm outcomes --judgment adds a 7-day… — lesson: When a score needs a month to settle, sh…
- T-2499 [FEATURE M, done, 2 steps] Bets settle with no session: the night tick runs fmoutcomes.maintain; the digest names the kind whose Brier trails its base rate most —…
- decision 2026-10-30: T-2138 clauses gate staleness: a one-day window, not the current turn's start
- similar finished tasks took 2–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_board_surfaces.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_cost.py, plugin/test…
## Why not caught
T-2584 fixed the survival line's censoring but no test asserted the same rule for track, the ledger or base_rate: each read had its own test fixture with closes whose windows were never open, so the bias never showed in a test
## Lessons
- When one read of a time-windowed signal is fixed for censoring, grep every other read of the same signal in the same change: T-2584 fixed one line of five, and the four left still steered focus and the bar check
## Plan gaps
- failed first: step 1 red: test_outcomes.CensoredReads for the track record, the ledger and base_rate
- failed first: step 2 fix: scored() marks open-window task and choice bets pending with early; track and base_rate gate o…
## Files touched
- plugin/tests/test_outcomes.py
- plugin/lib/fmoutcomes.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/intake/references/planning.md
- plugin/lib/fmtrials.py
- plugin/tests/test_metacog.py
