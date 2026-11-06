# Brainstorm — lens: approaches

- **Fill cells by dogfooding Exhaustive thinking on each cell** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: the cells are about #2, so run `fm graph blast` and the plan gate on "fill cell R×S×T" and store the plan record's id as the cell's grounding. A pack-listed fix ("ground each idea before proposing it") is the lesson from Missions 3 and 4.
  Done when: each filled cell cites a plan record id that `fm genesis check` can open, and a cell citing a missing id fails the sweep.

- **Let the surface detector decide n/a mechanically** — CLEAN — value 3 — effort S — risk low — category: n/a rules
  Why: the pack says "Surfaces found: web UI". Cells for surfaces the project doesn't have (car, watch) need no prose. Assumption: coverage.md has a surface column the detector can read.
  Done when: an n/a cell for an absent surface is written by the verb with the detector's output as its reason, and a surface the detector finds can't be marked n/a this way.

- **Prove each cell with a probe that fails on the parent of the feature commit** — FEATURE — value 5 — effort M — risk med — category: red-first grid
  Why: the "Coverage must be real" steer, plus the repo's red-first habit. Use `git log -S` to find the introducing commit, run the probe at its parent and at HEAD, and count the cell only if it fails then and passes now.
  Done when: `fm genesis cells --verify` prints red-at-parent and green-at-HEAD per cell, and a cell that passes at both is flagged as not grounded.

- **Add inherit-with-condition cells** — FEATURE — value 3 — effort S — risk med — category: schema
  Why: many of the 58 cells likely share one plan-gate path. A cell may say `inherits: plan×web UI if <probe>`, and a lint re-runs the probe for the new surface. This is the "do less" approach without the templated sentences the steer rejects. Assumption: the "no phrasing reused across rows" lint accepts a structured pointer.
  Done when: an inherit cell passes only while its condition probe passes, and two inherit cells with identical text still trip the duplicate lint.

- **Serve one cell at a time with `fm cells next`** — FEATURE — value 3 — effort S — risk low — category: workflow
  Why: filling 58 cells in one pass is where the templated wording comes from. The verb hands out the highest-risk empty cell with its file anchors and the neighbours' wording to avoid, and accepts only a grounded answer.
  Done when: the verb returns one cell, refuses a submission that matches a neighbour, and the empty count drops by one.

- **Fill the cells with one cheap lane per cell and a cold read per batch** — PERFORMANCE — value 4 — effort M — risk med — category: parallel fill
  Why: Pillar 1 says independent tasks go in parallel builder lanes on the cheapest model. Haiku writes a cell, a Sonnet cold read decides on any non-pass (the 2026-11-01 cold-read rule), and cells are merged in row order.
  Done when: 58 cells land, each with a cold-read verdict recorded, and the run's cost is logged against the budget.

- **Derive plan-stage cells from the refusal codes in the code** — FEATURE — value 4 — effort M — risk low — category: extraction
  Why: every distinct refusal in the plan gate, `fm task finish` and the race trigger is a real, differently worded behaviour. Scanning for them gives cells that can't reuse phrasing. Assumption: the refusals sit in greppable string constants.
  Done when: each extracted refusal maps to a cell or a recorded "already covered by cell X", and a new refusal without a cell fails the sweep.

- **Require a ledger or decisions.md incident for each gap cell** — FIX — value 3 — effort S — risk low — category: evidence
  Why: the Missions 3 and 4 lesson was that most ideas were already built or had never failed. A gap cell with no incident becomes "pending, no evidence" rather than a task.
  Done when: every gap cell names an incident id or is marked pending, and no pending cell creates a task.

- **Triage the 58 cells into existing, gap and n/a before writing any prose** — CLEAN — value 4 — effort S — risk low — category: triage
  Why: the pack shows #2 has many deferred "Later from T-07xx" items and most of the capability is probably built. A deterministic grep-evidence pass gives the user one count (for example 40/12/6) to approve.
  Done when: `fm genesis cells --triage` prints the three counts, each with a cited file or reason per cell.

- **Add a click-to-fill action on empty cells in the web UI** — FEATURE — value 3 — effort M — risk med — category: web UI
  Why: web UI is the only surface found, and Pillar 4 wants states that move. An empty cell opens a panel with its triage track and starts the one-cell lane. Assumption: the web UI can already start lanes.
  Done when: clicking an empty cell starts a lane, the cell shows a loading state, then filled or an error with the refusal text.

- **Wild: let the cells be filled by usage** — FEATURE — value 3 — effort M — risk med — category: passive grounding
  Why: wild. A hook stamps a cell whenever a real session uses a deliberation verb on that surface and stage, so cells still empty after a month are the real gaps. Assumption: hook events can carry a surface tag.
  Done when: a session that runs the plan gate stamps its cell with the session id, and the stamp shows in the cell's record.

- **Wild: propagate coverage like a sudoku** — FEATURE — value 2 — effort M — risk high — category: derivation
  Why: wild. When rows and columns share a probe, a verified cell implies its neighbours' preconditions, so Foreman fills a minimal set and proposes the rest as candidates that still need their own probe. It must never count a derived cell as filled.
  Done when: the verb lists derived candidates separately and none counts toward the filled total until its probe passes.

- **Wild: have a writer describe each cell from the web UI screenshot alone** — FEATURE — value 3 — effort M — risk med — category: blind write
  Why: wild. A tool-less child sees only the screenshot and the stage name and writes what it expects deliberation to look like. Where it expects something the UI doesn't show, that is the gap. This pairs with Pillar 4's screenshot rule.
  Done when: each web UI cell has a blind expectation, a match or mismatch mark, and every mismatch becomes a gap task.

Next question: Of the 58 empty cells, how many are cells where the existing feature path is real but the column's surface can't reach it, as opposed to cells with no capability at all?
Next question: What do the 58 cells cost to keep true, since each probe has to rerun on every sweep and counts against the lean ratchet?
