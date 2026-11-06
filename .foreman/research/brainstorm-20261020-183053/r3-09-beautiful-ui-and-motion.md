# Brainstorm — lens: beautiful UI and motion

- **Give every view one grid and spacing scale** — CLEAN — value 4 — effort M — risk low — category: design language
  Why: the user said the TUI "looked like crap with all the text"; the ideas list has motion and themes but no layout system. Assumption: views currently size and pad their panels ad hoc.
  Done when: all views take margins, gutters and column widths from one spacing table (2 or 4 cells), and a test fails if a view hardcodes padding.

- **Define semantic color roles with a contrast check** — FEATURE — value 4 — effort S — risk low — category: theming
  Why: the request is "not just static colors". Assumption: themes today map a handful of fixed slots. Roles like `focus`, `proof`, `refused`, `waiting`, `cost-warn`, plus a computed 3-step ramp each, let any widget pick meaning instead of hue. Contrast is checked against the probed background.
  Done when: a theme missing a role fails load with a named error, and `fm code tui --doctor` lists any role/background pair below 4.5:1.

- **Use box-drawing hierarchy instead of text labels** — FEATURE — value 4 — effort M — risk low — category: layout
  Why: assumption: much of the remaining "all the text" is labels like "Step 3 of 7: running". Rounded corners for the active card, single line for done, dotted for pending, and heavy rule for the focused one carry state without words.
  Done when: a golden frame of a 7-step plan has no "Step N of M" strings, and the active, done and pending states are told apart with colors stripped.

- **Add skeleton shimmer for pending content** — FEATURE — value 3 — effort S — risk low — category: loading states
  Why: the ideas list covers shimmer on the thinking line, not on placeholders for the diff, verify output and Gantt before they exist. Layout stays still when real data arrives.
  Done when: before the first verify event the verify card shows a shimmering placeholder of the final height, and the card's row count doesn't change when output arrives.

- **Give each view a designed empty and error face** — FEATURE — value 3 — effort S — risk low — category: states
  Why: "design empty, loading and error states" is listed once, as a bullet. This makes it its own deliverable: a small glyph drawing, one sentence, and the one key that gets you out, per view. Errors keep the last good data dimmed under a red edge.
  Done when: each view renders a distinct empty frame and error frame in golden tests, and each names its exit key.

- **Add a focus ring that travels** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: ease-between-states exists for stations, not for keyboard focus. When focus moves between cards, the highlight edge slides (about 120 ms, eased) rather than jumping, so the eye follows.
  Done when: moving focus renders at least 3 intermediate frames of the ring between cards, and none under `--calm`.

- **Draw the plan as a connected rail with branching for subagents** — FEATURE — value 4 — effort M — risk med — category: information design
  Why: the screenshot in the pack shows the pane with a stage rail and agents graph, but the TUI has a flat station track. Steps hang on a vertical rail, retries fork off a side branch and rejoin, and a failed-then-fixed step shows its loop visibly.
  Done when: a run with one retried step renders a fork-and-rejoin on the rail in a golden frame.

- **Add a type scale made of glyph weight and case** — CLEAN — value 2 — effort S — risk low — category: typography
  Why: terminals have one size, so the hierarchy comes from bold, dim, small caps (using spaced uppercase) and Unicode numerals. Three named text styles (`title`, `body`, `meta`) replace per-widget bold/dim choices.
  Done when: no widget sets bold or dim directly; a lint over the TUI source finds only the three style names.

- **Scale the layout by breakpoints with a docked-pane mode** — FEATURE — value 4 — effort M — risk med — category: responsive
  Why: the pack mentions "responsive layouts" and the docked pane's #262626 background (T-1217), but no named widths. Breakpoints at about 40, 80 and 120 columns each pick a different composition, and the 40-column one is built for the Claude Code side pane.
  Done when: golden frames at 40, 80 and 120 columns exist for every view, with no wrapped or truncated box edges.

- **Wild: Turn the finished run into a title-card sequence** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Closing a task plays a 3-second end-credits roll: goal, the proof that closed it, and files touched, scrolling up from a settled frame. It is skippable by any key and is the same content as the receipt card, in motion.
  Done when: closing a proved task plays the roll once, any key skips it, and `--calm` prints it as one static card.

- **Wild: Let the border be a progress ring around the whole screen** — FEATURE — value 3 — effort M — risk med — category: ambient
  Why: wild. The outer frame's lit portion runs clockwise as the plan's steps close, so progress is readable from across the room with no text. The color follows the semantic roles, turning to `waiting` when the run needs you.
  Done when: at 3 of 6 steps the lit part of the border covers half the perimeter in a golden frame, and its color changes when a run is waiting for the user.

- **Wild: Add a dim "memory trail" of the last five screens as ghost layers** — FEATURE — value 2 — effort L — risk high — category: motion
  Why: wild. When a view changes, the previous view lingers as a faint offset layer for half a second, like a motion trail. Assumption: the renderer can composite two buffers per frame.
  Done when: after a view switch, the next 5 frames contain cells from the old view at reduced intensity, and none under `--calm`.

- **Add a press-feedback flash on every control** — FEATURE — value 2 — effort S — risk low — category: micro-interaction
  Why: the key-hint bar flash is mentioned, but not the controls themselves. Each chip, tab or button inverts for about 80 ms when pressed or clicked, which confirms the input landed even when the result is slow.
  Done when: a simulated keypress produces one inverted frame on the target control before its action result.
