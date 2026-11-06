# Brainstorm — lens: approaches

- **Fill each cell as a key in one goal receipt** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the Goal capability has no single output a cell can cite, so cells default to prose. Assumption: `fm goal status --json` or a similar verb exists or is cheap to add. Each cell becomes a key (`stage.resume.reconciled`, `surface.web.state`), and an unfilled cell is a missing key.
  Done when: `fm genesis sweep` lists a cell as filled only if its key appears in the receipt printed by a fixture goal run, and deleting a key turns that cell red.

- **Cap each filler's grounding effort and read exhaustion as a gap** — CLEAN — value 4 — effort S — risk low — category: coverage method
  Why: the pack's rule is that a cell counts only when grounded in a file or a real gap. A filler lane gets five greps and one MASTER.md search per cell. If it finds no `file:symbol`, the cell is recorded as `gap` with the queries it tried, not invented prose.
  Done when: every one of the 58 cells is either a resolvable `file:symbol` or a `gap` row with a non-empty queries-tried list, and none has neither.

- **Retrieve candidates with BM25 over MASTER.md and symbols, using no model** — PERFORMANCE — value 3 — effort S — risk low — category: coverage method
  Why: the zero-token arms are the pack's cheap default. Query each cell's "stage × surface" words against MASTER.md clauses and `plugin/lib` docstrings. Auto-propose the top hit above a threshold, and send the rest to a Haiku lane.
  Done when: a script prints a candidate per cell with its score, and a hand-checked sample of 10 shows at least 7 correct.

- **Write the finish card's "you can now…" lines first and trace every cell to one** — FEATURE — value 4 — effort M — risk low — category: reverse fill
  Why: cells are currently written from the grid, so they read as templated. Starting from the sentences a user would read at goal finish gives user-visible wording, and a cell with no sentence points at it as a gap or n/a.
  Done when: the draft finish card has at most 12 sentences, and each cell links to one sentence or carries a recorded n/a.

- **Verify cell citations with a golden transcript of a kill-and-resume run** — FEATURE — value 5 — effort M — risk med — category: evidence
  Why: the questions the earlier brainstorms left ask whether the cited behaviour still fires. One recorded run (start goal, plan, kill the session, compact, resume, finish) is replayed by the sweep. Cells cite transcript line ranges, so one run grounds many resume and crash cells at once.
  Done when: the sweep replays the transcript on a fixture repo, and breaking `fmcore` resume logic fails at least 3 cells by name.

- **Add a harness column set to every cell and mark Claude-only ones** — FIX — value 4 — effort S — risk low — category: portability
  Why: this answers the earlier question on harness dependence. Standing rule: Foreman isn't specific to Claude Code. Each cell carries `harness: any | claude-only | untested`, and the sweep counts "any" only if a no-`claude`-on-PATH probe passes.
  Done when: running the sweep with `claude` hidden from PATH changes the count of cells reported as "any".

- **Run column-rule fills with an exceptions list only for cells that differ** — CLEAN — value 3 — effort S — risk med — category: coverage method
  Why: many of the 58 cells are probably "same behaviour on a different surface". Writing one rule per column plus exceptions follows the standing rule against templated cells. Assumption: the linter treats rule-derived cells as distinct only if each names its own symbol.
  Done when: the grid renders 58 cells from at most 8 rules plus exceptions, and the templating lint passes.

- **Label each cell with its backtest class (backtestable, plant-only or unmeasurable)** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: this answers "which cells have too few events to backtest". A cell counts as measured only if the class is backtestable and its backtest ran. Plant-only cells report as planted.
  Done when: `fm genesis check` prints counts per class, and no plant-only cell is counted as measured.

- **Split fill by reach: cite the session path that reads the output, or mark it write-only** — FIX — value 4 — effort M — risk low — category: reach
  Why: this answers the earlier question on unread anticipation outputs. Cells whose output no session path reads (`fm next`, a hook or the drive) are filed as gap tasks rather than counted as filled.
  Done when: each filled cell names a reader (verb or hook), and a test deletes one reader and sees its cell go red.

- **Wild: let a tool-less child write the sweep's reject rules from five filled cells** — FEATURE — value 3 — effort M — risk med — category: adversarial check
  Why: the standing rule asks for checks from signals Foreman didn't author. A blind child sees five good cells and writes what a bad cell looks like, then we run its rules on all 58. Assumption: the child's rules are cheaper than a Sonnet cold read per cell.
  Done when: the child's rules reject a planted bad cell and pass all five exemplars.

- **Wild: use a web UI accessibility-tree snapshot per stage as the surface-column evidence** — FEATURE — value 3 — effort M — risk med — category: web UI
  Why: the mission surface is the web UI, and pillar 5 wants the real path. Drive the real page through fixture goal states (empty, active, stale, done) in a headless browser and cite the snapshot text, not a file.
  Done when: four stored snapshots exist and the surface-column cells cite them by name.

- **Wild: write a rival's goal-planner feature list blind and cell-match it** — FEATURE — value 3 — effort S — risk low — category: capability map
  Why: pillar 2 wants the capability map. A tool-less child lists what the best planners do (Spec Kit, Kiro, Devin plans), and each item must map to a cell or become a gap. Assumption: no network is needed, since the child works from its own knowledge.
  Done when: a table maps every listed item to a cell id or a filed gap task.

- **Wild: fill nothing in advance and let the 58 cells close only through real goal runs** — FEATURE — value 2 — effort L — risk med — category: usage-driven
  Why: avoid inventing cells at all. The night tick runs a canary goal through the stages, and a cell flips from empty to filled the first time the trace stamps its stage and surface. Unreached cells stay visibly empty.
  Done when: after two nightly runs, the filled-cell count rises only for cells whose stage appears in the trace.

Next question: Which of the 58 cells does a user actually look at on the Goal page, and does filling the ones nobody opens change any outcome?
Next question: If the sweep re-runs every cell's probe each generation, what is the wall-clock and token budget before it becomes the thing that fails?
