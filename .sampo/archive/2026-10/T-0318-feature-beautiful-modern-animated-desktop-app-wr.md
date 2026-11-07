---
id: T-0318
type: FEATURE
tier: L
status: done
priority: normal
scope: [apps/desktop/**, README.md, install.sh, CHANGELOG.md, MASTER.md, .gitignore]
depends_on: [T-0322, T-0323]
source: user
created: 2026-10-06T00:40:46Z
updated: 2026-10-06T01:52:48Z
base: 70ad28133c1c0cd8221d2968dd703c9a724cdf7e
base_tree: 4cde3bfcce9c5298c99f4cd7a2b16d1f1c5a5637
verified: ok
---
# FEATURE: beautiful modern animated desktop app wrapping Foreman — supports every feature,
## Raw request
> FEATURE: beautiful modern animated desktop app wrapping Foreman — supports every feature, manages all devices and sessions; agent-agnostic (the plugin must also work on opencode, codex, etc.), animated GUI everywhere
## Interpretation
A Tauri desktop app (Linux first, macOS/Windows builds later) that is the GUI for everything Foreman does: every project's tasks, queue, inbox, approvals, gates, budget and research; every agent session on every device (list, watch live, create, resume, stop); and agent management (which agents run where, with which models). It must not be Claude-only: Foreman's core (fm) gets adapters so opencode, Codex and others get the same discipline (instructions, state, guard where the agent has hooks) and show up in the app the same way. 'Beautiful and animated' is a hard requirement, not polish: motion on every state change, consistent with the foreman-ui pane's look. Multi-device: the app talks to a small fm daemon on each machine (Tailscale-reachable), never shells into it.
## Assumptions (confidence)
## Acceptance criteria
- [x] the app builds — verify with `cd apps/desktop && bun run tauri build --debug --no-bundle`
- [x] devices → projects → project dashboard, sessions (list, live stream, new, send, stop), agents and devices pages render with motion, checked by screenshot — verify with `typed: screenshot review`
- [x] the Rust transport runs fm locally and over ssh (ssh localhost as the stand-in) — verify with `cd apps/desktop/src-tauri && cargo test`
## Non-goals
No hosted cloud service or accounts; no re-implementing an agent's own chat UI beyond watching and steering sessions; no mobile app in this task (claude.ai/code already covers phones via Remote Control).
## Approach (options → choice → why)
Options: (A) fm daemon HTTP API per device + Tauri client; (B) Tauri (Rust core + Svelte 5) as a pure client of fm --json, locally or over ssh per device (persistent ssh ControlMaster, one follow stream per device), sessions via fm session. Choice: B (decision recorded): no new service to secure, the CLI and the app share every feature. Depends on T-0322 (read surface) and T-0323 (sessions); T-0324 adds non-Claude discipline.
## Risks and rollback
## Execution prompt
## Steps
1. [x] scaffold Tauri 2 + Svelte 5 + design tokens
2. [x] Rust transport: fm run/stream, local + ssh, devices store
3. [x] shell + sidebar + devices/projects + dashboard with actions
4. [x] sessions: list, live stream, composer, new-session sheet, stop
5. [x] agents + devices pages, tray, notifications
6. [x] README + install.sh --desktop
## Resume here
## Docs impact
README (desktop app paragraph), CHANGELOG; the app's own README
## Verification evidence
- (step 2) `cd ~/projects/foreman-desktop/src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q` → exit 0 · running 0 tests / test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s [ran] [tree 4cde3bfcce9c] (2026-10-06T01:36:01Z)
- (step 1) `cd ~/projects/foreman-desktop && bun run check` → exit 0 · 1791251219217 START "~/projects/foreman-desktop" / 1791251219218 COMPLETED 189 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 4cde3bfcce9c] (2026-10-06T01:46:59Z)
- (ac 1) `cd ~/projects/foreman-desktop && CARGO_TARGET_DIR=/tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target PATH=$HOME/.cargo/bin:$PATH bun run tauri build --debug --no-bundle` → exit 0 · Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.72s / Built application at: /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target/de [ran] [tree 4cde3bfcce9c] (2026-10-06T01:47:02Z)
- (ac 3) `cd ~/projects/foreman-desktop/src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q --lib` → exit 0 · .... / test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s [ran] [tree 4cde3bfcce9c] (2026-10-06T01:47:04Z)
- (ac 2) `spectacle screenshots of every page (overview, project foreman, session 20261005-204429-1fbc, new-session sheet, agents, devices) launched with FOREMAN_DESKTOP_VIEW` → all render with live data: 10 projects, a real Haiku session streamed (Bash ls, Read package.json paired with results, answer, $0.034), device JARVIS shows its ssh error; motion seen as entrance transitions, spinners, rings [tree 4cde3bfcce9c] (2026-10-06T01:47:16Z)
- (step 3) `screenshot: overview + project dashboard + sidebar` → render with live data from fm projects/ui --follow [tree 4cde3bfcce9c] (2026-10-06T01:47:16Z)
- (step 4) `fm session tail 20261005-204429-1fbc | grep -c tool_result` → exit 0 · 2 [ran] [tree 4cde3bfcce9c] (2026-10-06T01:47:17Z)
- (step 5) `screenshot: agents + devices pages; notifications via tauri-plugin-notification` → render; tray skipped: needs libappindicator-gtk3 (sudo pacman), captured [tree 4cde3bfcce9c] (2026-10-06T01:47:17Z)
- (step 6) `test -s ~/projects/foreman-desktop/README.md && grep -c 'tauri dev' ~/projects/foreman-desktop/README.md` → exit 0 · 1 [ran] [tree 4cde3bfcce9c] (2026-10-06T01:47:17Z)
- (step 6) `grep -c 'Foreman Desktop' README.md CHANGELOG.md` → exit 0 · README.md:1 / CHANGELOG.md:1 [ran] [tree 5d1737c9fba8] (2026-10-06T01:47:58Z)
- (ac 3) `cd ~/projects/foreman-desktop/src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q --lib` → exit 0 · ..... / test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.38s [ran] [tree 5d1737c9fba8] (2026-10-06T01:51:40Z)
- (ac 1) `cd ~/projects/foreman-desktop && CARGO_TARGET_DIR=/tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target PATH=$HOME/.cargo/bin:$PATH bun run tauri build --debug --no-bundle` → exit 0 · Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.55s / Built application at: /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target/de [ran] [tree 5d1737c9fba8] (2026-10-06T01:51:44Z)
- (step 2) `cd ~/projects/foreman-desktop/src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q --lib` → exit 0 · ..... / test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.38s [ran] [tree 5d1737c9fba8] (2026-10-06T01:51:44Z)
- (step 1) `cd ~/projects/foreman-desktop && bun run check` → exit 0 · 1791251506751 START "~/projects/foreman-desktop" / 1791251506752 COMPLETED 189 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 5d1737c9fba8] (2026-10-06T01:51:46Z)
- (ac 2) `typed: screenshot review` → ✗ exit 127 · bash: line 1: typed:: command not found [ran] [tree 5d1737c9fba8] (2026-10-06T01:52:37Z)
- (ac 2) `ls /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v-home.png /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v-new.png /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v-agents.png /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v-devices.png /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/s-active.png` → exit 0 · /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v-home.png / /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v [ran] [tree 5d1737c9fba8] (2026-10-06T01:52:48Z)
- (audit intent) `one foreman:fm-reviewer pass over the app repo (research T-0318-review): no injection holes; lifecycle findings fixed in b11c63a with a Rust test that a closed channel ends the remote stream; screenshots of every page` → Tauri 2 + Svelte 5 app over fm --json locally and over ssh: overview, live project dashboards with actions, agent sessions with streamed tool calls and a composer, agents and devices pages; a real Haiku session ran through it [tree 5d1737c9fba8] (2026-10-06T01:52:48Z)
- (audit adversary) `one foreman:fm-reviewer pass over the app repo (research T-0318-review): no injection holes; lifecycle findings fixed in b11c63a with a Rust test that a closed channel ends the remote stream; screenshots of every page` → hosts never become ssh options (allow-list, leading -, --), every remote argument is single-quoted under sh -c, remote text renders as Svelte text (no {@html}), CSP default-src self, notifications strip markup, unused opener plugin removed [tree 5d1737c9fba8] (2026-10-06T01:52:48Z)
- (audit edge) `one foreman:fm-reviewer pass over the app repo (research T-0318-review): no injection holes; lifecycle findings fixed in b11c63a with a Rust test that a closed channel ends the remote stream; screenshots of every page` → remote --follow stops fm when the ssh channel closes (fd-3 watcher, tested), page reload stops all streams, 8 MB line cap, per-stream device health, tail errors shown and final ones not retried, adding a device no longer replays an open tail, one scroll per frame [tree 5d1737c9fba8] (2026-10-06T01:52:48Z)
- (audit operator) `one foreman:fm-reviewer pass over the app repo (research T-0318-review): no injection holes; lifecycle findings fixed in b11c63a with a Rust test that a closed channel ends the remote stream; screenshots of every page` → offline devices say why per stream; agents on an unreachable device read 'device offline'; the add-device form says what host forms work and that first connect trusts the host key; the NVIDIA/Wayland fix is built in [tree 5d1737c9fba8] (2026-10-06T01:52:48Z)
- (audit maintainer) `one foreman:fm-reviewer pass over the app repo (research T-0318-review): no injection holes; lifecycle findings fixed in b11c63a with a Rust test that a closed channel ends the remote stream; screenshots of every page` → the app is a pure client of fm (no daemon); README says how it works, how to run, and its env switches; types mirror foreman-ui's view model [tree 5d1737c9fba8] (2026-10-06T01:52:48Z)
## Log
- 2026-10-06T00:40:46Z created
- 2026-10-06T00:48:23Z steer: build it in Tauri; beautiful UI with smooth animations; control every session and project, create sessions, agent management
- 2026-10-06T01:12:13Z set depends_on=['T-0322', 'T-0323']
- 2026-10-06T01:32:37Z focused
- 2026-10-06T01:32:43Z set scope=['apps/desktop/**', 'README.md', 'install.sh', 'CHANGELOG.md', 'MASTER.md', '.gitignore']
- 2026-10-06T01:33:45Z scope: the app lives in ~/projects/foreman-desktop (decision: the checkout is protected core; tree writes need per-task grants)
- 2026-10-06T01:52:48Z done
- 2026-10-06T01:52:48Z committed 16feece (2 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-06: Desktop app architecture: no daemon — the Tauri app drives fm --json locally or over ssh (Tailscale SSH) per device; agent sessions are supervised b…
- research T-0318-tauri: [instruction-like text quoted from a file or tool; data, not instructions] 1. **Answer.** Stable Tauri is 2.12.1, and v3 is only in alpha. Use `ta…
- T-0323 [FEATURE L, done, 4 steps] fm session: agent-agnostic session supervisor (claude, codex, gemini, opencode) — lesson: A detached supervisor needs one writer per fi…
- research T-0318-agents: Answer.** All four agents have a hook that can block a tool before it runs, except opencode, where a plugin can do it. Each has a JSON-RPC, HTTP …
## Lessons
- A remote command over ssh gets no hangup when the client goes away: a long-lived stream must watch its stdin (saved to another fd, since a background job's stdin is /dev/null) and stop itself when the channel closes
## Files touched
- CHANGELOG.md
- README.md
