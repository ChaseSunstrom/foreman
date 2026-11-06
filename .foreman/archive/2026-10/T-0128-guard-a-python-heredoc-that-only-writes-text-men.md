---
id: T-0128
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-03T04:44:01Z
updated: 2026-10-03T05:21:40Z
base: ef6f34a751db5c6279263b0f624cc7915ce56e46
base_tree: 33b692d3d1efeb28499cb452fb21da83ca28599a
verified: ok
---
# Guard: interpreter check reads only the code the interpreter runs, not the whole shell command
## Raw request
> Guard: a Python heredoc that only writes text mentioning 'claude plugin' is blocked as running it; flag interpreter code only when it executes the command
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a heredoc with backticks beside a shell 'claude plugin test' passes; -c, heredoc and $CODE routes to claude plugin install stay blocked — verify with `python3 plugin/tests/run.py -p test_guard.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, scope _CLAUDE_IN_CODE to interpreter code
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → ✗ exit 1 · Ran 44 tests in 0.2s (15 classes, 16 at a time; slowest: GitDestructive 0s, PluginChanges 0s, Authorization 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 236a2e856744] (2026-10-03T05:20:37Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, InterpreterWrites 0s, Authorization 0s) / OK [ran] [tree 236a2e856744] (2026-10-03T05:20:37Z)
- (ac 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, PipeShell 0s, PluginChanges 0s) / OK [ran] [tree ccad6119c676] (2026-10-03T05:20:49Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → 44 pass incl. piped-code route (2026-10-03T05:20:49Z)
- (ac 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, Publish 0s, Remote 0s) / OK [ran] [tree ccad6119c676] (2026-10-03T05:21:34Z)
- (audit adversary) `self: only the claude-command check is scoped; heredoc, -c, $CODE and piped-code routes to claude plugin install still blocked (tested); write-path and fm-internals checks unchanged` → $-sourced -c and piped stdin fall back to the whole command; a script file was never visible either way [tree ccad6119c676] (2026-10-03T05:21:34Z)
- (audit self) `self: only the claude-command check is scoped; heredoc, -c, $CODE and piped-code routes still blocked (tested)` → write-path and fm-internals checks unchanged [tree ccad6119c676] (2026-10-03T05:21:40Z)
- (audit adversary) `self: only the claude-command check is scoped; heredoc, -c, $CODE and piped-code routes still blocked (tested)` → $-sourced -c and piped stdin fall back to the whole command; a script file was never visible either way [tree ccad6119c676] (2026-10-03T05:21:40Z)
## Log
- 2026-10-03T04:44:01Z created
- 2026-10-03T05:20:18Z planned from capture
- 2026-10-03T05:20:18Z focused
- 2026-10-03T05:21:40Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0016-adversary-r3: hemeral_5m_input_tokens":21309,"ephemeral_1h_input_tokens":0},"output_tokens":5,"service_tier":"standard","inference_geo":"not_available"},"…
- research t0016-adversary-recheck: n## Findings\n\n**CRITICAL — `claude --settings` / `claude --mcp-config` flags entirely unclassified** — `plugin/lib/fmguard.py:656-670…
- research t0018-final-adversary: HIGH** — `plugin/lib/fmguard.py:201-222` (`classify_tree` / `_new_context_file` / `_protected_roots`) — Tree-write commands (`cp -r`, `ta…
- research T-0120-review: Verdict
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
