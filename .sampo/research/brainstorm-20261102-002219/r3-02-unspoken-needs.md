# Brainstorm — lens: unspoken needs

Answers to earlier questions, from this lens: the cells most likely to depend on Claude Code are the ones citing hook-driven reach (SessionStart, PreToolUse), and the pack gives no per-cell harness field, so that is an assumption. The unread outputs I'd bet on are the sealed predictions and any draft file that only `fm night` writes.

- **Pre-register the fill's pass bar** — CLEAN — value 4 — effort S — risk low — category: process
  Why: Lessons from Missions 3-6: a heuristic ships only behind a backtest with its bar stated first (T-2546 failed, T-2554 met it). The 58-cell fill has no such bar yet. The user's repeated worry is templating and metric-gaming, and the fill is the next place it could happen.
  Done when: `fm decide` holds a bar (max pointer-only share, min cold-read pass rate, max reused 20-line shingles) with a timestamp before the first cell commit, and the final report prints each result against it.

- **Close a goal as superseded** — FEATURE — value 4 — effort M — risk med — category: goal lifecycle
  Why: assumption: goals carry over days, and later asks or commits can cover their rows. Task-level "made moot" exists in the list above, but nothing closes a whole goal on that basis. Without it, a goal stays open and the "knows when it's done" claim is only half true.
  Done when: a fixture goal whose rows are all covered by later closed tasks is marked `superseded`, with the covering task ids, and `fm next` stops offering its rows.

- **Persist vetoes through replans** — FIX — value 4 — effort S — risk low — category: plan memory
  Why: Standing steers say not to re-litigate decided matters. Plans are rewritten after compaction and crashes, and a row the user struck could be re-derived by the decomposer. assumption: no tombstone check exists for goal rows (the list above has it only for rejected approaches).
  Done when: a test strikes a row, forces a compaction plus a replan, and the row doesn't come back. A re-add needs a new user word and is logged.

- **Tag each plan row with the cheapest capable model** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: Pillar 1 says independent tasks run on "the cheapest model that can". Row cost estimates exist in the list above, but nothing learns per-row model tiers from retry and reopen history.
  Done when: after N closed rows, `fm goal plan` prints a model tier per new row, and a backtest on past rows shows no more reopens than always using the strong model, at lower cost.

- **Derive non-goals from the dropped ledger** — FEATURE — value 3 — effort S — risk low — category: scope
  Why: The pack has many "dropped … false alarm / captured by mistake" entries and standing "no new maintenance tasks" steers. A finished version also has things it must not contain, and the goal contents list only says what to add.
  Done when: a goal's plan has a "Not in this goal" block that cites ledger entries or steers, and a row matching one of them is refused at plan time with that citation.

- **Name the verb behind each filled cell's pointer** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: A cell that says "existing path" is only useful if the user can try it. assumption: `reach` names a session path but not the one command or phrase that exercises it.
  Done when: every pointer cell lists one runnable command that exits 0 in the sweep, and the sweep goes red on a cell with none.

- **Reserve slack for steers (wild)** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: The user's steers keep arriving mid-run (2026-10-31 steers #1-#3 reshaped round 1), and eight missed asks were never predicted. Plans assume a still user. A fixed slice of each goal's budget for unplanned steers would turn the "steer receipt with queue impact" into a draw from a reserve instead of a scope fight.
  Done when: a goal plan shows a reserve line (default 10% of rows or budget), a steer draws from it and the draw is logged, and the reserve is reported unused at finish.

- **Stop-now receipt (wild)** — FEATURE — value 4 — effort M — risk med — category: goal lifecycle
  Why: assumption: the user will sometimes need to walk away mid-goal. Ordering rows so any stop day leaves something runnable is on the list above, but a receipt that proves the tree is safe to abandon isn't.
  Done when: `fm goal stop-now` prints half-done rows, uncommitted files, open lanes, and the step that would leave a clean state. A killed-mid-row fixture reports "unsafe" until that step runs.

- **Park a goal until its files change (wild)** — FEATURE — value 3 — effort M — risk med — category: triggers
  Why: Waiting out usage limits and blocked rows is already a theme. Waking on a clock is covered in the list above, but waking when the files a parked goal cites are touched, by the user or a commit, isn't.
  Done when: a parked fixture goal resumes with a "why now" line within one tick of a commit touching a cited path, and not before.

- **Reconcile a user hand-edit against a done row** — FIX — value 3 — effort S — risk low — category: drift
  Why: assumption: the user edits files by hand between sessions. A done row whose cited file changed by a non-Foreman author would now show as regressed, which is a false alarm like the dropped breakage-ahead items in the pack.
  Done when: a hand-edit to a cited file flips the row to "touched by user, re-verify" rather than "regressed", and the row re-verifies itself on the next resume.

- **Spawn a sequel goal from parked growth** — FEATURE — value 3 — effort S — risk low — category: scope
  Why: Scope growth is already logged with a threshold ask. The user's "never idle" and "no mid-run asks" rules suggest the overflow should become a queued sequel stub instead of growing the finished goal.
  Done when: growth past the threshold files one titled sequel goal with its rows and a link to the parent, and the parent's finished verdict ignores them.

- **Show a resume cost line before the user decides (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: after days away, the user wants to know whether picking the goal back up is a five-minute or a long job. A single honest line (rows left, drift found, compactions survived) lets them choose without opening the goal.
  Done when: the first resume line states rows left, days idle and drift count, and a test against a drifted fixture shows the number changing.

- **Flag fills no session has ever reached** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: The unread-outputs question has no answer in the pack. A cell filled by a capability that no session path ever calls is the most likely silent failure.
  Done when: the sweep lists, per cell, whether its capability appears in the event log in the last N sessions, and "never called" cells go on the final report's user-only list.

Next question: Which of the 58 cells would the user only notice missing after a goal had already stalled, and what in the event log would show that earlier?
Next question: When the cells are filled, what will the user check first on opening the result, and does the report put that check on the first line?
