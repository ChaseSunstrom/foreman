---
id: T-1201
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T14:26:47Z
updated: 2026-10-16T14:45:54Z
base: bca4e1d0db03ccc96a5ab792116716647268943d
base_tree: a4cafa459ce54bc3d61b3597b66b90123c144aa7
plan0_at: 2026-10-16T14:44:43Z
plan0_scope: []
verified: ok
---
# test_parallel mid-batch test waits for the slow session's pid instead of racing it
## Raw request
> test_parallel test_a_failure_mid_batch_stops_every_session_and_frees_its_tasks failed once in the affected run at load ~45 and passed alone twice and in a full rerun: find its timing assumption and make it load-proof
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the quick stub ends only after the slow stub has written its pid (bounded wait), so a loaded machine can't end the batch before the pid file exists — verify with `python3 plugin/tests/run.py test_parallel`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Quick stub waits up to 20 s for the pid file before ending
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_parallel` → exit 0 · Ran 15 tests in 30.5s (3 classes, 16 at a time; slowest: Parallel 30s, CaptureAndIntake 1s, GuardMine 1s) / OK [ran] [tree e0c01f1f41f5] (2026-10-16T14:45:21Z)
- (ac 1) `python3 plugin/tests/run.py test_parallel` → exit 0 · Ran 15 tests in 25.4s (3 classes, 16 at a time; slowest: Parallel 25s, CaptureAndIntake 1s, GuardMine 1s) / OK [ran] [tree e0c01f1f41f5] (2026-10-16T14:45:53Z)
- (audit self) `self: the wait is bounded (200 x 0.1 s) so a broken slow stub can't hang the test; it only orders the two fake sessions, the asserted behaviour (kill on failure, lanes freed) is unchanged` → no findings [tree e0c01f1f41f5] (2026-10-16T14:45:53Z)
## Log
- 2026-10-16T14:26:47Z created
- 2026-10-16T14:44:43Z planned from capture
- 2026-10-16T14:44:43Z focused
- 2026-10-16T14:45:54Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0744 [FIX S, done, 2 steps] Full suite flakes under load: find and fix the timing-sensitive classes
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-04: T-0212 (L) self-approved under full autonomy after self-critique: cases are validated fail-to-pass; sessions isolated by FOREMAN_STATE and a temp wo…
- similar finished tasks took 2–5 steps
## Regression test
none: a load race that 10 concurrent runs didn't reproduce; the fix removes the race (the quick stub now waits, bounded at 20 s, for the slow stub's pid file before it ends the batch), and test_parallel itself is the check
## Files touched
- plugin/tests/test_parallel.py
