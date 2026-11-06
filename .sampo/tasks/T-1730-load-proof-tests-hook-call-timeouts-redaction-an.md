---
id: T-1730
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/tests/run.py, plugin/tests/helpers.py, plugin/tests/test_hooks.py, plugin/tests/test_code.py, plugin/tests/test_loop.py, plugin/tests/test_site_hero.py, plugin/tests/test_showpieces.py, plugin/lib/city.html, plugin/lib/graph.html, site/**, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T03:35:15Z
updated: 2026-10-23T05:02:59Z
batch: [T-1719, T-1721, T-1728]
base: f4f4ded3f28dfc3ae1a9a44c8ec2500dcafb9819
base_tree: 7c22c488dc47b37933ef8487be8165a3b3efca73
plan0_at: 2026-10-23T04:01:24Z
plan0_scope: [plugin/tests/run.py, plugin/tests/helpers.py, plugin/tests/test_hooks.py, plugin/tests/test_code.py, plugin/tests/test_loop.py, plugin/tests/test_site_hero.py, plugin/tests/test_showpieces.py, plugin/lib/city.html, plugin/lib/graph.html, site/**, CHANGELOG.md]
verified: strong
---
# Load-proof tests: hook-call timeouts, redaction and loop-review races, and frame-count windows that fail only with buil…
## Raw request
> T-1719: test_hooks.NoTaskGate hook calls time out at their 10 s limit under the 16-way parallel run (flaky under load)
> T-1721: Flaky under load: test_code.Review.test_tool_results_and_the_journal_are_redacted and test_loop.LoopReview.test_round_brief_quotes_seen_paths_and_survives_a_missing_git fail with six builders running and pass after (fm check flagged a race)
> T-1728: Flaky under load: test_site_hero.Scene frame counts (133 != 198) and test_showpieces.CityBrowser first-key frame window (33 != 36) fail with builders running and pass alone
## Interpretation
Do T-1719, T-1721, T-1728 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1730. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1719: test_hooks.NoTaskGate passes with the machine under load (run.py --load 24 runs the named tests beside 24 busy processes) — verify with `python3 plugin/tests/run.py --load 24 test_hooks.NoTaskGate`
- [x] T-1721: test_code.Review and test_loop.LoopReview pass under the same load — verify with `python3 plugin/tests/run.py --load 24 test_code.Review test_loop.LoopReview`
- [x] T-1728: test_site_hero.Scene and test_showpieces.CityBrowser and GraphBrowser frame-count checks pass under the same load (windows judged by frames per animation time, not wall time) — verify with `python3 plugin/tests/run.py --load 24 test_site_hero.Scene test_showpieces.CityBrowser test_showpieces.GraphBrowser`
## Non-goals
## Approach (options → choice → why)
First add --load N to plugin/tests/run.py: N busy-loop child processes for the run's duration, killed after (a deterministic way to reproduce load flakes). Then fix each flake at its cause, not by raising timeouts blindly: hook calls in tests get a timeout scaled by the measured load or judged by CPU time as the bench already does (T-0805); races get an explicit wait on the condition (a file, an event) instead of a sleep; browser frame counts are judged against the animation clock the page reports (frames per second of animation time) rather than wall-clock windows. Options considered: skip under load (rejected: hides real failures), retry once (rejected: masks races), scale by load (chosen where a time limit is the point), wait on a condition (chosen for races).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1719: Test_hooks.NoTaskGate hook calls time out at their 10 s limit under the 16-way parallel ru
2. [x] T-1721: Flaky under load: test_code.Review.test_tool_results_and_the_journal_are_redacted and test
3. [x] T-1728: Flaky under load: test_site_hero.Scene frame counts (133 != 198) and test_showpieces.CityB
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py --load 24 test_hooks.NoTaskGate test_run.Load` → exit 0 · Ran 34 tests in 68.3s (2 classes, 16 at a time; slowest: NoTaskGate 68s, Load 1s) / OK [ran] [tree e87bfaa147cf] (2026-10-23T04:14:10Z)
- (step 2) `python3 plugin/tests/run.py --load 24 test_code.Review test_loop.LoopReview` → exit 0 · Ran 14 tests in 21.3s (2 classes, 16 at a time; slowest: Review 21s, LoopReview 11s) / OK [ran] [tree d5bd5a5630c4] (2026-10-23T04:14:39Z)
- (step 3) `python3 plugin/tests/run.py --load 24 test_site_hero.Scene test_showpieces.CityBrowser test_showpieces.GraphBrowser test_run` → exit 0 · Ran 58 tests in 27.9s (28 classes, 16 at a time; slowest: Scene 28s, GraphBrowser 14s, CityBrowser 14s) / OK [ran] [tree 3d6a9f030700] (2026-10-23T04:19:59Z)
- (ac 1) `python3 plugin/tests/run.py --load 24 test_hooks.NoTaskGate` → exit 0 · Ran 30 tests in 63.7s (1 classes, 16 at a time; slowest: NoTaskGate 63s) / OK [ran] [tree fcb8e79c0585] (2026-10-23T04:54:31Z)
- (ac 2) `python3 plugin/tests/run.py --load 24 test_code.Review test_loop.LoopReview` → exit 0 · Ran 14 tests in 19.4s (2 classes, 16 at a time; slowest: Review 19s, LoopReview 9s) / OK [ran] [tree fcb8e79c0585] (2026-10-23T04:54:55Z)
- (ac 3) `python3 plugin/tests/run.py --load 24 test_site_hero.Scene test_showpieces.CityBrowser test_showpieces.GraphBrowser` → exit 0 · Ran 16 tests in 22.9s (3 classes, 16 at a time; slowest: Scene 23s, CityBrowser 13s, GraphBrowser 13s) / OK [ran] [tree fcb8e79c0585] (2026-10-23T04:55:18Z)
- (ac 1) `python3 plugin/tests/run.py --load 24 test_hooks.NoTaskGate` → exit 0 · Ran 30 tests in 74.8s (1 classes, 16 at a time; slowest: NoTaskGate 75s) / OK [ran] [tree fcb8e79c0585] (2026-10-23T04:57:34Z)
- (ac 2) `python3 plugin/tests/run.py --load 24 test_code.Review test_loop.LoopReview` → exit 0 · Ran 14 tests in 28.1s (2 classes, 16 at a time; slowest: Review 28s, LoopReview 15s) / OK [ran] [tree fcb8e79c0585] (2026-10-23T04:57:34Z)
- (ac 3) `python3 plugin/tests/run.py --load 24 test_site_hero.Scene test_showpieces.CityBrowser test_showpieces.GraphBrowser` → exit 0 · Ran 16 tests in 24.9s (3 classes, 16 at a time; slowest: Scene 25s, CityBrowser 17s, GraphBrowser 14s) / OK [ran] [tree fcb8e79c0585] (2026-10-23T04:57:34Z)
- (audit intent) `self: read the branch diff; --load N spawns busy loops that die with run.py; hang guards (hook 10 s, fm 30 s, fm code 60 s) scale by measured runnable tasks per core up to 8x while timings tests check on purpose stay fixed; frame checks poll the page's own animation clock and rest state instead of wall-clock windows; two of three flakes reproduced at --load 64 and fixed at the cause, and a deliberate break of city.html's key handling makes the key test fail` → load flakes reproduce on demand (run.py --load N) and the three named ones pass under load [tree fcb8e79c0585] (2026-10-23T04:57:34Z)
- (audit edge) `self: read the branch diff; --load N spawns busy loops that die with run.py; hang guards (hook 10 s, fm 30 s, fm code 60 s) scale by measured runnable tasks per core up to 8x while timings tests check on purpose stay fixed; frame checks poll the page's own animation clock and rest state instead of wall-clock windows; two of three flakes reproduced at --load 64 and fixed at the cause, and a deliberate break of city.html's key handling makes the key test fail` → on a machine under 10 frames a second the key test can't catch a broken key; T-1721 never failed here, so its fix rests on an inferred cause (timeouts) [tree fcb8e79c0585] (2026-10-23T04:57:34Z)
- (audit maintainer) `self: read the branch diff; --load N spawns busy loops that die with run.py; hang guards (hook 10 s, fm 30 s, fm code 60 s) scale by measured runnable tasks per core up to 8x while timings tests check on purpose stay fixed; frame checks poll the page's own animation clock and rest state instead of wall-clock windows; two of three flakes reproduced at --load 64 and fixed at the cause, and a deliberate break of city.html's key handling makes the key test fail` → one busy_factor in helpers.py; the frame spy assumes pages cap a frame's step at 0.1 s (all three do) [tree fcb8e79c0585] (2026-10-23T04:57:34Z)
- (audit intent) `self: read the branch diff; --load N spawns busy loops that die with run.py; hang guards (hook 10 s, fm 30 s, fm code 60 s) scale by measured runnable tasks per core up to 8x while timings tests check on purpose stay fixed; frame checks poll the page's own animation clock and rest state instead of wall-clock windows; two of three flakes reproduced at --load 64 and fixed at the cause, and a deliberate break of city.html's key handling makes the key test fail` → load flakes reproduce on demand (run.py --load N) and the three named ones pass under load [tree 0cf8b41c796a] (2026-10-23T04:59:23Z)
- (audit adversary) `self: read the branch diff; --load N spawns busy loops that die with run.py; hang guards (hook 10 s, fm 30 s, fm code 60 s) scale by measured runnable tasks per core up to 8x while timings tests check on purpose stay fixed; frame checks poll the page's own animation clock and rest state instead of wall-clock windows; two of three flakes reproduced at --load 64 and fixed at the cause, and a deliberate break of city.html's key handling makes the key test fail` → this lane changes only test infrastructure; fmguard.py and test_guard.py reach it through the merge of foreman/build (T-1722, T-1727's base), not through this task's edits, and the guard suites pass after the merge [tree 0cf8b41c796a] (2026-10-23T04:59:23Z)
- (audit edge) `self: read the branch diff; --load N spawns busy loops that die with run.py; hang guards (hook 10 s, fm 30 s, fm code 60 s) scale by measured runnable tasks per core up to 8x while timings tests check on purpose stay fixed; frame checks poll the page's own animation clock and rest state instead of wall-clock windows; two of three flakes reproduced at --load 64 and fixed at the cause, and a deliberate break of city.html's key handling makes the key test fail` → on a machine under 10 frames a second the key test can't catch a broken key; T-1721 never failed here, so its fix rests on an inferred cause (timeouts) [tree 0cf8b41c796a] (2026-10-23T04:59:23Z)
- (audit maintainer) `self: read the branch diff; --load N spawns busy loops that die with run.py; hang guards (hook 10 s, fm 30 s, fm code 60 s) scale by measured runnable tasks per core up to 8x while timings tests check on purpose stay fixed; frame checks poll the page's own animation clock and rest state instead of wall-clock windows; two of three flakes reproduced at --load 64 and fixed at the cause, and a deliberate break of city.html's key handling makes the key test fail` → one busy_factor in helpers.py; the frame spy assumes pages cap a frame's step at 0.1 s (all three do) [tree 0cf8b41c796a] (2026-10-23T04:59:23Z)
- (audit intent) `self: read the branch diff; --load N spawns busy loops that die with run.py; hang guards (hook 10 s, fm 30 s, fm code 60 s) scale by measured runnable tasks per core up to 8x while timings tests check on purpose stay fixed; frame checks poll the page's own animation clock and rest state instead of wall-clock windows; two of three flakes reproduced at --load 64 and fixed at the cause, and a deliberate break of city.html's key handling makes the key test fail` → load flakes reproduce on demand (run.py --load N) and the three named ones pass under load [tree 0cf8b41c796a] (2026-10-23T05:01:31Z)
- (audit adversary) `self: read the branch diff; --load N spawns busy loops that die with run.py; hang guards (hook 10 s, fm 30 s, fm code 60 s) scale by measured runnable tasks per core up to 8x while timings tests check on purpose stay fixed; frame checks poll the page's own animation clock and rest state instead of wall-clock windows; two of three flakes reproduced at --load 64 and fixed at the cause, and a deliberate break of city.html's key handling makes the key test fail` → this lane changes only test infrastructure; fmguard.py and test_guard.py reach it through the merge of foreman/build, not through this task's edits, and the guard suites pass after the merge [tree 0cf8b41c796a] (2026-10-23T05:01:31Z)
- (audit edge) `self: read the branch diff; --load N spawns busy loops that die with run.py; hang guards (hook 10 s, fm 30 s, fm code 60 s) scale by measured runnable tasks per core up to 8x while timings tests check on purpose stay fixed; frame checks poll the page's own animation clock and rest state instead of wall-clock windows; two of three flakes reproduced at --load 64 and fixed at the cause, and a deliberate break of city.html's key handling makes the key test fail` → on a machine under 10 frames a second the key test can't catch a broken key; T-1721 never failed here, so its fix rests on an inferred cause (timeouts) [tree 0cf8b41c796a] (2026-10-23T05:01:31Z)
- (audit maintainer) `self: read the branch diff; --load N spawns busy loops that die with run.py; hang guards (hook 10 s, fm 30 s, fm code 60 s) scale by measured runnable tasks per core up to 8x while timings tests check on purpose stay fixed; frame checks poll the page's own animation clock and rest state instead of wall-clock windows; two of three flakes reproduced at --load 64 and fixed at the cause, and a deliberate break of city.html's key handling makes the key test fail` → one busy_factor in helpers.py; the frame spy assumes pages cap a frame's step at 0.1 s (all three do) [tree 0cf8b41c796a] (2026-10-23T05:01:31Z)
## Log
- 2026-10-23T03:35:15Z created
- 2026-10-23T04:01:13Z criterion 1 verify: `` → `python3 plugin/tests/run.py --load 24 test_hooks.NoTaskGate`
- 2026-10-23T04:01:13Z criterion 1 text: T-1719: Test_hooks.NoTaskGate hook calls time out at their 10 s limit under the 16-way parallel ru works → T-1719: test_hooks.NoTaskGate passes with the machine under load (run.py --load 24 runs the named tests beside 24 busy processes)
- 2026-10-23T04:01:13Z criterion 2 verify: `` → `python3 plugin/tests/run.py --load 24 test_code.Review test_loop.LoopReview`
- 2026-10-23T04:01:13Z criterion 2 text: T-1721: Flaky under load: test_code.Review.test_tool_results_and_the_journal_are_redacted and test works → T-1721: test_code.Review and test_loop.LoopReview pass under the same load
- 2026-10-23T04:01:13Z criterion 3 verify: `` → `python3 plugin/tests/run.py --load 24 test_site_hero.Scene test_showpieces.CityBrowser test_showpieces.GraphBrowser`
- 2026-10-23T04:01:13Z criterion 3 text: T-1728: Flaky under load: test_site_hero.Scene frame counts (133 != 198) and test_showpieces.CityB works → T-1728: test_site_hero.Scene and test_showpieces.CityBrowser and GraphBrowser frame-count checks pass under the same load (windows judged by frames per animation time, not wall time)
- 2026-10-23T04:01:14Z set scope=['plugin/tests/run.py', 'plugin/tests/helpers.py', 'plugin/tests/test_hooks.py', 'plugin/tests/test_code.py', 'plugin/tests/test_loop.py', 'plugin/tests/test_site_hero.py', 'plugin/tests/test_showpieces.py', 'plugin/lib/city.html', 'plugin/lib/graph.html', 'site/**', 'CHANGELOG.md']
- 2026-10-23T04:01:15Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1730.builder.md
- 2026-10-23T04:01:24Z focused
- 2026-10-23T04:14:17Z red: run.py --load 64 test_hooks.NoTaskGate -> TimeoutExpired: hook Stop timed out after 10 seconds (test_at_stop_the_requests_with_evidence_close_together); Review/LoopReview never failed here even at --load 96 or 6 parallel runs: fixed as the same cause, hang guards (fm 30 s, fm code 60 s) scaled by busy_factor
- 2026-10-23T04:38:27Z merged worktree-agent-a11a23eae92d1532c (6 file(s))
- 2026-10-23T04:38:28Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a11a23eae92d1532c
- 2026-10-23T04:53:27Z focused
- 2026-10-23T04:55:26Z scope: merged lane files (run.py --load, helpers.py busy_factor and frame spy, test_hooks, test_code, test_loop, test_site_hero, test_showpieces, test_run)
- 2026-10-23T05:02:57Z done
- 2026-10-23T05:02:59Z committed eba3e2b1 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1731 [FIX M, planned, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski…
- T-0877 [FIX S, done, 2 steps] fm friction reads right: a pass whose recon is out isn't 'due' again, and once-per-file tripwire notes aren't 'repeated… — lesson: A 'due' …
- T-0710 [FEATURE M, done, 4 steps] Frontier 10 — Milestone work compiler and merge train — lesson: Landing a milestone as a stack needs the edit order, not timestamps: th…
- decision 2026-10-23: Edit the main checkout while a background fm check runs under heavy builder load
- similar finished tasks took 2–4 steps
- likely tests for the scope: plugin/tests/test_safety.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/lib/graph.html, plugin/tests/helpers.py, plugin/tests/run.py, plugin/tests/test_code.py, plugin/tests/test_showpieces.py, plugin/tests/test_site_hero.py; re-ground the plan against them before editing
## Why not caught
none: flakes appear only under load, which no test reproduced before run.py --load
## Regression test
none: the builder reproduced T-1719 and T-1728 at run.py --load 64 before the fix (recorded red on the lane); a red run on the start tree depends on the machine's load, so prove can't reproduce it deterministically
## Lessons
- Judge animation tests by the page's animation clock, never by wall-clock frame counts
## Files touched
- plugin/tests/test_run.py
- plugin/tests/run.py
- plugin/tests/helpers.py
- r1.out
- r2.1.out
- r2.2.out
- r2.3.out
- r2.4.out
- r2.5.out
- r2.6.out
- plugin/tests/test_code.py
- plugin/tests/test_site_hero.py
- plugin/tests/test_showpieces.py
- plugin/lib/city.html
- check.out
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmguard.py
- plugin/lib/fmhome.py
- plugin/lib/fmsync.py
- plugin/tests/test_code_tui.py
- plugin/tests/test_docs.py
- plugin/tests/test_doctor.py
- plugin/tests/test_guard.py
- plugin/tests/test_help.py
- plugin/tests/test_portability.py
- plugin/tests/test_sync.py
