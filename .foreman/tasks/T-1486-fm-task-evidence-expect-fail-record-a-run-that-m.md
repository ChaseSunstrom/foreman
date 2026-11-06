---
id: T-1486
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_task_ergonomics.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T17:33:46Z
updated: 2026-10-22T17:53:33Z
base: 90612893d4e7ce0818a125598c53a8f1ca89e088
base_tree: 06e0e7d8480bbaa8358ec7aee411bcc3e3e67d9b
plan0_at: 2026-10-22T17:51:56Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_task_ergonomics.py, CHANGELOG.md]
verified: strong
---
# Fm task evidence --expect-fail: record a run that must fail (non-zero exit required, recor
## Raw request
> fm task evidence --expect-fail: record a run that must fail (non-zero exit required, recorded as 'expected red', exit 0 returned) so a failing-test step's red run can be recorded without fm task prove; the red-step scans skip that marker (fmcli.py:4993-5003, 535-559, 952)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task evidence --step N --run CMD --expect-fail records a failing run as the expected red and exits 0; a passing run is refused and records nothing; --ac with it is refused — verify with `cd plugin/tests && python3 -m unittest test_task_ergonomics.ExpectFail`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] --expect-fail on fm task evidence
## Resume here
## Docs impact
CHANGELOG.md line; the flag's help text
## Verification evidence
- `cd plugin/tests && python3 -m unittest test_task_ergonomics.ExpectFail` → ✗ exit 1 · Ran 3 tests in 1.233s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree bf474be8f209] (2026-10-22T17:52:39Z)
- `cd plugin/tests && python3 -m unittest test_task_ergonomics.ExpectFail` → exit 0 · Ran 3 tests in 1.105s / OK [ran] [tree bf474be8f209] (2026-10-22T17:52:39Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_task_ergonomics.ExpectFail` → exit 0 · Ran 3 tests in 1.040s / OK [ran] [tree bf474be8f209] (2026-10-22T17:52:40Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_task_ergonomics` → exit 0 · Ran 16 tests in 6.728s / OK [ran] [tree bf474be8f209] (2026-10-22T17:52:47Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_task_ergonomics` → exit 0 · Ran 16 tests in 6.934s / OK [ran] [tree bf474be8f209] (2026-10-22T17:52:55Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_task_ergonomics.ExpectFail` → exit 0 · Ran 3 tests in 1.039s / OK [ran] [tree 729a42d2a3c9] (2026-10-22T17:53:04Z)
- (audit adversary) `self: test-first (red on the start tree, green now); --expect-fail needs --step, a non-zero exit that reached its check (never_ran reuses T-0985's rule), then records 'red as expected (exit N)' with no ✗ so the red-step scans and _refuse_failed_run don't read it as a failure; returns 0; test_task_ergonomics green` → it can't launder a failure into a pass on a criterion (refused with --ac) or a check that never ran (refused); the step still needs its passing work later at close through the criteria [tree 729a42d2a3c9] (2026-10-22T17:53:04Z)
- (audit edge) `self: test-first (red on the start tree, green now); --expect-fail needs --step, a non-zero exit that reached its check (never_ran reuses T-0985's rule), then records 'red as expected (exit N)' with no ✗ so the red-step scans and _refuse_failed_run don't read it as a failure; returns 0; test_task_ergonomics green` → an exit code from a missing command (127) is 'never ran' and refused [tree 729a42d2a3c9] (2026-10-22T17:53:04Z)
- (audit self) `self: test-first (red on the start tree, green now); --expect-fail needs --step, a non-zero exit that reached its check (never_ran reuses T-0985's rule), then records 'red as expected (exit N)' with no ✗ so the red-step scans and _refuse_failed_run don't read it as a failure; returns 0; test_task_ergonomics green` → no findings [tree 729a42d2a3c9] (2026-10-22T17:53:04Z)
## Log
- 2026-10-22T17:33:46Z created
- 2026-10-22T17:51:55Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_task_ergonomics.py', 'CHANGELOG.md']
- 2026-10-22T17:51:55Z focused
- 2026-10-22T17:53:32Z done
- 2026-10-22T17:53:33Z committed 412c63d8 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1101 [FEATURE S, done, 2 steps] Fm check should not fail one task's close on another checkpointed task's recorded red test — lesson: A loop variable that reuses an out…
- research T-0271-review-1: Changes needed. `task_prove_hunks` can record passing evidence when nothing was proven, and mishandles files with spaces and deleted files. I r…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-14: Block T-0760 rather than edit its failing AC, since the AC already has evidence
- similar finished tasks took 2–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
red steps were only recordable through fm task prove
## Lessons
- Give each evidence kind its own wording rather than a flag on the result parser.
## Files touched
- plugin/tests/test_task_ergonomics.py
- plugin/lib/fmcli.py
- CHANGELOG.md
