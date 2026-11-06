# Brainstorm — lens: self-modification: a planner that learns from which plans held and which needed rework (every item added after done was a missed contents line), measured and reversible

- **Log every post-done addition as a missed line** — FEATURE — value 5 — effort M — risk low — category: goal ledger
  Why: the gap map wants a goal ledger (contents → tasks → done-when → coverage) but nothing records what was added after "done". The lens's core signal is this. Assumption: a task or criterion added to a goal after its done verdict is detectable by timestamp against the verdict event in the hash-chained ledger.
  Done when: finishing a goal, then adding a task to it, writes a `missed` event naming the new line and its source (user words, review, failing exam, own discovery), and `fm goal show` lists it.

- **Classify each miss by cause class** — FEATURE — value 4 — effort M — risk low — category: planner learning
  Why: the lens needs a lesson, not a count. The pack's own history shows classes: satellites forgotten (T-2120..2127 were all missed asks), docs/site/pane surfaces, error states, a table-less seed. Assumption: a small closed set (surface, satellite, edge-input, ordering, scope-misread) covers most misses.
  Done when: every missed event carries one class from the closed set, and `fm goal misses --by class` prints a count per class for a fixture ledger.

- **Distil misses into a contents-list prior** — FEATURE — value 5 — effort L — risk med — category: planner learning
  Why: the gap map says contents lists are model boilerplate; a per-project and cross-project prior of "lines that were missed before" grounds them. Assumption: misses repeat by class across goals.
  Done when: planning a new goal on a fixture project with three past misses of one class adds a contents line of that class, citing the miss ids it came from.

- **Score every planner edit by rework rate on replay** — PERFORMANCE — value 4 — effort M — risk low — category: measurement
  Why: "measured" is required; the exam grades capabilities, but not the planner. Rework rate = missed lines per finished goal. Assumption: past goals' ledgers can be replayed as a held-out set by planning each from its original words only.
  Done when: `fm goal plan-score` replays N archived goals and outputs the share of eventual missed lines the new plan already contained (recall) and the share of planned lines never used (padding).

- **Version the planner's rules as sealed files with one-command revert** — SECURITY — value 4 — effort M — risk low — category: reversibility
  Why: the lens demands reversibility; the NEVER "lower your own guard" means the planner must not edit its own guards. Assumption: learned rules live in a declarative file (not code) separate from the protected core.
  Done when: `fm goal rules revert` restores the previous sha-sealed rules file, the ledger records both, and a test shows a rule edit touching the guard clauses is refused.

- **Promote a learned rule only after it holds on N goals** — FEATURE — value 4 — effort M — risk med — category: planner learning
  Why: the previous missions' lesson was precision over volume; padding every plan with speculative lines costs attention and false work. Assumption: three goals is a workable evidence floor.
  Done when: a candidate rule stays "shadow" (listed, not injected) until it would have caught misses in ≥3 distinct goals, then flips on with a ledger event; a fixture with two shows it stays shadow.

- **Retire a rule that pads without catching** — CLEAN — value 3 — effort S — risk low — category: planner learning
  Why: the same economy as the probe-retirement ideas above, applied to planning. A contents line that was always dropped as "not applicable" is cost.
  Done when: a rule whose injected lines were dropped in 5 consecutive goals is flagged `retire?` by `fm goal rules`, and removed with one command that records why.

- **Tell a done goal from a stopped one by its tail** — FEATURE — value 5 — effort M — risk low — category: done verdict
  Why: the gap map lists the done-vs-stopped verdict as missing. The lens extends it: a "done" that is followed by additions was really a stop. Assumption: the stop reason is in the ledger (drive cap, usage limit, no-progress, crash, model "done").
  Done when: `fm goal verdict` returns one of done / stopped:<reason> / reopened, and a goal reopened within a window is retro-labelled so the planner's score counts it as a miss.

- **Wild: Pre-mortem pass: ask a cold model what the user will add next week** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: wild. Before sealing a plan, a tool-less child sees only the plan and goal words and lists likely later additions; later, actual misses grade its guesses, so its hit rate decides whether it stays on.
  Done when: the pre-mortem lines are stored as predictions, and after the goal ends `fm goal premortem --score` reports hits and misses.

- **Wild: Hindsight replay: re-plan the last ten finished goals with today's rules** — PERFORMANCE — value 4 — effort M — risk low — category: measurement
  Why: wild. It shows whether Foreman is getting better at planning, as a chart on the Genesis page; a regression is blamed on the specific rule changed. Assumption: the original goal words are kept in the ledger.
  Done when: the command outputs per-goal recall before and after the latest rules change, and a rules change that drops mean recall is flagged without being applied.

- **Wild: Plant a missing line in a finished plan and see if the planner reinvents it** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild. This applies the exam's planted-defect idea to plans: delete one line from an archived good plan, replan from the goal words, and score whether the line comes back. It gives the planner its own held-out exam.
  Done when: `fm exam` gains a plan kind; the report lists planted lines recovered, with a train/holdout split of the archived goals.

- **Pool miss classes across projects with literals scrubbed** — PRIVACY — value 3 — effort M — risk med — category: local-first
  Why: a new project has no history, so a cold start gives boilerplate. Assumption: class-level lessons transfer; they stay on the owner's machine and need no network.
  Done when: a miss is stored cross-project only as class plus a generic phrase, with paths, names and user words removed; a test confirms a seeded secret string never appears in the pooled file.

- **Show the planner's report card on the pane and site** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the MUST list for any capability requires a pane/status surface and a site page for stateful features. Assumption: three numbers suffice: recall, padding, and reopen rate, each with a trend.
  Done when: the pane line and the site page render the same three values from one export, and a golden-file test covers an empty state with no finished goals.

- **Tell the user which lines came from a lesson** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: users who find extra lines in their plan should see why; an unexplained rule is hard to trust or veto. Assumption: a "from lesson L-n" tag on the line is enough.
  Done when: each learned contents line carries its lesson id and the miss it came from, and `fm goal drop-lesson L-n` removes the lesson and its pending lines and writes a veto fingerprint.

Next question: Does a miss caused by the user changing their mind count against the planner, and how does the ledger tell a changed mind from a forgotten line?
Next question: What is the smallest number of finished goals before a learned prior beats the plain model's contents list, and how would we know?
