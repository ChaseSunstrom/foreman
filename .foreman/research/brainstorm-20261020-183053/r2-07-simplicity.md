# Brainstorm — lens: simplicity

- **Cut the TUI to one screen with a drill-down key** — CLEAN — value 5 — effort M — risk med — category: simplicity
  Why: the user said it "looked like crap with all the text" and the fix produced several views (station track, chips, Gantt, token columns). Round 1 mostly adds more on top. assumption: the current TUI still has 4+ separate views.
  Done when: a fresh `fm code` run opens on a single screen with the focal "now" line, station track and one summary strip; every other view is one key away and Esc returns, verified by a frame test.

- **Delete the panels with zero keypresses** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: the pack lists nothing about use data; Foreman already logs hook and command use. assumption: the TUI can count view opens locally.
  Done when: `fm code tui --usage` prints per-view open counts from local logs, and any view with 0 opens over 30 days is removed or listed in a tidy brief.

- **Make the TUI a pure function of the event log** — CLEAN — value 5 — effort M — risk med — category: architecture
  Why: replay, golden frames, SVG export and the web mirror (all already proposed) each need state rebuilt from events. One `render(events, t, size) → frame` makes them all free. assumption: the harness already writes an event log.
  Done when: live mode and replay call the same render function, and a test feeds a recorded log and gets byte-identical frames both ways.

- **Collapse animation to three named motions** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: the ideas list names about 20 separate effects (ripple, shake, confetti, shimmer, breath, particles). A design-led team ships a small vocabulary. assumption: no motion primitive exists yet.
  Done when: the code has exactly three motion functions (pulse, ease, flash), each effect is built from them, and a grep finds no other time-based color code.

- **Ship one theme with two knobs** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the gallery, hot reload and animated palettes are listed, but the user's complaint was "static colors", not too few themes. One accent hue and a light/dark switch derive every slot through the gradient ramp.
  Done when: `theme.toml` of at most 3 lines recolors the entire TUI, and a test confirms every slot is derived with no hardcoded RGB outside the ramp.

- **Zero-config first launch** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: customizable and extendable were requested, but nothing says defaults are good. Detect capability, motion preference and size automatically with no setup prompt.
  Done when: running with an empty HOME under truecolor, 256-color and NO_COLOR terminals gives a correct render each time with no prompts and no config files written.

- **Print the one-line status instead of opening the TUI when piped** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: CI and logs get escape junk if the TUI starts non-interactively. assumption: no non-tty path exists.
  Done when: `fm code tui | cat` emits a single plain-text status line and exits 0, with no escape codes.

- **Render with one 150-line stdlib-only file, no framework** — CLEAN — value 3 — effort M — risk med — category: dependencies
  Why: Foreman is stdlib-oriented (stdlib model client) and the CI matrix includes macOS and Linux 3.12. A tiny diffed-buffer renderer avoids adding Textual or Rich. assumption: the current renderer is ad hoc.
  Done when: the renderer module has no third-party imports and a test at 80x24 draws a full frame with a changed-cells-only second pass.

- **Wild: Make the TUI a single sentence** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: a calm mode that shows only a plain sentence ("Step 3 of 5, checking tests, 2 min in") that changes color and cadence with state. It would be the most-used view by far.
  Done when: `--sentence` shows one line that updates on every station change and flags a red step in its color.

- **Wild: Make a still frame carry the whole run** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: with no animation, one static image should still tell the story. A "contact sheet" prints the final frame with the track, Gantt and chips, shareable in a PR comment.
  Done when: `fm code tui --last` prints a self-contained colored frame from the last run's log, and it matches a golden file.

- **Wild: Make the harness bell itself quiet when it's fine** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: the "needs you" alert and terminal-title status are both proposed. Combine them into the rule "silent unless it needs you": no motion, no sound, a dim screen when all is well, and one change when it doesn't.
  Done when: in a healthy 10-minute fake run the screen redraws under 1 time per second on average, and a stalled step produces exactly one visible alert change.

- **Pin the TUI's cost in the bench** — PERFORMANCE — value 3 — effort S — risk low — category: reliability
  Why: Foreman's identity is cheaper and faster; the TUI must not tax a run. The existing context-tax ratchet pattern applies.
  Done when: a test running a 1,000-event fake session at 30fps asserts the CPU time stays under a fixed budget, and fails if exceeded.
