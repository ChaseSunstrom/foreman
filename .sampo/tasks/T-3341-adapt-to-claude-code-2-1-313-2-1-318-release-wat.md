---
id: T-3341
type: FEATURE
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py, plugin/agents/fm-builder.md]
depends_on: []
source: discovered
created: 2026-11-06T05:09:24Z
updated: 2026-11-06T06:47:45Z
lane: ~/.claude/foreman/.claude/worktrees/agent-ae02f38ec38d05dfc
lane_branch: worktree-agent-ae02f38ec38d05dfc
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T06:19:42Z
plan0_scope: [plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py, plugin/agents/fm-builder.md]
builder_returned: 2026-11-06T06:47:45Z
group: Claude Code release adaptation
---
# Claude Code 2.1.311-2.1.318 adaptation: doctor gate for SubagentStop firing once per subagent (2.1.311; older versions overcount budget rows), and fm-builder.md pins effort: high like every other agent (2.1.316-317 effort routing), with a test that every agent names effort
## Raw request
> Adapt to Claude Code 2.1.313-2.1.318 (release watch 2026-11-06): doctor's CC_FEATURES (doctor.py:1099) stops at 2.1.312. Add: pooled group budgets and CLAUDE_CODE_SUBAGENT_EFFORT (2.1.316) set per lane class (builder, reviewer, scout) and shown by doctor; a doctor warning when hook fan-out passes the 24-concurrent-hooks cap (2.1.312); ingest the claude_code.safety_event OTel event (2.1.307) into the guard's audit stats; gate the subagent worktree lifetime fix (2.1.311) for lanes. Source: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] check_cc_features((2,1,310)) warns naming SubagentStop and (2,1,318) passes; every plugin/agents/*.md names effort: — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] two failing tests  <- CURRENT
2. [x] CC_FEATURES row and the builder's effort line
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 116 tests in 261.8s (44 jobs, 16 at a time; slowest: ViewsRepair 6s, Timing 4s, LockProbe 3s) / OK (ran] (tree bd56b52649db] (world 2f1906870a] (2026-11-06T06:26:25Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_audit test_builder test_claims test_claude test_debug test_diagnosis test_docs test_doctor test_export test_foresight test_handoff test_judgment test_lanes test_left_out test_lib_hostile test_models test_onwrite test_rename_scan test_roles test_session test_session_fixes test_site_sections test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 124 (timed out after 846.259s) · timed out after 846.259s (ran] (tree bd56b52649db] (world 2f1906870a] (2026-11-06T06:40:39Z)
## Log
- 2026-11-06T05:09:24Z created
- 2026-11-06T05:52:52Z planned from capture
- 2026-11-06T06:19:40Z focused
- 2026-11-06T06:19:42Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T06:42:35Z moot: 24-hook cap (prompt/agent hooks only; Sampo has none), safety_event (CC stopped sending it in 2.1.312), pooled group budgets (gateway admin only). CLAUDE_CODE_SUBAGENT_EFFORT and worktree-lifetime gate stay in T-3384.
- 2026-11-06T06:42:40Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- research claude-code-capabilities: Method.** I read the README, the plugins/ and examples/ directory listings, the docs overview, and the CHANGELOG (about 1.06M characte…
- decision 2026-11-05: [costly] T-3219: the standing core yes now passes self-change gate holds made only of footprint, verb-count or hook-speed rows, per the user's 'I sa…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_agents.py, plugin/tests/test_audit.py, plugin/tests/test_builder.py, plugin/tests/test_claims.py, plugin/tests/test_claude.py, plugin/test…
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/agents/fm-builder.md, plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py; re-ground the plan against them before editing
