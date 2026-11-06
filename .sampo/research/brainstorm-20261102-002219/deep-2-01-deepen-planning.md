# Brainstorm — lens: deepen: planning

- **Plan the goal as a cell-filling DAG: one node per empty coverage cell** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: the request is "fill 58 empty coverage cells"; the grid rule says each cell holds a grounded idea, an existing path or a recorded n/a. Treat the 58 as a goal plan whose rows are cells, each with a state (empty, drafted, cold-read, grounded, n/a) and dependencies (a cell citing a predictor needs that predictor's interface first).
  Done when: `fm goal plan` on the coverage goal lists 58 rows with state and edges, and closing a row flips exactly that cell in coverage.md.

- **Lint each cell against the "real cell" rule before it counts** — FIX — value 5 — effort S — risk low — category: planning
  Why: steer "a cell counts only when it names a concrete capability grounded in a file or real gap, no reused phrasing". Merge this with the row-readiness lint (ready-to-build rules): a row cannot enter the plan if its text shares an n-gram template with another row.
  Done when: a test feeds two cells differing only by the area name and the lint rejects the second.

- **Make every plan row carry a probe, and fail the goal's "done" while any lacks one** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: merges "Flag a goal row with no probe" with "knows when it's actually done rather than merely stopped". The questions left ask which cells can only be planted, not measured; the probe field must say `measured`, `planted` or `n/a` honestly.
  Done when: `fm goal done` refuses with the list of rows lacking a probe, and the output separates measured from planted probes.

- **Backtestability triage as the first wave: sort cells by how much history exists** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the pack asks which of the 58 have too few events to backtest. Count events per cell's data source up front, and plan the data-rich cells first (they can be measured and teach the bar) and the sparse ones as explicit "plant and wait" rows with a revisit date.
  Done when: the plan prints a per-cell event count and a wave number, and a sparse cell is never marked grounded by measurement.

- **Citation liveness check: the sweep re-runs each cell's cited path, not only the file's existence** — CLEAN — value 4 — effort M — risk med — category: planning
  Why: the last question left says the sweep checks the file exists, but later generations can change a path so it no longer fires. Each plan row stores a one-line cheap check (grep for the symbol, or call the public interface) that the sweep re-runs.
  Done when: renaming a cited function turns its cell red in `fm genesis sweep` with the cell's name.

- **Cut the harness-dependence out in the plan: tag each row with the harnesses it was verified on** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: the standing rule says Foreman is not Claude-Code-specific, and a question asks which cells quietly depend on it. Add a `harness:` tag to rows; untagged or claude-only rows in a surface meant to be general get flagged.
  Done when: the plan lists cells whose probe ran only under claude-code, and a cell with a `fm code` probe passes.

- **Spike-first ordering: unknown-interface cells become short spike rows ahead of their dependents** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: `fmforesight` may not have a public interface a cell can cite. A spike row ("find or create the public entry point") must close before any cell that cites it; this follows the spike rule of failing with 2 or more approaches before filing to not-yet.md.
  Done when: the plan puts the interface spike ahead of every dependent, and a failed spike produces a not-yet.md entry with two recorded approaches.

- **Plan the acted-on versus ignored split into the forecast cells** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: a question asks which forecast the user acts on. Each anticipation output (prefetch files, drafts, sealed predictions) gets a row with its reader path; outputs with no reader are listed as candidates to wire or delete.
  Done when: the plan lists outputs with zero session-path readers, each either wired to a reader or removed.

- **Wild: the plan argues with itself: a rival decomposition drawn by a tool-less child that never sees the first plan** — FEATURE — value 3 — effort M — risk low — category: planning (wild)
  Why: assumption: blind second plans expose grouping mistakes the same way blind exams expose weak spots. The diff of two decompositions (rows in one, missing from the other) becomes the review list.
  Done when: a command prints rows present in only one of two plans, and at least one such row gets added or struck with a reason.

- **Wild: a "last 10 cells" budget bet: the user and Foreman each predict the finish wave, scored when it ends** — FEATURE — value 3 — effort S — risk low — category: planning (wild)
  Why: bets already exist in `fm outcomes --judgment`; pace on a long cell-filling goal is unusually forecastable, so the bet is cheap to score.
  Done when: a goal start records a predicted finish with a bucket and the finish writes a scored bet row.

- **Wild: a salvage value per row, so an interrupted run keeps what it filled** — FEATURE — value 3 — effort S — risk low — category: planning (wild)
  Why: the goal must survive crashes, compactions and usage limits; each cell fills independently and commits alone, so killing the run midway leaves a valid coverage.md with a correct count.
  Done when: killing the drive after 20 cells leaves exactly 20 filled, none half-written, and resume continues at cell 21.

- **Reserve a slack lane for steers that land mid-goal** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: the user steers often (many dated steers in this pack). The plan holds ~10% of rows as unassigned slack so a new steer replaces a row instead of reordering the DAG.
  Done when: filing a steer mid-goal adds or swaps a row and the plan prints the new count without losing ordering.

- **Finish line with a marginal-value floor: stop only when the remaining cells fall below it, and say so** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: "knows when it's actually done rather than merely stopped". "No empty cells" ends the whole run per the steer; for each cell the plan scores expected value and records an n/a with a reason instead of padding with a templated filler.
  Done when: the final report separates cells filled, cells n/a with a reason, and cells cut by the floor, and no cell is filled with reused phrasing.

Next question: Which of the 58 empty cells share a missing capability, so that one new capability fills many cells at once, and which ones need a recorded n/a?
Next question: What does the cold-read pass cost across 58 cells with the Haiku-then-Sonnet rule, and does it fit inside a single drive without a pause?
