# Brainstorm — lens: approaches

- **Derive cells from a rule table, not 58 sentences** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the standing rule rejects templated cells, yet the pack shows 58 empty cells for "Exhaustive thinking" and many prior ideas on filling by rule. A task-kind × stage table (readings, options, race, edge cases, blast radius, depth) where each entry cites one symbol or an n/a reason makes distinct cells fall out of the structure.
  Done when: `fm genesis sweep` reports 0 empty cells for capability #2 and the templating lint finds no shared 20-line shingle between any two cells.

- **Probe each cell against the live repo before writing it** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: the Lesson from Missions 3 and 4 says most ideas were already built. One grep pass over MASTER.md and plugin/lib, shared by all fillers, sorts every cell into existing / gap / n/a before prose.
  Done when: each cell file lists its triage class and the grep hit (path:symbol), and gap cells each name a task id.

- **Do less: mark n/a cells with a counterexample search** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: many surfaces (web UI only) make stages like "hook-time" truly n/a. An n/a counts only when a recorded search for a counterexample comes back empty, with an expiry date.
  Done when: every n/a cell carries a search command, its empty output and an expiry, and the sweep rejects one without them.

- **Fill with two independent fillers and treat disagreement as the gap** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: assumption: a single writer biases toward templated wording; the steer requires cold Haiku-then-Sonnet reads. Disagreement between two blind fills is a cheap signal of an unclear cell.
  Done when: a run emits a disagreement list and each listed cell is resolved by the Sonnet cold read with a quoted line.

- **Reuse exam scenarios as the coverage probes** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: the standing rules demand coverage be real and measured by signals Foreman didn't author. Child-authored exam scenarios already exist; mapping each to the cell it exercises proves the cell without new prose.
  Done when: `fm exam` output lists, per cell, at least one scenario id or marks it "unprobed", and gap cells go red only if unprobed and in a gap class.

- **Run the fill as one lane per stage column, merged in order** — PERFORMANCE — value 3 — effort S — risk low — category: parallel lanes
  Why: the Parallel Missions steer says S/M briefs run in parallel fm lanes. Columns are independent, so lanes cannot collide on rows if coverage.md is sharded by capability with a write-owner lint.
  Done when: the lanes merge with no conflict and the owner lint passes on the merged file.

- **Show the 58 cells as a web UI plan page with a click-to-fill state** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the only surface is the web UI and the user cannot see grid progress except in a file; empty/loading/error states are Pillar 4.
  Done when: a screenshot shows the grid with filled, gap, n/a and unread cells, each linking to its evidence.

- **Mark a cell "unread" until a cold read passes** — CLEAN — value 3 — effort S — risk low — category: reliability
  Why: the filing rule says Haiku reads first, Sonnet decides on any non-pass. Counting only read cells prevents silent credit.
  Done when: the sweep's count excludes cells without a recorded read verdict.

- **Delete a deliberation step for each one a cell adds** — CLEAN — value 3 — effort M — risk med — category: lean
  Why: the lean ratchet and "pay by deletion" ideas appear repeatedly; gap cells that produce features must not grow the hook budget unmeasured.
  Done when: each gap task closed from this Mission names a cleanup candidate or a "pending measurement" label.

- **Wild: Let a tool-less child guess the 58 cells blind, then diff against the repo** — FEATURE — value 4 — effort M — risk low — category: blind spots
  Why: wild; the child never sees Foreman's code, so what it proposes that the repo lacks is a real gap, and what it misses shows where the cells are redundant.
  Done when: a diff file lists child-only ideas, each filed as a task or dropped with reason.

- **Wild: Refuse the 59th cell unless one is retired** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: wild; the idea list shows the grid grew from 58 to 61 across missions. A cap forces merging cells into real distinct capabilities.
  Done when: the sweep fails a grid over the cap with no retirement recorded.

- **Wild: Compute the grid live, store only exceptions** — CLEAN — value 4 — effort L — risk med — category: architecture
  Why: wild; coverage.md as generated output removes rot, with the file holding only gap tasks and n/a reasons.
  Done when: deleting the generated section and re-running regenerates an identical grid.

- **Spot-check five random cells with the user in one-word answers** — FEATURE — value 3 — effort S — risk low — category: user trust
  Why: the user's steers reject templated cells; a five-cell sample at the report catches wording they dislike cheaply.
  Done when: the final report lists five cells with yes/no marks and any "no" files a fix task.

Next question: Which of the 58 cells have no session path (hook, `fm next`, drive, skill) that calls them, per the reach check?
Next question: What would a user returning after a week see for a deliberation that died silently, and which channel shows it?
