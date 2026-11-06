# Brainstorm — lens: bold bets

- **Write the press release and FAQ before the plan** — FEATURE — value 4 — effort M — risk low — category: goal contents
  Why: assumption: a vague goal loses rows when the plan is written from the goal sentence alone. A tool-less child writes the "finished product" launch note plus a hard-questions FAQ from three personas (user, skeptic, maintainer). Each sentence becomes a contents row or a recorded cut, which fills the "what a finished version contains" cells from the user's side.
  Done when: `fm goal new` on a fixture goal emits a press-release file, and every sentence in it maps to a row id or a "cut: reason" line; a test fails on an unmapped sentence.

- **Soak finished goals before they count as done** — FEATURE — value 5 — effort M — risk med — category: finish detection
  Why: the capability says "knows when it's actually done rather than merely stopped". assumption: no state exists between "closed" and "stays closed". A goal enters `soaking` for N days after its finish oracle passes. `fm night` re-runs the oracle, and a regression reopens the row that broke, with lineage.
  Done when: in a fixture, a planted regression after close flips the goal from `soaking` to `reopened` on the next tick, naming the row; a clean soak ends in `done`.

- **Mine a goal-shape library from the user's closed goals** — FEATURE — value 4 — effort M — risk med — category: decomposition
  Why: assumption: Foreman has many closed goals, and each leaves a plan-versus-final-rows diff. The rows added late show what planners forget (migration, docs, uninstall, error states). Seed new plans with the user's own recurring late rows. Per the lessons from Missions 3-6, ship it only behind a backtest: recall of late-added rows on held-out closed goals must beat the no-library control, with the bar stated first.
  Done when: `fm exam` prints late-row recall for library vs control on held-out closed goals, and the feature stays off unless the bar is met.

- **Write the finish back into MASTER.md** — FEATURE — value 4 — effort S — risk low — category: memory
  Why: the earlier "Already built, at birth" asks (T-2546) match requests against MASTER.md clauses. A goal that finishes without leaving clauses there is invisible to that check. Closing a goal drafts one clause per row, each with its task id, behind a yes.
  Done when: after a fixture goal closes, `fmrecall.covered` flags a paraphrase of one of its rows as already built.

- **Make finishing include deleting what the goal replaced** — FEATURE — value 4 — effort M — risk med — category: finish detection
  Why: pillar 6 covers dead and replaced functionality only at the end-of-run sweep. assumption: goals that replace something leave the old path alive. The finish oracle also requires a removal ledger listing the code, docs and settings the goal made obsolete, each deleted or explicitly kept with a reason.
  Done when: a fixture goal that adds a v2 path and leaves the v1 path cannot reach `done` until v1 is deleted or kept with a recorded reason.

- **Land a review pack timed to the user's next sitting** — FEATURE — value 4 — effort M — risk med — category: multi-day carry
  Why: assumption: the user returns on a cadence visible in session timestamps. A multi-day goal paces its waves so one coherent chunk is merged-ready, with a three-line "where we were" and the exact commands to check it, when they usually next appear. This avoids a half-finished state sitting there.
  Done when: in a replayed fixture history, a wave closes before the predicted sitting, and the review-pack file exists with its three lines and check commands.

- **Escalate by row, not by goal** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: pillar 1 says to use the cheapest model that can. A learned per-row-type difficulty score runs the goal on the cheap model and escalates only a row that fails its probe twice. Measured by cost per proven row against an all-strong control on replayed goals.
  Done when: a replay run reports cost per proven row for tiered vs all-strong, and tiered is cheaper at equal proven-row count.

- **Run a cross-harness completeness union (wild)** — FEATURE — value 3 — effort L — risk med — category: benchmark
  Why: wild; assumption: different harnesses and models decompose the same goal differently. Running one vague goal through 3 planners and taking the union gives a completeness benchmark with no hand-written answer key. A row only one planner found is a measured blind spot, and each one gets a cell and a plan-gate question.
  Done when: `fm exam` plans a fixture goal on 3 backends and prints union size, per-planner recall and the singleton rows.

- **Add `fm blame --goal` (wild)** — FEATURE — value 3 — effort M — risk low — category: provenance
  Why: wild; assumption: the commit-to-task link exists but not the commit-to-goal-row link. Each commit carries a goal-row trailer or git note, so any line answers "which row, whose words, which proof". This makes crash and compaction recovery check the repo against the plan.
  Done when: `fm blame --goal <file>:<line>` prints the row id, the user's quote and the proof status for a line in a fixture repo.

- **Rewind and replan to measure plan regret (wild)** — FEATURE — value 3 — effort L — risk med — category: planner quality
  Why: wild; assumption: git history plus the ledger show when each row was discovered. A time-machine run rolls a closed goal's repo back to day 0, replans with today's planner, and scores how many of the late rows it would have caught. This is a free-arm planner score from Foreman-unauthored history, in line with the standing rule on weakness-finding.
  Done when: the replay prints the share of late-added rows the replan included for at least 3 closed goals, with no session arm.

- **Let finishing goals vote a stage into the grid (wild)** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: wild; assumption: the 58 empty cells imply stage columns that might be missing. Each closed goal lists its late rows with the stage that caught them. `fm genesis grow` proposes a new column when 3 or more goals cluster the same missing stage, with evidence and a cold read, as the grow rule requires.
  Done when: a fixture set of three goals with the same late-row stage yields a grow proposal that names the stage and the three goal ids.

- **Probe each cell against a half-built goal** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the earlier questions ask whether the 58 probes run on other harnesses and have enough history. A fixture goal frozen at 40% done, with a known next row, lets every cell probe the same state: resume, done-check, drift and scope growth. Each probe records its harness and its backtest class (measured or planted).
  Done when: running the cell probes on the frozen fixture prints 58 lines, each with pass or fail, harness and backtest class.

Next question: which finish-detection failures came from a goal that was correct but under-specified (the user's intent changed), and does anything in the pack measure intent drift separately from plan drift?
Next question: does the goal engine have any consumer outside a live session, such as the night tick, the web UI or a second harness, so a cell can cite a session path other than Claude Code's hooks?
