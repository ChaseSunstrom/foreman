# Brainstorm — lens: bold bets

- **Map the blind regions before saying finished** — FEATURE — value 4 — effort M — risk low — category: done-detection
  Why: assumption: session transcripts record which files were read, edited or grepped. Existing ideas check diff hunks and proof witnesses, not the code the plan relied on but nobody opened. A "finished" verdict that lists unread modules makes "merely stopped" visible.
  Done when: on a fixture goal with a planted never-opened module, `fm goal` finish prints that module under "blind regions", and the list is empty once a session reads it.

- **Start a goal from a reference artifact** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: assumption: users describe vague goals by pointing ("like this app", "like that repo"). `fm goal --like <path|url|screenshot>` extracts a feature inventory as candidate contents rows, each citing the artifact region it came from, and marks every row must, should or could.
  Done when: running it on a fixture repo yields at least 10 cited rows and none lacks a source line.

- **Mine the repo's own debt markers into must-have candidates** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: `fm find` already runs as a free first pass. TODO and FIXME comments, skipped or xfail tests, and flags with no readers are the repo saying what unfinished means. Dated by git blame, they ground rows cheaply.
  Done when: a fixture with 5 planted markers produces 5 candidate rows, each with file:line and age.

- **Walk the finished web UI with a monkey** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: pillar 5 wants the real browser path. A seeded random walk over every reachable control at finish, capturing console errors, dead ends and empty/loading/error states, finds what scripted flows miss.
  Done when: a fixture UI with one planted dead button and one console error makes the walk report both with the replay seed.

- **Gate finish on a second harness's file-only read** — FEATURE — value 4 — effort M — risk med — category: harness-neutral
  Why: the pack asks which cells quietly depend on Claude Code. A finish verdict that needs agreement from a different installed CLI (codex, gemini or opencode), reading only the goal files and repo, exposes harness dependence. It also gives a cold judge from a different house.
  Done when: with the second harness stubbed to disagree, finish refuses and prints the disagreeing row. With none installed it says "single-harness" rather than passing.

- **Assign rows to humans, not only agents** — FEATURE — value 3 — effort M — risk med — category: collaboration
  Why: assumption: real goals include rows only people can do (design sign-off, API keys, a teammate's review). Today those land in a user-only list. A row with an owner, a due date and a git or PR signal for completion lets the goal wait on a person without going stale.
  Done when: a goal with a teammate-owned row shows "waiting on <owner>, day N" and unblocks when the named PR merges.

- **Check the goal for an XY problem before planning** — FEATURE — value 3 — effort S — risk med — category: planning
  Why: assumption: a vague goal is often a means ("add caching") to an end ("pages are slow"). One tool-less child writes the likely end goal and a cheaper alternative in one line each. The plan then shows "you asked X; the end may be Y" with a one-word keep/switch. At most one question.
  Done when: on 5 fixture goals with a planted underlying end, the child names it in at least 4, and the keep path changes nothing.

- **Use MASTER.md clauses as a free held-out exam for #4** — FEATURE — value 4 — effort M — risk med — category: measurement
  Why: MASTER.md clauses carry task ids, so each is a finished goal with a known answer. A tool-less child that never sees the code gets the vague phrasing and plans; recall is scored against what was actually built. This supports the standing rule that exam scenarios come from a separate child.
  Done when: `fm exam` prints plan-recall over at least 20 clauses, with the child's plans stored unseen by the scorer.

- **Rank the 58 cells by what a resume would notice missing** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: the pack's questions show some cells have no history to backtest. Ordering by cost rather than row order lets the fill spend its budget first on cells whose absence breaks a resume, such as baton, ledger and repo disagreement. Unbacktestable cells are tagged "planted".
  Done when: the fill report lists cells in rank order with a backtest class each, and the top 10 contain no template phrasing.

- **Wild: Quiz the user on what was built** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. After days of unattended work the user's mental model lags the repo. A three-question teach-back from the diff ("what now happens when X?") with one-word answers corrects it, and wrong answers show up as the next goal's first rows.
  Done when: finish emits three questions grounded in the diff, and each answer is stored with its right/wrong mark.

- **Wild: Distill the user's closed goals into a local row-writer** — FEATURE — value 3 — effort L — risk high — category: local-first
  Why: wild, assumption: enough closed goals exist. A small local model fine-tuned on this user's plan-to-outcome pairs drafts rows with no network. The free arm is graded against the frontier arm on held-out goals.
  Done when: the local arm's plan recall on 10 held-out goals comes within a stated margin of the session arm, or the result is recorded as a clean negative.

- **Wild: Run a nightly vague-goal fuzzer against the grid** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: wild. At night a child invents a vague goal and a hidden rubric, runs the planner with no tools, and files any cell the plan violated as a gap candidate. The cell count then grows from found failures instead of being fixed at 58.
  Done when: one night's run files at least one candidate with the seed goal and the missed rubric line, or logs "dry".

- **Make each of the 58 cells name one stage and one reader** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the pack's open questions are about outputs no session path reads. A cell without a named reader (session start, `fm next`, the drive, a hook) is the quiet failure.
  Done when: the sweep fails any cell lacking a resolvable reader.

Answer to a left-over question: I can't tell from the pack which cells depend on Claude Code. The second-harness gate above would make that visible.

Next question: Which of the 58 cells would the user only discover are missing after a multi-day goal stalled, and what did that stall cost them?
Next question: Does the existing history hold enough finished multi-day goals to score plan recall, or must the exam plant them?
