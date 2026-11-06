---
id: T-0708
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:27:55Z
updated: 2026-10-09T19:05:53Z
base: 829d7f1075990907c4f7a48c802d85eb72024673
base_tree: 7a6a64c8883304bd3523340e8bed5b574a80899e
verified: strong
---
# Frontier 08 — Orchestrator control plane
## Raw request
> FEATURE: Frontier 08 — Orchestrator control plane
> CONTEXT: One zero-token conductor, bus and lock layer runs every session on every machine.
> CONTEXT: first slice: Typed message bus with wake-on-mail, function-level leases, and a conductor that lists and steers all live sessions.
> CONTEXT: proof at close: Two sessions plus a JARVIS host edit overlapping code: leases prevent collisions, a steer reaches all, a killed child is restarted.
> CONTEXT: members (10, frontier catalogue research brainstorm-frontier-20261009; page https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW): The Conductor: a zero-token control plane that runs Foreman orchestrators on every venue; Session mailbox with wake-on-mail: anything can message a running Claude session, and it wakes; Orchestrator bus: typed messages, most handled by code, wake-on-mail only for judgment; Delegated permissions down the tree: a parent answers its children's prompts and can only grant what it holds; Supervision trees: restart, quarantine and escalate, the Erlang/OTP way, for agents; Steer cascade: one steer, typed anywhere, reaches and binds every node it concerns; Leases: function-level area locks across sessions and machines, enforced before the edit; Overwatch: a resident watcher that keeps every session (local and JARVIS) from idling, looping or thrashing; One conductor, several orchestrator sessions, one milestone; Disciplined agent teams: Claude Code's native teams run Foreman briefs, gated by TeammateIdle and TaskCreated
## Interpretation
First slice of Frontier 08, zero-token and local: a typed message bus between Claude sessions on this machine (fm bus send <session|all> --type steer|note; delivered on the session's next tool call, or when it tries to stop; --wake types one short line into a tmux-hosted session such as JARVIS's), function-level leases (an edit leases the function it lands in for 20 minutes; another session's edit inside that function is refused with who holds it; fm lease list|take|drop), and a conductor (fm conductor: live sessions with project, task, context, mail and leases; fm conductor steer "…" sends a steer to all). Deferred: supervision/restart, cross-machine leases, delegated permissions.
## Assumptions (confidence)
## Acceptance criteria
- [x] a message to one session or all reaches each on its next tool call once, and wakes a session at Stop — verify with `python3 plugin/tests/run.py -p test_bus.py -k Bus`
- [x] an edit leases its function; another session's edit inside it is refused, outside it allowed — verify with `python3 plugin/tests/run.py -p test_bus.py -k Lease`
- [x] fm conductor lists live sessions and its steer reaches them all — verify with `python3 plugin/tests/run.py -p test_bus.py -k Conductor`
## Non-goals
## Approach (options → choice → why)
Bus: (a) Claude Code's own SendMessage between sessions — model-driven, costs turns; (b) files under state/bus with a per-session cursor, delivered by the hooks that already run (PreToolUse note, Stop block) — chosen: zero tokens until a message lands; (c) a socket daemon — a process to supervise. Wake: tmux send-keys of one short line to the pane the statusline recorded (TMUX_PANE), only with --wake. Leases: (a) file-level — blocks too much; (b) enclosing definition by indentation, recomputed at check time from the symbol name so line shifts don't matter — chosen; (c) AST per language — later. Auto-lease in the async PostToolUse after an edit, check in PreToolUse for Edit/Write/MultiEdit. Conductor reads state/sessions snapshots (seen in the last 15 min = live).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] fmbus: messages, cursors, delivery hooks, wake
3. [x] leases: auto-lease, enforcement, fm lease
4. [x] conductor list and steer
5. [x] docs, CHANGELOG, bench and full suite
## Resume here
## Docs impact
CHANGELOG; MASTER.md module list (fmbus); fm help lists bus, lease, conductor
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_bus.py` → ✗ exit 1 · Ran 4 tests in 1.0s (3 classes, 16 at a time; slowest: Bus 1s, Lease 1s, Conductor 1s) / FAILED (3 classes) [ran] [tree 071c4778e56c] (2026-10-09T19:02:13Z)
- (step 2) `python3 plugin/tests/run.py -p test_bus.py -k Bus` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: Bus 1s) / OK [ran] [tree 77706ef57a7c] (2026-10-09T19:04:08Z)
- (step 3) `python3 plugin/tests/run.py -p test_bus.py -k Lease` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Lease 1s) / OK [ran] [tree 77706ef57a7c] (2026-10-09T19:04:09Z)
- (step 4) `python3 plugin/tests/run.py -p test_bus.py -k Conductor` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Conductor 1s) / OK [ran] [tree 77706ef57a7c] (2026-10-09T19:04:09Z)
- (step 1) `python3 plugin/tests/run.py -p test_bus.py` → exit 0 · Ran 4 tests in 1.2s (3 classes, 16 at a time; slowest: Bus 1s, Lease 1s, Conductor 1s) / OK [ran] [tree 77706ef57a7c] (2026-10-09T19:04:11Z)
- (step 5) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (32 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.6    34.3     150  [0] / SessionEnd                  29.9    31.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:01 UTC; python3 plugin/tests/run.py → exit 0 · Ran 1148 tests i [ran] [tree 57b61f2a70ba] (2026-10-09T19:05:43Z)
- (ac 1) `python3 plugin/tests/run.py -p test_bus.py -k Bus` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: Bus 1s) / OK [ran] [tree 57b61f2a70ba] (2026-10-09T19:05:52Z)
- (ac 2) `python3 plugin/tests/run.py -p test_bus.py -k Lease` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Lease 1s) / OK [ran] [tree 57b61f2a70ba] (2026-10-09T19:05:52Z)
- (ac 3) `python3 plugin/tests/run.py -p test_bus.py -k Conductor` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Conductor 1s) / OK [ran] [tree 57b61f2a70ba] (2026-10-09T19:05:52Z)
- (audit intent) `self review of fmbus and its hook wiring; all project gates passed (doctor, e2e roundtrip, hook bench, mod tests, full suite, replay)` → the first slice asked for a typed bus with wake-on-mail, function-level leases and a conductor that lists and steers sessions; all shipped, zero tokens until a message or a collision; supervision/restart and cross-machine leases stay for later slices [tree 57b61f2a70ba] (2026-10-09T19:05:52Z)
- (audit adversary) `self review of fmbus and its hook wiring; all project gates passed (doctor, e2e roundtrip, hook bench, mod tests, full suite, replay)` → messages are redacted and capped, live only in Foreman's state on this machine, and arrive as notes, not commands; --wake types a fixed line, never the message, into a pane id matching %N; a lease can only refuse an edit, never grant one, and only the holder drops it [tree 57b61f2a70ba] (2026-10-09T19:05:52Z)
- (audit edge) `self review of fmbus and its hook wiring; all project gates passed (doctor, e2e roundtrip, hook bench, mod tests, full suite, replay)` → a first read gets only broadcasts from the last 15 min; a session doesn't get its own messages; a lease is recomputed from the symbol name so line shifts don't matter, top-level edits lease nothing, a Write leases the file; the PreToolUse path skips the lease check when no lease file exists (bench gate passed) [tree 57b61f2a70ba] (2026-10-09T19:05:52Z)
## Log
- 2026-10-09T16:27:55Z created
- 2026-10-09T19:00:20Z focused
- 2026-10-09T19:05:52Z done
- 2026-10-09T19:05:53Z committed bd37a4f (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- T-0675 [FEATURE M, done, 6 steps] Milestone: Features — Orchestration, lanes and fleets — lesson: Watch the signal a session can't help emitting (its transcript mtime), …
- T-0707 [FEATURE M, done, 4 steps] Frontier 07 — Knowledge graph — lesson: Retrieval for a new task works best through past tasks: words match titles far better than path…
- decision 2026-09-26: T-0014 supersedes the tmux decision: Type=simple unit running claude remote-control directly (no TTY needed, verified live); fm serve status shows t…
- similar finished tasks took 4–6 steps
## Lessons
- Cross-session control fits in the hooks that already run: deliver on the next tool call, hold at Stop, refuse in PreToolUse; only an idle session needs an outside wake
## Files touched
- plugin/tests/test_bus.py
- plugin/lib/fmbus.py
- plugin/hooks/statusline
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
- .claude-plugin/marketplace.json
- plugin/.claude-plugin/plugin.json
