---
id: T-1485
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcodebench.py, plugin/tests/test_code_bench.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T17:25:19Z
updated: 2026-10-22T17:29:19Z
base: d52876df6d0715743916c02f31b7b89a38c9c522
base_tree: 2738e569449ebbfd704bb0040a719bc6084417a5
plan0_at: 2026-10-22T17:25:58Z
plan0_scope: [plugin/lib/fmcodebench.py, plugin/tests/test_code_bench.py, CHANGELOG.md]
verified: strong
---
# Fm code bench leaves orphaned test_calc.py processes running after a seed run (seen from t
## Raw request
> fm code bench leaves orphaned test_calc.py processes running after a seed run (seen from the volt session, its T-0651): tag each bench run's environment with FM_BENCH_SEED=<its temp dir> and, before the temp folder is deleted, kill every process carrying that marker (safe when runs go side by side; not a sweep of all children)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] after a bench seed whose run leaves a spinning test_calc.py, no process carrying a finished run's FM_BENCH_SEED marker is left — verify with `cd plugin/tests && python3 -m unittest test_code_bench.Bench.test_a_check_that_never_ends_is_reported_and_the_run_still_kept`
## Non-goals
## Approach (options → choice → why)
Options: kill every child of the bench (would kill unrelated children); a subreaper (fm code's own _kill_orphans; doesn't reach a process that detached into its own session under fm code); chosen: an environment marker FM_BENCH_SEED=<temp dir> on the seed's env, and before the temp folder is deleted, SIGKILL every process (own uid, /proc/*/environ) carrying exactly that marker. Safe side by side; Linux /proc only (elsewhere a no-op).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: no orphan carries a finished run's marker
2. [x] FM_BENCH_SEED in the run's env; kill its carriers before the temp folder goes
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- `cd plugin/tests && python3 -m unittest test_code_bench.Bench.test_a_check_that_never_ends_is_reported_and_the_run_still_kept` → ✗ exit 1 · Ran 1 test in 6.289s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 3404b79f2bd5] (2026-10-22T17:27:24Z)
- `cd plugin/tests && python3 -m unittest test_code_bench.Bench.test_a_check_that_never_ends_is_reported_and_the_run_still_kept` → ✗ exit 1 · Ran 1 test in 6.157s / FAILED (failures=1) [ran] [tree 3404b79f2bd5] (2026-10-22T17:27:24Z)
- `cd plugin/tests && python3 -m unittest test_code_bench.Bench.test_a_check_that_never_ends_is_reported_and_the_run_still_kept` → ✗ exit 1 · Ran 1 test in 6.257s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree ef9e8c047e26] (2026-10-22T17:27:45Z)
- `cd plugin/tests && python3 -m unittest test_code_bench.Bench.test_a_check_that_never_ends_is_reported_and_the_run_still_kept` → exit 0 · Ran 1 test in 6.156s / OK [ran] [tree ef9e8c047e26] (2026-10-22T17:27:45Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_bench.Bench.test_a_check_that_never_ends_is_reported_and_the_run_still_kept` → exit 0 · Ran 1 test in 6.155s / OK [ran] [tree ef9e8c047e26] (2026-10-22T17:27:56Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_code_bench` → exit 0 · Ran 13 tests in 16.572s / OK [ran] [tree ef9e8c047e26] (2026-10-22T17:28:13Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_bench` → exit 0 · Ran 13 tests in 16.498s / OK [ran] [tree ef9e8c047e26] (2026-10-22T17:28:30Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_bench.Bench.test_a_check_that_never_ends_is_reported_and_the_run_still_kept` → exit 0 · Ran 1 test in 6.158s / OK [ran] [tree cf434325f22d] (2026-10-22T17:28:46Z)
- (audit adversary) `self: test-first (a seed whose fix loops forever; the test counts processes left in this run's deleted temp folder, red on the start tree, green now); run_seed's body moved to _run_in unchanged under a try/finally that kills the marked processes before TemporaryDirectory removes the folder; test_code_bench 13 OK; 17 existing stragglers killed by hand` → kills only this user's processes (st_uid check) whose environ holds exactly FM_BENCH_SEED=<this run's mkdtemp path>, never the bench itself; a random temp path can't match another run's marker [tree cf434325f22d] (2026-10-22T17:28:46Z)
- (audit edge) `self: test-first (a seed whose fix loops forever; the test counts processes left in this run's deleted temp folder, red on the start tree, green now); run_seed's body moved to _run_in unchanged under a try/finally that kills the marked processes before TemporaryDirectory removes the folder; test_code_bench 13 OK; 17 existing stragglers killed by hand` → a process that clears its environment escapes the marker (none of fm code's do); macOS has no /proc, so it's a no-op there (ponytail note) [tree cf434325f22d] (2026-10-22T17:28:46Z)
- (audit intent) `self: test-first (a seed whose fix loops forever; the test counts processes left in this run's deleted temp folder, red on the start tree, green now); run_seed's body moved to _run_in unchanged under a try/finally that kills the marked processes before TemporaryDirectory removes the folder; test_code_bench 13 OK; 17 existing stragglers killed by hand` → the volt session's T-0651 plan, done here so volt needs no core grant [tree cf434325f22d] (2026-10-22T17:28:46Z)
- (audit self) `self: test-first (a seed whose fix loops forever; the test counts processes left in this run's deleted temp folder, red on the start tree, green now); run_seed's body moved to _run_in unchanged under a try/finally that kills the marked processes before TemporaryDirectory removes the folder; test_code_bench 13 OK; 17 existing stragglers killed by hand` → no findings [tree cf434325f22d] (2026-10-22T17:28:46Z)
## Log
- 2026-10-22T17:25:19Z created
- 2026-10-22T17:25:53Z set scope=['plugin/lib/fmcodebench.py', 'plugin/tests/test_code_bench.py', 'CHANGELOG.md']
- 2026-10-22T17:25:55Z focused
- 2026-10-22T17:29:18Z done
- 2026-10-22T17:29:19Z committed 8172fcf8 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1044 [FEATURE M, done, 4 steps] Process-group reaper and a startup orphan sweep for the claude -p helpers (ideas, second, — lesson: start_new_session protects children…
- research T-1044-review: Verdict: changes needed.** There is one MEDIUM regression, and the pid-reuse guard itself is sound. [stale: plugin/lib/fmideas.py changed since i…
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
- likely tests for the scope: plugin/tests/test_bench.py
## Why not caught
the bench tests checked the verdict, never what was left running
## Lessons
- A child started with start_new_session leaves the parent's process group, so killing the group misses it; tag the run's environment and kill by tag.
## Files touched
- plugin/tests/test_code_bench.py
- plugin/lib/fmcodebench.py
- CHANGELOG.md
