# Brainstorm — lens: reliability

**Answers to earlier questions (reliability lens):**
- Probes that call `fm` verbs on files run on any harness. Probes that need a hook event (compaction survival, guard blocks) quietly depend on Claude Code. Each probe should record the harness it ran on.
- Ask-stream backtests are unavailable for cells that need long multi-day goals, because the pack shows few such events. Those cells can only be planted and replayed, not measured.

- **Falsify the finish oracle at the goal's start commit** — FEATURE — value 5 — effort M — risk low — category: done-detection
  Why: the gen-0 text for #4 says it "knows when it's actually done rather than merely stopped". An oracle that is also green on the pre-goal tree is vacuous. The pack has the per-task "fails without the change" proof, but no goal-level equivalent.
  Done when: `fm goal finish` refuses and names the vacuous check when the goal's oracle passes at the recorded start commit, tested with a planted always-true oracle.

- **Define "empty cell" with a placeholder corpus** — FIX — value 4 — effort S — risk low — category: coverage
  Why: the mission is "fill 58 empty cells", so the count depends on the parser's definition of empty. A cell holding `-`, `TBD`, `see above`, `same as row N`, `?` or a bare `n/a` with no reason must count as empty or templated, not filled. The pack shows no such corpus.
  Done when: a test feeds 20+ placeholder variants to the coverage parser and each counts as empty, while a cell with a cited file and a reason counts as filled.

- **Fuzz the coverage.md parser with pipes and CRLF** — FIX — value 4 — effort S — risk low — category: coverage
  Why: probes are shell commands, and `a | b` inside a markdown table cell splits the row. That can silently shift columns and miscount the grid. Assumption: cells are still stored as a pipe table.
  Done when: a fuzz test with pipes, backticks, CRLF, trailing columns and escaped pipes round-trips every cell unchanged, or fails loudly with the line number.

- **Reject collateral edits in a lane's cell fill** — FIX — value 4 — effort S — risk low — category: fill integrity
  Why: parallel lanes (steer on Missions 5-8) fill cells in the same file. A lane that "tidies" a neighbour cell changes work that was already cold-read.
  Done when: the merge step diffs coverage.md before and after and refuses any lane whose patch touches a cell outside its assignment, tested with a planted stray edit.

- **Keep a dead-letter list for cells that fail twice** — FEATURE — value 4 — effort S — risk low — category: fill integrity
  Why: the standing rule says a failed spike gets 2 or more different approaches and then goes to not-yet.md with its blocker. A cell that fails the cold read twice should follow the same path, not be filled with filler or retried forever.
  Done when: a cell failing two fills with identical approaches is refused a third identical attempt, and a cell failing with two different approaches is written to not-yet.md with its blocker and shown as "dead-letter" in status.

- **Make oracle outcomes three-valued** — FEATURE — value 4 — effort M — risk low — category: done-detection
  Why: a timeout, missing binary or network failure in a finish check is not a fail. Treating it as one wrongly blocks finish, and treating it as a pass wrongly allows it. Assumption: the oracle currently returns a boolean.
  Done when: each oracle command returns pass, fail or unknown with a timeout, and finish refuses on any unknown while naming it.

- **Lint the plan DAG when the plan is written** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: a plan carried over days breaks if a row depends on a row that doesn't exist, or on a cycle. Nothing in the pack shows a check at plan-write time.
  Done when: `fm goal` refuses a plan with a cycle, an orphan row or a duplicate row id, and prints the offending ids.

- **Re-run finished goals' oracles at ship, only when the diff touches their paths** — FEATURE — value 4 — effort M — risk med — category: regression
  Why: "done" can silently rot after a later commit. A path-scoped re-run is cheap and fits the ship gate (`fm ship`, full suite).
  Done when: a commit that breaks a finished goal's oracle makes `fm ship` name that goal, and an unrelated commit runs no goal oracles.

- **Model-based test of the goal verbs with random kills** — FEATURE — value 4 — effort M — risk low — category: crash safety
  Why: kill-at-every-boundary tests are hand-picked. A small pure reference model with a random sequence of verbs and SIGKILLs finds the sequences nobody wrote down.
  Done when: 500 seeded random runs end with the real goal state equal to the reference model's, and a planted torn-write bug is caught within them.

- **Wild: have an adversary lane try to pass the sweep with 58 cheap cells** — FEATURE — value 4 — effort M — risk low — category: gate testing
  Why: the standing rules fence metric-gaming. A child told to go green as cheaply as possible should fail the templating linter and the cold read, and any pass is a gate bug.
  Done when: the adversary's fill is rejected by the gates on at least 95% of cells across 3 runs, and each pass becomes a linter test.

- **Wild: run a kill-the-lanes fixpoint on the fill** — FEATURE — value 3 — effort M — risk low — category: crash safety
  Why: a multi-lane fill that is interrupted and rerun until stable should end with the same cell-to-citation mapping as an uninterrupted run. Differences show hidden order dependence.
  Done when: a scratch run with random lane deaths and reruns ends with citations identical to the clean run's, modulo wording.

- **Wild: score a cold-resume comprehension probe on the goal file** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: a tool-less child sees only the goal file and says what is done, what is next and what is risky. Disagreement with the computed next row shows the file is ambiguous, whatever model resumes it.
  Done when: for 10 sample goal files, the child's "next" matches the computed next row in at least 9, and a mismatch files a task against the file format.

- **Add a harness field to every cell probe** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: the earlier question about non-Claude harnesses has no recorded answer. Probes today could pass on Claude Code only.
  Done when: each probe row records the harness it ran on, and the sweep lists cells with only one harness.

Next question: which of the 58 cells would the goal engine fail to notice if its own state file were silently rolled back one day?
Next question: does any sweep check read a cell's probe result from a cache, so that a stale pass could hide a regression?
