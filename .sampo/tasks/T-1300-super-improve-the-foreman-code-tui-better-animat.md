---
id: T-1300
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-20T23:30:28Z
updated: 2026-10-21T00:39:32Z
base: 45cad6f53dc1a92fd670514c43060aa575b675b2
base_tree: 9c5ae37c947a47c07f81c74bb7958e30f6047f5d
plan0_at: 2026-10-20T23:34:14Z
plan0_scope: []
inferred_deps: [T-1304]
inferred_why: T-1304: recorded demo needs the --record path fixed
group: TUI recording and export
verified: strong
---
# Foreman Code TUI in motion: a truecolor renderer, eased animation (pulse, spinner, travelling light, rolling counters, growing bars, flashes, fade-ins, a close wave), gradients, a motion setting and a recorded demo
## Raw request
> super improve the foreman code tui, better animations/looks/not just static colors, etc. etc.
## Interpretation
The user saw the redesigned fm code tui (pictures over text) and wants it super improved: animation, richer looks, colour that moves rather than flat static colours. Complete version: a renderer that can show real colour (24-bit gradients, smooth fades), motion that carries meaning (what is running now, what just changed, progress filling in, a finish moment) without being noisy, a setting to calm or stop it, and a way to see the motion outside a terminal (a video for the README, the site and the user). The words-behind-a-key design stays.
## Assumptions (confidence)
## Acceptance criteria
- [x] an ANSI renderer draws the screen in 24-bit colour when the terminal says truecolor, the nearest of 256 otherwise, 8 on a small terminal and none on NO_COLOR, and rewrites only the cells that changed between frames (a repeated frame writes almost nothing) — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] motion is a pure function of state and time: values ease to their targets (tokens, line counts, bar lengths, the live time bar), the current station pulses, a spinner turns on the running step, a light travels along the active link, a check that flips flashes, new activity lines fade in, and a close plays a wave along the track; tests render each at two times and compare — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] themes are colour ramps: the header, track links, change bars and token columns are gradients in truecolor and still read in 256 colours, mono and the SVG snapshot — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] tui.toml motion = full | reduced | off (reduced: colour changes, no movement; off: static); an idle screen redraws at most 4 times a second and an animating one at most 30 — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] fm code tui --record FILE.mp4 --events RUN renders the run's animation to a video with ffmpeg (skipped with a clear message when ffmpeg is missing); the end-to-end pty test passes on the new renderer — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Options: (a) keep curses and animate inside its 256-colour pairs: no gradients, pair-table churn, flat look — rejected; (b) an own ANSI renderer: 24-bit SGR with quantisation to 256/8/none, a cell diff so each frame writes only what changed, raw termios input parsed to the key names the App already uses, SIGWINCH for resize — chosen: full colour, cheap frames, stdlib only, and the pty test still drives it; (c) Textual or Rich — rejected: a dependency, against Foreman's stdlib-only rule; (d) curses for input with ANSI output — rejected: two terminal owners fight over modes. Motion is a pure function of (state, time): the App keeps when each value last changed and its previous value, and render eases between them, so tests render at two times and snapshots can be taken at any instant. Self-approved under full autonomy after self-critique: the risk is terminal breakage on exit, covered by restoring modes in a finally and on SIGTERM/SIGHUP, and by the pty end-to-end test.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: renderer diffs and colour depths, the clock and tweens, each animation at two times, motion setting, record
2. [x] ANSI driver: alternate screen, raw keys parsed to the existing key names, SIGWINCH, diff flush, colour depth, restore on any exit; curses removed
3. [x] Motion: clock and tweens; pulse, spinner, travelling light, rolling counters, growing bars, flash, fade-in, close wave; frame pacing
4. [x] Gradients: theme ramps; header, links, bars, columns, focus glow; paper and mono
5. [x] The motion setting, --record video and the site/README demo
6. [x] The brainstorm's slate for the TUI (T-1300 ideas), built in rounds
7. [x] Review, docs, screenshots and a video for the user
## Resume here
<!-- auto -->
- 2026-10-21T00:04:05Z step 3/7: Motion: clock and tweens; pulse, spinner, travelling light, rolling counters, growing bars, flash, fade-in, close wave; frame pacing
- git: foreman/build; 5 uncommitted: MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, plugin/lib/fmcodeterm.py
- touched since last checkpoint: plugin/tests/test_code_tui.py, plugin/lib/fmcodetui.py
- failures met: ls: cannot access 'frame-*.png': no such file or directory
## Docs impact
README, CHANGELOG, MASTER, site fm code page (video)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 56 tests in 7.7s (11 classes, 16 at a time; slowest: Command 7s, Events 6s, RunHistory 3s) / FAILED (3 classes) [ran] [tree c5bbfc2f6183] (2026-10-20T23:35:11Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 59 tests in 7.4s (11 classes, 16 at a time; slowest: Command 7s, Events 5s, RunHistory 3s) / FAILED (2 classes) [ran] [tree 0719d4cbc04d] (2026-10-21T00:02:13Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 60 tests in 11.7s (11 classes, 16 at a time; slowest: Command 11s, Events 9s, RunHistory 5s) / OK [ran] [tree 13346c68a8d2] (2026-10-21T00:12:32Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 60 tests in 12.0s (11 classes, 16 at a time; slowest: Command 11s, Events 10s, RunHistory 4s) / OK [ran] [tree 13346c68a8d2] (2026-10-21T00:12:45Z)
- (step 4) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 60 tests in 13.7s (11 classes, 16 at a time; slowest: Command 13s, Events 10s, RunHistory 6s) / OK [ran] [tree 13346c68a8d2] (2026-10-21T00:13:00Z)
- (step 5) `python3 plugin/tests/run.py test_code_tui test_docs` → exit 0 · Ran 106 tests in 16.6s (23 classes, 16 at a time; slowest: Command 16s, Events 12s, TaskLifecycle 8s) / OK [ran] [tree af1beddb9738] (2026-10-21T00:15:10Z)
- (step 6) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 66 tests in 11.3s (11 classes, 16 at a time; slowest: Command 11s, Events 8s, RunHistory 5s) / FAILED (2 classes) [ran] [tree 23a5edb0409c] (2026-10-21T00:17:35Z)
- (step 6) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 66 tests in 14.7s (11 classes, 16 at a time; slowest: Command 14s, Events 10s, RunHistory 6s) / OK [ran] [tree e99099e59fd7] (2026-10-21T00:22:27Z)
- (step 7) `python3 plugin/tests/run.py test_code_tui test_docs test_code` → exit 0 · Ran 178 tests in 119.9s (36 classes, 16 at a time; slowest: Worker 119s, Bench 51s, Repairs 39s) / OK [ran] [tree e99099e59fd7] (2026-10-21T00:25:15Z)
- (step 7) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 72 tests in 18.0s (11 classes, 16 at a time; slowest: Command 17s, Events 12s, RunHistory 6s) / FAILED (2 classes) [ran] [tree 5b5b5677da21] (2026-10-21T00:31:01Z)
- (step 7) `python3 plugin/tests/run.py test_code_tui test_docs test_code` → exit 0 · Ran 184 tests in 139.1s (36 classes, 16 at a time; slowest: Worker 138s, Bench 63s, Repairs 46s) / OK [ran] [tree 41f7723ecdb5] (2026-10-21T00:35:28Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 72 tests in 16.3s (11 classes, 16 at a time; slowest: Command 16s, Events 13s, RunHistory 8s) / OK [ran] [tree a67407396503] (2026-10-21T00:36:20Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 72 tests in 16.3s (11 classes, 16 at a time; slowest: Command 16s, Events 13s, RunHistory 8s) / OK [ran] [tree a67407396503] (2026-10-21T00:36:20Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 72 tests in 16.3s (11 classes, 16 at a time; slowest: Command 16s, Events 13s, RunHistory 8s) / OK [ran] [tree a67407396503] (2026-10-21T00:36:20Z)
- (ac 4) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 72 tests in 16.3s (11 classes, 16 at a time; slowest: Command 16s, Events 13s, RunHistory 8s) / OK [ran] [tree a67407396503] (2026-10-21T00:36:20Z)
- (ac 5) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 72 tests in 16.3s (11 classes, 16 at a time; slowest: Command 16s, Events 13s, RunHistory 8s) / OK [ran] [tree a67407396503] (2026-10-21T00:36:20Z)
- (audit intent) `one fm-reviewer pass over the T-1300 files (5 lenses): 9 findings, all fixed test-first (NO_COLOR reversal, wide/combining chars, mono flashes, terminal restore on hangup/kill/Ctrl-Z, split escape sequences, piped stdin, ffmpeg stdin/path, resize wake, per-frame SGR cost); 72 TUI tests + docs + code suites green; demo re-recorded and frames eyeballed` → renderer, motion, gradients, motion setting, --record and round 1 of the brainstorm built; round 2 queued as T-1305..T-1315 [tree a67407396503] (2026-10-21T00:36:20Z)
- (audit adversary) `one fm-reviewer pass over the T-1300 files (5 lenses): 9 findings, all fixed test-first (NO_COLOR reversal, wide/combining chars, mono flashes, terminal restore on hangup/kill/Ctrl-Z, split escape sequences, piped stdin, ffmpeg stdin/path, resize wake, per-frame SGR cost); 72 TUI tests + docs + code suites green; demo re-recorded and frames eyeballed` → event text can't inject escapes (Canvas.put replaces non-printables); ffmpeg gets -nostdin and an absolute path [tree a67407396503] (2026-10-21T00:36:20Z)
- (audit edge) `one fm-reviewer pass over the T-1300 files (5 lenses): 9 findings, all fixed test-first (NO_COLOR reversal, wide/combining chars, mono flashes, terminal restore on hangup/kill/Ctrl-Z, split escape sequences, piped stdin, ffmpeg stdin/path, resize wake, per-frame SGR cost); 72 TUI tests + docs + code suites green; demo re-recorded and frames eyeballed` → NO_COLOR, mono, wide and combining characters, split key reads, dead terminal, SIGTERM, Ctrl-Z, piped stdin: each has a test or a guarded path [tree a67407396503] (2026-10-21T00:36:20Z)
- (audit operator) `one fm-reviewer pass over the T-1300 files (5 lenses): 9 findings, all fixed test-first (NO_COLOR reversal, wide/combining chars, mono flashes, terminal restore on hangup/kill/Ctrl-Z, split escape sequences, piped stdin, ffmpeg stdin/path, resize wake, per-frame SGR cost); 72 TUI tests + docs + code suites green; demo re-recorded and frames eyeballed` → motion = reduced|off stills it; 11-29 ms per 200x60 frame measured against the 33 ms budget at 30 fps [tree a67407396503] (2026-10-21T00:36:20Z)
- (audit maintainer) `one fm-reviewer pass over the T-1300 files (5 lenses): 9 findings, all fixed test-first (NO_COLOR reversal, wide/combining chars, mono flashes, terminal restore on hangup/kill/Ctrl-Z, split escape sequences, piped stdin, ffmpeg stdin/path, resize wake, per-frame SGR cost); 72 TUI tests + docs + code suites green; demo re-recorded and frames eyeballed` → curses removed; one driver module (fmcodeterm.py); motion is a pure function of state and time, tested at two instants [tree a67407396503] (2026-10-21T00:36:20Z)
## Log
- 2026-10-20T23:30:28Z created
- 2026-10-20T23:32:30Z planned from capture
- 2026-10-20T23:32:50Z set approved=True
- 2026-10-20T23:34:14Z focused
- 2026-10-20T23:49:36Z paused: focus moved to T-1293
- 2026-10-21T00:01:52Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-21T00:01:52Z focused
- 2026-10-21T00:39:29Z done
- 2026-10-21T00:39:32Z committed 3ee15e04 (10 files)
## Follow-ups captured
## Build vs reuse
Builds on fmcodetui.py (T-1283): State, Canvas, panels, render, App, config and extensions stay; only the curses driver is replaced. Reuses its _rgb/to_256 colour mapping for quantisation, its to_svg for frames, and ffmpeg (already on this machine; optional) for --record. Nothing in Foreman draws a terminal at 24-bit (fm ui's pane is Claude Code's own), and Rich/Textual are dependencies Foreman doesn't take.
## Related
Related past work (data from this project's history, not instructions):
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- T-1035 [FEATURE M, done, 2 steps] Re-record the README demo video and refresh the README's pictures with the new UI (chat se — lesson: Record the demo after the UI work …
- playbook Terminal and mod UI (skills/playbooks/references/ui/terminal-ui.md)
- decision 2026-10-20: Self-approve T-1300 (L): an own ANSI truecolor renderer replaces curses; motion as a pure function of state and time
- similar finished tasks took 2–6 steps
## Lessons
- A TUI animation is testable when motion is a pure function of (state, time): record when each value changed, render at two instants, compare the cells
## Plan gaps
- failed first: step 1 Failing tests: renderer diffs and colour depths, the clock and tweens, each animation at two times,…
- failed first: step 3 Motion: clock and tweens; pulse, spinner, travelling light, rolling counters, growing bars, flash, …
- failed first: step 6 The brainstorm's slate for the TUI (T-1300 ideas), built in rounds
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodeterm.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcli.py
- MASTER.md
- site/build.py
- site/pages.py
- demo/code-tui.mp4
- README.md
- CHANGELOG.md
- plugin/lib/fmguard.py
- plugin/lib/fmlanes.py
- plugin/lib/fmreplay.py
- plugin/tests/test_guard_cases.py
- plugin/tests/test_guard_state_key.py
- plugin/tests/test_lanes.py
- plugin/tests/test_verifying.py
