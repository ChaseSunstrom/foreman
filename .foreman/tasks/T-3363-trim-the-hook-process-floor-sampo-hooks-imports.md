---
id: T-3363
type: PERFORMANCE
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/hooks/hook, plugin/tests/test_bench_hooks.py, plugin/lib/sampo/core.py, plugin/lib/sampo/fixes.py]
depends_on: []
source: followup
created: 2026-11-06T05:54:53Z
updated: 2026-11-06T06:59:14Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a519553639925a6b6
lane_branch: worktree-agent-a519553639925a6b6
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-06T06:19:37Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/hooks/hook, plugin/tests/test_bench_hooks.py]
builder_returned: 2026-11-06T06:59:14Z
---
# Trim the hook process floor: sampo.hooks imports its stdlib extras lazily (tempfile/random, shutil/bz2, hashlib) and hooks/hook runs python3 -I, so the floor (TaskCompleted p50, 37.5 ms) drops to 30 ms or less with every gate green
## Raw request
> Trim the hook process floor: sampo.hooks imports its stdlib extras lazily (tempfile/random, shutil/bz2, hashlib) and hooks/hook runs python3 -I, so the floor (TaskCompleted p50, 37.5 ms) drops to 30 ms or less with every gate green
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] bench_hooks floor (TaskCompleted p50) is 30 ms or less and the gates still pass — verify with `python3 plugin/tests/run.py test_bench_hooks test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] measure the floor before (bench_hooks --runs 30)
2. [x] lazy imports and -I; measure after
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_bench_hooks` → exit 0 · Ran 7 tests in 143.3s (4 jobs, 16 at a time; slowest: Modules 6s, Floor 0s, ScriptBudget 0s) / OK (ran] (tree 3d97d09e8ee2] (world 2f1906870a] (2026-11-06T06:27:12Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_agents test_bench test_bench_hooks test_board_posture test_board_surfaces test_bus test_cli test_cloned_config test_code_tui test_code_worker test_compact test_core test_design_surfaces test_docs test_doctor test_evolve test_firewall test_fixes test_guard_hardening test_hooks test_hunks test_left_out test_library test_models test_onwrite test_plugins test_rename_scan test_resilience test_safety test_sandbox test_scout test_settings test_setup test_ship test_statusline_ui test_supply_delta test_tool_injection test_ui_replay test_verify_alias test_visibility && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 124 (timed out after 801.27s) · timed out after 801.27s (ran] (tree 3d97d09e8ee2] (world 2f1906870a] (2026-11-06T06:40:41Z)
- (step 1) `python3 plugin/tests/run.py test_bench_hooks` → exit 0 · Ran 7 tests in 21.2s (6 jobs, 16 at a time; slowest: Modules.test_a_hook_run_records_the_plugin_files_its_process_imported 5s, Modules.test_the_hook_writes_only_under_the_temp_dir 1s, Floor 1s) / OK (ran] (tree e0cab305cf20] (world 2f1906870a] (2026-11-06T06:54:15Z)
## Log
- 2026-11-06T05:54:53Z created
- 2026-11-06T06:19:34Z focused
- 2026-11-06T06:19:37Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-06T06:21:21Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/hooks/hook', 'plugin/tests/test_bench_hooks.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/fixes.py']
- 2026-11-06T06:21:22Z scope widened: the deferred imports (tempfile, shutil, hashlib) live in core.py and fixes.py, not only hooks.py
- 2026-11-06T06:53:08Z focused
- 2026-11-06T06:59:07Z Measurements: alternating A/B, 40 PreToolUse runs, user+sys CPU, loaded host: base 62.8 ms, new 62.5 ms (no gain, the guard path still imports hashlib and tempfile). Cold importtime sampo.hooks 82 ms to 14.6 ms before the guard loads them. -I dropped: env -S fails open on coreutils < 8.30.
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Python: the standard library first (fm playbooks show lang/stdlib-python)
- T-2023 [PERFORMANCE M, done, 2 steps] Hooks import subprocess, shutil and glob only when a call uses them — lesson: Trace imports with a meta-path spy before deferring: …
- T-2121 [FEATURE L, done, 2 steps] fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (…
- decision 2026-11-06: No Rust rewrite now: a Bash tool call costs ~37 ms of process floor plus ~90 ms of Python handler work that tripled in three days; the handler's gro…
- similar past tasks were L: consider --tier L
- similar finished tasks took 2–2 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_affected_hubs.py, plugin/tests/test_agents.py, plugin/tests/test_bench.py, plugin/tests/test_board_posture.py, plugin/tests/test_board_sur…
