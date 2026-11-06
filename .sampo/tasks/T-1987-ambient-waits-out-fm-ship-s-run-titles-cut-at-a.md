---
id: T-1987
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T13:23:09Z
updated: 2026-10-29T13:33:17Z
batch: [T-1984, T-1985, T-1986]
base: 2abd17ceb4298f7d846a48a479563f817aaa8e66
base_tree: 6ad45df6e5d8c1f4ce272ddbb969a9b1c7fb8363
plan0_at: 2026-10-29T13:23:20Z
plan0_scope: []
verified: strong
---
# Ambient waits out fm ship's run, titles cut at a word, budget-limited loop rounds aren't dry
## Raw request
> T-1984: FIX: an edit while fm ship's test run is live starts an ambient run beside it (fmambient.after_edit checks only gates_running), two suites at once; skip it then, and have fm ship start one afterward when the tree changed during its run (as T-1973 does for fm check)
> DONE-WHEN: an edit during a live ship_testing marker starts no ambient run :: python3 plugin/tests/run.py test_ambient
> T-1985: FIX: a captured task title is cut mid-word at 90 characters ("…DONE-WHEN fallbac") and its first word is capitalized even when it is a command or identifier ("Fm batch", "C.first_touch"); cut at a word boundary with an ellipsis and leave an identifier-like first word as typed
> DONE-WHEN: a long capture's title ends at a word boundary with … and "fm batch …" stays lowercase :: python3 plugin/tests/run.py test_cli
> T-1986: FIX: a forever-loop round run while optional work is dropped (risk or usage budget) counts toward the dry streak although it had no ideas fan-out, so a spent budget can end the loop as "2 dry rounds"; a budget-limited round leaves the dry streak as it was and says so
> DONE-WHEN: fm loop yield 1 with the budget degraded keeps the dry count :: python3 plugin/tests/run.py test_loop
## Interpretation
Do T-1984, T-1985, T-1986 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1987. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1984: an edit during a live ship_testing marker starts no ambient run — verify with `python3 plugin/tests/run.py test_ambient`
- [x] T-1985: a long capture's title ends at a word boundary with … and "fm batch …" stays lowercase — verify with `python3 plugin/tests/run.py test_cli`
- [x] T-1986: fm loop yield 1 with the budget degraded keeps the dry count — verify with `python3 plugin/tests/run.py test_loop`
## Non-goals
## Approach (options → choice → why)
T-1984: options (a) ambient waits for ship (blocks the hook) (b) skip ambient while ship_testing is live and have fm ship start one after if the tree changed (c) queue a dirty flag. Choice (b): mirrors T-1965/T-1973, no blocking hook. T-1985: options (a) textwrap.shorten (b) rsplit at the last space before 90 + … (c) no cut. Choice (b): stdlib-simple, keeps the head. First word: leave as typed when it holds . _ / ( or no vowel (fm, ls, npm). T-1986: options (a) skip yield under degrade (b) keep the dry count when degraded and n < DRY_YIELD (c) halve DRY_YIELD. Choice (b): yield still recorded, streak untouched.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1984: An edit while fm ship's test run is live starts an ambient run beside it (fmambient.after_
2. [x] T-1985: A captured task title is cut mid-word at 90 characters ("…DONE-WHEN fallbac") and its firs
3. [x] T-1986: A forever-loop round run while optional work is dropped (risk or usage budget) counts towa
## Resume here
## Docs impact
CHANGELOG Unreleased line (T-1987); MASTER fmambient line (ship_testing, T-1984) and forever-loop line (budget-limited yield, T-1986).
## Verification evidence
- `python3 plugin/tests/run.py test_ambient test_cli test_loop` → ✗ exit 1 · Ran 159 tests in 26.9s (42 classes, 16 at a time; slowest: TaskLifecycle 26s, Ambient 20s, CaptureAndIntake 12s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 7e42d7582ed4] (2026-10-29T13:25:01Z)
- `python3 plugin/tests/run.py test_ambient test_cli test_loop` → ✗ exit 1 · Ran 159 tests in 24.2s (42 classes, 16 at a time; slowest: TaskLifecycle 24s, Ambient 18s, CaptureAndIntake 10s) / FAILED (3 classes) [ran] [tree 7e42d7582ed4] (2026-10-29T13:25:01Z)
- `python3 plugin/tests/run.py test_ambient test_cli test_loop` → ✗ exit 1 · Ran 159 tests in 32.0s (42 classes, 16 at a time; slowest: TaskLifecycle 30s, Ambient 22s, CaptureAndIntake 14s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 668bdb3f4432] (2026-10-29T13:26:34Z)
- `python3 plugin/tests/run.py test_ambient test_cli test_loop` → exit 0 · Ran 159 tests in 27.8s (42 classes, 16 at a time; slowest: TaskLifecycle 27s, Ambient 21s, CaptureAndIntake 13s) / OK [ran] [tree 668bdb3f4432] (2026-10-29T13:26:34Z)
- (step 1) `python3 plugin/tests/run.py test_ambient` → exit 0 · Ran 10 tests in 15.5s (1 classes, 16 at a time; slowest: Ambient 15s) / OK [ran] [tree 668bdb3f4432] (2026-10-29T13:27:01Z)
- (step 2) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 134 tests in 23.4s (38 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 9s, StateViews 9s) / OK [ran] [tree 668bdb3f4432] (2026-10-29T13:27:25Z)
- (step 3) `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 15 tests in 4.3s (3 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, PipeProgramDebris 0s) / OK [ran] [tree 668bdb3f4432] (2026-10-29T13:27:29Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmambient.py, plugin/lib/fmcli.py, plugin/lib/fmloop.py — commit it through a task, or git checkout it back / fm doct; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.0    41.4     150  [0] / SessionEnd                  35.5    37.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 2c2f2e0c5dc2] (2026-10-29T13:31:54Z)
- (ac 1) `python3 plugin/tests/run.py test_ambient` → exit 0 · Ran 10 tests in 15.6s (1 classes, 16 at a time; slowest: Ambient 15s) / OK [ran] [tree 2c2f2e0c5dc2] (2026-10-29T13:32:48Z)
- (ac 2) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 134 tests in 23.6s (38 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 9s, StateViews 8s) / OK [ran] [tree 2c2f2e0c5dc2] (2026-10-29T13:32:48Z)
- (ac 3) `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 15 tests in 4.3s (3 classes, 16 at a time; slowest: Loop 4s, LoopReview 3s, PipeProgramDebris 0s) / OK [ran] [tree 2c2f2e0c5dc2] (2026-10-29T13:32:48Z)
- (audit intent) `self-review (optional work dropped): ship_testing checked with any root so the ship's inner check's T-1973 trigger is skipped too; empty or space-free titles fall back cleanly; a degrade() error counts the round normally` → each of the three fixes has a red-then-green test; full suite 4198 OK [tree 2c2f2e0c5dc2] (2026-10-29T13:32:48Z)
- (audit edge) `self-review (optional work dropped): ship_testing checked with any root so the ship's inner check's T-1973 trigger is skipped too; empty or space-free titles fall back cleanly; a degrade() error counts the round normally` → a 90+ char title with no space is hard-cut at 89 plus …; a first word with . _ / ( or no vowel keeps its case [tree 2c2f2e0c5dc2] (2026-10-29T13:32:48Z)
- (audit adversary) `self-review (optional work dropped): ship_testing checked with any root so the ship's inner check's T-1973 trigger is skipped too; empty or space-free titles fall back cleanly; a degrade() error counts the round normally` → a stale ship_testing marker only skips ambient while its pid lives; a fruitful round (n >= 3) still resets the dry streak under a degraded budget [tree 2c2f2e0c5dc2] (2026-10-29T13:32:48Z)
## Log
- 2026-10-29T13:23:09Z created
- 2026-10-29T13:23:19Z focused
- 2026-10-29T13:33:15Z done
- 2026-10-29T13:33:17Z committed b4df3e9f (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1967 [FEATURE M, done, 3 steps] round 12: fm check waits for an ambient run, ambient skips during gates, loop round respects pace — lesson: A slowdown reason from fmbu…
- T-1974 [FIX M, done, 3 steps] round 13: one full check per tree, fm risk shows what spent it, ambient after mid-gate edits — lesson: A shared marker written by one proce…
- T-1980 [FIX M, done, 4 steps] Batch keeps DONE-WHEN verify, gates name why-not-caught, fm ship marks its test run, first_touch keeps project files — lesson: A marker tha…
- decision 2026-10-29: Round 6 runs lean: review ideas only, no fm ideas fan-out
- similar finished tasks took 3–4 steps
## Why not caught
none: no test drove an edit during a ship run, a 90+ char capture or a yield under a degraded budget
## Lessons
- A loop's stop rule should count only rounds that ran at full strength; a throttled round is no evidence the ideas ran out
## Files touched
- plugin/tests/test_ambient.py
- plugin/tests/test_loop.py
- plugin/tests/test_cli.py
- plugin/lib/fmambient.py
- plugin/lib/fmcli.py
- plugin/lib/fmloop.py
- CHANGELOG.md
- MASTER.md
