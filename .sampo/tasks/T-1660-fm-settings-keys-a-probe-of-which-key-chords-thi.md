---
id: T-1660
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmcli.py, plugin/tests/test_control_room.py, plugin/commands/settings.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:58:54Z
updated: 2026-10-23T02:48:38Z
group: settings surfaces and safety
base: d11847b050922c5b95a4a49a474f810d1b59afa8
base_tree: 6b6644fc3b9969dc307329f4537f08bc8bb7c047
plan0_at: 2026-10-23T02:44:59Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_control_room.py, CHANGELOG.md]
verified: strong
---
# fm settings keys: a probe of which key chords this terminal delivers
## Raw request
> fm settings keys: a probe of which key chords this terminal delivers
## Interpretation
fm settings keys reads raw key presses and prints the chord each one arrives as in this terminal (Ctrl, Alt, Shift and function keys), using the app's own key decoder, so a user knows which bindings their terminal can deliver before binding them.
## Assumptions (confidence)
## Acceptance criteria
- [x] a scripted byte stream is listed as named chords — verify with `python3 plugin/tests/run.py test_control_room.Chords`
## Non-goals
## Approach (options → choice → why)
Options: document terminal quirks (incomplete); probe live with the app's decoder; skip. Choice: the live probe: it answers the real question for this terminal.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test feeding bytes
2. [x] reuse the app's key decoder
## Resume here
## Docs impact
plugin/commands/settings.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_control_room.Chords` → red as expected (exit 1) · Ran 3 tests in 0.7s (1 classes, 16 at a time; slowest: Chords 0s) / FAILED (1 classes) [ran] [tree 842e18c4f1c5] (2026-10-23T02:45:12Z)
- (step 2) `python3 plugin/tests/run.py test_control_room test_settings_power test_settings test_docs` → exit 0 · Ran 137 tests in 16.2s (30 classes, 16 at a time; slowest: Fences 15s, Command 10s, Monkey 6s) / OK [ran] [tree eaecda33798a] (2026-10-23T02:46:43Z)
- (ac 1) `python3 plugin/tests/run.py test_control_room.Chords` → exit 0 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: Chords 1s) / OK [ran] [tree eaecda33798a] (2026-10-23T02:46:46Z)
- (ac 1) `python3 plugin/tests/run.py test_control_room.Chords` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: Chords 0s) / OK [ran] [tree eaecda33798a] (2026-10-23T02:46:58Z)
- (audit intent) `self-review: the probe reuses fmcodeterm.parse_keys and fmcodetui.key_name (fm code's own decoder), so what it prints is what [keys] can bind; raw mode is restored in finally; non-terminal stdin exits 2; it reads at most 64 bytes a press and stops on q or 30 s idle; unknown sequences are shown escaped` → fm settings chords shows each press as fm code reads it, so a user knows a chord arrives before binding it [tree eaecda33798a] (2026-10-23T02:46:58Z)
- (audit edge) `self-review: the probe reuses fmcodeterm.parse_keys and fmcodetui.key_name (fm code's own decoder), so what it prints is what [keys] can bind; raw mode is restored in finally; non-terminal stdin exits 2; it reads at most 64 bytes a press and stops on q or 30 s idle; unknown sequences are shown escaped` → Alt chords show as esc then the key; a sequence fm code skips shows as not delivered; a paste is ignored; no terminal → exit 2 with the ! hint [tree eaecda33798a] (2026-10-23T02:46:58Z)
- (audit operator) `self-review: the probe reuses fmcodeterm.parse_keys and fmcodetui.key_name (fm code's own decoder), so what it prints is what [keys] can bind; raw mode is restored in finally; non-terminal stdin exits 2; it reads at most 64 bytes a press and stops on q or 30 s idle; unknown sequences are shown escaped` → the plugin's /foreman:settings chords tells the user to run it in their terminal (it reads their key presses) [tree eaecda33798a] (2026-10-23T02:46:58Z)
- (audit self) `self-review: the probe reuses fmcodeterm.parse_keys and fmcodetui.key_name (fm code's own decoder), so what it prints is what [keys] can bind; raw mode is restored in finally; non-terminal stdin exits 2; it reads at most 64 bytes a press and stops on q or 30 s idle; unknown sequences are shown escaped` → no findings [tree eaecda33798a] (2026-10-23T02:46:58Z)
## Log
- 2026-10-22T20:58:54Z created
- 2026-10-22T20:58:55Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_control_room.py', 'CHANGELOG.md']
- 2026-10-22T20:58:56Z split from T-1545 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:30:02Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_control_room.Chords`
- 2026-10-22T21:30:25Z criterion 1 text: a scripted byte stream is listed as named chords — verify with python3 plugin/tests/run.py test_control_room.Chords → a scripted byte stream is listed as named chords
- 2026-10-23T02:44:58Z focused
- 2026-10-23T02:45:00Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings_power.py', 'plugin/commands/settings.md', 'CHANGELOG.md']
- 2026-10-23T02:45:10Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_control_room.py', 'plugin/commands/settings.md', 'CHANGELOG.md']
- 2026-10-23T02:48:32Z done
- 2026-10-23T02:48:38Z committed 319db56a (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1545 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Control Room and direct manipulation: a loopback web app generated from
- T-1511 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 16): key, layout and runner editors inside the fm code — lesson: Rebindable navigation needs a floor…
- research T-1511-review: Verdict: changes needed.** The runner test is sound. Key capture can lock the user out of list navigation, and two other findings are real but na…
- decision 2026-10-20: Self-approve T-1300 (L): an own ANSI truecolor renderer replaces curses; motion as a pure function of state and time
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py; re-ground the plan against them before editing
## Lessons
- A probe must use the product's own decoder, or it reports a terminal the app doesn't see
## Files touched
- plugin/tests/test_control_room.py
- plugin/lib/fmsettings.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- plugin/commands/settings.md
