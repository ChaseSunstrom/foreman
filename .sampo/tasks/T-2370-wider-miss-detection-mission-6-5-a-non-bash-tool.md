---
id: T-2370
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, MASTER.md, CHANGELOG.md]
depends_on: [T-2369]
source: self
created: 2026-10-31T14:01:59Z
updated: 2026-10-31T15:46:56Z
builder_model: sonnet
base: feaac80630dc468bc4593f94ed206140f9e23153
base_tree: f8aae18301d1ec7b66c66418cdc3e79a78446377
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T15:00:00Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Wider miss detection (Mission 6, #5): a non-Bash tool failure on an unsupported file type or an unknown tool, and a guard refusal of an install, feed the same capability-miss path
## Raw request
> Wider miss detection (Mission 6, #5): a non-Bash tool failure on an unsupported file type or an unknown tool, and a guard refusal of an install, feed the same capability-miss path
## Interpretation
T-2270 reads three Bash error shapes only. The ledger holds 0 capability_miss events since it merged, and the project's 494-line failures log has 5 missing-command failures in its whole history (rsync 3, javac, bc), so most misses never reach the trigger: a Read of a format the host can't parse, a call to a tool or MCP server that isn't there, an install the guard refuses because the session wanted a tool it lacks.
## Assumptions (confidence)
## Acceptance criteria
- [x] a Read failure on an unsupported file type names fm which <extension> once per session; a call to an unknown tool or MCP server names fm which NAME; a guard refusal of a plugin or install target logs capability_miss with that target; a 'command not found' in an fm task evidence run logs it too, with no hook involved; odd names are ignored and subagent failures stay out — verify with `python3 plugin/tests/run.py test_hooks test_tool_loop`
## Non-goals
## Approach (options → choice → why)
1) Extend post_tool_use_failure past Bash for a fixed set of error shapes (an unsupported or binary file type, with its extension; an unknown tool or MCP server name); have the PreToolUse guard refusal of a plugin target (and of an install target once the guard has that category) call the same _capability_miss with the target; and scan the output of fm task evidence's own runs for the miss shapes, which fm captures on every host, so a host with no post-tool failure event still feeds the same path. Names stay [A-Za-z0-9_.+-]{1,64} or are ignored; subagent failures stay out (T-1110). 2) Mine the final reply at Stop for 'I can't' prose: not now, prose regexes raise false alarms (precision over volume); captured to the inbox with its kill-it-fast test. 3) Leave detection at Bash: rejected, its live count is 0. Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests first in test_hooks for the three sources, the name filter and the subagent rule
2. [x] fmhooks: non-Bash failure shapes and the guard-refusal call into _capability_miss
3. [x] docs: MASTER.md hooks line, CHANGELOG.md
## Resume here
## Docs impact
## Verification evidence
- (step 3) `python3 plugin/tests/run.py test_hooks.CapabilityMiss test_tool_loop 2>&1 | tail -8` → exit 0 · Ran 27 tests in 42.9s (2 classes, 16 at a time; slowest: MissLoop 42s, CapabilityMiss 6s) / OK [ran] [tree ceee4cbe18b6] (2026-10-31T15:06:54Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.CapabilityMiss test_tool_loop` → exit 0 · Ran 27 tests in 39.5s (2 classes, 16 at a time; slowest: MissLoop 39s, CapabilityMiss 6s) / OK [ran] [tree ceee4cbe18b6] (2026-10-31T15:07:39Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_board_verbs test_cli test_compact test_core test_docs test_drive_side test_guard_cases test_guard_evasions test_hooks test_memory test_onwrite test_paused test_robustness test_tool_loop test_tool_taint test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [22.19s] [ran] [tree ceee4cbe18b6] (2026-10-31T15:09:18Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_tool_loop` → exit 0 · Ran 253 tests in 59.7s (31 classes, 16 at a time; slowest: Stop 59s, MissLoop 41s, NoTaskGate 38s) / OK [ran] [tree 946e74a948f7] (2026-10-31T15:31:03Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_tool_loop` → exit 0 · Ran 253 tests in 61.3s (31 classes, 16 at a time; slowest: Stop 61s, MissLoop 42s, NoTaskGate 38s) / OK [ran] [tree b06efae68646] (2026-10-31T15:32:14Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_tool_loop` → exit 0 · Ran 253 tests in 61.3s (31 classes, 16 at a time; slowest: Stop 61s, MissLoop 42s, NoTaskGate 38s) / OK [ran] [tree b06efae68646] (2026-10-31T15:32:14Z)
- (audit edge) `self-review of the merged lane: four new miss sources (Read of an unsupported type, unknown tool or MCP server, a plugin guard refusal, a failed evidence run with a miss shape) feed _capability_miss; names filtered to [A-Za-z0-9_.+-]{1,64}; the three non-command kinds are logged without a task (nothing could resolve them, so they never trap a finish); regexes run on the last 4000 chars and the ledger tail is read only after a match; 253 tests OK after merge` → the Read and unknown-tool strings are the builder's best guess at Claude Code's wording; if the host words them differently the miss silently won't fire (noted as the weakest link) [tree b06efae68646] (2026-10-31T15:32:14Z)
- (audit adversary) `self-review of the merged lane: four new miss sources (Read of an unsupported type, unknown tool or MCP server, a plugin guard refusal, a failed evidence run with a miss shape) feed _capability_miss; names filtered to [A-Za-z0-9_.+-]{1,64}; the three non-command kinds are logged without a task (nothing could resolve them, so they never trap a finish); regexes run on the last 4000 chars and the ledger tail is read only after a match; 253 tests OK after merge` → miss names are filtered and untrusted text never enters a brief unfiltered; a subagent's failure stays out [tree b06efae68646] (2026-10-31T15:32:14Z)
- (audit self) `self-review of the merged lane: four new miss sources (Read of an unsupported type, unknown tool or MCP server, a plugin guard refusal, a failed evidence run with a miss shape) feed _capability_miss; names filtered to [A-Za-z0-9_.+-]{1,64}; the three non-command kinds are logged without a task (nothing could resolve them, so they never trap a finish); regexes run on the last 4000 chars and the ledger tail is read only after a match; 253 tests OK after merge` → no findings [tree b06efae68646] (2026-10-31T15:32:14Z)
## Log
- 2026-10-31T14:01:59Z created
- 2026-10-31T14:59:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2370.builder.md
- 2026-10-31T14:59:59Z focused
- 2026-10-31T15:00:00Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T15:30:00Z merged worktree-agent-adf55aab92c91d5a8 (5 file(s))
- 2026-10-31T15:30:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-adf55aab92c91d5a8
- 2026-10-31T15:30:01Z focused
- 2026-10-31T15:31:12Z scope: plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/tests/test_hooks.py, plugin/tests/test_tool_loop.py, MASTER.md, CHANGELOG.md
- 2026-10-31T15:34:12Z done
- 2026-10-31T15:34:19Z committed ee84c15b (1 file)
- 2026-10-31T15:35:10Z guard authorization added: publish
- 2026-10-31T15:46:56Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2369-review: Verdict: changes needed.** The core loop works: log the miss, lead in `fm next`, refuse finish and done, resolve by run evidence. But the module-…
- research T-1849-review: Verdict:** approve with nits. I found no defects in the feature itself. The data sources, validation, name handling and layout all hold up. I did…
- research mission-20261031-083834: Request: Mission 6, Genesis gen 1: 5. Getting the tools it lacks. When it hits something it can't do, it finds an existing plugin, skil…
- decision 2026-10-30: [revisited: every capability genesis builds must be called] [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: python3…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, plugin/lib/fmhooks.py, plugin/tests/test_hooks.py; re-ground the plan against them before editing
## Lessons
- A signal that nothing can resolve must not gate a close
## Files touched
- plugin/tests/test_hooks.py
- plugin/tests/test_tool_loop.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
