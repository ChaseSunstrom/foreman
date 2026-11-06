# Brainstorm — lens: capability map

- **Truecolor gradient + animated theme engine** — FEATURE — value 5 — effort M — risk low — category: look
  Why: the request is "not just static colors". Assumption: the TUI emits ANSI and nothing yet interpolates colors. Add 24-bit gradients on the station track, a breathing pulse on the active station, and a shimmer sweep over a running verify. Degrade to 256 and 16 colors, and honor NO_COLOR.
  Done when: a frame-capture test shows the active station's color differs across 3 consecutive ticks in truecolor and is static under NO_COLOR=1.

- **Frame-diff renderer with a 30fps tick loop** — PERFORMANCE — value 5 — effort M — risk med — category: rendering
  Why: assumption: animation needs flicker-free redraws. Keep a cell buffer, emit only changed cells inside synchronized-output markers (DEC 2026), and run the tick separately from model streaming so animation never blocks input.
  Done when: a 60-second run with animation on writes under X KB/s to the tty (X set in the test), with no full-screen clears in the byte stream.

- **Spinner and progress vocabulary per station** — FEATURE — value 4 — effort S — risk low — category: motion
  Why: T-0796 lists spinner, progress bar and motion as deferred. Give plan, edit, guard, verify and finish each a distinct braille or block animation. Step progress becomes a smooth sub-cell bar (▏▎▍…) that eases to its new value.
  Done when: a unit test renders the bar at 0.0 to 1.0 in 1/8-cell steps, and each station's spinner has a different frame set.

- **Guard-verdict micro-animations** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: guard verdicts are Foreman's identity. A refusal flashes red and shakes one column. A pass draws a short green check sweep. A held command shows a lock glyph closing.
  Done when: a recorded session shows a refused command's row cycling through ≥3 distinct style frames, then settling.

- **Live Gantt and token sparklines that scroll** — FEATURE — value 4 — effort M — risk low — category: charts
  Why: the steer ("looked like crap with all the text") already moved the TUI to a Gantt and token columns. Make them live: bars grow in real time, per-turn token cost shows as braille sparklines, and the cost-cap burn rate is a gauge that warms from green to amber to red as the dollar cap nears.
  Done when: a fake-model run with a $1 cap shows the gauge color change at 50% and 90%, asserted in a render test.

- **Command palette with fuzzy search (Ctrl-P)** — FEATURE — value 4 — effort M — risk low — category: navigation
  Why: T-0796 names the palette. The earlier TUI request wanted "customizable, extendable", and a palette gives keybindings, themes, views and plugin actions one discoverable entry point.
  Done when: typing "thm" lists theme actions and Enter applies one without restart, covered by a scripted-input test.

- **Mouse support and clickable ids** — FEATURE — value 4 — effort M — risk med — category: interaction
  Why: T-0796 lists clickable ids. Click a T-id to open its task, a file path to open its diff, and a chip to expand its output. Add the scroll wheel, plus OSC 8 hyperlinks where the terminal supports them.
  Done when: a synthetic SGR mouse click on a T-id opens that task's detail view in a test.

- **Theme pack and user theme files with hot reload** — FEATURE — value 4 — effort S — risk low — category: customization
  Why: "customizable, extendable" was in the original TUI ask. Ship themes such as dusk, paper, high-contrast and colorblind-safe, plus ~/.foreman/themes/*.toml that reload on save. Contrast is checked on load.
  Done when: editing a theme file changes the colors of a running TUI within 1 s, and a theme with contrast below 4.5:1 prints a warning.

- **Diff view with intra-line highlights and syntax color** — FEATURE — value 4 — effort M — risk med — category: diffs
  Why: the pack lists diffs as a station. Best-in-class tools (lazygit, delta) show word-level changes, side-by-side at wide widths, and fold unchanged hunks, with the new lines easing in.
  Done when: a diff of a one-word change highlights only that word, verified in the ANSI output.

- **Responsive layouts and a minimal mode** — FEATURE — value 3 — effort M — risk low — category: layout
  Why: assumption: it is a fixed layout today. Collapse to a one-line status bar under 60 columns and go three-pane above 160. Handle resize live, and degrade cleanly over SSH or in tmux.
  Done when: render tests at 50, 80 and 200 columns produce no overflow or wrapped chrome.

- **Session replay scrubber (wild)** — FEATURE — value 4 — effort L — risk med — category: replay
  Why: wild. Every run already has stations and events, so record them and play any past run back in the TUI with a timeline scrubber, speed control and jump-to-failure. It doubles as a demo generator that replaces the SVG and MP4 recording hacks.
  Done when: `fm code replay RUN` renders the same final frame as the live run and seeking to 50% shows the mid-run state.

- **Reactive ambient background (wild)** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. A subtle starfield or rain-line background in the idle margins that speeds up with token throughput, calms when the run is waiting on you, and goes dark red-tinted when the guard blocks. It is off by default under a "calm" setting.
  Done when: the toggle is persisted, and with it off the margin cells are blank in render tests.

- **Audio and bell cues plus terminal-title status (wild)** — FEATURE — value 3 — effort S — risk low — category: notifications
  Why: wild. Marathon unattended runs (the pack's showcase work) need a way to say "done" or "needs you". Set the terminal title to the stage and progress, send OSC 9/777 desktop notifications on finish or block, and optionally play a soft chime.
  Done when: a finish event emits the OSC title and notification sequences once, and nothing when notifications are disabled.

- **Plugin API for custom panels and widgets** — FEATURE — value 4 — effort L — risk med — category: extensibility
  Why: the original ask wanted "extendable". Let ~/.foreman/tui/*.py register a panel with a render(ctx) function that gets run state, plus keybinding hooks. Panels run under a time budget so a bad one can't stall the loop.
  Done when: a sample plugin panel appears in the layout, and one that sleeps 2 s is skipped with a visible error chip.

- **Golden-frame visual regression tests** — CLEAN — value 3 — effort M — risk low — category: testing
  Why: T-0166 and the heavy CI history suggest UI churn. Snapshot rendered frames (ANSI stripped, plus a color map) at fixed ticks per view, and add `fm code tui --snapshot` to update them.
  Done when: changing a glyph in one widget fails exactly one snapshot test with a readable diff.
