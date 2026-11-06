---
id: T-0328
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T01:54:20Z
updated: 2026-10-06T02:22:29Z
base: 16feeceebbbdb45455fce0e142433be7a7b3e266
base_tree: 5d1737c9fba850a8b7608d923a816cbcf5fea61e
verified: strong
---
# FEATURE: Foreman Desktop v2 — clean up the UI so it looks less AI-made and better organize
## Raw request
> FEATURE: Foreman Desktop v2 — clean up the UI so it looks less AI-made and better organized; a real minimalistic SVG logo; more features: subagents, control every Claude session (Remote Control, terminal, headless) on every device, send messages to them, see their scratchpad files and pictures; scroll and view every inbox and queue item (no caps), everything; actually usable and good
## Interpretation
Make Foreman Desktop something the user would actually use every day, and make it not look AI-made: a restrained, well-organised UI with one accent colour, no gradient glow, aurora or sparkle tropes, and a real minimal SVG logo. It must reach every Claude Code session on every device, not only the ones fm session started: terminal sessions, Remote Control units, headless runs. For each: read the conversation (text, tool calls, images), see its subagents and their transcripts, browse its scratchpad files and pictures, and send it a message (a headless continuation by its own id, forked when the terminal session is still live). Project pages show every queue, inbox and blocked item (no caps) with search. Remote Control units can be started and stopped.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm claude lists this device's Claude sessions (terminal, headless, remote) with title, folder, liveness; show/files/file/image/send work on real transcripts, scratchpads and images — verify with `python3 plugin/tests/run.py -k test_claude`
- [x] fm serve status --json lists Remote Control units — verify with `python3 plugin/tests/run.py -k Serve`
- [x] the app builds and its Rust tests pass — verify with `cd ~/projects/foreman-desktop && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target PATH=$HOME/.cargo/bin:$PATH bun run tauri build --debug --no-bundle && cd src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q --lib`
- [x] new look, logo, full lists, Claude sessions with subagents, files, images and send, Remote Control panel, palette: checked by screenshots of each — verify with `ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v2-*.png`
## Non-goals
## Approach (options → choice → why)
Options for reaching every Claude session: (A) drive the TUI (tmux send-keys) or Anthropic's remote-control relay — neither works for sessions in a plain terminal or without a claude.ai connection; (B) read Claude Code's own session store (~/.claude/projects/<dir>/<id>.jsonl, <id>/subagents/agent-*.jsonl + .meta.json, /tmp/claude-<uid>/<dir>/<id>/scratchpad) through a new fm claude command (list/show/files/file/image/send, with --follow), and continue a session with claude -p --resume (--fork-session while it's live). Choice: B — the same data on every device over ssh, read-only except send, which reuses fm session. The transcript format is internal: parse defensively, keep unknown entries out, test against real transcripts on this machine. UI: rebuild the shell (sidebar with search, Ctrl+K palette), project tabs (Overview, Queue, Inbox, Blocked, Activity) from fm state --json, a unified Sessions page (fm and Claude sessions, filters), a session view with Conversation, Subagents, Files and Images tabs, and a Remote Control panel from fm serve status --json.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm claude: tests (red) against fixture transcripts
2. [x] fm claude list/show/files/file/image/send + --follow
3. [x] fm serve status --json
4. [x] logo + design system (restrained palette, type, spacing, motion)
5. [x] shell: sidebar + search + Ctrl+K palette
6. [x] project page tabs with full lists from fm state
7. [x] sessions: unified list + Claude sessions + conversation/subagents/files/images + send
8. [x] Remote Control panel; agents/devices polish
9. [x] screenshots, docs
## Resume here
## Docs impact
MASTER CLI + module table, CHANGELOG, README, the app's README
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_claude` → ✗ exit 1 · Ran 5 tests in 0.6s (2 classes, 16 at a time; slowest: Claude 1s, Remote 0s) / FAILED (1 classes) [ran] [tree 91fd5d064106] (2026-10-06T01:58:22Z)
- (ac 1) `python3 plugin/tests/run.py -k test_claude` → exit 0 · Ran 5 tests in 1.3s (2 classes, 16 at a time; slowest: Claude 1s, Remote 0s) / OK [ran] [tree daf228ce42d5] (2026-10-06T02:01:45Z)
- (ac 2) `python3 plugin/tests/run.py -k Serve` → exit 0 · Ran 11 tests in 2.3s (1 classes, 16 at a time; slowest: Serve 2s) / OK [ran] [tree daf228ce42d5] (2026-10-06T02:01:47Z)
- (step 1) `python3 plugin/tests/run.py -k test_claude` → exit 0 · Ran 5 tests in 1.3s (2 classes, 16 at a time; slowest: Claude 1s, Remote 0s) / OK [ran] [tree daf228ce42d5] (2026-10-06T02:01:49Z)
- (step 2) `cd /tmp && fm claude list --json | python3 -c 'import json,sys; v=json.load(sys.stdin)["sessions"]; assert v and all(s["cwd"] for s in v); print(len(v), "sessions")'` → exit 0 · 49 sessions [ran] [tree daf228ce42d5] (2026-10-06T02:01:50Z)
- (step 3) `python3 plugin/tests/run.py -k test_status_json` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Serve 0s) / OK [ran] [tree daf228ce42d5] (2026-10-06T02:01:50Z)
- (ac 3) `cd ~/projects/foreman-desktop && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target PATH=$HOME/.cargo/bin:$PATH bun run tauri build --debug --no-bundle && cd src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q --lib` → exit 0 · ......... / test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.66s [ran] [tree 92288a92e87f] (2026-10-06T02:18:21Z)
- (ac 1) `python3 plugin/tests/run.py -k test_claude` → exit 0 · Ran 6 tests in 1.6s (2 classes, 16 at a time; slowest: Claude 2s, Remote 0s) / OK [ran] [tree 708f4a69e8b3] (2026-10-06T02:20:54Z)
- (ac 2) `python3 plugin/tests/run.py -k Serve` → exit 0 · Ran 11 tests in 2.3s (1 classes, 16 at a time; slowest: Serve 2s) / OK [ran] [tree 708f4a69e8b3] (2026-10-06T02:20:57Z)
- (ac 3) `cd ~/projects/foreman-desktop && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target PATH=$HOME/.cargo/bin:$PATH bun run tauri build --debug --no-bundle && cd src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q --lib` → exit 0 · ......... / test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.39s [ran] [tree 708f4a69e8b3] (2026-10-06T02:21:01Z)
- (ac 4) `ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v2-*.png` → exit 0 · /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v2-rp.png / /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v2 [ran] [tree 708f4a69e8b3] (2026-10-06T02:21:01Z)
- (step 1) `python3 plugin/tests/run.py -k test_claude` → exit 0 · Ran 6 tests in 1.6s (2 classes, 16 at a time; slowest: Claude 2s, Remote 0s) / OK [ran] [tree 708f4a69e8b3] (2026-10-06T02:21:03Z)
- (step 2) `cd /tmp && fm claude list --json | python3 -c 'import json,sys; v=json.load(sys.stdin)["sessions"]; assert v and all(s["cwd"] for s in v); print(len(v), "sessions")'` → exit 0 · 27 sessions [ran] [tree 708f4a69e8b3] (2026-10-06T02:21:04Z)
- (step 3) `python3 plugin/tests/run.py -k test_status_json` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Serve 0s) / OK [ran] [tree 708f4a69e8b3] (2026-10-06T02:21:05Z)
- (step 4) `cd ~/projects/foreman-desktop && bun run check` → exit 0 · 1791253266979 START "~/projects/foreman-desktop" / 1791253266980 COMPLETED 199 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 708f4a69e8b3] (2026-10-06T02:21:07Z)
- (step 5) `cd ~/projects/foreman-desktop && bun run check` → exit 0 · 1791253268974 START "~/projects/foreman-desktop" / 1791253268975 COMPLETED 199 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 708f4a69e8b3] (2026-10-06T02:21:09Z)
- (step 6) `cd ~/projects/foreman-desktop && bun run check` → exit 0 · 1791253270967 START "~/projects/foreman-desktop" / 1791253270967 COMPLETED 199 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 708f4a69e8b3] (2026-10-06T02:21:11Z)
- (step 7) `cd ~/projects/foreman-desktop && bun run check` → exit 0 · 1791253272926 START "~/projects/foreman-desktop" / 1791253272926 COMPLETED 199 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 708f4a69e8b3] (2026-10-06T02:21:12Z)
- (step 8) `cd ~/projects/foreman-desktop && bun run check` → exit 0 · 1791253274902 START "~/projects/foreman-desktop" / 1791253274903 COMPLETED 199 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 708f4a69e8b3] (2026-10-06T02:21:14Z)
- (step 9) `ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v2-*.png && fm docs` → exit 0 · /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v2-sessions.png / No doc drift in ~/.claude/foreman. [ran] [tree 708f4a69e8b3] (2026-10-06T02:21:15Z)
- (ac 1) `python3 plugin/tests/run.py -k test_claude` → exit 0 · Ran 6 tests in 1.6s (2 classes, 16 at a time; slowest: Claude 2s, Remote 0s) / OK [ran] [tree 708f4a69e8b3] (2026-10-06T02:22:29Z)
- (ac 2) `python3 plugin/tests/run.py -k Serve` → exit 0 · Ran 11 tests in 2.2s (1 classes, 16 at a time; slowest: Serve 2s) / OK [ran] [tree 708f4a69e8b3] (2026-10-06T02:22:29Z)
- (ac 3) `cd ~/projects/foreman-desktop && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target PATH=$HOME/.cargo/bin:$PATH bun run tauri build --debug --no-bundle && cd src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q --lib` → exit 0 · ......... / test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.38s [ran] [tree 708f4a69e8b3] (2026-10-06T02:22:29Z)
- (ac 4) `ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v2-*.png` → exit 0 · /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v2-rp.png / /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/v2 [ran] [tree 708f4a69e8b3] (2026-10-06T02:22:29Z)
- (audit intent) `one foreman:fm-reviewer pass (research T-0328-review) + the background security review; findings fixed test-first (fmclaude) and in app a4d6b36; screenshots of every page` → every Claude session on every device (terminal, remote, headless under its own filter) with conversation, images, subagents, scratchpad files and pictures, and send; every queue/inbox/blocked item with search and the full brief; Remote control page; restrained design and the F. logo; Ctrl+K palette [tree 708f4a69e8b3] (2026-10-06T02:22:29Z)
- (audit adversary) `one foreman:fm-reviewer pass (research T-0328-review) + the background security review; findings fixed test-first (fmclaude) and in app a4d6b36; screenshots of every page` → ids fullmatch; scratchpad reads require a real, user-owned claude-<uid> and scratchpad folder, stay inside it (.., absolute, symlinks refused, O_NOFOLLOW at open); send always forks and never takes options from the message; Markdown builds elements only; copied resume command single-quotes the folder; Rust allow-list holds with claude and serve status/start/stop [tree 708f4a69e8b3] (2026-10-06T02:22:29Z)
- (audit edge) `one foreman:fm-reviewer pass (research T-0328-review) + the background security review; findings fixed test-first (fmclaude) and in app a4d6b36; screenshots of every page` → U+2028 and non-string blocks no longer break parsing or crash show; transcripts read a megabyte at a time; the app loads the latest 4000 lines first with a full-history link; empty sessions skipped; terminal sessions never cut by the headless limit; the memo keeps one entry per transcript; list updated times coarse to 15 s so --follow doesn't churn [tree 708f4a69e8b3] (2026-10-06T02:22:29Z)
- (audit operator) `one foreman:fm-reviewer pass (research T-0328-review) + the background security review; findings fixed test-first (fmclaude) and in app a4d6b36; screenshots of every page` → a planted or foreign scratchpad says why it can't be read; files over the 2000 listing cap are flagged; text-mode list/files/agents strip control characters [tree 708f4a69e8b3] (2026-10-06T02:22:29Z)
- (audit maintainer) `one foreman:fm-reviewer pass (research T-0328-review) + the background security review; findings fixed test-first (fmclaude) and in app a4d6b36; screenshots of every page` → fm claude is one module over Claude Code's store, documented (MASTER, CHANGELOG, both READMEs), with fixture-transcript tests shaped like real ones on this machine [tree 708f4a69e8b3] (2026-10-06T02:22:29Z)
## Log
- 2026-10-06T01:54:20Z created
- 2026-10-06T01:57:09Z set approved=True
- 2026-10-06T01:57:09Z focused
- 2026-10-06T01:57:09Z scope: plugin/lib (fmclaude.py, fmserve.py, fmcli.py), plugin/tests, docs; and ~/projects/foreman-desktop
- 2026-10-06T02:03:19Z guard authorization added: rm-outside
- 2026-10-06T02:22:29Z done
- 2026-10-06T02:22:29Z committed 1a67e08 (9 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
- T-0179 [FEATURE M, done, 3 steps] Each reply is a panel: a round-bordered box per message, the closing report accented — lesson: Check a layout change in the live render…
- research T-0318-surfaces: 1. **Answer.** Foreman has a per-project JSON view model (`fm ui --json`) and a read-only MCP server. The only cross-project data are a hand-re…
- playbook Terminal and mod UI (skills/playbooks/references/ui/terminal-ui.md)
- the similar finished task took 3 steps
## Lessons
- Read another tool's internal store defensively: split on \n only, type-check every field, skip what you don't know, and never let one odd entry stop the stream
## Files touched
- plugin/tests/test_claude.py
- plugin/lib/fmclaude.py
- plugin/lib/fmcli.py
- plugin/lib/fmsession.py
- plugin/lib/fmserve.py
- plugin/tests/test_serve.py
- CHANGELOG.md
- MASTER.md
- README.md
