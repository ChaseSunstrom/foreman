# Brainstorm — lens: beautiful UI and motion

- **Replace confirm dialogs with a five-second undo bar** — FEATURE — value 4 — effort S — risk low — category: interaction
  Why: the pack shows the user wants reversal ("undo a whole run in one command"). Assumption: the pane and web UI ask before discarding a task.
  Done when: discarding a task shows an undo bar for 5 s, and pressing Enter or Esc in that window restores the task unchanged.

- **Collapse unchanged diff context into expandable chips** — FEATURE — value 3 — effort S — risk low — category: diff reading
  Why: assumption: the pane prints every context line, so on narrow widths the changed line gets buried.
  Done when: a diff with 40 unchanged lines shows one "… 37 lines" chip per hunk gap, and clicking it or pressing `e` expands that gap.

- **Freeze the user's text selection while the pane repaints** — FIX — value 4 — effort S — risk low — category: terminal
  Why: assumption: live repaints clear a selection the user is dragging across the pane's log.
  Done when: a selection made during a run keeps its cells unchanged across 50 journal events, checked by a repaint test that compares the selected cells.

- **Show progress as a bar with its own error range** — FEATURE — value 3 — effort S — risk low — category: progress
  Why: the pack has long, variable gates (the 480 s test kill, the 35-minute macOS cap), so a bare spinner hides whether a run is stuck. Assumption: last-run durations are already stored.
  Done when: a gate with a 120 s median shows "~90–150 s" beside its bar, and the range widens when a run exceeds the median by 50%.

- **Keep the last good view on screen when the web UI loses its feed** — FIX — value 4 — effort S — risk low — category: resilience
  Why: assumption: a dropped event stream blanks the web UI until a manual reload, and the stalled card needs the rest of the screen visible.
  Done when: cutting the stream for 30 s leaves the last state on screen with a "last update 30 s ago" pill, and the state refreshes on reconnect with no blank frame.

- **Fix the light/dark flash on first paint** — FIX — value 2 — effort S — risk low — category: web polish
  Why: assumption: the site and web UI apply the theme after CSS loads, so a light frame shows before a dark one.
  Done when: a capture taken 0 ms after navigation already has the final background colour, with no frame of the other theme.

- **Add a text-only mode for slow links** — PERFORMANCE — value 3 — effort M — risk low — category: low bandwidth
  Why: assumption: the web UI ships charts and a large SVG to every visitor, including phones on weak links.
  Done when: on a 100 kbps throttled profile, the stage rail and work bar are readable with under 150 KB transferred.

- **Peek a task's last proof on hover or long-press** — FEATURE — value 3 — effort S — risk low — category: navigation
  Why: the History list hides the proof behind a click, so checking a result means leaving the list.
  Done when: hovering a History row for 300 ms shows its proof command and exit code in a card, without navigating, and the card closes on mouse-out.

- **Mirror the stage rail and diff for right-to-left text** — FEATURE — value 2 — effort M — risk low — category: internationalisation
  Why: assumption: the layout hard-codes left-to-right order in the rail, gutter and receipt.
  Done when: with `dir="rtl"` the stage rail runs right to left and the diff gutter moves to the right, with a screenshot test on each surface.

- **Deal each task a playing card by its kind** — FEATURE — value 2 — effort M — risk low — category: delight
  Why (wild): tasks already have kinds (FIX, FEATURE, CLEAN, PERFORMANCE, SECURITY), and a card suit would make the list scannable at a glance.
  Done when: each task shows one card, and a test maps each of the five kinds to a fixed suit.

- **Let picked tasks swim to the front of a fish-tank queue** — FEATURE — value 2 — effort M — risk low — category: delight
  Why (wild): assumption: a queue with many tasks reads as a flat list, and motion that shows order could make priority visible.
  Done when: picking a queued task moves its glyph to the head of the lane within 400 ms, and reduced-motion mode jumps it there at once.

- **Fill a tide line in the web header as tasks close** — FEATURE — value 3 — effort S — risk low — category: progress
  Why (wild): the usage reset gives a weekly clock, and a rising line shows the week's progress without a number.
  Done when: the line rises one mark per closed task this week and resets at the usage reset, checked against a fixture of closed tasks.
