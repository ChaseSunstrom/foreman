---
id: T-0777
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmbus.py, plugin/monitors/*, plugin/tests/test_bus.py, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T17:49:41Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
base: ad52fc60b0df0183e72f79895c0aa00061451520
base_tree: 6a4cf3c1e06b1db417c6c4d380e21845d0f42f77
verified: strong
---
# Never idle without tmux: a plugin monitor streams this session's Foreman mail, and fm bus --wake prefers it over typing into tmux
## Raw request
> FEATURE: Never idle: a plugin monitor delivers Foreman wakes (bus mail, drive nudges) into the session instead of tmux send-keys
> CONTEXT: T-0760, cluster liveness (40 ideas). fmbus.py:93-102 types into the session's tmux pane (needs tmux; typed text can land in a dialog). Plugin monitors (monitors/monitors.json, CC 2.1.105): [{name, command, description, when}], strict keys, session-long, interactive only, ${CLAUDE_PLUGIN_ROOT}/${CLAUDE_PROJECT_DIR} substituted; each stdout line reaches Claude as a notification. Session id env in monitors is unverified: the command must find its own session another way (e.g. the newest statusline snapshot for the project, or a parent pid).
> DONE-WHEN: plugin/monitors/monitors.json runs an fm command that prints one line per new bus message or wake for this session and nothing otherwise; fm bus --wake prefers it when the session has the monitor; tmux send-keys stays the fallback.
## Interpretation
fm bus wake (fmbus.py:92) types a line into the session's tmux pane: no tmux, no wake, and typed text can land in an open dialog. Claude Code plugins can ship monitors (monitors/monitors.json, 2.1.105): a command that runs for the whole interactive session, each stdout line reaching Claude as a notification that wakes it. fm bus watch prints one line per new message addressed to this session (or all) and nothing else; it writes a heartbeat so senders know the session has a watcher and skip tmux.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm bus watch prints each new message for its session once and ignores others' mail; --wake skips tmux for a session whose watcher heartbeat is fresh — verify with `cd plugin/tests && python3 -m unittest test_bus.Watch`
- [x] the plugin still validates with the monitor declared — verify with `claude plugin validate --strict plugin`
## Non-goals
## Approach (options → choice → why)
Options: SendMessage from the sender (a model tool, not callable from fm); ScheduleWakeup (only under /loop); CronCreate polling (costs a turn per tick); a plugin monitor (zero turns until mail arrives). Chose the monitor; tmux stays the fallback for sessions without it. Session id: CLAUDE_CODE_SESSION_ID when the monitor has it, else the project's newest statusline snapshot.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing bus test for watch and heartbeat-aware wake
2. [x] fm bus watch + heartbeat; wake prefers the watcher
3. [x] plugin/monitors/monitors.json; validate; MASTER.md
## Resume here
<!-- auto -->
- 2026-10-14T17:46:32Z step 1/3: Failing bus test for watch and heartbeat-aware wake
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: .claude/worktrees/agent-a2ea8660a204cb90f/plugin/tests/test_bus.py, .claude/worktrees/agent-a2ea8660a204cb90f/plugin/lib/fmcli.py, .claude/worktrees/agent-a2ea8660a204cb90f/plugin/lib/fmhooks.py, /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/orphan.py, .claude/worktrees/agent-a2ea8660a204cb90f/plugin/lib/fmbus.py, .claude/worktrees/agent-a2ea8660a204cb90f/plugin/monitors/monitors.json, .claude/worktrees/agent-a2ea8660a204cb90f/MASTER.md
- failures met: this agent is isolated in the worktree agent-a0ea0a0cb0f, but this command runs export fo…
## Docs impact
MASTER.md bus section names fm bus watch and the monitor
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_bus.Watch` → ✗ exit 1 · Ran 3 tests in 1.368s / FAILED (failures=1, errors=2) [ran] [tree b05b168b4270] (2026-10-14T17:26:16Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_bus.Watch` → exit 0 · Ran 3 tests in 3.335s / OK [ran] [tree b09ba8aeb335] (2026-10-14T17:28:36Z)
- (step 3) `claude plugin validate --strict plugin` → exit 0 · /plugin install foreman --marketplace <owner>/<repo> / ✔ Validation passed [ran] [tree 81026f90c5f9] (2026-10-14T17:31:49Z)
- (step 1) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 9 tests in 3.7s (5 classes, 16 at a time; slowest: Approvals 4s, Watch 2s, Bus 1s) / OK [ran] [tree 8f752e6c98e7] (2026-10-14T17:47:33Z)
- (step 2) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 9 tests in 3.7s (5 classes, 16 at a time; slowest: Approvals 4s, Watch 2s, Bus 1s) / OK [ran] [tree 8f752e6c98e7] (2026-10-14T17:47:37Z)
- (step 3) `claude plugin validate --strict plugin` → exit 0 · /plugin install foreman --marketplace <owner>/<repo> / ✔ Validation passed [ran] [tree 8f752e6c98e7] (2026-10-14T17:47:37Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (36 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.0    34.6     150  [0] / SessionEnd                  30.5    35.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 8f752e6c98e7] (2026-10-14T17:49:14Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_bus.Watch` → exit 0 · Ran 4 tests in 2.230s / OK [ran] [tree 8f752e6c98e7] (2026-10-14T17:49:40Z)
- (ac 2) `claude plugin validate --strict plugin` → exit 0 · /plugin install foreman --marketplace <owner>/<repo> / ✔ Validation passed [ran] [tree 8f752e6c98e7] (2026-10-14T17:49:40Z)
- (audit intent) `self-review of the merged diff (fmbus watch/record_pid/_by_pid/wake, monitors.json, SessionStart hook); live probe: a process under this session with no session env resolves af0c3568 via state/sessions/by-pid (claude pid 6836); the monitor itself arms only in a new interactive session (plugin monitors aren't started headless or retroactively), so live arming is unverified` → DONE-WHEN met — monitors.json runs fm bus watch printing one line per new message for its session (test_it_prints_each_new_message_for_its_session_once), --wake skips tmux when the heartbeat is <10 s old and falls back to tmux when stale (test_wake_prefers_a_fresh_watcher_over_tmux); drive nudges not built (the Stop hook already continues the session) [tree 8f752e6c98e7] (2026-10-14T17:49:40Z)
- (audit adversary) `self-review of the merged diff (fmbus watch/record_pid/_by_pid/wake, monitors.json, SessionStart hook); live probe: a process under this session with no session env resolves af0c3568 via state/sessions/by-pid (claude pid 6836); the monitor itself arms only in a new interactive session (plugin monitors aren't started headless or retroactively), so live arming is unverified` → mail text reaches the session as a notification exactly as tmux typing did (same local user, no new trust boundary); reused pids are refused by matching /proc start time; a monitor-key typo is caught by test_the_monitor_entry_uses_only_the_keys_claude_code_reads since validate --strict doesn't [tree 8f752e6c98e7] (2026-10-14T17:49:40Z)
- (audit edge) `self-review of the merged diff (fmbus watch/record_pid/_by_pid/wake, monitors.json, SessionStart hook); live probe: a process under this session with no session env resolves af0c3568 via state/sessions/by-pid (claude pid 6836); the monitor itself arms only in a new interactive session (plugin monitors aren't started headless or retroactively), so live arming is unverified` → no session id found → watcher idles without a heartbeat, so senders keep using tmux; watcher removes its heartbeat on exit; parent or claude process gone → it exits [tree 8f752e6c98e7] (2026-10-14T17:49:40Z)
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T16:06:41Z planned from capture
- 2026-10-14T17:24:23Z design (main thread, before the lane): the monitor command is ${CLAUDE_PLUGIN_ROOT}/bin/fm bus watch. Session id: CLAUDE_CODE_SESSION_ID when the monitor's env has it (unverified for plugin monitors); else SessionStart records state/sessions/by-pid/<claude pid> = sid (the hook's parent pid is the claude process) and fm bus watch walks its own parent chain (/proc/<pid>/stat on Linux, ps -o ppid= elsewhere) to the first recorded pid. It polls state/bus/mail.jsonl's size every 2 s (stdlib only), prints one line per new message for its session or 'all' (sender, type, first 160 chars, then 'fm bus read'), never marks mail read (the PreToolUse note does), writes a heartbeat state/bus/watch-<sid> each poll; fm bus --wake skips tmux when that heartbeat is under 10 s old. monitors.json strict keys: name, command, description, when=always.
- 2026-10-14T17:24:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0777.builder.md
- 2026-10-14T17:24:32Z focused
- 2026-10-14T17:27:18Z set scope=['plugin/lib/fmbus.py', 'plugin/monitors/*', 'plugin/tests/test_bus.py', 'MASTER.md', 'plugin/lib/fmcli.py', 'plugin/lib/fmhooks.py']
- 2026-10-14T17:27:18Z scope widened: fmcli.py (bus watch action) and fmhooks.py (SessionStart records by-pid), both named by the main thread's design
- 2026-10-14T17:46:28Z merged worktree-agent-a2ea8660a204cb90f (6 file(s))
- 2026-10-14T17:46:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2ea8660a204cb90f
- 2026-10-14T17:46:29Z focused
- 2026-10-14T17:49:41Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0708 [FEATURE M, done, 5 steps] Frontier 08 — Orchestrator control plane — lesson: Cross-session control fits in the hooks that already run: deliver on the next tool c…
- research brainstorm-20261014: 609 ideas from 11 lenses x 4 rounds + 3 deepen rounds, in 30 capability clusters. Every idea is listed under its cluster. Marks: build (rou…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- decision 2026-10-09: Added JARVIS (<user>@<host>) as a fm conductor remote so the Foreman pane shows its sessions as tiles: the user's own host over their own …
- likely tests for the scope: plugin/tests/test_bus.py
## Preflight
Changed in scope since this was planned (2026-10-14): MASTER.md, plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/monitors/monitors.json, plugin/tests/test_bus.py; re-ground the plan against them before editing
## Lessons
- claude plugin validate --strict does not check monitors.json keys; a unit test has to
## Plan gaps
- failed first: step 1 Failing bus test for watch and heartbeat-aware wake
## Files touched
- plugin/tests/test_bus.py
- plugin/lib/fmbus.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/monitors/monitors.json
- MASTER.md
