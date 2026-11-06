# Brainstorm — lens: reliability

- **Render every frame through a diffed double buffer** — PERFORMANCE — value 5 — effort M — risk med — category: rendering
  Why: assumption: the TUI repaints whole regions, and richer animation will make flicker and tearing visible. The request asks for more motion, and "views fade the screen" from the earlier steer is exactly where full repaints show.
  Done when: a test feeds 200 animated frames to a fake terminal and the bytes written per frame after the first are under 10% of a full repaint. A recorded session shows no cursor flashes.

- **Degrade animation by terminal capability** — FEATURE — value 5 — effort M — risk low — category: compatibility
  Why: assumption: the user wants gradients and "not just static colors", which needs truecolor, but Foreman also runs on macOS CI, over SSH and in the docked pane. T-1217 already shows Claude Code overriding pane colors. Detect NO_COLOR, COLORTERM, TERM=dumb, and non-TTY output, and fall back truecolor → 256 → 16 → plain.
  Done when: the same scripted run renders under each of the four settings. The plain mode has zero escape sequences and still shows every station's state.

- **Make the frame clock drop frames, not stall the loop** — FIX — value 5 — effort M — risk med — category: responsiveness
  Why: assumption: animation timers share a thread with the model stream and guard verdicts. A slow redraw must never delay a worker's output or a keypress. Run animation on a time budget and skip ticks when behind.
  Done when: a test injects a 300 ms render delay and the event queue still drains in order with input latency under 50 ms. Skipped frames are counted in `fm code` debug output.

- **Restore the terminal on every exit path** — FIX — value 5 — effort S — risk low — category: crash-safety
  Why: assumption: the TUI uses alt-screen, hidden cursor and raw mode. A crash, SIGTERM, SIGHUP or a worker kill that leaves the shell broken is the worst failure a prettier UI can add.
  Done when: tests kill the TUI with SIGINT, SIGTERM, SIGHUP and an uncaught exception. After each, the pty shows the main screen, a visible cursor and cooked mode.

- **Handle resize and tiny terminals without corrupting layout** — FIX — value 4 — effort M — risk med — category: layout
  Why: assumption: Gantt bars, station tracks and token columns are width-dependent and will break on SIGWINCH or in a narrow docked pane. Re-layout on resize and show a compact "too small" view below a minimum size instead of wrapping garbage.
  Done when: a pty test resizes from 120 to 40 to 20 columns mid-run, and no frame has a line wider than the terminal. The 20-column case shows the compact view.

- **Golden-frame snapshot tests for every view and theme** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: the repo has 231 test files and a bench culture, but no evidence of visual regression tests. Look changes are subjective, so pin them. Render each view at a fixed size and time and compare to stored frames, with `--update` to bless changes.
  Done when: `python3 plugin/tests/...` fails when a color or glyph in the station track changes unexpectedly, and passes after the snapshot is updated.

- **Strip or neutralize escape sequences in model and tool output** — SECURITY — value 4 — effort S — risk low — category: injection
  Why: assumption: model words, diffs and verify output are shown inside the TUI. Raw ANSI or OSC sequences in them could clear the screen, spoof a guard verdict, or retitle the window. The pack lists injection defenses as a deferred theme (T-0791).
  Done when: a test feeds output containing `\x1b[2J`, an OSC 52 clipboard write and a fake "guard: allowed" line. The screen shows them as inert escaped text.

- **Cap TUI cost: CPU and memory budget in the bench** — PERFORMANCE — value 4 — effort S — risk low — category: performance budget
  Why: the project already ratchets hook CPU time (`bench_hooks.py`) and context bytes. Animation is the next thing to creep. Add a budget for idle CPU and for memory over a long run.
  Done when: a 10-minute simulated run keeps idle CPU under a set percent and memory growth under a set number of MB. CI fails when either is exceeded.

- **Wild: Replay any run as a scrubbable film from its event log** — FEATURE — value 4 — effort L — risk med — category: replay — wild
  Why: assumption: a run's events (plan, steps, verdicts, diffs) are already stored. Driving the TUI from a log instead of a live run makes animations testable and deterministic. It also lets you share a session, as the demo SVG does. `fm code replay RUN --speed 4` with pause and seek.
  Done when: replaying a stored run twice produces byte-identical frames at a fixed clock, and seeking to a step shows that step's state.

- **Wild: Heartbeat strip that shows the harness is alive or wedged** — FEATURE — value 3 — effort S — risk low — category: liveness — wild
  Why: assumption: with long unattended runs and compaction storms, the user can't tell "thinking" from "hung". A pulse in the status line is tied to real worker I/O and goes amber, then red, as silence grows. Decoration alone can't fake this, because the pulse comes from events.
  Done when: with the fake worker silent for 60 s the strip turns red and names the last event's age. Resuming output returns it to green.

- **Wild: Self-test mode that plays every animation and flags drift** — FEATURE — value 3 — effort M — risk low — category: diagnostics — wild
  Why: assumption: terminals differ on wide glyphs, braille and box-drawing widths. `fm code tui --selftest` draws every glyph and gradient, asks the terminal for cursor position after each, and reports mismatches, with a suggested ASCII theme.
  Done when: on a terminal where a glyph measures wrong, the report names the glyph, and `--ascii` fixes the alignment.

- **Wild: Auto-fallback when frames repeatedly fail to render** — FIX — value 3 — effort S — risk low — category: resilience — wild
  Why: assumption: custom themes and extensions are part of the earlier ask ("customizable, extendable"). A broken theme file or plugin view should never take the run down. Catch render exceptions per view, log them, and switch to the built-in plain view after three failures.
  Done when: a theme with a bad color value and a view that raises each leave the run going. A one-line notice appears and the exception is in the log.

- **Validate themes and keybindings at load, with line-accurate errors** — FIX — value 3 — effort S — risk low — category: config
  Why: customizable themes and keybinds mean user-written files. Silent partial loads are the usual failure. Check the schema, contrast against the background, and key conflicts, and then name the file and key.
  Done when: a theme with a missing key or a duplicate binding exits with a message naming file, field and line, and the default theme still loads with `--theme default`.

- **Pause animation when the pane is hidden or output is piped** — PERFORMANCE — value 3 — effort S — risk low — category: efficiency
  Why: assumption: the TUI can run docked or in the background beside Claude Code. Rendering frames nobody sees wastes CPU on a project that sells being cheaper and faster.
  Done when: with stdout not a TTY or focus lost, the tick count drops to zero, and animation resumes on the next event.
