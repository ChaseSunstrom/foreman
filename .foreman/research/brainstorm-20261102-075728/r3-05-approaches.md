# Brainstorm — lens: approaches

- **Close the plan by needs/provides** — FEATURE — value 4 — effort M — risk low — category: completeness
  Why: assumption: rows are free text, so a missing row is invisible. If each row declares `needs:` and `provides:` (files, commands, data), any need with no producer is a missing row. The check is mechanical and needs no model.
  Done when: a fixture plan with one row needing `config.toml` and nothing producing it makes `fm goal lint` print that row as a gap, and adding a producer row clears it.

- **Write the finished repo's target manifest** — FEATURE — value 4 — effort M — risk low — category: plan form
  Why: the pack's repo map already knows entry points and layout. A manifest lists the expected paths, CLI verbs, exported symbols and commands, and the diff between it and the tree is the work left. It survives crashes because it is a file in git.
  Done when: deleting one listed symbol from a fixture makes the manifest diff name exactly that symbol as remaining.

- **Keep goal checks as tagged tests in the repo's own runner** — CLEAN — value 4 — effort S — risk low — category: do less
  Why: the repo already gates on `fm doctor`, `roundtrip.py` and `bench_hooks.py`, and the steer on external signals favours checks Foreman didn't author. Goal "done" becomes `pytest -m goal` (or a shell script per row) in CI. That gives no new state engine, resume is `git checkout`, and a clean runner is the outside witness.
  Done when: a goal marked done runs its tagged checks in a fresh clone's CI, and one red check turns the goal's verdict to "not done".

- **Declare done by quiescence** — FEATURE — value 4 — effort M — risk med — category: done detection
  Why: assumption: an oracle only covers what was imagined. Each day a blind child on a different model gets the original goal text plus a repo summary and lists what is missing. Done requires empty lists on three consecutive days across two models, plus the oracle.
  Done when: a fixture goal with a planted gap is reported by the child, and a complete fixture yields three consecutive empty lists that set the "done" verdict.

- **Journal the goal from the host transcript** — FEATURE — value 4 — effort M — risk med — category: crash recovery
  Why: the request stresses crashes and compactions, and a model-reported journal is only as good as the model remembering to call the verb. A scribe that tails the harness transcript file and records row starts, commands run and results works even when the session dies mid-step.
  Done when: killing a session mid-row, with the model never having called a goal verb, leaves a journal that resume uses to name that row as in progress.

- **Audit every compaction against the plan** — FEATURE — value 3 — effort S — risk low — category: compaction
  Why: the task text names compaction as a hazard. At the next SessionStart after a compact, check that the summary carries the goal, current row and cut line, and re-inject whatever it dropped, logging the loss.
  Done when: a fixture compaction summary that omits the current row triggers an injection naming it, and one that includes it injects nothing.

- **Grade each row on a readiness ladder** — FEATURE — value 3 — effort S — risk low — category: done detection
  Why: assumption: a binary row state is how a goal "merely stops" while rows read as done. The rungs are stubbed, works, tested, documented, and works from a fresh clone. The goal verdict reports the lowest rung of any must-row.
  Done when: a row with code and no test shows as "works", not "tested", and the goal verdict names it.

- **Seed rows from a noun-by-verb grid** — FEATURE — value 3 — effort S — risk low — category: completeness
  Why: a vague goal names nouns (report, user, file). Crossing each with a fixed verb set (create, edit, delete, import, export, search, share, undo, back up, diagnose) yields candidate rows, and the user strikes the ones that don't apply.
  Done when: the goal "a notes app" produces a grid with at least one candidate per noun-verb cell, and struck cells are recorded as out of scope.

- **Promote an oversized row to a sub-goal** — FEATURE — value 3 — effort M — risk med — category: structure
  Why: assumption: L rows are where plans stall. The same goal engine runs recursively, with its own oracle and baton, and the parent row's probe is the child's verdict. This adds no new structure.
  Done when: a row estimated L spawns a child goal, and closing the child flips the parent row's probe to green.

- **Review the plan as a pull request** — FEATURE — value 3 — effort M — risk low — category: user review
  Why: the user already reads diffs. The plan lives in `GOAL.md` and each revision is a commit or PR, so comments become steers and replans show as diffs. This reuses existing tooling.
  Done when: a replan produces a reviewable diff of `GOAL.md`, and a comment on a row is captured as a steer.

- **Generate properties from the goal text** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: assumption: example tests miss classes of bug. A child proposes properties (round-trip, idempotence, no data loss) that a property-testing library runs, and "done" requires no counterexample after a fixed budget.
  Done when: a fixture with a planted idempotence bug is caught by a generated property.

- **Compile the goal to a Makefile with stamp files** — FEATURE — value 2 — effort M — risk med — category: unconventional (wild)
  Why: wild. `make` already gives a dependency DAG, incremental re-runs and idempotent resume for free, with no engine to maintain. The trade-off is that it feels foreign and fits Windows poorly.
  Done when: killing the run mid-goal and re-running `make` skips every stamped row and resumes at the first unstamped one.

- **Interpolate the plan at four completeness levels** — FEATURE — value 3 — effort S — risk low — category: planning method (wild)
  Why: wild. A child describes the product at 25, 50, 75 and 100 percent in user-visible terms. The differences between adjacent levels are the rows, already ordered so that any stopping day is a coherent product.
  Done when: a goal yields four level descriptions, and every row traces to exactly one level step.

- **Bet on each row's necessity and settle at finish** — FEATURE — value 3 — effort M — risk low — category: calibration (wild)
  Why: wild. Foreman already scores bets with a Brier ledger. At plan time a row stakes "needed". At finish a row that no probe, journey or user word touched is settled as speculative, which measures the decomposer's over-planning rate.
  Done when: closing a fixture goal settles each row's bet and `fm outcomes` shows an over-planning rate for the kind.

Next question: Which approach here would the user pick if forced to delete the others, and does their record of dropped self-filed work say they prefer files in git or ledger verbs?
Next question: When the finish oracle and the quiescence read disagree on a real past goal, which one was right, and where would that be recorded?
