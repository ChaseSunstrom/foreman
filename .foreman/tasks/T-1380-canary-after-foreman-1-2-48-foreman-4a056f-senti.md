---
id: T-1380
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_verify_strength.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-21T16:40:12Z
updated: 2026-10-22T15:58:40Z
group: canary failures after Foreman releases
base: 04565bdd3aff5cc7c358b0d533f345032c1a9566
base_tree: 62fa6fb1fff9f71b74c9ccabd09d956c2a3c10a3
plan0_at: 2026-10-22T15:56:57Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_verify_strength.py, CHANGELOG.md]
verified: strong
---
# Sentinel skips point-in-time checks and reruns a failure once
## Raw request
> Canary after Foreman 1.2.48: ✗ foreman-4a056f: Sentinel: 10 past check(s) from 10 finished task(s); 3 failing now; 3 with side effects skipped
## Interpretation
Release canaries after 1.2.48 and 1.2.50 reported failing past checks: T-1367's `git log origin/main -1 … | grep -q 'Foreman 1.2.47'` (a release check that can only stay true until the next release) and test suites (test_code_worker, test_code, test_bench test_evolve) that pass today — load flakes while canaries ran side by side. Ledger sentinel events 2026-10-21 16:37 and 23:36.
## Assumptions (confidence)
## Acceptance criteria
- [x] a check reading origin/ is skipped as point-in-time; a check that fails then passes is flaky, not failing — verify with `cd plugin/tests && python3 -m unittest test_verify_strength.VerifyStrength.test_point_in_time_skipped_and_flake_rerun`
## Non-goals
## Approach (options → choice → why)
In cmd_sentinel: a criterion command that reads a remote-tracking ref (origin/…, @{u}, ls-remote) is point-in-time, skipped and counted like side effects; a failing rerun is run once more and reported as flaky (not failing) when the second run passes — as _close_affected already does. Options: skip release tasks by title (misses other remote checks) → by command shape.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] skip remote-ref checks, rerun a failure once
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_verify_strength.VerifyStrength.test_point_in_time_skipped_and_flake_rerun` → ✗ exit 1 · Ran 1 test in 2.670s / FAILED (failures=1) [ran] [tree 1ca0e03e342b] (2026-10-22T15:57:03Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_verify_strength.VerifyStrength.test_point_in_time_skipped_and_flake_rerun` → exit 0 · Ran 1 test in 3.035s / OK [ran] [tree 86b10627d81b] (2026-10-22T15:57:08Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_verify_strength.VerifyStrength.test_point_in_time_skipped_and_flake_rerun` → exit 0 · Ran 1 test in 2.662s / OK [ran] [tree 2afb947d5100] (2026-10-22T15:57:44Z)
- (audit intent) `self: _POINT_IN_TIME skips origin/, @{u}, ls-remote checks (counted like side effects); a failing check (not a timeout) runs once more and counts as flaky when it then passes, as _close_affected already does. Test covers both; test_verify_strength green (incl. the existing reruns test, whose failing check still fails twice).` → the canary's three failures: a point-in-time release check (now skipped) and load flakes (now rerun once) [tree 2afb947d5100] (2026-10-22T15:57:44Z)
- (audit edge) `self: _POINT_IN_TIME skips origin/, @{u}, ls-remote checks (counted like side effects); a failing check (not a timeout) runs once more and counts as flaky when it then passes, as _close_affected already does. Test covers both; test_verify_strength green (incl. the existing reruns test, whose failing check still fails twice).` → a timeout (124) isn't rerun (it already cost its full timeout); assumption checks are unchanged [tree 2afb947d5100] (2026-10-22T15:57:44Z)
- (audit adversary) `self: _POINT_IN_TIME skips origin/, @{u}, ls-remote checks (counted like side effects); a failing check (not a timeout) runs once more and counts as flaky when it then passes, as _close_affected already does. Test covers both; test_verify_strength green (incl. the existing reruns test, whose failing check still fails twice).` → a real break fails twice and still reports; skipping only drops checks about a remote's state [tree 2afb947d5100] (2026-10-22T15:57:44Z)
- (audit self) `self: _POINT_IN_TIME skips origin/, @{u}, ls-remote checks (counted like side effects); a failing check (not a timeout) runs once more and counts as flaky when it then passes, as _close_affected already does. Test covers both; test_verify_strength green (incl. the existing reruns test, whose failing check still fails twice).` → no findings [tree 2afb947d5100] (2026-10-22T15:57:44Z)
## Log
- 2026-10-21T16:40:12Z created
- 2026-10-22T15:42:39Z planned from capture
- 2026-10-22T15:44:55Z plan: grounded in cmd_sentinel (fmcli ~3711-3770); test + fix drafted (scratchpad t1380.edit); applies when the full gate run frees the checkout
- 2026-10-22T15:56:56Z focused
- 2026-10-22T15:58:37Z done
- 2026-10-22T15:58:40Z committed 217f13bc (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1448 [FIX M, dropped, 0 steps] Canary after Foreman 1.2.50: ✗ foreman-4a056f: Sentinel: 10 past check(s) from 10 finished
- T-1368 [FIX M, dropped, 0 steps] Canary after Foreman 1.2.47: ✗ foreman-4a056f: Sentinel: 8 past check(s) from 10 finished
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-16: T-1080 self-approved under full autonomy: risk points from today's ledger (destructive guard blocks 1, failed closes 2) and today's Revert commits (…
- similar past tasks were M: consider --tier M
- the similar finished task took 5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcli.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/lib/fmcli.py
- plugin/tests/test_verify_strength.py
- CHANGELOG.md
