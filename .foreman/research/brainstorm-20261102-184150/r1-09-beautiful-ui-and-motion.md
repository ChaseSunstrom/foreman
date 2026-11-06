# Brainstorm — lens: beautiful UI and motion

Lens: beautiful UI and motion. Gen 4 Mission 1 is "exhaustive thinking": the request grid, the left-out receipt, dissents scored against outcomes, and Exam readings. The pack already lists many UI ideas (grid board, stale badges, hatched "unproven", one verdict component, stage-rail motion). These go past them, toward the screens that make exhaustiveness *felt*.

- **Draw the left-out receipt as a torn-edge slip** — FEATURE — value 4 — effort M — risk low — category: receipts
  Why: the Mission's point is that Foreman "says what it left out"; the pack has the receipt as data but no visual form that distinguishes it from the finish card. A slip with a perforated edge, set apart from the green close card, is read as a separate object.
  Done when: a rendered Mission page shows the left-out slip as its own element with a distinct class, and a screenshot test confirms it is present and not nested inside the verdict card.

- **Fill the request grid with a coverage wash, not icons** — FEATURE — value 4 — effort M — risk low — category: grid
  Why: the grid is rows by columns of filled, empty and n/a cells. Use area and texture instead: filled = solid, empty = open outline, n/a = diagonal hatch with its falsifier on hover. This reads in about 2 seconds, and colour-blind users are covered by texture alone.
  Done when: the grid renders correctly in a greyscale screenshot, and the three states are distinguishable in a test that samples pixel patterns.

- **Animate a cell filling when its brief closes** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: motion should explain state. A cell flipping from outline to solid on a real ledger close shows that "exhaustive" is a changing quantity. It runs once and respects reduced-motion.
  Done when: with `prefers-reduced-motion` off, the cell's class transition fires exactly once per close event. With it on, there is no transition and the end state is identical.

- **Show a dissent as a two-sided scale that tips on the outcome** — FEATURE — value 4 — effort M — risk low — category: dissent
  Why: the carried gap is "dissents scored against outcomes". A balance glyph that rests level while the outcome is unobserved and tips toward whichever side the later result favoured makes the score visible without reading a number. A fourth "never observed" state keeps it level and dashed.
  Done when: a dissent card renders four distinct glyph states from fixture data (upheld, overruled, mixed, unobserved), each with an accessible text label.

- **Make Exam readings a two-line "meter and clock" pair** — FEATURE — value 4 — effort S — risk low — category: exam
  Why: each Exam now names an outcome measure and a live-state reading. Render the outcome as a gauge with its target tick and the live reading as a timestamped number that fades with age. Absent lines show a visible empty socket instead of vanishing, so a missing `outcome:` is seen, not silent.
  Done when: a brief with no `live:` line renders an empty-socket element, and a stale reading has a lower opacity than a fresh one in a snapshot test.

- **Give every empty state a "what I left out" line** — FEATURE — value 3 — effort S — risk low — category: empty states
  Why: assumption: the web UI's empty states currently say "nothing here". An empty page is a place where Foreman can show the nearest-miss canary and the one command that fills it, which supports the Mission directly.
  Done when: every web view's empty state contains a copyable `fm` command and passes a lint that rejects the bare strings "No data" and "Nothing here".

- **Scrub the Mission as a timeline of what was considered** — FEATURE — value 3 — effort L — risk med — category: timeline
  Why: exhaustive thinking is a process (lenses, grounding, drops). A horizontal scrubber that replays the grid being filled and ideas being dropped, with the drop reason in a tooltip, makes the reasoning auditable.
  Done when: dragging the scrubber to a past timestamp renders the grid and drop list as they were at that time, matching the ledger replay.

- **Pin a single "interpretation" banner above every Mission** — FEATURE — value 4 — effort S — risk low — category: clarity
  Why: the user's words are the thing most easily misread, and the earlier ideas list a one-line interpretation. Design it as a quoted banner with the user's words on the left and Foreman's reading on the right, with a diff underline where they differ.
  Done when: the Mission page's top element contains both strings, and a test fails if the reading is blank.

- **Dim the grid by recency of the user's touch** — FEATURE — value 3 — effort S — risk low — category: heat
  Why: the pack asks whether a passing cell is "covered or just unvisited". A faint heat overlay, off by default, shows cells nobody has asked about, as a toggle rather than a second grid.
  Done when: toggling heat changes cell opacity according to the fixture's ask counts and does not change the cell states.

- **Wild: Let the left-out slip be physically torn off and kept** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Dragging the slip off the page animates a tear and saves it to a "kept" tray, which becomes a promise ledger the next Mission reads. It turns dismissing into a deliberate, rememberable act.
  Done when: the tear gesture adds the item to the kept list in state, which survives reload, and a keyboard "keep" button does the same.

- **Wild: Render the grid as a night-sky map where empty cells are dark** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Filled cells glow, n/a cells are muted, and empty cells are black. Constellation lines join cells covered by the same brief. Dark patches then literally show the unexplored space.
  Done when: an alternate theme renders the same grid data as points with brightness mapped to state, and a toggle swaps to the table view with identical cell counts.

- **Wild: Give the hard hat a lamp that dims as unexamined cells shrink** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The logo is a hard hat. A small lamp on it shows grid completeness in the pane header and the site. It is steady and never flashes, so it stays calm.
  Done when: the header lamp's brightness value equals the filled-over-total cell ratio from the same data the grid uses, checked in a test.

- **Respect colour-depth and reduced motion in the grid and slip** — FIX — value 3 — effort S — risk low — category: accessibility
  Why: the pack notes the docked pane background mismatch (T-1217), so terminal palette handling is already fragile. Use a 16-colour fallback with shape glyphs for the three cell states.
  Done when: rendering with NO_COLOR and with 16-colour output both yield distinguishable cell glyphs, checked by a snapshot test.

Next question: which of the grid's states does the user check first on a phone, and does the left-out slip need its own notification-sized form?
Next question: when the web UI renders from a stale snapshot, which of these animations must be suppressed so motion never implies live data?
