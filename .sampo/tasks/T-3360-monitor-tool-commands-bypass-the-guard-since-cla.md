---
id: T-3360
type: SECURITY
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py, plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py]
depends_on: []
source: discovered
created: 2026-11-06T05:52:49Z
updated: 2026-11-06T06:09:01Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a09d67b7a4e0566b9
lane_branch: worktree-agent-a09d67b7a4e0566b9
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T05:53:11Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py, plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py]
builder_returned: 2026-11-06T06:09:01Z
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
- (step 1) `python3 plugin/tests/run.py test_hooks.GuardAblation test_doctor` → ✗ exit 1 · run.py: no test matches test_hooks.GuardAblation [ran] [tree 149f75b8cd91] [world 2f1906870a] (2026-11-06T05:55:05Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.Ablate test_doctor` → exit 0 · Ran 116 tests in 656.6s (45 jobs, 16 at a time; slowest: ViewsRepair 50s, NightTimers 11s, Ablate 7s) / OK [ran] [tree 4e68c9bb5424] [world 2f1906870a] (2026-11-06T06:08:43Z)
## Log
- 2026-11-06T05:52:49Z created
- 2026-11-06T05:53:08Z focused
- 2026-11-06T05:53:11Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3222 [FEATURE L, done, 5 steps] Network and filesystem sandboxing as a Sampo feature: one sampo sandbox verb that turns… — lesson: running the whole suite inside the n…
- T-2563 [FEATURE M, done, 3 steps] Anergy for permission prompts: time each prompt to its PostToolUse and report reflex-approved command classes (spike) — lesson: A spike…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- decision 2026-10-30: [cites: user steer 2026-10-30: Foreman shouldn't be specific to CC and must work outside it] [check: python3 plugin/tests/run.py test_setup.NoClaude…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py, plugin/tests/test_hooks.py
