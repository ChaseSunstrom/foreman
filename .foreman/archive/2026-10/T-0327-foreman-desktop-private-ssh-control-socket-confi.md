---
id: T-0327
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T01:54:16Z
updated: 2026-10-06T01:56:15Z
base: 16feeceebbbdb45455fce0e142433be7a7b3e266
base_tree: 5d1737c9fba850a8b7608d923a816cbcf5fea61e
verified: ok
---
# Foreman Desktop: private ssh control socket, confirmed host keys, no stderr deadlock, fm command allow-list
## Raw request
> Foreman Desktop: private ssh control socket, confirmed host keys, no stderr deadlock, fm command allow-list
## Interpretation
The background security review of ~/projects/foreman-desktop found: (1) ControlPath falls back to shared /tmp when XDG_RUNTIME_DIR is unset (socket pre-creation hijack); (2) accept-new silently trusts first host keys, including tailnet peer names other members control; (3) the 16 KiB stderr cap stops draining stderr, so a chatty child blocks and leaks processes; (4) the webview can run any fm subcommand on any device.
## Assumptions (confidence)
## Acceptance criteria
- [x] the Rust tests cover the private ControlPath, the allow-list, a 1 MB stderr child that still ends, and host trust parsing — verify with `cd ~/projects/foreman-desktop/src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q --lib`
## Non-goals
## Approach (options → choice → why)
Options: per finding, minimal fix vs redesign. Choice: (1) ControlPath under ~/.ssh (user-private) when XDG_RUNTIME_DIR is unset; (2) StrictHostKeyChecking=yes, and an unknown host key becomes an explicit Trust step in the app that shows ssh-keyscan's fingerprint and appends to known_hosts only on the user's click; (3) drain stderr fully, keep the last 16 KiB; (4) Rust allow-list of fm subcommands the app uses. Why: each closes its hole without changing how the app works.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red)
2. [x] fixes in lib.rs
3. [x] Trust step in the Devices page
## Resume here
## Docs impact
the app README's How it works
## Verification evidence
- (ac 1) `cd ~/projects/foreman-desktop/src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q --lib` → exit 0 · ......... / test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.39s [ran] [tree 5d1737c9fba8] (2026-10-06T01:56:00Z)
- (step 1) `tests written beside the fixes in lib.rs (one file): control_sockets_stay_private, only_the_apps_own_commands_run, a_chatty_stderr_never_blocks_the_child, host_keys_are_only_this_hosts` → red before: none of control_dir/allowed/drain_tail/key_line_ok existed (compile-red); green after: 9/9 [tree 5d1737c9fba8] (2026-10-06T01:56:01Z)
- (step 2) `cd ~/projects/foreman-desktop/src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q --lib` → exit 0 · ......... / test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.39s [ran] [tree 5d1737c9fba8] (2026-10-06T01:56:01Z)
- (step 3) `cd ~/projects/foreman-desktop && bun run check` → exit 0 · 1791251763638 START "~/projects/foreman-desktop" / 1791251763639 COMPLETED 189 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 5d1737c9fba8] (2026-10-06T01:56:03Z)
- (ac 1) `cd ~/projects/foreman-desktop/src-tauri && CARGO_TARGET_DIR=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target ~/.cargo/bin/cargo test -q --lib` → exit 0 · ......... / test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.39s [ran] [tree 5d1737c9fba8] (2026-10-06T01:56:14Z)
- (audit intent) `fixes follow the independent background security review (sdk-py 56ca00e6) finding by finding; main-thread adversary pass over the new surface` → all four findings closed in ~/projects/foreman-desktop 1003769: ControlPath in XDG_RUNTIME_DIR or ~/.ssh (0700), StrictHostKeyChecking=yes with an explicit fingerprint Trust step, stderr drained to a 16 KiB tail, fm subcommand allow-list in Rust [tree 5d1737c9fba8] (2026-10-06T01:56:14Z)
- (audit adversary) `fixes follow the independent background security review (sdk-py 56ca00e6) finding by finding; main-thread adversary pass over the new surface` → the allow-list refuses trust/uninstall-user/doctor/run and task done (tested), skips only leading -p pairs; host_key_scan/trust validate the alias and the ssh -G host name, accept only 'host|[host]:port type base64' lines for that exact host and port, and re-check them on trust (no TOCTOU via the page); a changed host key gets no trust button; remaining: session start --arg can pass agent flags (same power as starting a session) [tree 5d1737c9fba8] (2026-10-06T01:56:14Z)
## Log
- 2026-10-06T01:54:16Z created
- 2026-10-06T01:54:16Z focused
- 2026-10-06T01:54:16Z scope: ~/projects/foreman-desktop (the app's own repo); found by the background security review (sdk-py session 56ca00e6)
- 2026-10-06T01:56:15Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0318-review: Verdict: changes needed.** There are no injection holes. The real problems are remote process leaks and silent failures in the session view.
- research T-0206-review: Verdict: changes needed.** There is one MEDIUM robustness bug and two LOWs. I found no HIGH SSRF hole. I traced this by reading the code and did …
- T-0318 [FEATURE L, done, 6 steps] FEATURE: beautiful modern animated desktop app wrapping Foreman — supports every feature, — lesson: A remote command over ssh gets no h…
- research T-0120-review: Verdict [stale: mods/foreman-ui/hooks/register.tsx, plugin/lib/fmguard.py changed since it was written]
- similar past tasks were L: consider --tier L
## Lessons
- A shared-connection socket path is an authentication boundary: never put it in a world-writable dir, and never trust a first host key the user didn't look at
