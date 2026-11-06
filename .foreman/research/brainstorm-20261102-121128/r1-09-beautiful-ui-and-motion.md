# Brainstorm — lens: beautiful UI and motion

- **Give every receipt one visual verdict grammar** — FEATURE — value 5 — effort M — risk low — category: design language
  Why: "Which UI checks can't run… how does the receipt say 'unproven' so it can't be read as a pass?" and "override isn't proof" are open. Pack shows proven/held/unproven text only. Assumption: statuses are plain text today.
  Done when: web UI, the foreman-ui pane and `fm task finish` output render proven, unproven, overridden and failed with distinct shape plus color (not color alone), and a snapshot test fails if two states share a glyph.

- **Draw "unproven" as hatched, never green** — FEATURE — value 5 — effort S — risk low — category: accessibility
  Why: The open question about headless CI, no display or no browser. A diagonal-hatch fill and an outlined icon make absence of proof look visibly empty.
  Done when: a receipt with a skipped UI check renders the hatched state in the web UI and a text marker in the terminal, and a contrast test passes at 4.5:1 in light and dark.

- **Animate the stage rail to explain state** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: The demo shows a stage rail, work bar and Activity lanes. Motion should say what changed: a segment fills when a proof command runs, pulses while waiting, and a single settle on close. Assumption: the rail is currently static between redraws.
  Done when: the web UI rail animates only on state transitions, and `prefers-reduced-motion` turns each animation into an instant change, covered by a test.

- **Ship designed empty, loading and error states for every web screen** — FEATURE — value 4 — effort M — risk low — category: states
  Why: With 2117 files and many ledgers (bets, exams, outcomes, genesis), many screens are empty on a fresh install. Assumption: empty states are bare tables. T-0862/T-0863 first-hour deferrals support it.
  Done when: each screen in `plugin/templates/web/index.html` has a skeleton, an empty state saying which command fills it, and an error state with a retry, checked by a screenshot test per state.

- **Show the calibration as a reliability diagram** — FEATURE — value 4 — effort M — risk low — category: data viz
  Why: Recent work (T-2610, T-2611) is about Brier scores, base rates and bet windows, shown as numbers. A diagonal calibration plot with bucket dots sized by count and an "early misses" ghost layer makes the verdict readable.
  Done when: the web UI shows a diagram from `fm outcomes --judgment`, with split by harness (the new field) toggleable, and unsettled bets drawn hollow.

- **Make the Today charts one shared chart kit** — CLEAN — value 3 — effort M — risk low — category: design language
  Why: T-0166 notes `register.tsx` is overloaded, and the pane, the web UI and the site each draw their own bars. Assumption: duplicated drawing code.
  Done when: one module supplies the bar, sparkline and time-bar primitives, and the pane and web UI import it with no remaining copies.

- **Fix the pane background mismatch** — FIX — value 3 — effort S — risk low — category: polish
  Why: T-1217 says Claude Code paints the docked pane #262626, so Foreman's palette clashes. Detect the paint and derive the palette from it.
  Done when: the pane renders with no visible seam at 48;2;38;38;38 and at the default background, in a captured-frame test.

- **Add a ledger-health strip with outside-signal ticks** — FEATURE — value 4 — effort M — risk med — category: ops gauge
  Why: The question about gauges trusted only because Foreman wrote them. Show timer liveness, bet settlement and canary state as a strip where each lamp has a "self-reported" or "externally confirmed" ring.
  Done when: `fm doctor` and the web UI show the strip, a lamp whose systemd `LastTriggerUSec` contradicts the ledger turns amber, and a test injects that contradiction.

- **Wild: Play the session back as a scrubbable timeline** — FEATURE — value 4 — effort L — risk med — category: replay — wild
  Why: assumption: events (plan, edit, proof run, guard block) are timestamped in the task log. A scrubber replays the work bar, diffs and guard stops, so you can see where it went wrong.
  Done when: opening a closed task in the web UI offers a scrubber that steps through at least plan, edit, proof and close events in order.

- **Wild: Show the guard as a visible tripwire** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: The guard stops commands in bypass mode, and its saves are invisible. A brief red-edge flash in the pane plus a "blocked, here's why" card with a running tally of saves makes the quiet value felt.
  Done when: a blocked command shows the card in the pane and the web UI, and the tally increments across sessions.

- **Wild: Turn the tower into a living map** — FEATURE — value 3 — effort L — risk med — category: genesis viz — wild
  Why: `site/genesis` already publishes tower data, and coverage.md is a capability-by-surface grid. Render it as a heatmap whose empty cells glow, and generations fade in as layers, so gaps are visible at a glance.
  Done when: the genesis page draws the grid from coverage data, empty and templated cells are visually distinct, and a generation slider changes it.

- **Wild: Give the hard hat a mood** — FEATURE — value 2 — effort S — risk low — category: delight — wild
  Why: The logo is a hard hat with a check. Its tilt could carry the status line (level while proven, tipped when held, a spark on a guard save) in the tray icon (T-0325), the site favicon and the pane header.
  Done when: the favicon and pane header switch between three hat states by task status, with a static fallback.

- **Add a keyboard command palette to the web UI** — FEATURE — value 3 — effort M — risk low — category: navigation
  Why: T-1344 asks for type-to-jump on the fm code home, and T-0796 for clickable ids. The ids T-2624 style appear everywhere. One ⌘K palette jumps to any task, bet or exam.
  Done when: pressing ⌘K or Ctrl+K opens a fuzzy palette that jumps to a task id, and every screen is reachable by keyboard alone.

- **Mark override and unproven rows with a persistent badge** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: "When the user overrides an unproven row by hand, who records that the override isn't proof?" The badge stays on the row in every list and export.
  Done when: an overridden row shows "overridden by you, not proven" in the list, the receipt and the exported report.

Next question: Which screens does the user actually open, and how often, so motion effort goes where eyes are?
Next question: Does the foreman-ui pane have a measured redraw cost, so animation can't push the hook latency bench past its gate?
