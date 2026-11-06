---
id: T-2891
type: FIX
tier: S
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-11-04T03:59:08Z
updated: 2026-11-04T07:21:20Z
trigger: baseline
trigger_key: 10fcf811dfa9eeb8
baseline: true
builder_model: sonnet
base: 9fb71634ddb327bd60e553574efb745bf4d77aba
base_tree: 4d2dd279e0bfd8a01d0a0317baac4c8d7e77da05
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T06:35:19Z
plan0_scope: []
lane_stop: merged 2026-11-04T07:07:58Z
verified: strong
unproven: [meaning]
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_code_hardening.LeanPlanner.test_a_lean_claude_planner_whose_init_lists_an_mcp_server_is_stopped, test_code_worker.Worker.test_a_claude_plan_override_without_stream_json_plans_from_plain_output, test_code_worker.Worker.test_a_cli_planner_error_is_said, test_code_worker.Worker.test_a_named_planner_not_verified_here_warns, test_code_worker.Worker.test_a_planner_stream_with_no_result_line_is_an_error, test_code_worker.Worker.test_a_planner_that_changes_files_is_stopped_before_any_task …. Captured by sampo check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
Reading 1 (chosen): restore the baseline. test_code_hardening.LeanPlanner.test_a_lean_claude_planner_whose_init_lists_an_mcp_server_is_stopped fails on every run: a fake claude worker whose init lists an MCP server 'evil' should stop fm code with 'MCP server evil' on stderr, but the run prints only 'Next: fm task show T-0001'. Find the change that made the lean planner path skip the init check (suspects: 06d5019a, fm code starting on the --escalate model; the T-2847 respell; T-2893's models changes) and fix the cause, not the test. Reading 2 (ruled out): relax the test. Ruled out because the check is a security guard: a planner with an unvetted MCP server must be stopped.
## Assumptions (confidence)
## Acceptance criteria
- [x] the lean planner with an MCP server in its init is stopped with 'MCP server evil' on stderr — verify with `python3 plugin/tests/run.py test_code_hardening test_code_worker`
## Non-goals
## Approach (options → choice → why)
1) Bisect with git log on smith.py, claude.py, models.py and the code CLI since the test last passed (fm check history), reproduce with the test alone, and fix the path that no longer reads the planner's init line. Likely outcome: a one-place fix where the lean planner's init check is reached again. Fails if the failure is environmental (PATH or HOME leakage), in which case the test's isolation is fixed instead. Choice 1 (75%). 2) use what exists: sampo whyred on the failing test names the suspects from recent diffs. Likely outcome: a faster bisect, so it's used inside option 1. Fails if the cause is older than its window. 3) do less: mark the test expected-to-fail. Likely outcome: green gates, but the guard stays broken. Fails the security intent, so it's ruled out.
## Risks and rollback
## Execution prompt
## Steps
1. [x] reproduce and bisect the cause
2. [x] fix the cause; the test passes unchanged
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_code_hardening.LeanPlanner` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: LeanPlanner 0s) / OK [ran] [tree 8face0a4941a] [world 2f1906870a] (2026-11-04T06:42:48Z)
- (step 2) `python3 plugin/tests/run.py test_code_hardening.LeanPlanner` → exit 0 · Ran 1 tests in 5.9s (1 classes, 16 at a time; slowest: LeanPlanner 2s) / OK [ran] [tree 157cf958afac] [world 2f1906870a] (2026-11-04T06:58:57Z)
- (step 1) `python3 plugin/tests/run.py test_code_hardening test_code_worker` → exit 0 · Ran 94 tests in 71.4s (11 classes, 16 at a time; slowest: Worker 71s, Failover 9s, Routing 3s) / OK [ran] [tree 1d4651fccfae] [world 2f1906870a] (2026-11-04T07:14:28Z)
- (step 2) `python3 plugin/tests/run.py test_code_hardening test_code_worker` → exit 0 · Ran 94 tests in 112.5s (11 classes, 16 at a time; slowest: Worker 112s, Failover 8s, Routing 3s) / OK [ran] [tree 1d4651fccfae] [world 2f1906870a] (2026-11-04T07:16:21Z)
- `python3 plugin/tests/run.py test_code_hardening.LeanPlanner` → ✗ exit 1 · Ran 1 tests in 52.2s (1 classes, 16 at a time; slowest: LeanPlanner 51s) / FAILED (1 classes: test_code_hardening.LeanPlanner) (start tree + this task's tests) [ran] [tree 1d4651fccfae] [world 2f1906870a] (2026-11-04T07:17:20Z)
- `python3 plugin/tests/run.py test_code_hardening.LeanPlanner` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: LeanPlanner 1s) / OK [ran] [tree 1d4651fccfae] [world 2f1906870a] (2026-11-04T07:17:20Z)
- (ac 1) `python3 plugin/tests/run.py test_code_hardening test_code_worker` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T07:16:21Z [ran] [tree 1d4651fccfae] [world 2f1906870a] (2026-11-04T07:17:27Z)
- (audit intent) `lane diff read: models._local honours FOREMAN_NO_LOCAL_MODELS and the fm code test env sets it; 94 tests green; red on the start tree, green now; the planner's MCP init check was never broken` → the baseline is green again; the lean-planner security test runs its real path [tree 1d4651fccfae] (2026-11-04T07:17:27Z)
- (audit edge) `lane diff read: models._local honours FOREMAN_NO_LOCAL_MODELS and the fm code test env sets it; 94 tests green; red on the start tree, green now; the planner's MCP init check was never broken` → the variable only hides local servers from discovery for tests; real runs never set it; other test files that call fm code with their own env can still see a local server [tree 1d4651fccfae] (2026-11-04T07:17:27Z)
- (audit adversary) `lane diff read: models._local honours FOREMAN_NO_LOCAL_MODELS and the fm code test env sets it; 94 tests green; red on the start tree, green now; the planner's MCP init check was never broken` → no check was loosened: the MCP-server refusal path is unchanged and is exercised again [tree 1d4651fccfae] (2026-11-04T07:17:27Z)
- (audit self) `lane diff read: models._local honours FOREMAN_NO_LOCAL_MODELS and the fm code test env sets it; 94 tests green; red on the start tree, green now; the planner's MCP init check was never broken` → no findings [tree 1d4651fccfae] (2026-11-04T07:17:27Z)
## Log
- 2026-11-04T03:59:08Z created
- 2026-11-04T06:35:07Z set tier=S
- 2026-11-04T06:35:08Z planned: it has criteria and steps
- 2026-11-04T06:35:08Z set approved=True
- 2026-11-04T06:35:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2891.builder.md
- 2026-11-04T06:35:18Z focused
- 2026-11-04T06:35:19Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T07:07:58Z merged worktree-agent-a0880814fbbb588ad (2 file(s))
- 2026-11-04T07:07:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0880814fbbb588ad
- 2026-11-04T07:13:15Z focused
- 2026-11-04T07:21:20Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-1388 [SECURITY M, done, 2 steps] A coding CLI that fm code runs only reads Foreman's state: fm refuses every state-changing command under FOREMAN_WORKER_OF, and a lean…
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
## Why not caught
the suite had always run on a machine with no local model server
## Lessons
- a test that shells out to a CLI inherits the machine: a model server started on the box changed which path fm code took
## Files touched
- plugin/lib/sampo/smith.py
- plugin/lib/sampo/models.py
- plugin/tests/test_code.py
