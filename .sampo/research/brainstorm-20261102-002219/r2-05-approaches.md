# Brainstorm — lens: approaches

- **Triage the 58 cells before writing any prose** — CLEAN — value 5 — effort M — risk low — category: coverage
  Why: Lessons from Missions 3-6 say most of #2, #3, #11 and #12 was already built. Assumption: much of #4 is too (goal verb, baton, finish audit).
  Done when: every empty cell carries one of existing (file:symbol), gap (a task id) or n/a (a counterexample-search result), and `fm genesis sweep` reports zero templated or duplicated cells.

- **Fill from a rule table: columns are rules, cells are exceptions** — FEATURE — value 4 — effort M — risk med — category: coverage
  Why: the standing rule rejects templated cells, and the grid is stage by surface. A small table (stage rule → session path) generates the obvious cells, and prose is written only where the rule fails. Assumption: at least 20 of the 58 follow one rule.
  Done when: `coverage.md` for #4 is compiled from the table plus an exceptions list, and the templating check passes with no phrase reused across rows.

- **Dogfood: run #4 on the 58 cells themselves** — FEATURE — value 4 — effort M — risk med — category: goal engine
  Why: the capability is "turn a vague goal into a plan and carry it across crashes". Filling its own grid is a real multi-hour goal. Assumption: `fm goal` can hold 58 rows without the baton diverging.
  Done when: a goal of 58 rows is killed once mid-fill, resumes from files alone, and finishes with each cell's verdict recorded.

- **One cheap lane per surface column, a cold read per batch** — PERFORMANCE — value 4 — effort M — risk low — category: coverage
  Why: the pack's rule is independent S/M briefs in parallel lanes on the cheapest model. The cold-read rule (Haiku first, Sonnet decides on a non-pass) is already in force. Trade-off: lanes can duplicate phrasing, so a cross-lane overlap lint runs at merge.
  Done when: the lanes merge in order, each batch of 10 has a recorded cold-read verdict, and the cross-lane overlap lint is green.

- **Make each cell a re-runnable one-line probe** — FEATURE — value 5 — effort M — risk med — category: coverage
  Why: a cell counts only if grounded, and the questions left over ask whether a cited path still fires. Citing a file proves only that it exists. Assumption: most #4 behaviour (resume, finish check) can be driven by a fixture goal.
  Done when: the sweep re-runs every filled cell's probe, and deleting a cited function turns that cell red.

- **Two blind fillers; disagreement is the gap signal** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: the standing rule wants signals Foreman didn't author. Where two independent fillers disagree on existing versus gap, the cell is probably wrong. Trade-off: it costs twice the tokens, so run it only on cells the triage left ambiguous.
  Done when: the disagreement list is written, and every disagreeing cell is resolved by a probe rather than a vote.

- **Derive cells from replayed closed goals and tasks** — FEATURE — value 4 — effort L — risk med — category: evidence
  Why: the dropped-as-built ledger and the ~30 most recent closed tasks are real moments. A gap cell needs an incident anyway. Trade-off: the history has few multi-day goals, so some cells can only be planted, not measured.
  Done when: each gap cell links a ledger or decisions.md entry, and cells with no history are tagged "planted" rather than "measured".

- **Do less: fill only evidenced cells and hand the rest on with an expiry** — CLEAN — value 3 — effort S — risk med — category: scope
  Why: the standing rule says empty cells go to the next Seed and "no empty cells" ends the run, not a generation. Trade-off: this doesn't meet the Mission as written (58 filled), so the mission report must say how many were deferred.
  Done when: the unfilled cells each name an unreached reason and a revisit date, and the report states the count.

- **Anchor each cell to a public symbol and its session path** — CLEAN — value 4 — effort S — risk low — category: reach
  Why: the reach rule says a capability must be called by a real session path. Assumption: citing `fmforesight`-style internals breaks when modules move, so cell citations use a symbol name, not a line number.
  Done when: a lint rejects any cell lacking a symbol plus a named caller (session start, `fm next`, drive, skill or hook).

- **Add a read-only Goal page to the web UI as the surface-column probe** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the web UI is the only surface in this mission, and the pillars require screenshots before and after. The page shows rows, verdicts, stale and done states, and links to cells.
  Done when: the screenshot shows empty, loading, error and done states, and a stalled goal visibly differs from a finished one.

- **Wild: let a tool-less child invent the 58 cells blind, then diff against reality** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: wild. It uses a signal Foreman didn't author. Children never see the code, so what they propose that the repo lacks is a gap candidate, and what the repo has that they missed is a cell worth documenting.
  Done when: a diff file lists blind-only and repo-only cells, and each blind-only item is filed as a task or an n/a.

- **Wild: delete the cited feature in a scratch copy and see which cells survive** — CLEAN — value 3 — effort M — risk low — category: coverage
  Why: wild. A cell whose probe still passes after its feature is removed is decorative. Trade-off: it needs a per-cell removal recipe, so run it on a sample of 10.
  Done when: for the sampled cells, removal flips the probe red, and any survivor is rewritten or marked n/a.

- **Wild: reconstruct the goal from git and the ledger alone as a goal autopsy** — FEATURE — value 3 — effort M — risk med — category: goal engine
  Why: wild. If rebuilding "where were we" from the repo matches the stored baton, the resume cells are real. If not, the divergence is the gap (assumption: baton, ledger and repo can disagree after a kill).
  Done when: an autopsy command on a killed fixture goal reproduces the baton's open rows exactly, or prints each mismatch.

Next question: Which of the 58 cells are decidable by reading the code (existing or n/a), and which need a live fixture goal that is killed mid-run, so that the lane split follows cost instead of column?
Next question: Does the cold-read charter flag a cell that cites a real file but whose behaviour a later generation changed, and if not, what is the cheapest check that would?
