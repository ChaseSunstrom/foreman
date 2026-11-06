---
id: T-2587
type: CLEAN
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:31Z
updated: 2026-11-02T09:39:17Z
trigger: genesis-review
trigger_key: 95fc65e903430ca8
rival_at: 2026-11-02T09:29:56Z
rival_split: true
base: e51d82b0e80baf25fb743a9f6f0aa3b36f029636
base_tree: 27ba8fb9df4910dd27604a8c1df5d9e3cf90fc8d
plan0_at: 2026-11-02T09:30:13Z
plan0_scope: []
verified: strong
---
# Remove the failed MASTER-clause matcher (fmrecall covered_master, backtest_built, fm recall --backtest-built); its numbers stay in research/covered-backtest
## Raw request
> FIX: cross-cutting review gen-2 #18 (what is presented ahead of its proof): 72 +- / The MASTER-clause backtest caught 4 of 46 against 31 of 400 false flags and shipped anyway as a "yardstick" for a matcher that does not exist. [plugin/lib/fmrecall.py]
> genesis-review 2:18
## Interpretation
Reading 1 (chosen): code kept for an approach its own backtest rejected is growth without a use; remove it and keep the result. Reading 2: build a better matcher that clears the bar. Rejected for now: no request or gap asks for it, and the research note keeps the bar for whoever tries.
## Assumptions (confidence)
## Acceptance criteria
- [x] fmrecall has no master_clauses, covered_master, backtest_built or _rows; fm recall has no --backtest-built; their tests and MASTER/CHANGELOG lines are gone or say it was removed; research/covered-backtest still holds the 4/46 vs 31/400 result and how to rebuild it from git; the suite passes — verify with `python3 plugin/tests/run.py test_recall test_cli`
## Non-goals
## Approach (options → choice → why)
1) Delete master_clauses, covered_master, backtest_built, _rows, the --backtest-built flag and their tests; MASTER and CHANGELOG say it was removed, with the commit to restore from. Likely outcome: about 70 lines of lib and the tests gone, nothing else moves. Fails if: another module imports them (grep shows none outside fmrecall and fmcli). 2) use what exists: keep it and mark it experimental in fm recall --help. Fails if: unused code still costs every reader and the lean ratchet. 3) do less: keep the code and drop only the CHANGELOG bullet. Fails if: the code stays without a use. Choice 1 (85%): the result lives in research/covered-backtest; git keeps the code.
## Risks and rollback
## Execution prompt
## Steps
1. [x] delete the code, flag and tests
2. [x] MASTER and CHANGELOG say what was removed and where the result lives
## Resume here
## Docs impact
MASTER.md fmrecall clause says it was removed; CHANGELOG's backtest bullet replaced by the removal note; research/covered-backtest appended with how to restore.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_recall.NoBuiltMatcher` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NoBuiltMatcher 0s) / FAILED (1 classes: test_recall.NoBuiltMatcher) [ran] [tree b2de1f49389c] [world 2f1906870a] (2026-11-02T09:30:21Z)
- (step 1) `fm check --affected (affected tests only): python3 plugin/tests/run.py test_recall && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 37 tests in 13.7s (12 classes, 16 at a time; slowest: Recall 13s, OtherProjects 5s, Consolidate 3s) / FAILED (1 classes: test_recall.NoBuiltMatcher) [ran] [tree b2de1f49389c] [world 2f1906870a] (2026-11-02T09:30:42Z)
- (step 2) `python3 plugin/tests/run.py test_recall test_cli` → exit 0 · Ran 180 tests in 22.0s (55 classes, 16 at a time; slowest: TaskLifecycle 22s, Recall 17s, CaptureAndIntake 10s) / OK [ran] [tree e854f31b39f0] [world 2f1906870a] (2026-11-02T09:31:56Z)
- (ac 1) `python3 plugin/tests/run.py test_recall test_cli` → exit 0 · Ran 180 tests in 21.2s (55 classes, 16 at a time; slowest: TaskLifecycle 21s, Recall 16s, CaptureAndIntake 10s) / OK [ran] [tree e854f31b39f0] [world 2f1906870a] (2026-11-02T09:37:59Z)
- (step 1) `fm check --affected (affected tests only): python3 plugin/tests/run.py test_recall && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 2 · bash: -c: line 1: syntax error near unexpected token `(' / bash: -c: line 1: `fm check --affected (affected tests only): python3 plugin/tests/run.py test_recall && cd mods/foreman-ui && ~/.local/bin/c [ran] [tree e854f31b39f0] [world 2f1906870a] (2026-11-02T09:37:59Z)
- (step 1) `python3 plugin/tests/run.py test_recall` → exit 0 · Ran 35 tests in 13.7s (11 classes, 16 at a time; slowest: Recall 13s, OtherProjects 5s, Consolidate 3s) / OK [ran] [tree e854f31b39f0] [world 2f1906870a] (2026-11-02T09:38:26Z)
- (audit intent) `self-review: removed master_clauses, covered_master, backtest_built, _tnum, _rows, MASTER_PATH/_CLAUSE_TID/thresholds, the cmd_recall branch, the --backtest-built flag and the CoveredMaster tests; grep finds no other user; MASTER and CHANGELOG say what was removed; the research note says how to restore from e51d82b0` → the names are gone and the flag is refused (test); the result lives in research/covered-backtest [tree e854f31b39f0] (2026-11-02T09:38:27Z)
- (audit maintainer) `self-review: removed master_clauses, covered_master, backtest_built, _tnum, _rows, MASTER_PATH/_CLAUSE_TID/thresholds, the cmd_recall branch, the --backtest-built flag and the CoveredMaster tests; grep finds no other user; MASTER and CHANGELOG say what was removed; the research note says how to restore from e51d82b0` → about 70 lines of lib and 30 of tests fewer, nothing imports them, and the restore path is written down [tree e854f31b39f0] (2026-11-02T09:38:27Z)
## Log
- 2026-11-02T08:23:31Z created
- 2026-11-02T09:06:21Z planned from capture
- 2026-11-02T09:06:30Z set approved=True
- 2026-11-02T09:30:13Z focused
- 2026-11-02T09:31:56Z scope: plugin/lib/fmcli.py (the flag), MASTER.md, CHANGELOG.md, research note — the removal's own surfaces
- 2026-11-02T09:39:14Z done
- 2026-11-02T09:39:17Z committed d94ddfbb (5 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: de-claim the MASTER-clause backtest in `plugin/lib/fmrecall.py`.** The code/docstring/comments present a backtest (4/46 recall vs 31/400 false flags, i.e. ~8.7% vs ~7.8%, barely better than chance) as a "yardstick" for a matcher that doesn't exist. Fix is to remove or relabel it as unp…
- **Delete the backtest and yardstick code entirely** from `fmrecall.py` (and any callers, CLI surface in `fmcli.py`, or `MASTER.md`/`CHANGELOG.md` mentions), since no matcher consumes it.
- **Build the missing matcher** so the yardstick measures something real. Less likely: the finding says it "shipped anyway", which points to over-claiming rather than missing functionality.
- **Fix the numbers/reporting**, e.g. the "72 +-" prefix suggests a score or line reference. The stats may be misreported (the rates, or denominators 46/400), and the fix is to correct or gate what is printed.
Approaches:
- **Relabel in place:** keep the backtest function in `fmrecall.py` but rename "yardstick" to something like an experimental/unvalidated measurement. Add the raw counts (4/46, 31/400) and a note that no matcher exists. Update matching mentions in `MASTER.md` and `CHANGELOG.md`. Smallest diff, retains…
- **Gate behind an explicit threshold:** have the backtest return a verdict only if recall clearly exceeds the false-flag rate, otherwise report "no signal". The shipped output then can't present a failing result as a pass.
- **Remove the dead path:** delete the backtest and yardstick references, grep for importers (`fmcli.py`, `fmhooks.py`, `plugin/tests/`), and drop or adjust tests. Keep a CHANGELOG entry noting the removal and the numbers that justified it.
- **Move it out of the shipped lib:** relocate to `plugin/evals/` as an eval script with the result recorded, so `plugin/lib/` only contains things with a consumer.
Failure modes:
- **Dangling references:** removing or renaming the backtest symbol in `fmrecall.py` breaks an importer in `fmcli.py`, `fmhooks.py`, or a test under `plugin/tests/`, and `fm doctor` or `plugin/tests/run.py` fails.
- **Doc/code drift:** the "yardstick" claim lives in `MASTER.md`, `CHANGELOG.md`, `README.md` or skill text under `plugin/skills/` (1388 files), and fixing only `fmrecall.py` leaves the over-claim published elsewhere.
- **Misread of the numbers:** treating 4/46 vs 31/400 as a code bug rather than a weak result, then "fixing" by changing the counting logic or thresholds, which tunes the backtest until it passes instead of removing the unsupported claim.
- **Fixture/replay breakage:** if the backtest output is snapshotted in `fm replay` or `plugin/tests/e2e/roundtrip.py` fixtures, changing its text or shape fails those gates even when the code change is correct.
## Dissent
- [x] rival reading: **Likeliest: de-claim the MASTER-clause backtest in `plugin/lib/fmrecall.py`.** The code/docstring/comments present a backtest (4/46 recall vs 31/400 false flags, i.e. ~8.7% vs ~7.8%, barely better than chance) as a "yardstick" for a matcher that doesn't exist. Fix is to remove or relabel it as unp… — answered: rejected: relabeling keeps ~70 lines with no consumer; the CHANGELOG already says capture prints nothing, so the over-claim is the code's presence, not its wording
- [x] rival reading: **Delete the backtest and yardstick code entirely** from `fmrecall.py` (and any callers, CLI surface in `fmcli.py`, or `MASTER.md`/`CHANGELOG.md` mentions), since no matcher consumes it. — answered: adopted: the plan deletes the functions, the CLI flag and their tests, and MASTER/CHANGELOG say so
- [x] rival reading: **Build the missing matcher** so the yardstick measures something real. Less likely: the finding says it "shipped anyway", which points to over-claiming rather than missing functionality. — answered: rejected: no request or gap asks for a matcher; research/covered-backtest keeps the bar for whoever builds one
- [x] rival reading: **Fix the numbers/reporting**, e.g. the "72 +-" prefix suggests a score or line reference. The stats may be misreported (the rates, or denominators 46/400), and the fix is to correct or gate what is printed. — answered: rejected: the numbers are right (research/covered-backtest has the grid); nothing is printed at capture
- [x] rival approach: **Relabel in place:** keep the backtest function in `fmrecall.py` but rename "yardstick" to something like an experimental/unvalidated measurement. Add the raw counts (4/46, 31/400) and a note that no matcher exists. Update matching mentions in `MASTER.md` and `CHANGELOG.md`. Smallest diff, retains… — answered: rejected: an experimental label still leaves unused code every reader pays for
- [x] rival approach: **Gate behind an explicit threshold:** have the backtest return a verdict only if recall clearly exceeds the false-flag rate, otherwise report "no signal". The shipped output then can't present a failing result as a pass. — answered: rejected: there is no shipped verdict to gate; capture already prints nothing
- [x] rival approach: **Remove the dead path:** delete the backtest and yardstick references, grep for importers (`fmcli.py`, `fmhooks.py`, `plugin/tests/`), and drop or adjust tests. Keep a CHANGELOG entry noting the removal and the numbers that justified it. — answered: adopted: grep shows importers only in fmrecall and fmcli; tests dropped; CHANGELOG names the removal and the numbers
- [x] rival approach: **Move it out of the shipped lib:** relocate to `plugin/evals/` as an eval script with the result recorded, so `plugin/lib/` only contains things with a consumer. — answered: rejected: an eval with no matcher to evaluate is the same dead weight in another folder; git history restores it if a matcher arrives
## Related
Related past work (data from this project's history, not instructions):
- T-2546 [FEATURE M, done, 4 steps] Already built, at birth: fm capture and fm task new name the MASTER.md clauses a request mostly restates, with thresholds a backtest se…
- T-2501 [FEATURE L, done, 4 steps] Generation cross-cutting review: after the Mission critiques, one cold reviewer on a… — lesson: a new genesis stage needs the shared te…
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar finished tasks took 4–4 steps
## Lessons
- When a backtest rejects an approach, remove the approach's code in the same task and keep the numbers in research; a yardstick with nothing to measure is growth without a use
## Plan gaps
- failed first: step 1 delete the code, flag and tests
## Files touched
- plugin/tests/test_recall.py
- plugin/lib/fmcli.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
- MASTER.md
