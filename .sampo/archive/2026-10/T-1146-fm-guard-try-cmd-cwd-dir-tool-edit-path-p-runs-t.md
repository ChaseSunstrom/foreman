---
id: T-1146
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_guard_try.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-16T10:08:43Z
updated: 2026-10-16T10:45:20Z
base: 86e3640c41927f007145f49638656af067e6228d
base_tree: e94cf88bb825d27efc306ecd24963e2811ab69ac
plan0_at: 2026-10-16T10:22:18Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_guard_try.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Fm guard try "<cmd>" [--cwd DIR] [--tool Edit --path P]: runs the real guard on a command
## Raw request
> fm guard try "<cmd>" [--cwd DIR] [--tool Edit --path P]: runs the real guard on a command as this session would (task, grants, cwd) and prints the decision, category and rule, never running it; replaces scratch replay scripts when chasing a false positive
## Interpretation
When a command is refused, or Claude suspects it will be, there is no fm way to ask the guard 'would this pass here, and why?'. The main thread twice wrote scratch scripts that fed the real hook a payload with the real cwd (T-1125, T-1141). fm guard try runs the real decision path without running the command.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm guard try prints allow for 'ls', deny with category for a state write, and the cwd changes the answer for a relative path into state/ — verify with `python3 plugin/tests/run.py test_guard_try`
## Non-goals
## Approach (options → choice → why)
A 'guard' command with action try. It builds the PreToolUse payload (tool Bash with command, or --tool Edit/Write with --path), with cwd from --cwd or the current dir and the session from the environment, and calls fmhooks._guard_decision(pl, fmguard) in-process: the same ctx (active task, grants, standing, trust) the hook uses. It prints allow, or deny/ask with the category and the guard's message, and --json. It never executes anything. Options considered: spawn the hook binary (slower, the same answer), or call fmguard.check directly (misses the hook's ctx and its other checks).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_guard_try.py): allow, deny with category and message, --cwd, --tool Edit --path, --json, nothing executed
2. [x] The guard try command (lazy, in fmcli's help tier 'Finding your way'); MASTER and CHANGELOG lines
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_try` → ✗ exit 1 · Ran 4 tests in 1.0s (1 classes, 16 at a time; slowest: GuardTry 0s) / FAILED (1 classes) [ran] [tree 46640d1696d7] (2026-10-16T10:22:44Z)
- (step 1) `python3 plugin/tests/run.py test_guard_try` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: GuardTry 1s) / OK [ran] [tree fe00f2b36d44] (2026-10-16T10:24:29Z)
- (step 2) `python3 plugin/tests/run.py test_guard_try` → exit 0 · Ran 4 tests in 0.7s (1 classes, 16 at a time; slowest: GuardTry 1s) / OK [ran] [tree fe00f2b36d44] (2026-10-16T10:24:30Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_try` → exit 0 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: GuardTry 1s) / OK [ran] [tree d1c78d64a70d] (2026-10-16T10:42:43Z)
- (audit intent) `self: reviewed merged diff; scout traced _guard_ctx/findings/check: no grant, ask slot or taint spent (only _pre_tool_use spends); usage errors for a bad action or missing target` → answers 'would this be blocked for me now' with the hook's own path [tree d1c78d64a70d] (2026-10-16T10:42:43Z)
- (audit adversary) `self: reviewed merged diff; scout traced _guard_ctx/findings/check: no grant, ask slot or taint spent (only _pre_tool_use spends); usage errors for a bad action or missing target` → never executes the command; spends nothing; output is the guard's own message [tree d1c78d64a70d] (2026-10-16T10:42:43Z)
- (audit edge) `self: reviewed merged diff; scout traced _guard_ctx/findings/check: no grant, ask slot or taint spent (only _pre_tool_use spends); usage errors for a bad action or missing target` → --tool Edit without --path is a usage error; NotebookEdit maps to notebook_path [tree d1c78d64a70d] (2026-10-16T10:42:43Z)
- (audit operator) `self: reviewed merged diff; scout traced _guard_ctx/findings/check: no grant, ask slot or taint spent (only _pre_tool_use spends); usage errors for a bad action or missing target` → one line allow/deny category: message; --json for scripts [tree d1c78d64a70d] (2026-10-16T10:42:43Z)
- (audit maintainer) `self: reviewed merged diff; scout traced _guard_ctx/findings/check: no grant, ask slot or taint spent (only _pre_tool_use spends); usage errors for a bad action or missing target` → reuses _guard_decision so it can't drift from the hook [tree d1c78d64a70d] (2026-10-16T10:42:43Z)
- (audit self) `self: reviewed merged diff; scout traced _guard_ctx/findings/check: no grant, ask slot or taint spent (only _pre_tool_use spends); usage errors for a bad action or missing target` → no findings [tree d1c78d64a70d] (2026-10-16T10:42:43Z)
## Log
- 2026-10-16T10:08:43Z created
- 2026-10-16T10:09:04Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_guard_try.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-16T10:22:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1146.builder.md
- 2026-10-16T10:22:18Z focused
- 2026-10-16T10:38:54Z merged worktree-agent-a44061e37dc42a7ee (3 file(s))
- 2026-10-16T10:38:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a44061e37dc42a7ee
- 2026-10-16T10:39:12Z focused
- 2026-10-16T10:39:44Z paused: focus moved to T-1145
- 2026-10-16T10:42:21Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T10:42:21Z focused
- 2026-10-16T10:42:41Z scope: MASTER.md and CHANGELOG.md lines
- 2026-10-16T10:45:18Z done
- 2026-10-16T10:45:20Z committed 532cf70 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-0698 [FIX M, done, 4 steps] Friction batch 2026-10-09: IFS false block from heredoc data, an undefined-name gate, MASTER.md read hint, builder refused-command list — l…
- decision 2026-10-15: Keep claude plugin install under the plugin category even with HOME=<scratch>; no exemption (T-0893 dropped)
- similar finished tasks took 2–6 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_hooks.py
## Plan gaps
- failed first: step 1 Failing tests (test_guard_try.py): allow, deny with category and message, --cwd, --tool Edit --path…
## Files touched
- plugin/tests/test_guard_try.py
- plugin/lib/fmcli.py
- plugin/lib/fmreplay.py
- plugin/lib/fmhooks.py
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmcore.py
- plugin/tests/test_verify_check.py
