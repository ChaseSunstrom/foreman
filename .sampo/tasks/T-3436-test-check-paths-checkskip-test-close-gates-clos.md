---
id: T-3436
type: FIX
tier: M
status: dropped
priority: urgent
scope: []
depends_on: []
source: discovered
created: 2026-11-06T14:02:51Z
updated: 2026-11-06T21:59:38Z
base_note: 
lane_branch: worktree-agent-afd0c3f102fbffc2c
base: 74e8d98a05b695ab98f8b23f241802a3b888d156
base_tree: 767124e325e1332b8ac205fbf3ebdca97ee37f1c
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T14:13:33Z
plan0_scope: []
builder_returned: 2026-11-06T14:48:18Z
---
# test_check_paths.CheckSkip, test_close_gates.CloseGates, test_cli_speed.ForkServer and…
## Raw request
> FIX!: test_check_paths.CheckSkip, test_close_gates.CloseGates, test_cli_speed.ForkServer and test_run.PerTestJobs time out under host load ~20 (forkcli socket timeouts at 30-42 s, CloseGates 478 s), fail alone too while the box is busy, and so turn the post-merge suite red (auto-revert attempts and 'merges wait' conflicts) and refuse sampo ship; give their nested fm check/evidence calls a base timeout sized from their idle time under the gate's own load (helpers.fm timeout=, still x busy_factor) and cut their nested work where cheap, so each passes at load 2x cpus
## Interpretation
Reading 1: nested fm/run.py calls in four classes outlast their fixed timeouts under load, so raise those timeouts per site (chosen). Reading 2: the code under test is slow and should be sped up; ruled out, idle times are small and the failures appear only under load.
## Assumptions (confidence)
## Acceptance criteria
- [ ] CheckSkip passes under load — verify with `python3 plugin/tests/run.py test_check_paths.CheckSkip`
- [ ] CloseGates passes under load — verify with `python3 plugin/tests/run.py test_close_gates.CloseGates`
- [ ] ForkServer passes under load — verify with `python3 plugin/tests/run.py test_cli_speed.ForkServer`
- [ ] PerTestJobs passes under load — verify with `python3 plugin/tests/run.py test_run.PerTestJobs`
## Non-goals
## Approach (options → choice → why)
1) Per-site explicit timeout= sized 3x idle (x busy_factor in helpers.fm); likely outcome: passes under load; fails if the wait is not a timeout but a load gate. 2) Raise the global fm default timeout; likely outcome: passes but hides real hangs; fails if a site is stuck anyway. 3) Stand-in runner like T-3417 (use what exists: that commit's pattern); likely outcome: fast; fails if the assertion needs the real runner. 4) Do less: only bump the four worst sites; likely outcome: others stay flaky. Choice 1 (85%): smallest change that keeps hang guards.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] give slow nested calls explicit timeouts; cut nested work  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T14:02:51Z created
- 2026-11-06T14:13:13Z planned: it has criteria and steps
- 2026-11-06T14:13:32Z focused
- 2026-11-06T14:13:33Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T15:19:35Z dropped: superseded by T-3442: the timeouts came from nested run.py queuing on the slot pool (a renamed env var), not from load; scaling the timeouts would only hide that
- 2026-11-06T15:19:35Z work at drop saved: bc05214b7c67 (restore: git -C ~/.claude/foreman restore --source=bc05214b7c67 --worktree -- :/)
- 2026-11-06T21:59:38Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afd0c3f102fbffc2c (branch worktree-agent-afd0c3f102fbffc2c kept: not merged); dropped: its task is closed; the lane was left behind after the merge
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3417 [PERFORMANCE M, done, 1 steps] test_cli.AffectedPairs takes ~70 s idle and 200-520 s under load (four builders tonight… — lesson: none: a reviewed builder lane; i…
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- T-3435 [FIX M, done, 1 steps] Sampo ship's scratch-tree full suite refuses on any red class with no flake rerun:… — lesson: none: a reviewed builder lane; its lessons ar…
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
