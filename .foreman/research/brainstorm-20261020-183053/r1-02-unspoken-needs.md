# Brainstorm — lens: unspoken needs

- **Snapshot-test every TUI frame** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: assumption: animation work can't be reviewed from a diff. CI has gone red several times on timing and environment (T-1281, the 3.12 runner), and the user already judged the look as "crap" after the fact. Render fixed-size, fixed-clock frames for each theme and station state, and compare them to golden files.
  Done when: `python3 plugin/tests/...` renders N named frames at 80x24 and 120x40, fails on a one-cell change, and `--update` rewrites the goldens.

- **Degrade by terminal capability** — FEATURE — value 4 — effort M — risk low — category: compatibility
  Why: assumption: "not just static colors" means gradients and truecolor, which break on tmux, SSH, macOS Terminal and Linux consoles. The macOS CI fixes (T-1249, T-1284) show the user's setups differ. Pick truecolor, 256, 16 or mono from the environment (`COLORTERM`, `NO_COLOR`), and fall back to ASCII glyphs.
  Done when: running with `COLORTERM=` and `NO_COLOR=1` gives readable, still-distinguishable frames, covered by snapshot tests.

- **Budget the animation's CPU and context cost** — PERFORMANCE — value 4 — effort S — risk low — category: perf
  Why: the user's recent work is about cost, speed and CPU-time bounds. A TUI that spins at 60fps works against that story. Cap the frame rate, drop to about 2fps when nothing changes or the terminal is unfocused, and ratchet idle CPU in a test like the context-tax test.
  Done when: a 10 s idle replay uses under X ms CPU, asserted in a test, and `--fps` is a setting.

- **Make motion explain state** — FEATURE — value 5 — effort M — risk med — category: animation
  Why: the request is "better animations", and the last redesign moved to pictures (station track, check chips, change bars, Gantt). Add eased movement for the active station, a pulse on running verify runs, a stamp-in for guard verdicts, bars that grow as tokens arrive, and diffs that wipe in. Every motion must correspond to a state change, with no decorative loops.
  Done when: each station transition has a defined animation, and a frame-sequence test shows the intermediate frames differ and settle on the final state.

- **Drive color from run state, not fixed theme slots** — FEATURE — value 4 — effort M — risk low — category: theming
  Why: "not just static colors" is the literal ask. Add palette ramps keyed to health: budget burn shifts cool to warm, a stalled step slowly desaturates, and a passing close-out brightens. Themes would be files with ramps and live reload.
  Done when: a theme file defines a ramp, the cost gauge visibly changes hue at 50% and 90% of the cap, and editing the file updates a running TUI within 1 s.

- **Raise a "needs you" alert for unattended runs** — FEATURE — value 4 — effort S — risk low — category: attention
  Why: assumption: the marathon and overnight work (T-0793) means the user is away, and the run later blocks on a question or a red step. Put a state glyph in the terminal title, ring the bell once, and show a calm banner that persists. An optional command hook (e.g. `notify-send`) is off by default.
  Done when: a blocked run sets the title to a "needs you" marker and the banner persists until the user answers.

- **Replay a finished run in the TUI** — FEATURE — value 4 — effort M — risk low — category: replay
  Why: assumption: the run log already holds the events the live view consumes. Replay with a scrubber, speed keys and jump-to-next-red-step, which doubles as the test fixture for animation (same events, same frames).
  Done when: `fm code tui --replay RUN` shows the run at 1x, 8x and by step, and the final frame matches the live one.

- **Show a live cost and token burn gauge with the dollar cap** — FEATURE — value 4 — effort S — risk low — category: cost
  Why: the user cares most about cheaper and faster than Claude Code, uses dollar caps in the bench, and added `fm cost`. A ring or bar that fills toward the cap, with a spend-rate sparkline, puts that in the user's view.
  Done when: the gauge matches `fm cost` for the same run within a cent, and warns at 80% of the cap.

- **Add a reduced-motion and color-blind-safe mode** — FEATURE — value 3 — effort S — risk low — category: accessibility
  Why: assumption: the animation work adds seizure and legibility risk, and pass/fail currently relies on red and green. Add `--calm` or a setting that swaps motion for static markers, and carry state through shape (✓ ✗ ◐) as well as color.
  Done when: with the setting on, no frame changes except on events, and each pass/fail/running state differs by glyph in monochrome.

- **Let users add widgets through a small extension API** — FEATURE — value 3 — effort L — risk med — category: extensibility
  Why: the original TUI request says "customizable, extendable" with themes and keybindings, but the pack shows only the TUI itself. Allow a widget to be a Python file that receives events and returns cells, with a slot in a layout file.
  Done when: a sample widget in the user's config dir shows up in the layout without editing Foreman, and a crash in it is caught and shown as a placeholder.

- **Show a pulse line for the run (wild)** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. A thin ECG-style line across the header: beats on tool calls, flatlines in red when stalled, spikes on a compaction. You read the run's health at a glance from across the room.
  Done when: the line's beat rate follows tool-call rate in a replay, and a 60 s stall flatlines it.

- **Run an ambient factory-floor mode (wild)** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. The product is called Foreman, so a full-screen view where tasks are crates on a conveyor, with the plan, steps and verify as stations, would be a screensaver for long marathon runs. Key `a` toggles it, and any other key returns to the normal view.
  Done when: `a` shows crates moving between stations as steps advance, and the real status stays in the title.

- **Share a run as an animated SVG or HTML (wild)** — FEATURE — value 4 — effort M — risk med — category: sharing
  Why: wild. The README leads with `demo/live.svg` and an MP4, so the demo is clearly important. Export any replay as a self-contained animated SVG with no recording step, ready for the Benchmarks page and issues.
  Done when: `fm code share RUN` writes one SVG under 1 MB that animates in a browser and has no external references.

- **Render charts as real images where supported (wild)** — FEATURE — value 2 — effort L — risk med — category: graphics
  Why: wild. Use the kitty or sixel graphics protocol for smooth Gantt, token and cost charts when the terminal supports them. Keep block characters as the fallback, tied to the capability detection above.
  Done when: in a kitty-compatible terminal the Gantt draws as an image, and elsewhere it falls back with no error.
