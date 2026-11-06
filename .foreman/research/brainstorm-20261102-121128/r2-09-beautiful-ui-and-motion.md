# Brainstorm — lens: beautiful UI and motion

- **Define one design-token sheet for every surface** — CLEAN — value 4 — effort M — risk low — category: design system
  Why: assumption: the web UI (`plugin/templates/web/index.html`), site, `demo/live.svg`, and the foreman-ui pane each carry their own colors and spacing; T-1217 (pane background #262626 mismatch) is that drift showing up.
  Done when: one tokens file (color, space, radius, duration, easing) feeds the web UI, the site and the pane, and a test fails on a hard-coded hex in those files.

- **Give every receipt one verdict grammar: solid, hatched, outlined** — FEATURE — value 5 — effort M — risk low — category: receipts
  Why: earlier ideas want "unproven" and "overridden" as states beside "proven"; the visual form is unspecified. Color alone fails color-blind users and monochrome terminals. Assumption: no shared glyph/pattern set exists today.
  Done when: proven, unproven and overridden rows render with distinct shape/pattern plus a text label in the web UI and the terminal, and a snapshot test pins all three.

- **Animate the stage rail as a state machine** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: the README demo shows a stage rail (plan, edit, prove, close); motion should show *why* it changed. Assumption: transitions today are instant.
  Done when: each stage change plays a ≤250 ms transition tied to the event that caused it (e.g. the prove step pulses once on a real command exit), and `prefers-reduced-motion` swaps it for a static marker.

- **Ship designed empty, loading and error states on every web screen** — FEATURE — value 4 — effort M — risk low — category: states
  Why: assumption: the single-file `index.html` shows blank panels while ledgers load or are absent. This is also where "could not run" must read as a first-class state, not a blank.
  Done when: each screen has skeleton, empty (with the one next action) and error (with cause and retry) variants, and a test renders all three per screen.

- **Add a keyboard command palette to the web UI** — FEATURE — value 4 — effort M — risk low — category: navigation
  Why: T-1344 asks for type-to-jump on the `fm code` home; the user lives in the keyboard. The palette jumps to tasks, verbs and ids.
  Done when: Ctrl/Cmd-K opens a palette, typing `T-26` jumps to the matching task, and every result is reachable without a mouse.

- **Draw calibration as a reliability diagram with live bet dots** — FEATURE — value 4 — effort M — risk low — category: charts
  Why: recent commits (T-2610, T-2611) centre on Brier scores and base rates, which are numbers the user can't see at a glance. A diagram, with a bet settling as a dot sliding into its bin, makes the claim checkable.
  Done when: the Today view shows predicted-vs-observed by bin with a count per bin, an under-20-sample bin is drawn dashed, and a settled bet animates into place.

- **Make clickable task ids and verdicts one component** — CLEAN — value 3 — effort S — risk low — category: consistency
  Why: T-0796 (terminal UI polish: clickable ids) is deferred, while ids appear in commit lines, steers and receipts. Assumption: they render as plain text in places.
  Done when: every `T-NNNN` in the web UI and the terminal (via OSC 8) is a link that opens that task's card.

- **Add a ledger-health strip with outside-signal ticks** — FEATURE — value 4 — effort M — risk low — category: observability UI
  Why: earlier rounds asked for timer liveness and cross-checks for gauges Foreman wrote itself. Rendered as one thin strip (timers, bets, canary), each with a tick showing whether an outside signal agrees, it stays glanceable and honest.
  Done when: the strip shows one chip per gauge with agree, disagree or no-outside-signal, and a stale gauge turns amber with its age.

- **Show the guard as a visible tripwire moment** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the guard stops commands the user would never want run, but the save is invisible. Assumption: the block today is a text line.
  Done when: a blocked command shows a brief, calm banner with the command, the rule that matched and the override path, and it never exceeds one screen line in the terminal.

- **Fix the docked pane background and add a contrast test** — FIX — value 3 — effort S — risk low — category: accessibility
  Why: T-1217 notes Claude Code paints the pane #262626 while Foreman's palette differs; blocked, but a palette that adapts to the painted background is within reach.
  Done when: the pane samples or is told the host background, text/background contrast passes WCAG AA in both, and a test fails below 4.5:1.

- **Wild: Play a finished day back as a scrubbable timeline** — FEATURE — value 4 — effort L — risk med — category: replay
  Why: wild. Sessions already log tool calls, stage changes and proofs; a scrubber with a time-bar lane per subagent (like the live tree) lets the user watch a day in 20 seconds and click into any receipt.
  Done when: `fm replay <day>` opens a page with a draggable playhead, lanes per agent and a receipt popover at each close, with the keyboard playing and pausing.

- **Wild: Let the hard hat carry the mood of the calibration** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The logo is a hard hat with a check mark; its tilt, check state or glow could reflect the week's held-rate and Brier trend, so health reads from the corner of the eye.
  Done when: the header logo has at least three states mapped to named thresholds, each with alt text, and a static fallback is used under reduced motion.

- **Wild: Turn the tower into a living map** — FEATURE — value 3 — effort L — risk med — category: visualization
  Why: wild. Genesis keeps generations, Missions, coverage cells and steers in files (site/genesis); a grid where cells fill as rows close, with lineage lines between generations, would make 13 capabilities by surfaces by stages comprehensible.
  Done when: the Genesis page draws the coverage grid with empty, grounded and n/a cells distinct, and a new generation animates in cell by cell from the data file.

- **Wild: Hatched "unproven" rendered as a visible fog over unrun checks** — FEATURE — value 3 — effort S — risk low — category: honesty UI
  Why: wild. When a UI check can't run (no display), a cloud overlay on that receipt row, which clears only when a real run lands, makes absence of proof physically visible instead of a missing green tick.
  Done when: an unrun check renders with the fog overlay and reason text, and it disappears only after a run record for that check exists.

Next question: Which web screens does a user actually open weekly (from any view logs), so motion and polish budget goes there first?
Next question: Does the terminal pane share a renderer with the web UI, or must each verdict/chart be drawn twice?
