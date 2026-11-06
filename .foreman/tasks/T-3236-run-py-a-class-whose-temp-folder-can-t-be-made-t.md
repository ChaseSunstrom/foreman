---
id: T-3236
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_run.py, CHANGELOG.md]
depends_on: [T-3222]
source: discovered
created: 2026-11-05T19:14:09Z
updated: 2026-11-05T20:51:26Z
base: 4933fd85b33b1241dd661773682d633924e4bfd0
base_tree: c754e9f1885bd83521d5f880f36178a2420d22d7
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T20:51:06Z
plan0_scope: [plugin/tests/run.py, plugin/tests/test_run.py, CHANGELOG.md]
verified: strong
---
# run.py: a class whose temp folder can't be made (/tmp full: OSError 28) crashes the…
## Raw request
> run.py: a class whose temp folder can't be made (/tmp full: OSError 28) crashes the whole run with a traceback and every result is lost; fail that class with the reason and go on (seen in T-3222's sandboxed full run at 14 min)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a class whose temp folder can't be made fails by name with the OSError, the other classes still run and the summary prints — verify with `python3 plugin/tests/run.py test_run`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: mkdtemp raising OSError fails one class, not the run
2. [x] run_one catches the temp folder's OSError and returns a failed result naming it
## Resume here
## Docs impact
CHANGELOG line (with T-3222's)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 91 tests in 4.2s (67 jobs, 16 at a time; slowest: Hang.test_the_run_deadline_kills_a_running_class_and_skips_unstarted_ones 3s, Ambient.test_a_full_check_waits_for_fm_ships_test_run_but_not_inside [ran] [tree c754e9f1885b] [world 2f1906870a] (2026-11-05T20:51:12Z)
- (step 2) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 91 tests in 4.7s (50 jobs, 16 at a time; slowest: Ship 4s, Hang.test_the_run_deadline_kills_a_running_class_and_skips_unstarted_ones 4s, Ambient 4s) / OK [ran] [tree c754e9f1885b] [world 2f1906870a] (2026-11-05T20:51:17Z)
- (ac 1) `python3 plugin/tests/run.py test_run` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T20:51:17Z [ran] [tree c754e9f1885b] [world 2f1906870a] (2026-11-05T20:51:25Z)
- (audit intent) `self: the fix and its test landed in T-3222 (4933fd85); a class whose temp folder can't be made returns (cid, 1, the reason) and the run goes on; red before was the sandboxed full runs dying at 12-14 min with the traceback` → one class fails by name instead of the whole run crashing [tree c754e9f1885b] (2026-11-05T20:51:25Z)
- (audit edge) `self: the fix and its test landed in T-3222 (4933fd85); a class whose temp folder can't be made returns (cid, 1, the reason) and the run goes on; red before was the sandboxed full runs dying at 12-14 min with the traceback` → the returned shape matches run_one's other early return (NOT_STARTED) [tree c754e9f1885b] (2026-11-05T20:51:25Z)
- (audit self) `self: the fix and its test landed in T-3222 (4933fd85); a class whose temp folder can't be made returns (cid, 1, the reason) and the run goes on; red before was the sandboxed full runs dying at 12-14 min with the traceback` → no findings [tree c754e9f1885b] (2026-11-05T20:51:25Z)
## Log
- 2026-11-05T19:14:09Z created
- 2026-11-05T19:15:46Z planned: it has criteria and steps
- 2026-11-05T19:15:46Z set scope=['plugin/tests/run.py', 'plugin/tests/test_run.py', 'CHANGELOG.md']
- 2026-11-05T19:15:50Z set depends_on=['T-3222']
- 2026-11-05T20:51:05Z focused
- 2026-11-05T20:51:06Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T20:51:07Z done in T-3222's commit 4933fd85 (run.py's run_one catches the temp folder's OSError; test_run.Tmp.test_tmp_a_class_whose_folder_cant_be_made_fails_alone), because the sandboxed full run that T-3222's criterion 5 needed kept dying on it
- 2026-11-05T20:51:26Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3222 [FEATURE L, done, 5 steps] Network and filesystem sandboxing as a Sampo feature: one sampo sandbox verb that turns… — lesson: running the whole suite inside the n…
- T-2091 [FEATURE S, done, 2 steps] fm tidy: drop a project state dir whose root folder is gone (throwaway temp projects…
- research T-1215-review: Changes needed. One MEDIUM bug (an uncaught timeout aborts the whole bench) and one MEDIUM comparison flaw. The rest are LOW. I read the code and…
- decision 2026-11-02: [check: python3 plugin/tests/run.py test_foresight] Tests never read the host's own services or config; they point XDG_CONFIG_HOME and HOME at their…
- similar finished tasks took 2–5 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Preflight
Changed in scope since this was planned (2026-11-05): CHANGELOG.md, plugin/tests/run.py, plugin/tests/test_run.py; re-ground the plan against them before editing
## Regression test
test_run.Tmp.test_tmp_a_class_whose_folder_cant_be_made_fails_alone: red before the fix (OSError: [Errno 28] No space left on device, raised out of run_one, run in T-3222's session), green after; it landed with T-3222's commit 4933fd85, so this task's own start tree already has both
## Why not caught
no test filled /tmp; test_run.Tmp now raises ENOSPC from mkdtemp
## Lessons
- a runner's per-unit setup must fail that unit, never the run
