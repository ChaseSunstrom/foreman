# Brainstorm — lens: beautiful UI and motion

- **Pin a one-line Interpretation banner above the grid, with the sting cell lit** — FEATURE — value 4 — effort S — risk low — category: web UI
  Why: the pack's open question "when the user reads a Mission page, which cell do they open first"; the request page has no first-screen anchor. assumption: the Mission page renders in `plugin/templates/web/index.html`.
  Done when: a Mission fixture renders the banner text and exactly one cell carries the `sting` class, checked by a DOM test.

- **Draw each Exam as a meter-and-clock pair** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: every brief's Exam now owes an outcome measure and a live-state reading, and the two have different time behaviour: the meter shows value against target, the clock shows the reading's age. assumption: one card per brief.
  Done when: a brief with a 3-day-old reading shows a meter at its value and a clock labelled "3d", and a test finds both elements.

- **Ship one four-state verdict glyph (proven, unproven, overridden, could-not-read)** — FEATURE — value 5 — effort M — risk low — category: design language
  Why: steers call for "unproven" as a state that is never green, and the pane, web UI, site and CLI each draw verdicts their own way. Shape carries the state, not only colour.
  Done when: one component renders all four states in the web UI, and a test fails if any two share a shape or the `unproven` state renders green.

- **Design empty, stale and "can't read" states for every web view** — FEATURE — value 4 — effort M — risk low — category: states
  Why: "the service is down, offline" and "no Exam yet" are open questions in the pack; today a missing reading probably shows blank or zero, which reads as a pass. assumption: blanks currently render as zero.
  Done when: each web view has a fixture for the three states, and each prints a reason and the one command that fills it.

- **Fill the request grid as a coverage wash, not icons** — FEATURE — value 4 — effort M — risk low — category: visualisation
  Why: the grid has filled, empty and n/a cells, and a count of "N left out" is easy to skim past; a wash of tone makes holes visible from across the room. Pair it with a hatched pattern, so the state isn't carried by colour alone.
  Done when: a grid fixture with 3 empty cells shows 3 hatched cells, and a contrast test passes in light and dark themes.

- **Animate a cell filling when its brief closes, mapped to a state edge** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: motion should explain state, so only a real edge (open to closed) animates; the pane already tracks task close.
  Done when: closing a brief toggles one `filled` transition under 400 ms, and with `prefers-reduced-motion` the cell changes with no transition.

- **Show a dissent as a two-sided scale that tips when its outcome lands** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: this Mission's carried gap is scoring dissents against outcomes; the page should show a dissent as pending (level) until a 14-day close-survival record tips it. Pending must look different from lost.
  Done when: three fixtures (pending, upheld, overruled) render three distinct scale positions, and the pending one has no tilt.

- **Add a "since you looked" ribbon at the top of every surface** — FEATURE — value 4 — effort M — risk med — category: orientation
  Why: users return to an unattended tower and have to scan for what changed; the earlier idea of a "while you were away" card exists only for session start. assumption: a last-seen timestamp can be kept locally per surface.
  Done when: after two ledger changes, a reload shows "2 changes since 09:40", and a second reload shows none.

- **Gate the web UI on contrast, colour depth and reduced motion** — SECURITY? No: CLEAN — value 3 — effort S — risk low — category: accessibility
  Why: T-1217 shows the pane painting a background Foreman didn't choose, so contrast has already broken once without a test noticing.
  Done when: `python3 -m pytest` runs a check computing WCAG contrast for every token pair, and a planted 3:1 pair fails it.

- **Design a "stop" card for guard blocks with the safe alternative** — FEATURE — value 4 — effort M — risk low — category: states
  Why: the user dropped items about guard refusals that show a trailing hint, so the block message is already a UI the user reads; a designed card gives the reason, what would have happened and the one allowed command.
  Done when: a blocked-command fixture renders three labelled parts and the allowed command is copyable by one key.

- **(wild) Tear-off left-out slip** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: "Left out" is the product's most distinctive output. Draw it as a torn-edge slip at the bottom of a Mission page, and drag it off to save a copy as a file the user keeps. wild
  Done when: dragging the slip to the edge downloads a text file whose lines equal the page's left-out list.

- **(wild) Night-sky map of the request** — FEATURE — value 3 — effort L — risk low — category: visualisation
  Why: the grid renders empty cells as dark and filled cells as lit stars, so the unexamined region is literally dark; the user finds a hole by sight. wild
  Done when: a fixture with 12 cells renders 12 points, lit points equal filled cells, and a table twin lists the same data for screen readers.

- **(wild) A hard-hat lamp that dims as unexamined cells shrink and flickers on a stale reading** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: the logo is a hard hat. Letting its lamp mirror the coverage state gives an at-a-glance gauge in the tab icon and the tray (T-0325). wild
  Done when: the favicon changes between three states for fixtures of 0, half and all cells filled.

- **Scrub a Mission as a timeline of what was considered** — FEATURE — value 3 — effort L — risk med — category: motion
  Why: a user who wants to know why a cell is empty has nowhere to look; the Mission's lens runs and drops are ordered events. assumption: they are in the ledgers with timestamps.
  Done when: dragging a scrubber to a past time shows only the ideas present then, and the first and last frames match the start and final pages.

Next question: Which of these surfaces does the user actually look at, given they steer almost entirely by typed asks and `fm next`: is the web UI opened at all, per the usage records?

Next question: Do the verdict glyph and the fill/hatch rules survive a terminal pane with 16 colours and no truecolor, or do they need a separate text design?
