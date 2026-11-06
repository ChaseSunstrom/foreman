---
id: T-1808
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T04:00:16Z
updated: 2026-10-28T04:05:00Z
base: d0243417c6fbcbc64edbf4f2666f6302c3d178ee
base_tree: ec1c0ccd540d77545f04596ca9d1f3865a6bc81e
plan0_at: 2026-10-28T04:00:17Z
plan0_scope: []
verified: strong
---
# run.py kills a test class that hangs and names it with its stack: CI's 20-min job cap hid where
## Raw request
> run.py kills a test class that hangs and names it with its stack: CI's 20-min job cap hid where
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a hanging class fails by name with its traceback — verify with `cd plugin/tests && python3 -m unittest -q test_run`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] run_one: own session, -X faulthandler, timeout -> SIGABRT then killpg; --timeout flag
## Resume here
## Docs impact
## Verification evidence
- `cd plugin/tests && timeout 120 python3 -m unittest -q test_run` → exit 0 · Ran 10 tests in 3.923s / OK (start tree + this task's tests) [ran] [tree 23b3749aa30a] (2026-10-28T04:00:56Z)
- `cd plugin/tests && timeout 120 python3 -m unittest -q test_run` → exit 0 · Ran 10 tests in 3.157s / OK [ran] [tree 23b3749aa30a] (2026-10-28T04:00:56Z)
- (step 1) `cd plugin/tests && timeout 120 python3 -m unittest -q test_run test_ci_annotations test_parallel` → exit 0 · Ran 25 tests in 24.140s / OK [ran] [tree 23b3749aa30a] (2026-10-28T04:01:21Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_run` → exit 0 · Ran 10 tests in 3.178s / OK [ran] [tree 23b3749aa30a] (2026-10-28T04:04:54Z)
- (audit edge) `self-review: own session + SIGABRT under -X faulthandler dumps every thread then killpg reaps children holding the pipes; a grandchild that leaves the session would still hold them (none do with FOREMAN_CHROME=none); 480 s is 4.8x the slowest class locally under 16-way load` → a class that finishes normally keeps its returncode and output; a killed one returns negative and its stderr ends with the named timeout line, which annotations() puts in a public ::error [tree 23b3749aa30a] (2026-10-28T04:04:54Z)
- (audit operator) `self-review: own session + SIGABRT under -X faulthandler dumps every thread then killpg reaps children holding the pipes; a grandchild that leaves the session would still hold them (none do with FOREMAN_CHROME=none); 480 s is 4.8x the slowest class locally under 16-way load` → --timeout S lets a slow machine or --load run widen it [tree 23b3749aa30a] (2026-10-28T04:04:54Z)
- (audit self) `self-review: own session + SIGABRT under -X faulthandler dumps every thread then killpg reaps children holding the pipes; a grandchild that leaves the session would still hold them (none do with FOREMAN_CHROME=none); 480 s is 4.8x the slowest class locally under 16-way load` → no findings [tree 23b3749aa30a] (2026-10-28T04:04:54Z)
## Log
- 2026-10-28T04:00:16Z created
- 2026-10-28T04:00:16Z focused
- 2026-10-28T04:01:21Z scope: plugin/tests/run.py (run_one timeout, --timeout) and test_run.py
- 2026-10-28T04:04:58Z done
- 2026-10-28T04:05:00Z committed 527753e3 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- T-1338 [FEATURE M, done, 4 steps] fm code durable runs: a new run names each unfinished one with its resume command, the app's history says how to resume, kills at each …
- T-1284 [FIX M, done, 5 steps] macOS: fm code --worker, the guard's /tmp case, the reaper, relate and context-tax tests pass on macOS, and the job fits its time limit — l…
- decision 2026-10-23: Cause: hooks handed Claude the exact fm command each turn, so it never loaded the skill describing the step; descriptions used Foreman jargon or use…
## Regression test
test_run.Hang.test_a_class_that_hangs_is_killed_and_named_with_its_stack: red before the fix (errors=1: run_one took no timeout and would wait on the hang), green after (10 OK). fm task prove can't show it: run.py sits under plugin/tests, so it's carried as a test file into the start tree.
## Why not caught
no class hung locally; on CI the job's 20-min cap killed the run before run.py printed any ::error line, and job logs need a login
## Lessons
- a CI job cap kills the run before it can report; give the runner its own per-unit cap below the job's so a hang fails by name
## Files touched
- plugin/tests/test_run.py
- plugin/tests/run.py
