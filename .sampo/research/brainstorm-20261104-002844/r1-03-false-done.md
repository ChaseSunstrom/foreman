# Brainstorm — lens: false done

- **Resolve state from the git common dir** — FIX — value 5 — effort S — risk low — category: reliability
  Why: evidence and lease commands fail inside the builder worktree the harness puts the agent in. Assumption: state is keyed on the worktree's toplevel or cwd instead of `git rev-parse --git-common-dir`.
  Done when: in a fresh `git worktree`, `fm evidence add` and `fm lease acquire` write to the main repo's state and a test fails if they error.

- **Bind evidence to a tree hash** — FEATURE — value 5 — effort M — risk low — category: done-gate
  Why: 6 false dones persist since gen 2. Assumption: evidence records a command and exit code but not the tree it ran against, so a later edit leaves it counting.
  Done when: editing any tracked file after an evidence run makes `fm task finish` list that evidence as stale and refuse.

- **Map each goal clause to proof, or refuse "done"** — FEATURE — value 5 — effort M — risk med — category: done-gate
  Why: a vague goal must become a complete plan and know when it is done. At intake, split the goal into numbered clauses and freeze them. Finish needs each clause tied to evidence or to a user-signed "not needed".
  Done when: a goal with 3 clauses and 2 proofs is refused, naming clause 3.

- **Replay recorded proofs on resume** — FIX — value 5 — effort M — risk med — category: resume
  Why: resume is the worst area, with 2 of 6 needing a later fix. On a resume, a compaction or a stale lease, re-run every cheap recorded proof before any "done" step is trusted, and flip the failures back to open.
  Done when: in a resume test, a step marked done whose proof now fails shows as reopened in `fm next`.

- **Re-inject the open-clause list at PreCompact and SessionStart** — FEATURE — value 4 — effort S — risk low — category: compaction
  Why: goals are carried over days and compactions. Assumption: the clause list lives only in the conversation or in scattered task notes.
  Done when: after a forced compaction, the first injected note lists the open clauses by id.

- **Gate the word "done" on the Stop hook** — FEATURE — value 4 — effort S — risk med — category: honesty
  Why: false done is first a claim in the final text. If the finish text says done, complete or fixed while the clause ledger shows unproved clauses, the Stop hook blocks once and prints the list.
  Done when: a scripted session claiming done with one open clause is blocked, and the block is logged.

- **Run a cold adversary on every done claim** — FEATURE — value 4 — effort M — risk med — category: review
  Why: standing rules favour signals Foreman didn't author. A different-model child gets only the goal, the diff and the evidence, and must name one unmet clause. The claim stands only if it can't.
  Done when: replaying the 6 known false dones, the adversary names a real gap in at least 4.

- **Turn the six known false dones into a regression corpus** — CLEAN — value 4 — effort M — risk low — category: tests
  Why: the long tier shows 0/6 true done, unchanged since gen 2. Save each as a replayable fixture with the claim, the repo state and the expected refusal.
  Done when: the corpus runs under `fm exam` free arms and each case is refused or flagged.

- **Write the goal-level acceptance check before building** — FEATURE — value 5 — effort L — risk med — category: planning
  Why: unit tests passing is not the goal being met. Intake emits a runnable acceptance script, red on the parent commit. Finish requires it green.
  Done when: for a replayed repo goal, the script fails at the rolled-back commit and passes on the true follow-on change.

- **Add a "decayed" status that re-runs proofs 24 hours later** — FEATURE — value 3 — effort M — risk low — category: durability
  Why: days-long carry-over. Closing is provisional, and a nightly re-run flips done to decayed if its proof now fails.
  Done when: a planted regression the next day turns the task decayed and files a followup.

- **Wild: Have a ghost user type the "but did you also…" follow-up** — FEATURE — value 4 — effort M — risk med — category: honesty
  Why: assumption: the user's real follow-ups ("also", "again") are the best false-done signal. A tool-less child, shown only the user's past follow-ups, guesses what they'd say next.
  Done when: on 10 closed tasks, the guesses match at least 2 real later asks.

- **Wild: Seal a done-forecast before the first edit** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: the builder writes "I'll show X, Y, Z" as a sealed file, and finish diffs the delivered proof against it. A shrunken promise counts as a false-done signal.
  Done when: finish prints "promised 3, proved 2" with the dropped item named.

- **Wild: Pay lanes a bounty for finding unmet clauses** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: assumption: a reviewer rewarded for gaps finds more than one asked to approve. A reviewer lane's score counts only gaps that a later user ask confirms.
  Done when: a bounty ledger shows the per-reviewer confirmed-gap rate after 20 closes.

- **Make crash-left leases self-describing on resume** — FIX — value 4 — effort S — risk low — category: resume
  Why: a dead process holds the lease and a new session may trust its "done" notes. The new session prints who held the lease, when it was last seen, and which notes are unverified.
  Done when: a killed-session fixture resumes and shows the previous holder's steps flagged unverified.

Next question: Which of the 6 false dones were wrong claims versus wrong clause lists, and does the gate catch each class?
Next question: Does a refused done make the agent finish the work, or only reword the claim?
