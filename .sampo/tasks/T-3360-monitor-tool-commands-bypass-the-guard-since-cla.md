---
id: T-3360
type: SECURITY
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py, plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py, plugin/lib/fmguard.py, plugin/hooks/hooks.json]
depends_on: []
source: discovered
created: 2026-11-06T05:52:49Z
updated: 2026-11-06T17:40:23Z
lane_branch: foreman/T-3360
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T05:53:11Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py, plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py]
builder_returned: 2026-11-06T06:51:16Z
lane: ~/.claude/foreman.lanes/T-3360
base: 81de6117ebb5eb92339e29c572d44667cd4faca5
base_tree: c12888948f73da30dbb93b4113f6ee92b9d1021b
group: guard bypass paths for interpreted scripts
---
# Monitor tool commands bypass the guard: since Claude Code 2.1.314 Bash-matching hooks also run for Monitor commands, but hooks.py GUARDED = FILE_TOOLS | {'Bash'} (hooks.py:31) returns early for tool_name Monitor, so a Monitor 'rm -rf ~' or force-push is never checked
## Raw request
> Monitor tool commands bypass the guard: since Claude Code 2.1.314 Bash-matching hooks also run for Monitor commands, but hooks.py GUARDED = FILE_TOOLS | {'Bash'} (hooks.py:31) returns early for tool_name Monitor, so a Monitor 'rm -rf ~' or force-push is never checked
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a PreToolUse payload {tool_name: Monitor, tool_input: {command: 'rm -rf ~'}} is denied exactly as the same Bash command is, and a safe Monitor command passes; doctor's CC_FEATURES has a 2.1.314 row for it — verify with `python3 plugin/tests/run.py test_hooks test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test: Monitor rm -rf ~ is denied like Bash  <- CURRENT
2. [x] treat Monitor's command as Bash in the PreToolUse guard path; doctor row
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.GuardAblation test_doctor` → ✗ exit 1 · run.py: no test matches test_hooks.GuardAblation (ran] (tree 149f75b8cd91] (world 2f1906870a] (2026-11-06T05:55:05Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.Ablate test_doctor` → exit 0 · Ran 116 tests in 656.6s (45 jobs, 16 at a time; slowest: ViewsRepair 50s, NightTimers 11s, Ablate 7s) / OK (ran] (tree 4e68c9bb5424] (world 2f1906870a] (2026-11-06T06:08:43Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 629 tests in 777.0s (244 jobs, 16 at a time; slowest: Approvals 20s, UserPromptSubmit 18s, PromptApprovals 17s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 4e68c9bb5424] (world 2f1906870a] (2026-11-06T06:21:48Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.Ablate test_doctor test_plugin` → exit 0 · Ran 144 tests in 401.4s (53 jobs, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, Command 3s) / OK (ran] (tree ddf70b533608] (world 2f1906870a] (2026-11-06T06:34:31Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_agents test_approve_reads test_bench test_board_posture test_board_surfaces test_bus test_cli test_cloned_config test_code_tui test_code_worker test_compact test_core test_design_surfaces test_docs test_doctor test_evolve test_firewall test_guard test_guard_diff test_guard_exec_vectors test_guard_git test_guard_hardening test_guard_overrefusal test_guard_pipes test_guard_sampo test_hooks test_hunks test_left_out test_library test_models test_onwrite test_plugins test_rename_scan test_resilience test_safety test_sandbox test_scout test_settings test_settings_scopes test_setup test_ship test_statusline_ui test_supply_delta test_tool_injection test_ui_replay test_visibility && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2268 tests in 925.9s (799 jobs, 16 at a time; slowest: AffectedPairs 218s, Ship 38s, Scout 29s) / FAILED (2 classes: test_cli.AffectedPairs, test_left_out.LeftOut) (ran] (tree ddf70b533608] (world 2f1906870a] (2026-11-06T06:50:09Z)
## Log
- 2026-11-06T05:52:49Z created
- 2026-11-06T05:53:08Z focused
- 2026-11-06T05:53:11Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T06:27:41Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/tests/test_hooks.py', 'plugin/lib/sampo/doctor.py', 'plugin/tests/test_doctor.py', 'plugin/lib/fmguard.py', 'plugin/hooks/hooks.json']
- 2026-11-06T17:39:28Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a09d67b7a4e0566b9 (branch worktree-agent-a09d67b7a4e0566b9 kept: not merged); dropped: relocated beside the repo: the train left it out on a conflict and the Ward refuses git merge under .claude/worktrees; its branch is kept and merged into the new lane
- 2026-11-06T17:39:29Z lane: ~/.claude/foreman.lanes/T-3360 on foreman/T-3360
- 2026-11-06T17:40:23Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3222 [FEATURE L, done, 5 steps] Network and filesystem sandboxing as a Sampo feature: one sampo sandbox verb that turns… — lesson: running the whole suite inside the n…
- T-2563 [FEATURE M, done, 3 steps] Anergy for permission prompts: time each prompt to its PostToolUse and report reflex-approved command classes (spike) — lesson: A spike…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- decision 2026-10-30: [cites: user steer 2026-10-30: Foreman shouldn't be specific to CC and must work outside it] [check: python3 plugin/tests/run.py test_setup.NoClaude…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/lib/fmguard.py, plugin/lib/sampo/doctor.py, plugin/lib/sampo/hooks.py, plugin/tests/test_doctor.py, plugin/tests/test_hooks.py; re-ground the plan against them before editing
