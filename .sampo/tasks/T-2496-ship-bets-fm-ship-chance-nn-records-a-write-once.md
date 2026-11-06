---
id: T-2496
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T19:05:34Z
updated: 2026-11-01T21:51:00Z
base: 9d7437a15bd664aaf3296127c44a3226ea2da7c2
base_tree: e4cf8f36609e080265739af5aaa4af82a49297f9
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T21:30:22Z
plan0_scope: []
verified: strong
---
# Ship bets: fm ship --chance NN records a write-once "ship" bet keyed by the pushed…
## Raw request
> FEATURE: ship bets: fm ship --chance NN records a write-once "ship" bet keyed by the pushed commit, the stated chance its blocking CI jobs pass; fm ci-watch settles it held or missed from the run, so a bet is scored in hours instead of SURVIVE_DAYS (30); fm next asks for the number before a ship
> DONE-WHEN: a ship bet is written once per commit and settled by ci-watch's blocking verdict, shown in fm outcomes --judgment as its own kind
## Interpretation
Readings: (a) likeliest: fm ship --chance NN books a write-once ship bet on the pushed commit and fm ci-watch's verdict on that commit settles it, scored as its own kind, never moving a bar (only survival does); (b) the bet is automatic from the plan's Choice percent with no flag: rejected, the plan's percent is about the approach holding, not CI passing on other hosts. Fails if: ci-watch never runs for a ship (then the bet stays pending, which costs nothing).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ship --chance 90 books one ship bet keyed by the pushed commit; a second ship of the same commit writes none; ci-watch's green or red on that commit settles it held or missed (src ci) and bar_rows ignores it — verify with `python3 plugin/tests/run.py test_judgment test_ci_watch test_release`
## Non-goals
## Approach (options → choice → why)
1) ship writes the bet after the push; watch() logs a ci_verdict ledger event (commit, green) when the commit's run completes, and _verdicts settles kind ship from it (src ci), then maintain() writes the grade. Fails if: a rerun flips a red to green after the grade is written (grades are write-once; the first verdict stands, which is what was bet on). 2) watch() writes the grade row itself. Fails if: it duplicates settle()'s write-once rule in a second place. 3) use what exists: a decision bet (fm decide --confidence) per ship. Fails if: a decision settles only by reversal or 30 days, not by CI, so it scores nothing in hours. 4) do less: log the CI verdict with no bet. Fails if: nothing is stated, so nothing is scored. Reused in 1: fmoutcomes.bet (write-once per task, kind, key), _verdicts/settle/scored, bar_rows (survival only), fmci.watch's completed-run branch, c.log_event. Choice 1 (85%): one write-once path, one reader, and the signal is GitHub's run, not a Foreman verdict.
## Risks and rollback
A ship without --chance writes no bet (the flag is optional: no friction for other projects). A cancelled or never-run job logs no verdict. Rollback: revert the commit; ship rows already in calibration.jsonl stay as data, read as an unknown kind by older code.
## Execution prompt
## Steps
1. [x] red tests: a ship bet written once per commit, settled by a ci_verdict event, ignored by bar_rows
2. [x] fm ship --chance writes the bet; fmci.watch logs ci_verdict; _verdicts settles kind ship; fm next's ship hint names --chance
3. [x] docs: README, MASTER, CHANGELOG
## Resume here
## Docs impact
plugin/skills/playbooks/references/release/ship-to-main.md, README.md, MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment test_ci_watch test_ship test_outcomes` → exit 0 · Ran 155 tests in 40.1s (32 classes, 16 at a time; slowest: Ship 40s, Survival 25s, ModelRouter 16s) / OK [ran] [tree 42905c5004de] (2026-11-01T21:35:14Z)
- (step 2) `python3 plugin/tests/run.py test_judgment test_ci_watch test_ship test_outcomes` → exit 0 · Ran 155 tests in 39.5s (32 classes, 16 at a time; slowest: Ship 39s, Survival 25s, ModelRouter 17s) / OK [ran] [tree 42905c5004de] (2026-11-01T21:35:54Z)
- (step 3) `python3 plugin/tests/run.py test_judgment test_ci_watch test_ship test_outcomes` → exit 0 · Ran 155 tests in 42.7s (32 classes, 16 at a time; slowest: Ship 42s, Survival 26s, ModelRouter 17s) / OK [ran] [tree 42905c5004de] (2026-11-01T21:36:38Z)
- `python3 plugin/tests/run.py test_judgment.ShipBets test_ci_watch.CiWatch.test_a_finished_run_logs_its_blocking_verdict_for_the_ship_bet test_ship.Ship.test_chance_books_one_ship_bet_on_the_pushed_commit` → ✗ exit 1 · Ran 3 tests in 3.2s (3 classes, 16 at a time; slowest: Ship 1s, ShipBets 0s, CiWatch 0s) / FAILED (3 classes: test_ci_watch.CiWatch, test_judgment.ShipBets, test_ship.Ship) (start tree + this task's tests) [ran] [tree 42905c5004de] (2026-11-01T21:36:44Z)
- `python3 plugin/tests/run.py test_judgment.ShipBets test_ci_watch.CiWatch.test_a_finished_run_logs_its_blocking_verdict_for_the_ship_bet test_ship.Ship.test_chance_books_one_ship_bet_on_the_pushed_commit` → exit 0 · Ran 3 tests in 1.8s (3 classes, 16 at a time; slowest: Ship 1s, ShipBets 0s, CiWatch 0s) / OK [ran] [tree 42905c5004de] (2026-11-01T21:36:44Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment test_ci_watch test_release` → exit 0 · Ran 115 tests in 18.5s (26 classes, 16 at a time; slowest: Release 18s, DoorPark 16s, DoorGate 8s) / OK [ran] [tree 42905c5004de] (2026-11-01T21:47:15Z)
- (audit intent) `self-review: the bet is validated before any push and booked after; one write-once row per commit; ci-watch logs the blocking verdict for success and failure only (cancelled and runner-less runs log nothing); the first verdict on a commit settles it; bar_rows still takes survival only` → Mission 2 brief 1: a stated number scored within hours by GitHub's run instead of after 30 days [tree 42905c5004de] (2026-11-01T21:47:15Z)
- (audit edge) `self-review: the bet is validated before any push and booked after; one write-once row per commit; ci-watch logs the blocking verdict for success and failure only (cancelled and runner-less runs log nothing); the first verdict on a commit settles it; bar_rows still takes survival only` → --chance 150 refuses before pushing and keeps the grant; a second ship of the same commit books nothing; a rerun's later verdict doesn't overwrite the first; no ci-watch means a pending bet, which costs nothing [tree 42905c5004de] (2026-11-01T21:47:15Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 42905c5004de] (2026-11-01T21:51:00Z)
## Log
- 2026-11-01T19:05:34Z created
- 2026-11-01T19:08:05Z criterion 1 verify: `python3 plugin/tests/run.py test_outcomes test_ci_watch test_release` → `python3 plugin/tests/run.py test_judgment test_ci_watch test_release`
- 2026-11-01T19:08:11Z planned: it has criteria and steps
- 2026-11-01T19:14:18Z set approved=True
- 2026-11-01T21:30:21Z focused
- 2026-11-01T21:30:22Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T21:36:54Z scope: fmoutcomes ship_bet + _verdicts ship kind, fmci _ci_verdict + watch hooks, fmcli ship --chance, fmrelease ship validation and booking, tests (judgment, ci_watch, ship), ship-to-main playbook, README, MASTER, CHANGELOG
- 2026-11-01T21:50:24Z done
- 2026-11-01T21:50:27Z committed ee25fa27 (11 files)
- 2026-11-01T21:51:00Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- research T-2335-review: Changes needed, but only for the MEDIUM items. I read the code and could not run it; no shell was available. The 9 PlanContent tests are green in…
- T-2461 [CLEAN L, done, 5 steps] Lean: fold six verbs into the verbs that already hold their job (proof → prove --rollup, triggers → outcomes --triggers, calibration → ou…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Lessons
- the fastest honest score for a stated confidence is an outside system's verdict on the same artifact (CI on the pushed commit), not a survival window
## Files touched
- plugin/tests/test_ci_watch.py
- plugin/tests/test_judgment.py
- plugin/tests/test_ship.py
- plugin/lib/fmci.py
- plugin/lib/fmcli.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/skills/playbooks/references/release/ship-to-main.md
