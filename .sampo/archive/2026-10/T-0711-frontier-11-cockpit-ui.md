---
id: T-0711
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:27:55Z
updated: 2026-10-09T19:22:44Z
base: 2e7fd5f4623a4cbfd7b1f60814c15ca218df0bf5
base_tree: ea9403a2825b6e4babf33893451bce977e6ac171
verified: strong
---
# Frontier 11 — Cockpit UI
## Raw request
> FEATURE: Frontier 11 — Cockpit UI
> CONTEXT: The user sees, steers and rewinds the plan, beliefs, fleet and probes from one live pane.
> CONTEXT: first slice: Live plan tree and fleet deck pane with steer input fed by the bus.
> CONTEXT: proof at close: Screenshot-verified run through shot.py: steer a node, rewind a moment, see a JARVIS tile update.
> CONTEXT: members (9, frontier catalogue research brainstorm-frontier-20261009; page https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW): Steerable live plan tree; Probe swarm on the hypothesis board; Verified-moment timeline: scrub, diff, fork, bisect; Fleet deck with JARVIS tiles and a steer channel; Subagent tree with in-flight messages; Agent whiteboard: a pane Claude draws on; Hedge radar: the model's own hedges become tracked obligations; Mind view: a cockpit of the agent's live beliefs, which the user can edit, rewind and fork; Claude as navigator while you drive, silent until a test flips
## Interpretation
First slice of Frontier 11: the Foreman pane gains a live plan tree (the active task's child tasks from fm task split, with their progress, under its steps) and a fleet deck (every live session on this machine from the T-0708 bus, plus tiles from remotes the user adds explicitly, such as JARVIS, fetched over their own ssh and cached), with a steer box that sends one steer to all of them (fm conductor steer, which also reaches the remotes). Nothing is fetched from a machine the user didn't add.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ui --json carries the fleet (local live sessions and cached remote tiles) and the active task's children; a remote is fetched only when added — verify with `python3 plugin/tests/run.py -p test_cockpit.py`
- [x] the pane shows a Fleet card with a remote tile and a steer box that runs fm conductor steer, and child tasks under the task card — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Data: (a) the mod shells out to ssh itself — a network call from UI code, and slow; (b) fm ui --json carries a fleet list: local snapshots read directly, remote tiles from a cache that a detached fm conductor refresh renews every 60 s — chosen: the UI never waits on the network, and the remote is an explicit setting (fm conductor remote add NAME TARGET). Steer: the pane's Input posts fm conductor steer; remotes get it with ssh fm bus send all. Plan tree: children listed under the task card's steps. Proof: the mod's own render tests, then a shot.py screenshot of the live pane with a JARVIS tile.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] fleet and children in fm ui; remotes and refresh in fmbus
3. [x] Fleet card, steer box and plan tree in the mod
4. [x] live screenshot, docs, CHANGELOG, full suite
## Resume here
## Docs impact
CHANGELOG; MASTER.md (fm conductor remote)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_cockpit.py` → ✗ exit 1 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: Cockpit 0s) / FAILED (1 classes) [ran] [tree 6b6cc81224b6] (2026-10-09T19:16:07Z)
- (step 2) `python3 plugin/tests/run.py -p test_cockpit.py` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: Cockpit 1s) / OK [ran] [tree 328f78ccfa7f] (2026-10-09T19:18:08Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 66 tests across 1 file. [3.10s] [ran] [tree 328f78ccfa7f] (2026-10-09T19:18:11Z)
- (step 1) `python3 plugin/tests/run.py -p test_cockpit.py` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: Cockpit 1s) / OK [ran] [tree 328f78ccfa7f] (2026-10-09T19:18:12Z)
- (step 4) `python3 plugin/tests/run.py` → exit 0 · Ran 1154 tests in 58.4s (332 classes, 16 at a time; slowest: Stop 36s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree 974365bcdbb9] (2026-10-09T19:19:11Z)
- (ac 1) `python3 plugin/tests/run.py -p test_cockpit.py` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: Cockpit 1s) / OK [ran] [tree 974365bcdbb9] (2026-10-09T19:19:23Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 66 tests across 1 file. [3.10s] [ran] [tree 974365bcdbb9] (2026-10-09T19:19:23Z)
- (audit intent) `self review of the fleet data path, the remotes and the mod's Fleet card; 66 mod tests and the full suite` → the first slice asked for a live plan tree and a fleet deck with a steer input fed by the bus; both shipped with remote tiles from explicitly added machines; the live screenshot with a JARVIS tile follows the next release (JARVIS's 1.2.21 has no fm conductor yet) [tree 974365bcdbb9] (2026-10-09T19:19:23Z)
- (audit adversary) `self review of the fleet data path, the remotes and the mod's Fleet card; 66 mod tests and the full suite` → a remote is fetched only after fm conductor remote add, over the user's own ssh in BatchMode with a 5 s connect timeout, never from the UI process; names and targets are validated before they reach ssh; the steer text is shell-quoted for the remote fm; the pane renders fetched fields as text [tree 974365bcdbb9] (2026-10-09T19:19:23Z)
- (audit edge) `self review of the fleet data path, the remotes and the mod's Fleet card; 66 mod tests and the full suite` → a stale or missing cache starts one detached refresh and the pane shows what it has; a remote that fails shows one warning row, not a crash; a pane with no fleet shows no card [tree 974365bcdbb9] (2026-10-09T19:19:23Z)
## Log
- 2026-10-09T16:27:55Z created
- 2026-10-09T19:15:56Z focused
- 2026-10-09T19:19:24Z done
- 2026-10-09T19:19:24Z committed b67b271 (9 files)
- 2026-10-09T19:22:44Z live proof after 1.2.22: shot.py snapshot of the pane shows Fleet 4 — this session, a volt session, the harness, and a JARVIS tile (jarvis-d7aeca, ctx 39%, 36s ago) — with the steer box (scratchpad/cockpit.png)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- T-0708 [FEATURE M, done, 5 steps] Frontier 08 — Orchestrator control plane — lesson: Cross-session control fits in the hooks that already run: deliver on the next tool c…
- T-0709 [FEATURE M, done, 4 steps] Frontier 09 — Orchestrators of orchestrators — lesson: Partitioning by graph needs the test-to-source links first: without them tests d…
- decision 2026-10-06: Desktop app architecture: no daemon — the Tauri app drives fm --json locally or over ssh (Tailscale SSH) per device; agent sessions are supervised b…
- similar finished tasks took 4–5 steps
## Lessons
- Remote data in a UI belongs behind a cache and a detached refresh, so the render path never waits on the network and an unreachable host costs nothing
## Files touched
- plugin/tests/test_cockpit.py
- plugin/lib/fmwatch.py
- plugin/lib/fmbus.py
- plugin/lib/fmcli.py
- mods/foreman-ui/types/index.d.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
- MASTER.md
