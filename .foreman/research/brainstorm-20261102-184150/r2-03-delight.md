# Brainstorm — lens: delight

- **Print a "Left out" slip at the end of every request** — FEATURE — value 4 — effort S — risk low — category: receipts
  Why: the request is "say what it left out"; the pack shows "N left out" on truncated lists but no end-of-request slip a user can keep. Short, five lines max, ranked by cost of being wrong, each with the flag or command that shows it.
  Done when: a finished Mission prints a slip of ≤5 lines, each naming a cell and a command, and an empty slip prints a count rather than "nothing".

- **Open the Mission page on its sting cell** — FEATURE — value 4 — effort S — risk low — category: web UI
  Why: an earlier question asks which cell the user opens first; assumption: it is the empty one that would hurt most, not the first in grid order.
  Done when: the page scrolls to and highlights the highest-sting empty cell on load, tested with a fixture grid.

- **Show a one-line interpretation banner above every Mission** — FEATURE — value 4 — effort S — risk low — category: clarity
  Why: the user's asks are long and compressed ("#2 Exhaustive thinking… Carried gaps…"); one plain sentence of how Foreman read it lets them correct it in seconds.
  Done when: every Mission page and finish card begins with an "I read this as:" line, and a cold child can recover the request's goal from that line alone.

- **Let a cell fill with a small animation when its brief closes** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: assumption: the grid is the Mission's face; motion that shows state change makes progress feel real. Respects reduced-motion and NO_COLOR.
  Done when: closing a brief changes the cell's state with a ≤300 ms transition, and no animation plays under `prefers-reduced-motion`.

- **Draw "unmeasured" as hatched, never green** — FEATURE — value 4 — effort S — risk low — category: design language
  Why: the carried gap is Exams with outcome and live-state readings; a reading that couldn't be taken must look different from one that passed. Shape, not colour alone.
  Done when: a snapshot test shows pass, fail, stale and unmeasured as four distinct glyph/pattern shapes at 16 colours.

- **Show dissents as a two-sided scale that tips on the outcome** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: dissents scored against outcomes is a carried gap, and the score is abstract; a scale that visibly tips toward the lens that was right makes it legible at a glance.
  Done when: a scored dissent renders with a tilt direction matching its recorded outcome, and an unobserved outcome renders level with a "not yet" label.

- **Give every empty state a "what I left out" line with the command that fills it** — FEATURE — value 3 — effort S — risk low — category: empty states
  Why: assumption: web views with nothing to show currently say little; an empty cell is a teachable moment.
  Done when: each web view's empty state names the one `fm` command that would populate it, checked by a test that parses the line.

- **Add a "run it yourself" line under every Exam** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user re-runs proof commands by hand (pack: "Notice when the user re-runs a proof command by hand"); a copyable line lowers that cost and shows Foreman has nothing to hide.
  Done when: each brief's Exam prints a single shell line that runs both its outcome measure and live reading, and it exits 0 or 1 in a scratch home.

- **Chime and badge a Mission closing with a first** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: small "first of its kind" moments (first dissent that beat its outcome, first cell filled from a left-out) are what people show others; opt-in only.
  Done when: the first occurrence of each named milestone prints a one-line badge once, and never again, recorded in a ledger.

- **Wild: Tear-off slip** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: wild. Render the left-out list as a torn-edge receipt that can be saved as a small PNG or SVG to paste in a chat or pin on a wall; the Genesis site gets a monthly wall of them.
  Done when: `fm` exports a slip as a self-contained SVG under 10 KB that renders without network.

- **Wild: Night-sky map of the request** — FEATURE — value 3 — effort L — risk low — category: wild
  Why: wild. Cells are stars: filled ones bright, n/a ones faint, empty ones dark gaps; constellation lines join cells a single brief touched. Darkness is what the eye lands on, which is the point.
  Done when: the web grid has a sky view toggle that renders from the same data as the table and a text-twin passes an accessibility check.

- **Wild: Hard hat lamp that dims as unexamined cells shrink** — FEATURE — value 2 — effort S — risk low — category: wild
  Why: wild. The logo is a hard hat; a status-line glyph whose brightness follows the share of cells examined gives the "how thorough was that" feeling without a number.
  Done when: the status line shows a 5-step glyph keyed to the cell coverage of the active Mission, and NO_COLOR falls back to text.

- **Kind wording for failed and empty cells** — FIX — value 3 — effort S — risk low — category: tone
  Why: assumption: gap reports read as accusations; saying "not yet looked at, here's why" keeps a user returning to them.
  Done when: a lint over Mission page templates rejects blame words from a short list, and the test fails on a planted one.

Next question: which part of a finished Mission does the user actually screenshot or paste elsewhere, and is that the part we design first?
Next question: does the user want to be delighted at all during an unattended run, or only on the morning card?
