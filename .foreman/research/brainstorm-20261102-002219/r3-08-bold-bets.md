# Brainstorm — lens: bold bets

- **Run the 58-cell fill as a goal whose oracle is the sweep** — FEATURE — value 5 — effort M — risk low — category: dogfood
  Why: the request is a goal ("finish #4's 58 empty cells"), and Foreman's own sweep already says when cells are empty or templated. Split the work into lanes by surface column, and let the goal close only when the sweep reports 0 empty and 0 templated.
  Done when: running `fm goal` on the fill reaches "finished" with a sweep that passes, and a deliberately re-templated cell makes the goal reopen.

- **Run one nightly canary goal whose stages are the grid's columns** — FEATURE — value 5 — effort M — risk med — category: canary
  Why: assumption: the stage columns map onto a scripted drill (vague goal, plan, forced compaction, killed session, usage-limit pause, misleading test, finish). A cell then cites the drill stage and its output, not prose. This makes the cells re-runnable and tells the sweep when a cited path has stopped firing.
  Done when: `fm night` runs the canary in a scratch repo, writes a per-stage pass/fail, and breaking resume-after-kill turns the matching cells red.

- **Score plan completeness against real 1.0 release notes** — FEATURE — value 4 — effort L — risk med — category: benchmark
  Why: the standing rules want signals Foreman didn't author, and held-out scenarios from a separate child. Take the tagline from an open-source project's README as the vague goal, take its 1.0 release notes as the hidden "finished contents", and score the plan's recall by language and product type. The cells get scenarios that don't come from the grid. Assumption: enough public repos have clean 1.0 notes.
  Done when: `fm exam` prints plan recall on 10 external repos, each with a free-arm baseline (a plain model asked for the plan).

- **Rate a plan by whether a cheap model can execute each row** — FEATURE — value 4 — effort M — risk med — category: plan quality
  Why: assumption: a row Haiku can't turn into a first action without asking is vague, however good it sounds. Walk every row with the cheapest model for one step and flag the rows where it asks, hallucinates a path, or writes no test.
  Done when: `fm goal plan` prints a count of non-executable rows, and a planted vague row ("make it good") is flagged.

- **Score plans against the user's own follow-up asks** — FEATURE — value 4 — effort M — risk low — category: backtest
  Why: the "what earlier brainstorms missed" list is a chain of follow-ups, such as T-2533 to T-2536 (lean ratchet, guard arm, commit naming, ablate). Each is a later ask the first plan should have contained. For past multi-ask arcs in the asked stream, give the planner only the first ask and measure how many later asks its rows cover. That gives a heuristic the bar to meet before it ships.
  Done when: a backtest over at least 8 historical arcs reports recall, the bar is stated before the run, and a shuffled-arc control scores lower.

- **Stack rows as dependent branches so any stopping day is mergeable** — FEATURE — value 4 — effort L — risk high — category: decomposition
  Why: assumption: "knows when it's done rather than merely stopped" needs partial states to be shippable. Each row becomes a small gated branch on the one below it, and the finish verdict is "the top of the stack merges". Crashes then lose at most one row.
  Done when: after killing the session mid-goal, `fm goal status` lists a bottom-up mergeable prefix, and `fm ship` lands it with the gates passing.

- **Stamp each plan with a model and host fingerprint, and re-prove a closed row on a mismatch** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: assumption: a plan written under one model or Claude Code build is resumed days later under another. On resume, if the fingerprint differs, replay the last closed row's verify before continuing, and record any difference.
  Done when: a faked fingerprint change on resume triggers the replay and prints one line saying so.

- **Run a goal across several repos with one shared oracle** — FEATURE — value 3 — effort L — risk high — category: scope
  Why: assumption: real goals often span a library and an app, or a repo and its site (Foreman itself has `plugin/` and `site/genesis`). Goal state is per repo today. Keep one goal file with per-repo rows and a finish verdict that needs all of them.
  Done when: a goal naming two scratch repos refuses to finish while one repo's row is red, and resumes in either repo.

- **Revert each closed row in a scratch tree and see what notices (wild)** — FEATURE — value 4 — effort M — risk low — category: mutation
  Why: assumption: some rows are padding that no check would miss. Revert row N's commits in a scratch copy and run the oracle and tests. A row whose removal changes nothing is unwitnessed, so the finish report lists it.
  Done when: a planted padding row is flagged "no check notices", and a real row shows the failing check that names it.

- **Hand a cold child the goal bundle and require it to continue correctly (wild)** — FEATURE — value 4 — effort M — risk med — category: handoff
  Why: the goal "carries the plan over days", so test the claim directly. Give a tool-less or no-Foreman child only the goal file, journal and evidence, and ask for the next action. The cell passes if it names the right unblocked row.
  Done when: for 5 historical mid-goal snapshots, the cold child's next-row choice matches the recorded one in at least 4.

- **Build the goal twice on two cheap models and diff the capability lists (wild)** — FEATURE — value 4 — effort L — risk med — category: spec ambiguity
  Why: assumption: where two independent builds disagree, the plan was under-specified. Diff the two builds' feature lists, not their code. Rows present in one and missing in the other become "decide this" questions or rows. Run it only on L goals, in worktrees.
  Done when: a seeded ambiguous goal ("add export") yields a disagreement list naming the format question, and the cost is shown next to it.

- **Replay a recorded multi-day goal at 100x as a faithful time machine (wild)** — FEATURE — value 3 — effort L — risk med — category: replay
  Why: assumption: ledger and journal events carry enough to re-run the "what did the goal think was done on day 3" verdict. Each historical day's computed verdict is compared with what was said then, and any "finished" claim that today's oracle would reject is shown.
  Done when: replaying one real goal prints a per-day verdict timeline, and a planted false "finished" is flagged on its day.

- **Stamp a cell's backtest class and grade the unbacktestable ones as plants** — CLEAN — value 3 — effort S — risk low — category: coverage honesty
  Why: this answers an earlier question. Where history has too few events, a cell can't be measured, only planted. Mark each cell "backtested" or "planted", and let the sweep show the planted share.
  Done when: `coverage.md` carries the tag for all 58 cells, and the sweep prints the planted fraction.

Next question: Which goal behaviours do the first 10 external 1.0-note benchmarks show the planner missing consistently, by product type?
Next question: When the goal's finish oracle and the user's later correction disagree, which one has been right so far?
