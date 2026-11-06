---
id: T-1472
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmplugins.py, plugin/tests/test_cloned_config.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T16:05:23Z
updated: 2026-10-22T17:04:51Z
base: cbaf787838aba5c1f0faeb1c20a124a5e6313566
base_tree: 56f841d412054945f7901ed9e836b8ed3defe665
plan0_at: 2026-10-22T16:37:10Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/lib/fmplugins.py, plugin/tests/test_cloned_config.py, CHANGELOG.md]
verified: strong
---
# A repo's own Claude config is named on its first Foreman session
## Raw request
> Cloned-repo config note: on a project's first Foreman session (SessionStart, keyed by a hash of the files) list what the repo's committed .claude/settings.json, .claude/settings.local.json and root .mcp.json would run (hook commands, MCP servers, allow rules) as one note, again when the hash changes; read bounded (size cap, no symlink out of the repo, malformed JSON named). Claude Code may already have run them when the session starts, so the note informs and records; it can't prevent (split from T-1263 after its plan review).
## Interpretation
A freshly cloned repo can commit .claude/settings.json hooks, MCP servers (.mcp.json) and allow rules; Claude Code runs them when it opens the repo, and Foreman never shows the user what they are.
## Assumptions (confidence)
## Acceptance criteria
- [x] a repo with committed hooks and an MCP server gets one SessionStart note naming them, not again until the files change — verify with `cd plugin/tests && python3 -m unittest test_cloned_config.ClonedConfig.test_named_once_per_content`
- [x] a symlink out of the repo, an oversized file and malformed JSON are named, never read — verify with `cd plugin/tests && python3 -m unittest test_cloned_config.ClonedConfig.test_hostile_files_are_named_not_read`
## Non-goals
## Approach (options → choice → why)
Options: (1) refuse to start a session in a repo with committed hooks — Foreman can't: Claude Code loads them first; (2) a doctor check — the user rarely runs it on a fresh clone; (3) chosen: the SessionStart hook, once per project per content hash of the repo's committed .claude/settings.json, .claude/settings.local.json and root .mcp.json, injects one short note listing each hook event and command, each MCP server and its command, and broad allow rules (Bash(*), mcp__*), and records the hash in the project meta so it shows again only when the files change. Reads are bounded: regular files only, at most 256 KB each, a symlink resolving outside the repo is named not read, malformed JSON is named. The note says plainly that Claude Code may already have started these. Reuse fmplugins' hook/MCP spec readers where they fit (capabilities, _handlers) rather than a second parser.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] bounded reader reusing fmplugins' spec readers
3. [x] SessionStart note keyed by content hash
## Resume here
<!-- auto -->
- 2026-10-22T16:48:34Z steps 3/3 done
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmplugins.py, plugin/tests/test_cloned_config.py
- touched since last checkpoint: .claude/worktrees/agent-a51e563c74f13fa7a/plugin/lib/fmhooks.py, .claude/worktrees/agent-a51e563c74f13fa7a/plugin/lib/fmplugins.py, .claude/worktrees/agent-a51e563c74f13fa7a/plugin/tests/test_cloned_config.py, plugin/lib/fmplugins.py, plugin/tests/test_cloned_config.py, CHANGELOG.md
## Docs impact
CHANGELOG line (it landed with T-1468's commit and was then reworded here)
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_cloned_config.py` → ✗ exit 1 · Ran 3 tests in 2.343s / FAILED (failures=3) [ran] [tree bcf672e1ac80] (2026-10-22T16:38:36Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_cloned_config.py` → exit 0 · Ran 3 tests in 2.919s / OK [ran] [tree 89910a21d876] (2026-10-22T16:39:25Z)
- (step 3) `python3 -m unittest plugin/tests/test_cloned_config.py plugin/tests/test_plugins.py plugin/tests/test_hooks.py` → ✗ exit 1 (never ran: the test module test_cloned_config couldn't import) · Ran 3 tests in 0.000s / FAILED (errors=3) [ran] [tree 89910a21d876] (2026-10-22T16:39:26Z)
- (step 3) `python3 plugin/tests/run.py -p test_cloned_config.py -p test_plugins.py -p test_hooks.py` → exit 0 · Ran 215 tests in 165.6s (25 classes, 16 at a time; slowest: Stop 165s, NoTaskGate 106s, PreToolUse 94s) / OK [ran] [tree 89910a21d876] (2026-10-22T16:42:21Z)
- (step 3) `python3 -m unittest discover -s plugin/tests -p test_cloned_config.py` → exit 0 · Ran 3 tests in 2.500s / OK [ran] [tree 3e94abf65a0c] (2026-10-22T16:42:40Z)
- `python3 -m unittest discover -s plugin/tests -p test_cloned_config.py` → ✗ exit 1 · Ran 3 tests in 1.058s / FAILED (failures=3) (start tree + this task's tests) [ran] [tree e54610df89a0] (2026-10-22T16:46:41Z)
- `python3 -m unittest discover -s plugin/tests -p test_cloned_config.py` → exit 0 · Ran 3 tests in 1.504s / OK [ran] [tree e54610df89a0] (2026-10-22T16:46:41Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cloned_config.ClonedConfig.test_named_once_per_content` → exit 0 · Ran 1 test in 0.732s / OK [ran] [tree e54610df89a0] (2026-10-22T16:46:46Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_cloned_config.ClonedConfig.test_hostile_files_are_named_not_read` → exit 0 · Ran 1 test in 0.508s / OK [ran] [tree e54610df89a0] (2026-10-22T16:46:47Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_cloned_config` → exit 0 · Ran 3 tests in 3.050s / OK [ran] [tree a804bf973234] (2026-10-22T16:47:19Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cloned_config.ClonedConfig.test_named_once_per_content` → exit 0 · Ran 1 test in 1.214s / OK [ran] [tree a804bf973234] (2026-10-22T16:47:21Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cloned_config.ClonedConfig.test_named_once_per_content` → exit 0 · Ran 1 test in 0.885s / OK [ran] [tree d9b770d27676] (2026-10-22T16:56:33Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_cloned_config.ClonedConfig.test_hostile_files_are_named_not_read` → exit 0 · Ran 1 test in 0.468s / OK [ran] [tree d9b770d27676] (2026-10-22T16:56:35Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_cloned_config` → exit 0 · Ran 7 tests in 3.553s / OK [ran] [tree d9b770d27676] (2026-10-22T16:56:39Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_cloned_config` → exit 0 · Ran 7 tests in 3.589s / OK [ran] [tree d9b770d27676] (2026-10-22T16:56:44Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_cloned_config` → exit 0 · Ran 7 tests in 3.674s / OK [ran] [tree d9b770d27676] (2026-10-22T16:56:48Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cloned_config.ClonedConfig.test_named_once_per_content` → exit 0 · Ran 1 test in 0.967s / OK [ran] [tree d9b770d27676] (2026-10-22T16:57:04Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_cloned_config.ClonedConfig.test_hostile_files_are_named_not_read` → exit 0 · Ran 1 test in 0.473s / OK [ran] [tree d9b770d27676] (2026-10-22T16:57:04Z)
- (audit intent) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → shown to the user and the model, once per content hash, not consumed by a headless run [tree d9b770d27676] (2026-10-22T16:57:04Z)
- (audit adversary) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → never-read and malformed warnings lead the note, so padding can't cut them; env values never shown; every item redacted, defanged, cut to 90 [tree d9b770d27676] (2026-10-22T16:57:04Z)
- (audit edge) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → a .claude folder linked out of the repo is named not read; deleted then restored files are named again; digest saved before delivery (a later SessionStart crash loses one note) accepted [tree d9b770d27676] (2026-10-22T16:57:04Z)
- (audit operator) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → CHANGELOG line describes the note [tree d9b770d27676] (2026-10-22T16:57:04Z)
- (audit maintainer) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → _spec_file reused with a cap and a malformed list; existing callers unchanged [tree d9b770d27676] (2026-10-22T16:57:04Z)
- (audit intent) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → shown to the user and the model, once per content hash, not consumed by a headless run [tree 716b5b6ab56e] (2026-10-22T16:59:10Z)
- (audit adversary) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → never-read and malformed warnings lead the note, so padding can't cut them; env values never shown; every item redacted, defanged, cut to 90 [tree 716b5b6ab56e] (2026-10-22T16:59:10Z)
- (audit edge) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → a .claude folder linked out of the repo is named not read; deleted then restored files are named again; digest saved before delivery (a later SessionStart crash loses one note) accepted [tree 716b5b6ab56e] (2026-10-22T16:59:10Z)
- (audit operator) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → CHANGELOG line describes the note [tree 716b5b6ab56e] (2026-10-22T16:59:10Z)
- (audit maintainer) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → _spec_file reused with a cap and a malformed list; existing callers unchanged [tree 716b5b6ab56e] (2026-10-22T16:59:10Z)
- (audit intent) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → shown to the user and the model, once per content hash, not consumed by a headless run [tree eb1b93ad9907] (2026-10-22T17:01:02Z)
- (audit adversary) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → never-read and malformed warnings lead the note, so padding can't cut them; env values never shown; every item redacted, defanged, cut to 90 [tree eb1b93ad9907] (2026-10-22T17:01:02Z)
- (audit edge) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → a .claude folder linked out of the repo is named not read; deleted then restored files are named again; digest saved before delivery (a later SessionStart crash loses one note) accepted [tree eb1b93ad9907] (2026-10-22T17:01:02Z)
- (audit operator) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → CHANGELOG line describes the note [tree eb1b93ad9907] (2026-10-22T17:01:02Z)
- (audit maintainer) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → _spec_file reused with a cap and a malformed list; existing callers unchanged [tree eb1b93ad9907] (2026-10-22T17:01:02Z)
- (audit intent) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → shown to the user and the model, once per content hash, not consumed by a headless run [tree eb1b93ad9907] (2026-10-22T17:02:57Z)
- (audit adversary) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → never-read and malformed warnings lead the note, so padding can't cut them; env values never shown; every item redacted, defanged, cut to 90 [tree eb1b93ad9907] (2026-10-22T17:02:57Z)
- (audit edge) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → a .claude folder linked out of the repo is named not read; deleted then restored files are named again; digest saved before delivery (a later SessionStart crash loses one note) accepted [tree eb1b93ad9907] (2026-10-22T17:02:57Z)
- (audit operator) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → CHANGELOG line describes the note [tree eb1b93ad9907] (2026-10-22T17:02:57Z)
- (audit maintainer) `builder (high) test-first; red proved with fm task prove; one fm-reviewer pass (5 lenses) found 5 issues, all fixed test-first: the user sees the note (systemMessage), headless runs leave it, warnings and settings commands come before hooks, env/plugin/marketplace names; delete-then-restore and a linked .claude folder tested; affected tests 373 OK` → _spec_file reused with a cap and a malformed list; existing callers unchanged [tree eb1b93ad9907] (2026-10-22T17:02:57Z)
## Log
- 2026-10-22T16:05:23Z created
- 2026-10-22T16:05:54Z planned from capture
- 2026-10-22T16:36:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1472.builder.md
- 2026-10-22T16:37:09Z focused
- 2026-10-22T16:46:29Z merged worktree-agent-a51e563c74f13fa7a (3 file(s))
- 2026-10-22T16:46:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a51e563c74f13fa7a
- 2026-10-22T16:46:33Z focused
- 2026-10-22T16:47:02Z steer: review noticed apiKeyHelper/awsAuthRefresh/awsCredentialExport/otelHeadersHelper are commands too and enableAllProjectMcpServers starts every .mcp.json server; named in the same note
- 2026-10-22T16:48:36Z paused: focus moved to T-1468
- 2026-10-22T16:53:05Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-22T16:53:05Z focused
- 2026-10-22T16:53:16Z steer: review: show the note to the user (systemMessage) too, skip it in headless runs, put not-read/malformed and settings-level commands before hook events, name env/plugin/marketplace keys; delete-then-restore and other command keys tested
- 2026-10-22T17:02:56Z scope: fmcodetui.py and test_code_tui.py were T-1468's edits, made and committed (6abed44d) while T-1472 was checkpointed; none are T-1472's
- 2026-10-22T17:04:48Z done
- 2026-10-22T17:04:51Z committed b912b1f2 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1392-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: changes needed.** The FAIL only fires for a narrow set of u…
- T-1263 [SECURITY M, active, 3 steps] Guard evasion corpus for the 24 dangerous commands, and an audit of a cloned repo's .claude config
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- likely tests for the scope: plugin/tests/test_hooks.py, plugin/tests/test_plugins.py
## Why not caught
new capability; the first review caught the delivery channel
## Lessons
- A note meant for the user goes in systemMessage as well as additionalContext; a once-only note must not be consumed by a headless session.
## Plan gaps
- failed first: step 1 failing tests
- failed first: step 3 SessionStart note keyed by content hash
## Files touched
- plugin/tests/test_cloned_config.py
- plugin/lib/fmplugins.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- plugin/lib/fmcodetui.py
- plugin/tests/test_code_tui.py
