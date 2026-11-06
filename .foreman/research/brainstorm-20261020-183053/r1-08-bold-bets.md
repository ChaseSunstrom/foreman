# Brainstorm — lens: bold bets

- **Add a frame-timed animation engine with easing and a reduced-motion fallback** — FEATURE — value 5 — effort M — risk med — category: motion
  Why: the user called the TUI "static colors" and asked for animations. T-0796 lists "progress bar, spinner, motion", and the earlier redesign added view fades. Assumption: fades are currently ad hoc, not on a shared clock.
  Done when: a test drives the engine with a fake clock and checks that tweened values (station-track progress, bar widths) follow the easing curve. With `NO_MOTION=1` the same state change renders in one frame.

- **Animate harness state as a living station track** — FEATURE — value 5 — effort M — risk low — category: motion
  Why: the pack shows the station track, check chips and change bars exist as pictures. State changes (plan to step to verify to guard verdict) are the natural things to animate. Assumption: they currently redraw instantly.
  Done when: a recorded session shows a pulse travelling along the track on each station transition. Chips flip from pending to pass or fail with a short sweep, and a snapshot test captures the mid-transition frame.

- **Render truecolor gradients and a theme engine with live-reloaded palettes** — FEATURE — value 4 — effort M — risk low — category: themes
  Why: "not just static colors" plus the earlier ask for a "customizable, extendable" TUI with themes. Assumption: themes are currently flat color maps.
  Done when: editing a theme file changes the running TUI within 1s. Gradient fills degrade to 256-color and 16-color terminals with tests for each depth.

- **Detect terminal capability and pick the best renderer** — FEATURE — value 4 — effort M — risk med — category: rendering
  Why: T-1217 shows Claude Code painting a pane background #262626, so terminal quirks are real. Assumption: one rendering path is used today.
  Done when: the TUI picks a tier (kitty graphics/sixel, truecolor, 256, mono) from the environment, and `fm code tui --tier mono` renders every view with no color-only information.

- **Draw a sparkline and braille-resolution Gantt of the whole run** — FEATURE — value 4 — effort M — risk low — category: data viz
  Why: the Gantt and token columns exist, but braille cells give 2×4 sub-cell resolution. Long unattended runs (the marathon work) need a compressed view.
  Done when: a 2-hour run fits one row of the Gantt. Tokens and cost per minute show as live-updating sparklines, checked against a fixture run.

- **Make ids, steps and diffs clickable with mouse hover previews** — FEATURE — value 4 — effort M — risk low — category: interaction
  Why: T-0796 names "clickable ids". Hover over a task id or step to see its criteria and last evidence in a popover.
  Done when: an OSC 8 link opens the task, and a mouse hover event over a step shows a popover in a pty-driven test.

- **Add a keybinding and layout config with a command palette** — FEATURE — value 4 — effort M — risk low — category: customization
  Why: the TUI task asked for "keybindings" and extendability. T-0796 lists "palette".
  Done when: `~/.foreman/tui.toml` remaps a key, and Ctrl-P fuzzy-opens any view, task or action. A test covers the remap and the palette result.

- **Record and replay sessions as shareable animated clips** — FEATURE — value 4 — effort M — risk low — category: sharing
  Why: the README leads with `demo/live.svg` and an MP4 built by hand. A built-in `fm code tui --record` would turn any run into that asset.
  Done when: a finished run produces an animated SVG under 1 MB that replays the TUI frames, with idle gaps compressed.

- **Make guard verdicts physical: a refusal shakes the frame and draws a red ripple** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the guard stopping a dangerous command is Foreman's signature moment but is probably only a text line. Needs a motion budget and a toggle.
  Done when: a refused command triggers a 300 ms effect and the verdict text is still readable in the final frame. The effect is off when motion is reduced.

- **Wild: Turn the run into a living "factory floor" diorama** — FEATURE — value 3 — effort L — risk med — category: wild
  Why: wild. The "Foreman" metaphor suggests tiny sprites for the planner, builder and guard moving between stations, with the work item as a crate on a belt. A fun alternate view to screenshot and share.
  Done when: `fm code tui --view floor` shows a crate moving through the stations in step with real events, and a test maps each event type to a sprite action.

- **Wild: Sonify the run with a quiet ambient soundtrack** — FEATURE — value 2 — effort M — risk low — category: wild
  Why: wild. Long unattended runs mean the user is often away. Pass, fail, refusal and finish get distinct tones, optional and off by default.
  Done when: `--sound` emits terminal bell or a local player call per event class, and nothing plays without the flag.

- **Wild: Let the model design its own theme from a sentence** — FEATURE — value 3 — effort S — risk low — category: wild
  Why: wild. `fm code theme "rainy Tokyo at night"` asks the configured model for a palette, validates contrast, and saves it as a theme file. This reuses the model client from T-1211.
  Done when: the command writes a theme that passes a WCAG contrast check on all text roles, and an invalid reply falls back to the current theme with an error message.

- **Auto-snapshot-test every TUI view across themes and sizes** — CLEAN — value 4 — effort M — risk low — category: quality
  Why: heavy visual and motion work regresses silently, and the project already ratchets other budgets (context tax, CPU time). Assumption: no frame snapshot suite exists yet.
  Done when: the CI job renders each view at 80×24 and 200×60 in each built-in theme and fails on an unreviewed diff.

- **Keep the render loop cheap with a frame-time budget ratchet** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: animation adds CPU on runs that last hours, and CI has already failed on CPU-time bounds. The TUI must not tax the harness.
  Done when: a test asserts idle TUI CPU stays under a set percent of one core. Redraw rate drops to 1 fps when nothing moves.
