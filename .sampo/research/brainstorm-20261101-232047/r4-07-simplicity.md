# Brainstorm — lens: simplicity

- **Fill the 58 cells from a task-kind by stage table** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the pack's 58 empty cells repeat the same rows and columns; earlier ideas already note templating is the risk. One table (task kind × stage) with each entry a verb path or a recorded n/a gives every cell a distinct reference without 58 sentences.
  Done when: `fm genesis check` reports 0 empty Exhaustive-thinking cells, and the templating linter passes with no cell sharing a 20-line shingle with another.

- **Make a cell one resolvable reference of at most 140 characters** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the standing rule says a cell counts only if it names a concrete capability grounded in a file. A cell that must resolve to a symbol or ADR stops prose bloat.
  Done when: a lint fails any cell over 140 characters or whose reference does not resolve by grep.

- **Collapse the plan gate's checks into one `plan lint` verdict** — CLEAN — value 4 — effort M — risk med — category: planning
  Why: pack lists readings, options, falsifier, tier floor, undo line and first-reading diff as separate checks. One verb with one scored result and one fix command is less to learn and cover.
  Done when: `fm plan lint` returns pass/fail with a single next command, and the old per-check verbs delegate to it.

- **Derive depth from one number** — CLEAN — value 4 — effort M — risk med — category: planning
  Why: tier labels, blast radius, reversibility and the race trigger each pick depth separately. One value (blast × irreversibility) set once and shown in one line removes four partly overlapping knobs.
  Done when: a test shows readings, race and research triggers all read the same depth value, and the plan prints "depth N because …".

- **Pay for every deliberation step with a deletion** — CLEAN — value 4 — effort S — risk low — category: lean
  Why: the lean ratchet has growth but the pack lists many added steps (rival, race, door ledger, confidence ledger). A ship check pairing an addition with a named removal keeps the thinking layer from growing.
  Done when: `fm ship` refuses a commit adding a deliberation verb without a retired-verb entry.

- **Show the deliberation as three lines at close** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption: the user reads receipts, not ledgers. Lines are: readings chosen, approach and runner-up, what would flip it.
  Done when: `fm task finish` prints exactly those three lines for tier M and above, and one line for S.

- **Stop asking when one reading is left alive** — FIX — value 3 — effort S — risk low — category: asking
  Why: standing rule says never block on process questions; ambiguity measured as disagreement already exists in ideas. Make the stop condition a single check (more than one live reading AND a one-way step).
  Done when: a test with one live reading and a one-way step proceeds with a receipt, and two live readings stops.

- **Mark most cells n/a or existing with the grep that proves it** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: Lesson from Missions 3 and 4: most ideas were already built. Expect many of the 58 cells to point at existing paths.
  Done when: each existing or n/a cell carries a grep command that returns a hit or, for n/a, a recorded surface-detector reason, and a probe re-runs them all.

- **Grep once and share the result with every filler** — PERFORMANCE — value 3 — effort S — risk low — category: coverage
  Why: parallel fillers each re-derive what MASTER.md and plugin/lib contain. One shared index of verbs and files cuts tokens and keeps cells distinct.
  Done when: the fill reads a single generated index file, and a run shows one grep pass rather than one per cell.

- **Wild: Refuse the 59th cell unless one is retired** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: wild; the grid has grown by rule each generation. A fixed cell budget forces merging near-duplicates.
  Done when: the coverage linter fails when the total cell count rises without a recorded retirement.

- **Wild: Compute the grid live and store only exceptions** — CLEAN — value 4 — effort L — risk med — category: coverage
  Why: wild; if reference rules per task kind and stage generate the cells, coverage.md only needs overrides and n/a reasons.
  Done when: `fm genesis coverage` prints the full grid from rules, and coverage.md holds only overrides.

- **Wild: Have a tool-less child compress the 58 cells to the distinct capabilities they really are** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: wild; it may show that 58 cells are really about 12 capabilities, which makes later fills a matter of pointing instead of writing.
  Done when: a recorded diff lists which cells collapse into which capability, and the number of distinct capabilities is reported.

- **Delete the race verb; a race is N lanes plus a judge file** — CLEAN — value 3 — effort M — risk med — category: planning
  Why: assumption: race, rival and picker share lane machinery. Reusing lanes removes a verb and a surface to cover.
  Done when: a race runs through the lane verb with a judge file, and the standalone race verb is removed with its tests moved.

Next question: Which of the 58 empty cells would still be empty if fm genesis grow were allowed to add a "none needed" status, and would that status itself be abusable?
Next question: How many Exhaustive-thinking verbs have no caller from a session path, and would deleting them leave any cell uncovered?
