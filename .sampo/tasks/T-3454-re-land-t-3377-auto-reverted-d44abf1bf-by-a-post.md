---
id: T-3454
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/which.py, plugin/tests/test_cli.py, CHANGELOG.md, MASTER.md, docs/**]
depends_on: []
source: user
created: 2026-11-06T16:02:57Z
updated: 2026-11-06T16:22:26Z
lane: ~/.claude/foreman.lanes/T-3454
base: 8612db1bfb737e1d9100ccc07cbe67339577708b
---
# Re-land T-3377: auto-reverted (d44abf1bf) by a post-merge runner that ran at a pre-T-3442 sha, on the same CheckSkip/Claims slot-pool false reds
## Raw request
> Re-land T-3377: auto-reverted (d44abf1bf) by a post-merge runner that ran at a pre-T-3442 sha, on the same CheckSkip/Claims slot-pool false reds
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] T-3377's change is back and its tests pass — verify with `python3 plugin/tests/run.py test_cli test_board_verbs test_task_ergonomics`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] revert the revert d44abf1bf in a lane; run the tests
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli test_board_verbs test_task_ergonomics` → exit 0 · Ran 210 tests in 15.2s (171 jobs, 16 at a time; slowest: StateViews.test_state_md_is_bounded 7s, AffectedPairs 5s, BoardVerbs.test_release_check_runs_doctor_and_demo_in_a_temporary_home 5s) / OK [ran] [tree de9767762758] [world 2f1906870a] (2026-11-06T16:03:50Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 164 tests in 35.9s (48 jobs, 16 at a time; slowest: TaskLifecycle 17s, CaptureAndIntake 8s, Checks 7s) / OK (start tree + this task's tests) [ran] [tree de9767762758] [world 2f1906870a] (2026-11-06T16:22:26Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 164 tests in 24.8s (119 jobs, 16 at a time; slowest: StateViews.test_state_md_is_bounded 7s, AuditPrep 6s, AffectedPairs 4s) / OK [ran] [tree de9767762758] [world 2f1906870a] (2026-11-06T16:22:26Z)
## Log
- 2026-11-06T16:02:57Z created
- 2026-11-06T16:03:01Z lane: ~/.claude/foreman.lanes/T-3454 on foreman/T-3454
- 2026-11-06T16:03:50Z start point recorded late (no focus had kept one): its diff starts at 8612db1
## Follow-ups captured
