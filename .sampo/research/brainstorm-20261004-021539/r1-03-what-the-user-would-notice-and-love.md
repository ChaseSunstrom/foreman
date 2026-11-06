# Brainstorm — lens: what the user would notice and love

- **Predict the finish time on the pane** — FEATURE — value 4 — effort S — risk low — category: pane
  Why: assumption: the ledger already holds per-step durations by tier and type. The user watches long drives and has asked about speed ("anything to speed it up").
  Done when: a task with 5+ similar finished tasks in the ledger shows "~N min left (from K similar)" in the pane, and the estimate drops as steps close.

- **Add `fm guard try "<cmd>"`, a dry-run verdict** — FEATURE — value 4 — effort S — risk low — category: guard UX
  Why: the friction list shows repeated guard false positives (`git stash list`, read-only python), and the user can't currently probe the guard without triggering it.
  Done when: `fm guard try "git stash list"` prints allow/block, the reason code and the matching rule without running anything, and the test suite proves it never executes the command.

- **Teach the right feature at the moment it would help** — FEATURE — value 4 — effort M — risk low — category: discoverability
  Why: a dozen commands shipped in a day (`prove --hunks`, `oracle`, `batch`, `surprise`). Assumption: the user can't hold them all. Foreman already has hint infrastructure that goes quiet when ignored.
  Done when: after three hand-fixed flaky reruns, `fm next` shows one line naming the flake ledger. The tip shows once per feature and is not shown again after the feature is used.

- **Show a savings meter next to the spend meter** — FEATURE — value 4 — effort M — risk low — category: cost
  Why: the user said savings should stop over-use, not remove capability. Prefix caching, batching and the gate cache all shipped, but their value isn't visible. Assumption: spend ledger entries can carry a "would have cost" estimate.
  Done when: the pane and `fm cost` show "saved ≈ $X today" split by mechanism, and a test with a cache hit shows a non-zero line.

- **Keep a catch reel of what Foreman stopped** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: every review found 3–7 real issues, including 2 HIGH ones in the proof tool. These catches are invisible once a task closes.
  Done when: `fm catches` lists the week's guard blocks, reviewer findings and red→green gates, each with a one-line before/after, and the pane shows a running count.

- **Review any ref or foreign PR with the audit lenses** — FEATURE — value 3 — effort M — risk low — category: review
  Why: assumption: the lenses and the read-only reviewer only run against Foreman's own tasks. The user's hand edits and others' PRs get no coverage.
  Done when: `fm review HEAD~2..HEAD` or `fm review <PR#>` prints lens findings without creating a task or editing files.

- **Add one unified `fm find` over every store** — FEATURE — value 3 — effort M — risk low — category: recall
  Why: lessons, decisions, surprises, research notes, briefs and friction all live in separate stores. The user rarely remembers which one holds "that retry thing".
  Done when: `fm find "retry"` returns ranked hits from at least five stores, each tagged with its source and date.

- **Wild: Draft the user's likely next request as a ghost brief** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: wild. Verbatim steers show a pattern: after each feature the user asks to "recursively improve". At drive end, a cheap child drafts one candidate brief from recent asks. It is parked in a ghost slot and costs nothing until the user accepts it with one key.
  Done when: a drive that empties the queue shows a ghost brief, `fm ghost accept` queues it, and ignoring it leaves no task and no spend beyond the cap.

- **Wild: Quiz the user weekly on three past decisions** — FEATURE — value 3 — effort S — risk low — category: decisions
  Why: wild. A 60-second "would you still pick this?" card per decision. The yes/no answers feed revisit triggers and lesson confidence, and replace the user's need to audit Foreman.
  Done when: `fm quiz` asks for three recorded decisions, a "no" marks the decision for revisit, and the answers appear in `fm friction`.

- **Wild: Draw a fault map in the pane's idle view** — FEATURE — value 3 — effort M — risk low — category: pane
  Why: wild. Combine the surprise log, flake ledger, reviewer findings and file churn into a heat map of the files where Foreman's model of the code keeps being wrong. It's something to show people, and it points to where to add tests.
  Done when: the idle pane lists the top 5 files by weighted incidents, and a file with a seeded surprise and flake outranks an untouched one.

- **Wild: Let the user ask "what did you almost do?"** — FEATURE — value 3 — effort M — risk med — category: transparency
  Why: wild, assumption: tool calls the model considered and then abandoned are not logged. Capturing them (rejected plans, abandoned edits, vetoed commands) would show the road not taken.
  Done when: `fm almost ID` lists abandoned approaches for a finished task, each with the reason it was dropped, and an empty list is reported as such.
