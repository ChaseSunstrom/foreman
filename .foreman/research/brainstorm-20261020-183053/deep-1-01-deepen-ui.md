# Brainstorm — lens: deepen: ui

- **Build one "scene graph" renderer with a frame-budgeted animation clock** — FEATURE — value 5 — effort L — risk med — category: ui engine
  Why: the existing ideas (depth, focal "now" scene, paint budget, motion linter, color budget, bytes/sec cap) all need one place that owns time and paint. Assumption: fm code's TUI currently draws screens directly. One scene graph with a single tick, easing, dirty-rect diffing and per-frame budgets turns those into settings of one engine instead of seven features.
  Done when: a test drives the TUI with a fake clock, and a 60-second replay stays under the configured bytes-per-frame and colors-per-frame while a tween (e.g. the station track advancing) renders ≥5 distinct intermediate frames.

- **Animate state transitions, not decoration (motion grammar)** — FEATURE — value 5 — effort M — risk low — category: motion
  Why: the user wants "not just static colors" yet already said text-heavy output looks bad. Assumption: motion must explain state. Define a small grammar: a step that starts pulses once, a passing check "locks" with a sweep, a guard refusal shakes one cell-width and holds red, a retry rewinds the track. Each maps to one named state change, and idle states are still.
  Done when: every state transition in the registry has a named motion in a table, and a test fails if a motion runs while the run state is unchanged for 2s.

- **Gradient and shimmer progress built from truecolor with graceful 256/16/mono fallback** — FEATURE — value 4 — effort M — risk low — category: color
  Why: "not just static colors". Work bar, Gantt bars and token columns get interpolated ramps (OKLCH, not RGB), a moving highlight on the active step, and a ramp-quantizing fallback tied to detected color depth. Assumption: current themes are flat palettes.
  Done when: rendering the same frame at truecolor, 256, 16 and NO_COLOR gives four snapshots, each distinct in hue steps, and the NO_COLOR one is still readable by glyph shape alone.

- **Add sub-cell smooth bars and sparklines (eighth-blocks, braille)** — FEATURE — value 4 — effort S — risk low — category: charts
  Why: station track, change bars and token columns look chunky at cell resolution. Eighth-block and braille drawing gives 8× horizontal resolution, so bars grow smoothly instead of jumping a column.
  Done when: a bar for 37.5% of 10 cells renders with a fractional-width glyph, and a snapshot test pins it.

- **Ship a theme gallery with live preview, hot reload and a `fm code theme` doctor** — FEATURE — value 4 — effort M — risk low — category: themes
  Why: the TUI task asked for customizable and extendable themes and keybindings. Editing a theme file should repaint the running TUI within a frame, show contrast ratios, and warn when a state relies on color alone (pairs with the existing lint idea).
  Done when: saving a theme file in a second shell repaints a running TUI under 300 ms, and `fm code theme check` fails on a pair below WCAG 4.5:1.

- **Record and replay a run as a deterministic "cast" for demos and regression** — FEATURE — value 4 — effort M — risk low — category: replay
  Why: the README leads with a recorded demo (demo/live.svg, mp4), so showing the TUI matters. A run's event stream plus the frame clock can replay exactly, export to SVG/GIF-ready frames, and serve as golden tests for visual changes.
  Done when: `fm code replay RUN --svg out.svg` produces byte-identical output twice, and a CI test diffs it against a golden.

- **Make a "heartbeat" ambient strip that proves liveness without noise** — FEATURE — value 3 — effort S — risk low — category: status
  Why: it combines the "why is this so quiet" and "mute the quiet" ideas. One line under the track shows a slow breathing glyph while the model is thinking, with elapsed time and the last event's age. After 30s with no tokens it says what it is waiting on (model, tool, verify run).
  Done when: with a fake model that stalls, the strip names the wait kind after the threshold, and it shows no animation when the run is paused for the user.

- **Wild: Turn the run into a living terrarium** — FEATURE — value 3 — effort L — risk med — category: delight
  Why: wild. An optional `--scene garden` view where tasks are plants: a step grows a stem, a passing proof blooms, a guard refusal wilts a leaf until fixed. The same state data is drawn as pictures, which matches the "show pictures, not text" steer, and people will screenshot it.
  Done when: the scene renders from the same run-state object as the default view, and the two never disagree in a test that compares step counts and pass/fail totals.

- **Wild: Sonify the run with terminal bell and optional soft tones** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. Off by default; a quiet tick on a passed check, a low tone on a refusal, a chord on close. Uses the bell or a local audio command only when enabled in settings, so nothing is sent anywhere.
  Done when: with sound on, a run emits exactly one cue per passed check and refusal in a recorded test, and with it off emits none.

- **Wild: Time-scrub the run like a video editor** — FEATURE — value 4 — effort L — risk med — category: replay
  Why: wild. A timeline along the bottom (the Gantt becomes the scrubber): drag or arrow through the run, and the whole screen (plan, diff, verify output) rewinds to that moment, then jump back to live. Builds on the cast format and the remembered per-task view idea.
  Done when: in a finished run, moving the scrubber to a step's start time shows the diff and station state as they were then, and `End` returns to live.

- **Wild: Morph diffs as they are written (typewriter patch view)** — FEATURE — value 3 — effort M — risk med — category: diff
  Why: wild but grounded in the "ghost cursor" and "morph failing test to passing" ideas. Combine them: hunks stream in with removed lines fading to dim red and added lines resolving from a brighter tint to steady green, then the proof stamp lands on the hunk when the covering test passes.
  Done when: replaying an edit event produces at least 4 frames for a hunk, the last shows the proof stamp only if a passing run covers that file.

- **Adapt layout to width with named breakpoints, down to a one-line mode** — FEATURE — value 4 — effort M — risk low — category: layout
  Why: the Foreman pane is docked beside Claude Code, so widths vary (assumption). Define breakpoints (≥140 full dashboard, 100 two-column, 60 stacked, <40 one-line). Each reuses the same widgets with fewer parts, and resize animates between them rather than snapping.
  Done when: a test renders at widths 30, 60, 100 and 160 and each snapshot has no wrapped or truncated glyph rows, with the one-line mode showing task, step and verdict.

- **Add a visual regression harness with frame snapshots and a perf gate** — CLEAN — value 4 — effort M — risk low — category: testing
  Why: the repo already gates on fm doctor, e2e and bench_hooks; a flashy TUI without the same gate will rot or flicker. Snapshot frames as text with ANSI escaped, fail on unreviewed diffs, and bench frame time and bytes so paint cost stays within a budget.
  Done when: `python3 plugin/tests/...` renders 20 canonical states, compares them to goldens, and fails if median frame render exceeds the budget on a 200-event replay.

- **Keep the UI honest with a truth strip that cross-checks pictures against the log** — SECURITY — value 3 — effort S — risk low — category: trust
  Why: the TUI turns evidence into pictures (check chips, change bars). A tiny footer recomputes pass/fail and changed-line totals straight from the event log and flags any mismatch, so animation polish can never hide a wrong state. Assumption: the log is the source of truth.
  Done when: injecting a deliberately wrong chip count in a test makes the strip show a visible mismatch marker, and normal runs show a quiet check.
