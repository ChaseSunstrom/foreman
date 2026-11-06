---
id: T-1453
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T05:50:56Z
updated: 2026-10-22T14:12:14Z
base: 6d0ee3bbae1930b0ba805153efb8b097c4559e75
base_tree: 0adb50752ae6ac477bd4df6c1e7769e09ad8e09f
plan0_at: 2026-10-22T14:02:07Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
verified: strong
---
# Stop hook still judges the turn when the project lock is busy
## Raw request
> Stop hook swallows LOCK_QUICK contention (fmhooks.py:2949, hooks.log 2026-10-20T23:28:39Z): a contended lock skips the evidence hold silently; retry once or log it as a hold-skipped note
## Interpretation
stop() takes the project lock for LOCK_QUICK (1 s) around the evidence/claims gates; contended (an fm command holding it), LockTimeout escapes, the hook logs a traceback and holds nothing, so a turn claiming unproven work slips through (hooks.log 2026-10-20T23:28:39Z).
## Assumptions (confidence)
## Acceptance criteria
- [x] a claim without evidence is held while another process holds the project lock — verify with `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_a_busy_project_lock_still_holds_a_claim_without_evidence`
## Non-goals
## Approach (options → choice → why)
ExitStack: try to take the lock; busy → still read the gate and judge the turn, only skip saving its counters (a repeated nudge next time is harmless). Options: longer timeout (slows every stop), retry loop (same) → rejected.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] judge without saving when the lock is busy
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_a_busy_project_lock_still_holds_a_claim_without_evidence` → ✗ exit 1 · Ran 1 test in 2.741s / FAILED (failures=1) [ran] [tree 6a7eca21d39d] (2026-10-22T14:05:54Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_a_busy_project_lock_still_holds_a_claim_without_evidence` → exit 0 · Ran 1 test in 2.618s / OK [ran] [tree 5539ebec62f5] (2026-10-22T14:05:58Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.Stop.test_a_busy_project_lock_still_holds_a_claim_without_evidence` → exit 0 · Ran 1 test in 1.724s / OK [ran] [tree c2cc3d971945] (2026-10-22T14:10:12Z)
- (audit edge) `self: ExitStack takes the lock if it can; busy → gates still judged from a fresh read, only _write_gate skipped. Test holds the project lock from the test process and the hook still blocks 'Step 2 is done.'; test_hooks green.` → unsaved counters may repeat one nudge next turn (harmless; stop_hook_active stops loops) [tree c2cc3d971945] (2026-10-22T14:10:12Z)
- (audit adversary) `self: ExitStack takes the lock if it can; busy → gates still judged from a fresh read, only _write_gate skipped. Test holds the project lock from the test process and the hook still blocks 'Step 2 is done.'; test_hooks green.` → no hold is weakened; a busy lock now holds where it didn't [tree c2cc3d971945] (2026-10-22T14:10:12Z)
- (audit self) `self: ExitStack takes the lock if it can; busy → gates still judged from a fresh read, only _write_gate skipped. Test holds the project lock from the test process and the hook still blocks 'Step 2 is done.'; test_hooks green.` → no findings [tree c2cc3d971945] (2026-10-22T14:10:12Z)
## Log
- 2026-10-22T05:50:56Z created
- 2026-10-22T14:02:05Z planned from capture
- 2026-10-22T14:02:06Z focused
- 2026-10-22T14:12:12Z done
- 2026-10-22T14:12:14Z committed 5b09e03e (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0087-review: Verdict:** approve with nits. PreToolUse can never be paused, and the pause cannot get stuck or flap. The findings below are all MEDIUM or LOW. […
- T-1449 [FIX S, done, 2 steps] Hook notes survive one failing builder — lesson: One try around a list of independent producers turns any one failure into total loss; isol…
- T-0886 [FEATURE M, done, 2 steps] The Stop hook checks the final message's specific claims (tests pass, fixed, verified) aga — lesson: Judge a run by its verdict, not by…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar finished tasks took 2–2 steps
- likely tests for the scope: plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmhooks.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/lib/fmhooks.py
- plugin/tests/test_hooks.py
- CHANGELOG.md
