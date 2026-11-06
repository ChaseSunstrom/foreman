# Brainstorm — lens: beautiful UI and motion

- **Delay loading feedback 300 ms so fast reads never flicker** — FIX — value 4 — effort S — risk low — category: loading states
  Why: assumption: the web UI and pane show a spinner or skeleton as soon as a read starts, and most journal reads finish in a few ms, so the screen flashes. Skeletons are already on the list, but nothing covers when they appear.
  Done when: a read that resolves in under 300 ms shows no loading element at any point in a recorded frame sequence, and a read over 300 ms shows one within 50 ms of the threshold.

- **Damp the finish estimate so the number never jumps backwards** — FEATURE — value 4 — effort S — risk low — category: progress honesty
  Why: second-order on the queue finish-estimate idea: a raw estimate re-computed on each closed task can move from 40 minutes to 2 hours and back. A smoothed value with a visible error range keeps trust.
  Done when: replaying a recorded queue where two tasks run long, the displayed estimate never decreases by more than 5% between consecutive events, and the range shown brackets the actual finish in at least 90% of replays.

- **Move queue reorders with FLIP so a moved task slides to its new row** — FEATURE — value 3 — effort S — risk low — category: list motion
  Why: assumption: when a task is picked, deferred or bumped, its row jumps and the eye loses the thread. FLIP keeps the row's identity visible and needs no library.
  Done when: moving row 5 to row 1 in a test fixture starts that row's transform at its old offset and reaches zero within 200 ms, and rows that did not move carry no transform.

- **Glide one focus indicator between controls instead of snapping per element** — FIX — value 3 — effort S — risk low — category: focus states
  Why: assumption: each control draws its own focus outline, so keyboard focus appears to jump and sometimes doubles. One indicator that moves between targets reads as one place of attention.
  Done when: tabbing across five controls in the web UI moves a single indicator node, each move takes at most 180 ms, and with reduced motion it jumps with no transition.

- **Honour forced-colors mode so status shapes survive high contrast** — FIX — value 3 — effort S — risk low — category: accessibility
  Why: assumption: Windows forced-colors mode strips backgrounds, box shadows and the pulse, so a status drawn only with colour, shadow or motion can vanish. The per-status shape idea covers shape but not this mode.
  Done when: under forced-colors emulation in the browser test, every status keeps a visible border or text mark, and the full-pass seal and failure crack stay distinguishable.

- **Let one element animate at a time on each screen** — FEATURE — value 4 — effort M — risk med — category: motion arbitration
  Why: assumption: with lanes, graph, work bar and pulse all reacting to the same event, the screen never rests. A small arbiter gives one element the motion and shows the others as an instant text change.
  Done when: an instrumented run with three simultaneous state changes records at most one element with an active transform at any frame, and the other two show their new text within one frame.

- **Tune hover intent so tooltips don't fire while the pointer crosses** — FIX — value 2 — effort S — risk low — category: hover behaviour
  Why: assumption: moving the pointer across the stage rail or lanes opens every tooltip in turn. A hover-intent delay stops the flicker and keeps the one the user stops on.
  Done when: crossing three controls at 300 px/s opens no tooltip, and holding still for 400 ms opens exactly one.

- **Snap the pane's width to its nearest stop on release** — FEATURE — value 2 — effort S — risk low — category: layout motion
  Why: assumption: the pane has a few useful widths (narrow, half, full), and a free drag can land between them and clip a row mid-draw.
  Done when: releasing a drag at any width settles on the nearest stop within 250 ms, and no frame shows a half-drawn row.

- **Animate chart data changes but never the axes** — FIX — value 2 — effort S — risk low — category: chart motion
  Why: assumption: the History and Today charts re-scale their axes on each update, so bars slide under a moving scale and the numbers become hard to read.
  Done when: updating the Today chart with new data keeps the axis tick values and positions fixed for the transition, and only bar heights change.

- **Wild: let closed tasks gather dust that wipes away when you open them** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild — a task untouched for a week gets a faint layer on its History row, and opening it wipes the layer in one stroke. It rewards returning and marks what has sat unread, with no alert.
  Done when: a closed task untouched for 7 days shows the dust layer at 30% opacity, clicking it clears the layer in at most 300 ms, and the layer is absent in reduced-motion mode.

- **Wild: paint each day's History background as deterministic marbled ink** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild — one swirl of ink per closed task gives each day a pattern that is recognisable at a glance and needs no chart to read. The same day always renders the same pattern, so screenshots match.
  Done when: rendering the same day's tasks twice produces byte-identical SVG, the SVG is under 8 KB for 50 tasks, and the page has no text contrast drop below WCAG AA.

- **Wild: draw the status glyphs from the user's own pen strokes** — FEATURE — value 2 — effort L — risk med — category: personal identity
  Why: wild — a glyph set traced once from the user's handwriting makes each run look like theirs. Assumption: the user's terse, direct register suits a hand-drawn mark more than a stock icon.
  Done when: a sample of at least 20 traced glyphs maps to the 12 status glyphs, each renders at one terminal cell in the pane and at 24 px in the web UI, and a fallback set is used when no sample exists.
