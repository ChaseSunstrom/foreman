# Brainstorm — lens: unspoken needs

- **Review the fill by surprise** — FEATURE — value 4 — effort S — risk low — category: review
  Why: assumption: the user can't read 58 cells, and the standing rules distrust templated or lazy-n/a fills. Show first only the cells whose class (existing, gap or n/a) differs from what the rule table predicted, or where Haiku and Sonnet disagreed. Everything else collapses to a count.
  Done when: the fill report's first screen lists only surprising cells, and a fixture with 3 seeded surprises among 20 plain cells shows exactly those 3.

- **Map the deferred "Later from" bundles onto cells before filing any gap task** — FIX — value 5 — effort S — risk low — category: dedupe
  Why: the open queue holds about 28 deferred bundles (T-0788..T-0869, T-0826..T-0832) and the user has dropped several items as already built. Many gap cells probably restate a parked idea. Each gap cell cites the existing task id or states "no match, searched: <terms>".
  Done when: no new gap task is filed whose title matches an open or deferred task. A test shows a cell about LSP blast radius linking T-0788.

- **Tie each cell to the user's words, or mark it tower-originated** — FEATURE — value 4 — effort S — risk low — category: provenance
  Why: the "asked" and steer streams show what the user actually needs, while the Genesis grid is the tower's own construct. Each filled cell names the steer or asked line it serves, or says "tower". The sweep prints the share that is tower-only.
  Done when: `fm genesis check` prints the user-grounded vs tower-only cell counts, and a cell with neither a citation nor the label fails.

- **Show a depth-vs-outcome table for thinking** — MEASURE (FEATURE) — value 5 — effort M — risk low — category: measurement
  Why: the lean-substance rule waits on growth that has no measurement, and the plan bets already exist (T-2507-era calibration). No view says whether deeper deliberation earned its cost. Group closed tasks by tier and plan depth and show reopen rate, first-time pass, cost and seconds.
  Done when: `fm outcomes --thinking` prints one row per tier. With under 20 tasks in a row it says "unmeasured", never a number.

- **Put a grid receipt of at most 10 lines in the final report** — FEATURE — value 4 — effort S — risk low — category: reporting
  Why: pillar 7 says user-only items go in the final report, and the user steers on "decide and record, don't ask". The receipt gives counts by existing, gap and n/a, the tasks filed, the costly decisions made, and the one-yes items.
  Done when: the final report ends with a grid block whose counts match `coverage.md` (checked by test), and every costly decision links its undo line.

- **Detect cells that contradict each other** — CLEAN — value 3 — effort M — risk low — category: coverage integrity
  Why: assumption: 58 cells written by different lanes will disagree. One cell says the plan gate refuses, another says it only advises, both citing nearby code. A linter extracts each cell's verb and refuse/advise word and flags pairs sharing a grounding file with opposite claims.
  Done when: a fixture with two opposed cells over one file fails the coverage pass and names both cells.

- **Turn the user's next correction into a cell diff within that session** — FEATURE — value 4 — effort M — risk med — category: learning loop
  Why: "what earlier brainstorms missed" lists asks the user had to make by hand (T-2525, T-2532, T-2533). On a recorded correction, Foreman names the cell that should have caught it, or proposes a new cell and a failing-first probe.
  Done when: replaying T-2532's request against the grid yields either a cell reference or a drafted new cell, and the draft is filed as a capture, not applied.

- **Pre-think deferred tasks on their revisit date** — FEATURE — value 3 — effort M — risk low — category: deferred work
  Why: T-2541 now carries deferred tasks with revisit dates to the critique, so a date arrives with nothing prepared. A cheap lane writes readings, options and blast radius into a plan draft on that date, so the revisit starts from a draft.
  Done when: a deferred task with today's date gets a `plan-draft` file without any session running. The file is never marked accepted.

- **Write an "if Foreman did nothing here" line per gap cell** — FEATURE — value 3 — effort S — risk low — category: prioritisation
  Why: assumption: the user wants gap cells ranked by consequence, and "58 gaps" reads as noise. Each gap names its cost: the ledger incident, correction, or "none seen". Cells with none get the lowest build priority.
  Done when: gap tasks are ordered by that evidence, and a cell with no incident is never filed above one with one.

- **Wild: Have a child write the post-mortem for next year** — FEATURE — value 3 — effort S — risk low — category: blind spots — wild
  Why: assumption: a tool-less child, told only the user's steers and this capability's text, that writes "how exhaustive thinking failed us a year from now" reaches failure classes nobody listed. Each class becomes a candidate cell, then goes through the grounding check.
  Done when: one run produces at least 5 failure classes, each marked already covered by cell X or a new candidate.

- **Wild: Show a thinking glyph on the status line** — FEATURE — value 2 — effort S — risk low — category: delight — wild
  Why: assumption: the user can't see whether the current task was deliberated at its tier. One small glyph reads "S: skipped on purpose", "L: readings, race, blast done" or "L: missing". It costs no context and runs from the same data as the plan gate.
  Done when: the status line prints the glyph for a task in each of those states, and the hook budget is unchanged.

- **Wild: Make cells fill from real near-misses overnight** — FEATURE — value 3 — effort L — risk med — category: capability map — wild
  Why: assumption: the night tick can replay the day's refused or edited plans against the grid. Any plan that hit no cell is a candidate gap, written to a morning file and never filed on its own.
  Done when: a recorded day with one plan-gate refusal produces one candidate line naming the unmatched stage and surface.

Next question: Which filled cells could pass every linter and cold read while describing a capability no session path ever reaches?
Next question: What did the user reverse or edit right after a plan was accepted, and does any cell cover that moment?
