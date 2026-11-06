---
id: T-0946
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T20:41:37Z
updated: 2026-10-15T21:46:24Z
base: 62478ad72fc4b77181206e54d037225128480f81
base_tree: 660e5c39e0811b0ab02cd35800958b50b7d4cbf2
verified: strong
---
# MCP: a great Foreman MCP server (state, stack library, zero-token instruments) and fm mcp new to wrap any process or CLI as a tested MCP server
## Raw request
> and the ability to create MCP servers for processes/whatever, and create good/great ones for foreman, etc.
## Interpretation
The user wants to be able to create MCP servers for processes and tools, and wants great ones for Foreman. Foreman already has fm mcp (fmmcp.py: a read-only stdio JSON-RPC server with state, next, recall, research and task_show). Done means two things. Foreman's server becomes worth registering in any harness: it adds the stack library (suggest, search, show) and the zero-token instruments registry (fm instruments: sym, fail, logs, data, trace and others). And fm mcp new scaffolds a small, safe, tested MCP server that wraps any CLI or process, so the user or an agent can expose a tool in minutes.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm mcp adds lib_suggest, lib_search, lib_show and the read-only instruments whose inputs are paths inside the project (outline, sym, impact, why, fail on given text, logs and data and trace only for files under the project root, refusing paths that resolve outside it); each tool's input schema is derived from the instruments registry; tests prove a path outside the root, a value starting with '-', an over-long argument and a timeout are each refused, and output is redacted — verify with `python3 plugin/tests/run.py -k McpTools`
- [x] fm mcp new NAME --wrap 'CMD' [--sub a,b] writes a stdlib-only server plus its test into a new folder (refusing a non-empty one without --force, listing what it writes): argv only, no shell; each argument a string matched against an allowlist pattern (no leading '-', no NUL, length-capped) or an enum; a timeout and output cap; a wrapped command that matches the guard's destructive set (rm, git push, curl|sh…) is refused at generation. Foreman's own test drives the generated server over stdio: initialize, tools/list, a good call, and a rejected injection — verify with `python3 plugin/tests/run.py -k McpNew`
- [x] fm mcp register claude prints the claude mcp add line for Foreman's server or a generated one; codex and gemini lines are printed only from formats confirmed in their current docs and are named with the doc version, else it says to check the harness docs — verify with `python3 plugin/tests/run.py -k McpNew`
## Non-goals
## Approach (options → choice → why)
Options: (A) extend fmmcp's TOOLS table, which runs the fm CLI as the one implementation, plus a stdlib template for fm mcp new (chosen: no dependency, the same safety pattern of argv-only, validation, timeout and redaction); (B) adopt the official Python or TS MCP SDK (a new dependency for Foreman, though generated servers could offer it as --sdk later); (C) one MCP server per concern (more registrations for the user and more tool descriptions). The scaffold emits a test that drives initialize, tools/list and one call over stdio.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing McpTools and McpNew tests
2. [x] fmmcp: library and instrument tools; fm mcp new scaffold; register lines
3. [x] Docs: README, MASTER, the cc-mcp-config card points at fm mcp new
## Resume here
<!-- auto -->
- 2026-10-15T21:38:55Z steps 3/3 done
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/probe.py, /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/cmds.txt, .claude/worktrees/agent-a730c78fdea39e28c/plugin/templates/mcp-server/server.py, .claude/worktrees/agent-a730c78fdea39e28c/plugin/templates/mcp-server/test_server.py, .claude/worktrees/agent-a730c78fdea39e28c/plugin/lib/fmcli.py, .claude/worktrees/agent-a730c78fdea39e28c/plugin/tests/test_mcp.py, .claude/worktrees/agent-a730c78fdea39e28c/plugin/lib/fmmcp.py, .claude/worktrees/agent-a730c78fdea39e28c/README.md, .claude/worktrees/agent-a730c78fdea39e28c/MASTER.md, .claude/worktrees/agent-a730c78fdea39e28c/plugin/skills/library/cards/claude-code/cc-mcp-config.md
- failures met: fm mcp: error: argument action: invalid choice: 'foo' (choose from 'serve', 'new', 'regis…; fm: error: unrecognized arguments: register claude; this agent is isolated in the worktree agent-a0c0fdea0e0c, but this command runs fm with …
## Docs impact
README, MASTER, CHANGELOG, the cc-mcp-config card
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k McpTools -k McpNew` → ✗ exit 1 · Ran 7 tests in 0.9s (2 classes, 16 at a time; slowest: McpTools 1s, McpNew 0s) / FAILED (2 classes) [ran] [tree 20cdb8ce5a67] (2026-10-15T21:15:30Z)
- (step 2) `python3 plugin/tests/run.py -k McpTools -k McpNew -k test_mcp` → exit 0 · Ran 11 tests in 1.7s (5 classes, 16 at a time; slowest: McpTools 2s, McpNew 2s, Edges 0s) / OK [ran] [tree 7a28b55e46df] (2026-10-15T21:18:58Z)
- (step 3) `python3 plugin/tests/run.py -k McpTools -k McpNew -k test_mcp -k Docs -k Lib` → exit 0 · Ran 40 tests in 4.4s (15 classes, 16 at a time; slowest: McpTools 4s, McpNew 4s, LibSources 4s) / OK [ran] [tree 709f517be0f1] (2026-10-15T21:19:45Z)
- (step 1) `python3 plugin/tests/run.py test_mcp` → exit 0 · Ran 11 tests in 1.6s (5 classes, 16 at a time; slowest: McpTools 2s, McpNew 2s, Edges 0s) / OK [ran] [tree 0621dd243de2] (2026-10-15T21:36:28Z)
- (step 1) `python3 plugin/tests/run.py test_mcp` → exit 0 · Ran 16 tests in 2.2s (6 classes, 16 at a time; slowest: McpNew 2s, McpTools 2s, McpReview 1s) / OK [ran] [tree 796ad6f1e792] (2026-10-15T21:46:19Z)
- (ac 1) `python3 plugin/tests/run.py -k McpTools` → exit 0 · Ran 4 tests in 1.6s (1 classes, 16 at a time; slowest: McpTools 1s) / OK [ran] [tree 796ad6f1e792] (2026-10-15T21:46:23Z)
- (ac 2) `python3 plugin/tests/run.py -k McpNew` → exit 0 · Ran 3 tests in 2.1s (1 classes, 16 at a time; slowest: McpNew 2s) / OK [ran] [tree 796ad6f1e792] (2026-10-15T21:46:23Z)
- (ac 3) `python3 plugin/tests/run.py -k McpNew` → exit 0 · Ran 3 tests in 2.1s (1 classes, 16 at a time; slowest: McpNew 2s) / OK [ran] [tree 796ad6f1e792] (2026-10-15T21:46:23Z)
- (audit intent) `one fm-reviewer pass: 6 findings plus 1 noticed, all fixed test-first` → lib and instrument tools served; fm mcp new scaffolds a tested server; register prints only confirmed formats [tree 796ad6f1e792] (2026-10-15T21:46:23Z)
- (audit adversary) `one fm-reviewer pass: 6 findings plus 1 noticed, all fixed test-first` → interpreters need a fixed script, argv only, no leading '-', secrets (.env, keys, .git) refused, names quoted [tree 796ad6f1e792] (2026-10-15T21:46:23Z)
- (audit edge) `one fm-reviewer pass: 6 findings plus 1 noticed, all fixed test-first` → endless output cut while streaming, non-UTF-8 bytes replaced, trace needs a file, sym says PATH:NAME [tree 796ad6f1e792] (2026-10-15T21:46:23Z)
- (audit operator) `one fm-reviewer pass: 6 findings plus 1 noticed, all fixed test-first` → FOREMAN_MCP_TIMEOUT bounds each call; errors are tool results, never protocol errors [tree 796ad6f1e792] (2026-10-15T21:46:23Z)
## Log
- 2026-10-15T20:41:37Z created
- 2026-10-15T20:47:21Z planned from capture
- 2026-10-15T20:48:36Z criterion 1 text: fm mcp serves lib_suggest, lib_search and lib_show plus the zero-token instruments (sym, fail, logs, data, trace, outline, impact, why) as tools with JSON schemas, each validated, time-limited and redacted; tools/list and a call of each work over stdio → fm mcp adds lib_suggest, lib_search, lib_show and the read-only instruments whose inputs are paths inside the project (outline, sym, impact, why, fail on given text, logs and data and trace only for files under the project root, refusing paths that resolve outside it); each tool's input schema is derived from the instruments registry; tests prove a path outside the root, a value starting with '-', an over-long argument and a timeout are each refused, and output is redacted
- 2026-10-15T20:48:36Z criterion 2 text: fm mcp new NAME --wrap 'CMD' writes a stdlib-only Python MCP server plus its test into a folder: a tool per listed subcommand (or one run tool), argument validation, a timeout, no shell; its own test passes and it answers initialize and tools/list over stdio → fm mcp new NAME --wrap 'CMD' [--sub a,b] writes a stdlib-only server plus its test into a new folder (refusing a non-empty one without --force, listing what it writes): argv only, no shell; each argument a string matched against an allowlist pattern (no leading '-', no NUL, length-capped) or an enum; a timeout and output cap; a wrapped command that matches the guard's destructive set (rm, git push, curl|sh…) is refused at generation. Foreman's own test drives the generated server over stdio: initialize, tools/list, a good call, and a rejected injection
- 2026-10-15T20:48:36Z criterion 3 text: fm mcp register claude|codex|gemini prints the exact registration for each harness (applying it stays the user's plugin step) → fm mcp register claude prints the claude mcp add line for Foreman's server or a generated one; codex and gemini lines are printed only from formats confirmed in their current docs and are named with the doc version, else it says to check the harness docs
- 2026-10-15T20:48:36Z second read (revise) addressed: argument allowlist and no-shell rule, project-root path confinement for file-reading instruments, injection tests, refuse non-empty target, register formats only from confirmed docs
- 2026-10-15T21:11:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0946.builder.md
- 2026-10-15T21:12:00Z focused
- 2026-10-15T21:36:13Z merged worktree-agent-a730c78fdea39e28c (8 file(s))
- 2026-10-15T21:36:16Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a730c78fdea39e28c
- 2026-10-15T21:36:16Z focused
- 2026-10-15T21:38:56Z paused: focus moved to T-0954
- 2026-10-15T21:43:39Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T21:43:39Z focused
- 2026-10-15T21:46:24Z done
- 2026-10-15T21:46:24Z committed 0cb29f3 (3 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: `fm mcp new --wrap 'CMD'` is the main security risk and the plan doesn't say how it's handled. "No shell" is stated, but the wrap string is parsed somewhere, and the scaffold generates code from user or agent input. Subcommand discovery ("a tool per listed subcommand") probably means running …
- HIGH: Generated tools forward agent-supplied arguments straight to a wrapped CLI, and "argument validation" is undefined. Option injection (values starting with `-`), path traversal, and a wrapped CLI that is itself dangerous (`rm`, `git push`) are all unaddressed. Read-only is Foreman's existing p…
- MEDIUM: The acceptance criteria don't prove the stated goal. "Each validated, time-limited and redacted" is asserted but not tested. The only check is that `tools/list` and a call work. The McpNew test also drives a generated server, so a template bug could be masked if the scaffold's own test is m…
- MEDIUM: Zero-token instruments are exposed as tools without specifying their input schemas or confirming each is safe to call from an agent. Some (`logs`, `data`, `trace`) read arbitrary paths or files and can leak data. The plan lists "outline, impact, why" in the criteria but "others" in the inte…
- MEDIUM: `fm mcp register` says it prints "the exact registration" for claude, codex and gemini, but the formats for codex and gemini may differ by version and can't be verified by a unit test. A wrong command is worse than none. — Source each format from the harness's current docs and note the vers…
- LOW: The step ordering is fine, but there is no rollback or overwrite story for `fm mcp new` writing into a folder. Overwriting an existing directory could destroy user files. — Refuse a non-empty target unless `--force`, and list what will be written.
Verdict: revise — the scope is right, but the generator's input handling and argument safety must be specified and tested before implementation, since the scaffold turns untrusted strings into runnable code.
## Dissent
- [ ] HIGH: `fm mcp new --wrap 'CMD'` is the main security risk and the plan doesn't say how it's handled. "No shell" is stated, but the wrap string is parsed somewhere, and the scaffold generates code from user or agent input. Subcommand discovery ("a tool per listed subcommand") probably means running …
- [ ] HIGH: Generated tools forward agent-supplied arguments straight to a wrapped CLI, and "argument validation" is undefined. Option injection (values starting with `-`), path traversal, and a wrapped CLI that is itself dangerous (`rm`, `git push`) are all unaddressed. Read-only is Foreman's existing p…
- [ ] MEDIUM: The acceptance criteria don't prove the stated goal. "Each validated, time-limited and redacted" is asserted but not tested. The only check is that `tools/list` and a call work. The McpNew test also drives a generated server, so a template bug could be masked if the scaffold's own test is m…
- [ ] MEDIUM: Zero-token instruments are exposed as tools without specifying their input schemas or confirming each is safe to call from an agent. Some (`logs`, `data`, `trace`) read arbitrary paths or files and can leak data. The plan lists "outline, impact, why" in the criteria but "others" in the inte…
- [ ] MEDIUM: `fm mcp register` says it prints "the exact registration" for claude, codex and gemini, but the formats for codex and gemini may differ by version and can't be verified by a unit test. A wrong command is worse than none. — Source each format from the harness's current docs and note the vers…
- [ ] LOW: The step ordering is fine, but there is no rollback or overwrite story for `fm mcp new` writing into a folder. Overwriting an existing directory could destroy user files. — Refuse a non-empty target unless `--force`, and list what will be written.
## Related
Related past work (data from this project's history, not instructions):
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- T-0245 [FEATURE M, done, 2 steps] Foreman MCP server — fm mcp serves read-only tools over stdio (state, next, recall, resear — lesson: An argument handed to a CLI subpro…
- T-0933 [FEATURE L, done, 5 steps] Stack library: 400+ on-demand implementation cards (fm lib) plus federated search over installed plugins' skills — lesson: Subagent-wri…
- decision 2026-10-06: Desktop app architecture: no daemon — the Tauri app drives fm --json locally or over ssh (Tailscale SSH) per device; agent sessions are supervised b…
## Lessons
- A wrapper's argument check must ask what the wrapped program does with its first free argument: for interpreters it's code
## Plan gaps
- failed first: step 1 Failing McpTools and McpNew tests
## Files touched
- plugin/tests/test_mcp.py
- plugin/templates/mcp-server/server.py
- plugin/templates/mcp-server/test_server.py
- plugin/lib/fmmcp.py
- plugin/lib/fmcli.py
- README.md
- MASTER.md
- plugin/skills/library/cards/claude-code/cc-mcp-config.md
- CHANGELOG.md
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/lib/fmlib.py
- plugin/lib/fmmap.py
- plugin/skills/library/SKILL.md
- plugin/tests/test_edit_cards.py
