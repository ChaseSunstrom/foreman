---
id: T-1388
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T20:28:26Z
base: 4305d5196ea44035d8280dc2e20b9d05c764bb8f
base_tree: 02a03dac04b9eb4760b7d337038c041e543876ff
plan0_at: 2026-10-21T17:34:28Z
plan0_scope: []
verified: strong
---
# A coding CLI that fm code runs only reads Foreman's state: fm refuses every state-changing command under FOREMAN_WORKER_OF, and a lean claude child whose init lists an MCP server or plugin tool is stopped
## Raw request
> SECURITY: A worker CLI can't change Foreman's grants or state (fm task set --allow, fm ask, state files) from inside a run, and a lean claude child whose init event lists a tool or MCP server outside the lean set is killed (S1, A9)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a fake worker running fm task set T --allow publish and fm ask under FOREMAN_WORKER_OF is refused and the grant absent; a stream-json child whose init lists an unexpected MCP server is stopped with an event naming it
## Interpretation
fm code hands steps to coding CLIs; codex's and gemini's shell commands aren't run through Foreman's guard. A worker (or a prompt-injected one) could run fm task set T --allow publish, fm ask, fm standing or fm autonomy and grant itself what only the user grants. And a lean claude worker should start with no MCP servers or plugin tools; if its init says otherwise the lean launch failed open.
## Assumptions (confidence)
## Acceptance criteria
- [x] with FOREMAN_WORKER_OF set, fm task set --allow publish, fm ask, fm standing, fm autonomy, fm task done and fm vetoes rm are refused and change nothing, while fm state, fm task show and fm lib search still work — verify with `python3 plugin/tests/run.py test_cli`
- [x] a claude worker whose stream's init event lists an MCP server or an mcp__ tool is stopped, with an event naming it, and the step fails — verify with `python3 plugin/tests/run.py test_code_worker`
## Non-goals
## Approach (options → choice → why)
Options: (A) fm itself refuses everything but an allowlist of read-only verbs when FOREMAN_WORKER_OF is set (chosen: one check in fmcli.main covers every shell any worker uses; fm code's own harness calls run without that variable), plus the reader thread reading claude's system/init event and stopping the turn on an MCP server or mcp__ tool; (B) the guard per CLI (codex and gemini don't run Foreman's PreToolUse); (C) a separate OS user (no sandbox here). Ceiling, stated: a worker that unsets the variable gets past (A); the judge and the codex sandbox remain the outer walls.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: grant and state verbs refused under FOREMAN_WORKER_OF, reads allowed; a fake claude whose init lists an MCP server
2. [x] fmcli.main's worker allowlist; the init check on the reader thread with a stop handle; docs
## Resume here
<!-- auto -->
- 2026-10-21T17:39:02Z step 1/2: Failing tests: grant and state verbs refused under FOREMAN_WORKER_OF, reads allowed; a fake claude whose init lists an MCP server
- git: foreman/build; 3 uncommitted: plugin/lib/fmcli.py, plugin/tests/test_cli.py, plugin/tests/test_worker_reads.py
- touched since last checkpoint: plugin/tests/test_worker_reads.py, plugin/lib/fmcli.py
## Docs impact
README lean paragraph; CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_worker_reads` → ✗ exit 1 · Ran 2 tests in 7.7s (1 classes, 16 at a time; slowest: WorkerOnlyReads 7s) / FAILED (1 classes) [ran] [tree 4b03675b9c56] (2026-10-21T17:34:54Z)
- (step 1) `python3 plugin/tests/run.py test_code_worker.Worker.test_a_lean_claude_worker_whose_session_loads_more_than_the_guard_is_stopped` → ✗ exit 1 · Ran 1 tests in 26.3s (1 classes, 16 at a time; slowest: Worker 26s) / FAILED (1 classes) [ran] [tree f96842c8604a] (2026-10-21T20:00:27Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_worker_reads` → exit 0 · Ran 64 tests in 141.0s (2 classes, 16 at a time; slowest: Worker 141s, WorkerOnlyReads 4s) / OK [ran] [tree 091517d4b365] (2026-10-21T20:03:21Z)
- (step 1) `python3 plugin/tests/run.py test_worker_reads` → ✗ exit 1 · Ran 2 tests in 9.7s (1 classes, 16 at a time; slowest: WorkerOnlyReads 9s) / FAILED (1 classes) [ran] [tree 89500ff509a0] (2026-10-21T20:07:07Z)
- (step 2) `python3 plugin/tests/run.py test_worker_reads test_cli` → exit 0 · Ran 108 tests in 75.5s (31 classes, 16 at a time; slowest: TaskLifecycle 75s, StateViews 30s, AuditPrep 27s) / OK [ran] [tree ad2821b97468] (2026-10-21T20:08:47Z)
- (audit adversary) `fm-reviewer` → 3 HIGH/MEDIUM bypasses found and fixed failing-first: task evidence's cmd positional posed as an allowed verb (now a verb default set per top-level command), fm log forged ledger events (removed), write flags on queue/recall/map (recall and map removed, queue --replan refused); init kill confirmed sound (killpg + reap, init precedes the model call, today's real shape passes) [tree ad2821b97468] (2026-10-21T20:09:09Z)
- (step 1) `python3 plugin/tests/run.py test_worker_reads test_code_worker` → exit 0 · Ran 64 tests in 156.1s (2 classes, 16 at a time; slowest: Worker 156s, WorkerOnlyReads 6s) / OK [ran] [tree ad2821b97468] (2026-10-21T20:12:02Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 106 tests in 58.4s (30 classes, 16 at a time; slowest: TaskLifecycle 58s, StateViews 22s, AuditPrep 21s) / OK [ran] [tree ad2821b97468] (2026-10-21T20:15:52Z)
- (ac 2) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 62 tests in 169.0s (1 classes, 16 at a time; slowest: Worker 169s) / OK [ran] [tree ad2821b97468] (2026-10-21T20:15:52Z)
- (audit intent) `fm-reviewer: 4 findings (cmd-clobbering bypass, fm log forgery, write flags on reads, a vacuous read test) fixed failing-first; init kill read as sound; planner init check and fm state's create-on-read captured (T-1426)` → under FOREMAN_WORKER_OF every listed state change, grant, evidence and ledger write is refused with exit 2 and nothing changes; status, state, task show/list, queue, next, lib search, vetoes and gates still work (test_worker_reads); a lean worker whose init lists an MCP server, an mcp__ tool or a non-builtin plugin is stopped before acting and the run blocks naming it (test_code_worker) [tree ad2821b97468] (2026-10-21T20:15:52Z)
- (audit edge) `fm-reviewer: 4 findings (cmd-clobbering bypass, fm log forgery, write flags on reads, a vacuous read test) fixed failing-first; init kill read as sound; planner init check and fm state's create-on-read captured (T-1426)` → today's real lean init shape passes; init need not be the first line; the check runs only when the worker was launched with --strict-mcp-config, so lean = false runs aren't stopped; the variable is advisory (unsetting it bypasses, ponytail note) [tree ad2821b97468] (2026-10-21T20:15:52Z)
- (audit intent) `fm-reviewer: 4 findings (cmd-clobbering bypass, fm log forgery, write flags on reads, a vacuous read test) fixed failing-first; init kill read as sound; planner init check and fm state's create-on-read captured (T-1426)` → under FOREMAN_WORKER_OF every listed state change, grant, evidence and ledger write is refused with exit 2 and nothing changes; status, state, task show/list, queue, next, lib search, vetoes and gates still work (test_worker_reads); a lean worker whose init lists an MCP server, an mcp__ tool or a non-builtin plugin is stopped before acting and the run blocks naming it (test_code_worker) [tree ad2821b97468] (2026-10-21T20:28:17Z)
- (audit edge) `fm-reviewer: 4 findings (cmd-clobbering bypass, fm log forgery, write flags on reads, a vacuous read test) fixed failing-first; init kill read as sound; planner init check and fm state's create-on-read captured (T-1426)` → today's real lean init shape passes; init need not be the first line; the check runs only when the worker was launched with --strict-mcp-config, so lean = false runs aren't stopped; the variable is advisory (unsetting it bypasses, ponytail note) [tree ad2821b97468] (2026-10-21T20:28:17Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T17:34:17Z planned from capture
- 2026-10-21T17:34:26Z focused
- 2026-10-21T17:39:03Z paused: focus moved to T-1378
- 2026-10-21T18:15:52Z user approved plugin in Claude Code's permission prompt
- 2026-10-21T18:30:01Z probe (live, claude lean worker and planner, init line): mcp_servers [], no mcp__ tool, plugins only 3 with path 'builtin' (cc-plugin-agents-md, -telemetry, -plugin-authoring); so stop on: a non-empty mcp_servers, any mcp__ tool, or any plugin whose path isn't builtin
- 2026-10-21T19:58:11Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-21T19:58:11Z focused
- 2026-10-21T20:28:18Z affected tests waived: every Python suite linked to the change passed; the one failure is the UI mod's JS test of subagent rows timing out at 5 s under load ~50, which reads no fm command or fm code path this task touched (
- 2026-10-21T20:28:22Z done
- 2026-10-21T20:28:26Z committed 0b8f3bda (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- research mission-20261021-115148.pack: and integrate all of these too, automatically, super enhanced harness, etc. fully featured/implemented, super recursive wild brain…
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Why not caught
the first test asserted on text the refusal never prints, so a refused read and an allowed write both passed; the reviewer's adversary lens found the gaps
## Lessons
- An allowlist keyed on a parsed field must use a field no subcommand can overwrite: set the verb as a parser default per top-level command
## Plan gaps
- failed first: step 1 Failing tests: grant and state verbs refused under FOREMAN_WORKER_OF, reads allowed; a fake claude …
## Files touched
- plugin/tests/test_worker_reads.py
- plugin/lib/fmcli.py
- plugin/tests/test_code_worker.py
- plugin/lib/fmcode.py
- README.md
- CHANGELOG.md
