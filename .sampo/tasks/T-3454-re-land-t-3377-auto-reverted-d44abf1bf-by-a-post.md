---
id: T-3454
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/which.py, plugin/tests/test_cli.py, CHANGELOG.md, MASTER.md, docs/**, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: user
created: 2026-11-06T16:02:57Z
updated: 2026-11-06T16:29:49Z
base: f6777351fdb37b15dc13ea94bc72fb5e2b0df1ae
base_tree: 468a34385c46d50f5c9d852259348fa4c549143c
lane_stop: merged 2026-11-06T16:24:06Z
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T16:24:09Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/which.py, plugin/tests/test_cli.py, CHANGELOG.md, MASTER.md, docs/**]
verified: strong
unproven: [meaning]
lane_verified: 1078ed22d6494ca5629c28117b4e869104cf7f74
---
# Re-land T-3377: auto-reverted (d44abf1bf) by a post-merge runner that ran at a pre-T-3442 sha, on the same CheckSkip/Claims slot-pool false reds
## Raw request
> Re-land T-3377: auto-reverted (d44abf1bf) by a post-merge runner that ran at a pre-T-3442 sha, on the same CheckSkip/Claims slot-pool false reds
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] T-3377's change is back and its tests pass — verify with `python3 plugin/tests/run.py test_cli test_board_verbs test_task_ergonomics`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] revert the revert d44abf1bf in a lane; run the tests
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli test_board_verbs test_task_ergonomics` → exit 0 · Ran 210 tests in 15.2s (171 jobs, 16 at a time; slowest: StateViews.test_state_md_is_bounded 7s, AffectedPairs 5s, BoardVerbs.test_release_check_runs_doctor_and_demo_in_a_temporary_home 5s) / OK [ran] [tree de9767762758] [world 2f1906870a] (2026-11-06T16:03:50Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 164 tests in 35.9s (48 jobs, 16 at a time; slowest: TaskLifecycle 17s, CaptureAndIntake 8s, Checks 7s) / OK (start tree + this task's tests) [ran] [tree de9767762758] [world 2f1906870a] (2026-11-06T16:22:26Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 164 tests in 24.8s (119 jobs, 16 at a time; slowest: StateViews.test_state_md_is_bounded 7s, AuditPrep 6s, AffectedPairs 4s) / OK [ran] [tree de9767762758] [world 2f1906870a] (2026-11-06T16:22:26Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 7107a4fad8e8] (2026-11-06T16:24:11Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 164 tests in 54.0s (48 jobs, 16 at a time; slowest: TaskLifecycle 16s, StateViews 6s, CaptureAndIntake 6s) / FAILED (1 classes: test_cli.CaptureAndIntake) (start tree + this task's tests) [ran] [tree 7107a4fad8e8] [world 2f1906870a] (2026-11-06T16:25:54Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 164 tests in 44.1s (94 jobs, 16 at a time; slowest: CaptureAndIntake 8s, StateViews.test_state_md_is_bounded 6s, AuditPrep 6s) / OK [ran] [tree 7107a4fad8e8] [world 2f1906870a] (2026-11-06T16:25:54Z)
- (ac 1) `python3 plugin/tests/run.py test_cli test_board_verbs test_task_ergonomics` → exit 0 · Ran 210 tests in 78.0s (171 jobs, 16 at a time; slowest: StateViews.test_state_md_is_bounded 6s, BoardVerbs.test_release_check_runs_doctor_and_demo_in_a_temporary_home 5s, Checks.test_the_suite_gate_d [ran] [tree 7107a4fad8e8] [world 2f1906870a] (2026-11-06T16:27:15Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 7107a4fad8e8] (2026-11-06T16:27:15Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 7107a4fad8e8] (2026-11-06T16:27:15Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 7107a4fad8e8] (2026-11-06T16:27:15Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 7107a4fad8e8] (2026-11-06T16:27:15Z)
## Log
- 2026-11-06T16:02:57Z created
- 2026-11-06T16:03:01Z lane: ~/.claude/foreman.lanes/T-3454 on foreman/T-3454
- 2026-11-06T16:03:50Z start point recorded late (no focus had kept one): its diff starts at 8612db1
- 2026-11-06T16:24:06Z merged foreman/T-3454 (3 file(s))
- 2026-11-06T16:24:07Z lane removed: ~/.claude/foreman.lanes/T-3454
- 2026-11-06T16:24:07Z focused
- 2026-11-06T16:24:09Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T16:24:11Z set scope=['plugin/lib/sampo/cli.py', 'plugin/lib/sampo/which.py', 'plugin/tests/test_cli.py', 'CHANGELOG.md', 'MASTER.md', 'docs/**', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T16:24:11Z scope: widened at merge to the reviewed lane's own diff (1078ed22d), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T16:28:36Z done
- 2026-11-06T16:28:45Z committed b2637ff28 (116 files)
- 2026-11-06T16:29:49Z verified: the full suite is green on 1078ed22d, which contains 1078ed22d
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3450 [FIX S, done, 1 steps] Re-land T-3120: auto-reverted on the same CheckSkip/Claims/CloseGates reds the slot-pool bug (T-3442) made — lesson: A post-merge revert ne…
- T-3445 [FIX S, done, 1 steps] Re-land T-2911 and T-3372: both auto-reverted on CheckSkip/Claims reds the slot-pool bug (T-3442) made, red at their parents too — lesson: …
- T-3456 [FIX S, done, 1 steps] The post-merge newest-first probe is skipped whenever any pending merge carries after_reverts, so after one revert every later record runs …
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_affected_hubs.py, plugin/tests/test_affected_symbols.py, plugin/tests/test_ambient.py, plugin/tests/test_board_export.py, plugin/tests/tes…
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a re-land of reviewed work
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/which.py
- plugin/tests/test_cli.py
