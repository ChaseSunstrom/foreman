---
id: T-3445
type: FIX
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, MASTER.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/hooks.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_cli.py, plugin/tests/test_cli_ergonomics.py, plugin/tests/test_task_ergonomics.py]
depends_on: []
source: user
created: 2026-11-06T15:16:56Z
updated: 2026-11-06T15:39:26Z
base: 0f041f3f124accbe21ab3de0210f85a00c1f6bb3
base_tree: 11ad039d1bd71e18a402bd5e2a6c3c6f50e722b6
lane_stop: merged 2026-11-06T15:28:32Z
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T15:28:35Z
plan0_scope: []
verified: strong
unproven: [docs, meaning]
---
# Re-land T-2911 and T-3372: both auto-reverted on CheckSkip/Claims reds the slot-pool bug (T-3442) made, red at their parents too
## Raw request
> Re-land T-2911 and T-3372: both auto-reverted on CheckSkip/Claims reds the slot-pool bug (T-3442) made, red at their parents too
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the two merges' changes are back and their own tests pass — verify with `python3 plugin/tests/run.py test_bookkeeping test_cli_ergonomics test_task_ergonomics`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] revert the two reverts (fa1d2afd7, fc66ce462) in a lane; run their tests
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 6a22e400a042] (2026-11-06T15:28:39Z)
- `python3 plugin/tests/run.py test_bookkeeping test_cli test_cli_ergonomics test_task_ergonomics` → ✗ exit 1 · Ran 224 tests in 233.0s (62 jobs, 16 at a time; slowest: TaskLifecycle 25s, CaptureAndIntake 12s, StateViews 10s) / FAILED (4 classes: test_task_ergonomics.SplitVerify, test_task_ergonomics.TaskErgono (start tree + this task's tests) [ran] [tree 6a22e400a042] [world 2f1906870a] (2026-11-06T15:36:27Z)
- `python3 plugin/tests/run.py test_bookkeeping test_cli test_cli_ergonomics test_task_ergonomics` → exit 0 · Ran 224 tests in 230.0s (177 jobs, 16 at a time; slowest: SplitVerify 8s, TaskErgonomics 6s, StateViews.test_state_md_is_bounded 5s) / OK [ran] [tree 6a22e400a042] [world 2f1906870a] (2026-11-06T15:36:27Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping test_cli_ergonomics test_task_ergonomics` → exit 0 · Ran 66 tests in 75.6s (46 jobs, 16 at a time; slowest: CommitOwnFiles 6s, StepEvidence 5s, CommitAfterFocus 5s) / OK [ran] [tree 6a22e400a042] [world 2f1906870a] (2026-11-06T15:37:45Z)
- (step 1) `python3 plugin/tests/run.py test_bookkeeping test_cli_ergonomics test_task_ergonomics` → exit 0 · Ran 66 tests in 75.6s (46 jobs, 16 at a time; slowest: CommitOwnFiles 6s, StepEvidence 5s, CommitAfterFocus 5s) / OK [ran] [tree 6a22e400a042] [world 2f1906870a] (2026-11-06T15:37:45Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 6a22e400a042] (2026-11-06T15:37:45Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 6a22e400a042] (2026-11-06T15:37:45Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 6a22e400a042] (2026-11-06T15:37:45Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 6a22e400a042] (2026-11-06T15:37:45Z)
## Log
- 2026-11-06T15:16:56Z created
- 2026-11-06T15:16:59Z lane: ~/.claude/foreman.lanes/T-3445 on foreman/T-3445
- 2026-11-06T15:28:32Z merged foreman/T-3445 (8 file(s))
- 2026-11-06T15:28:33Z lane removed: ~/.claude/foreman.lanes/T-3445
- 2026-11-06T15:28:34Z focused
- 2026-11-06T15:28:35Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T15:28:38Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'MASTER.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/hooks.py', 'plugin/tests/test_bookkeeping.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_cli_ergonomics.py', 'plugin/tests/test_task_ergonomics.py']
- 2026-11-06T15:28:38Z scope: widened at merge to the reviewed lane's own diff (97fd67e1e), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T15:39:23Z done
- 2026-11-06T15:39:26Z committed c93f915a6 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3450 [FIX S, planned, 1 steps] Re-land T-3120: auto-reverted on the same CheckSkip/Claims/CloseGates reds the slot-pool bug (T-3442) made
- T-3446 [FIX M, planned, 1 steps] The post-merge suite reverts a merge whose red classes are red at its parent too…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- A post-merge revert needs the red to be absent at the parent; otherwise the revert is noise.
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/hooks.py
- plugin/tests/test_bookkeeping.py
- plugin/tests/test_cli.py
- plugin/tests/test_cli_ergonomics.py
- plugin/tests/test_task_ergonomics.py
