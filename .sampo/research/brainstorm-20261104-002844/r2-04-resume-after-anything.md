# Brainstorm — lens: resume after anything

- **Resume from one checkpoint file written at every tool boundary** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: resume is the worst area (2 of 6 needed a later fix); state is scattered across ledgers, so a crash mid-step loses where it was. T-2900 only closes dead background work.
  Done when: killing the session at a random tool boundary, then starting a new one, makes `sampo resume --json` print goal, open clauses, current step, and last evidence in one document, and a test kills at every write point and gets the same state.

- **Reconcile on resume against git and ledgers** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: the checkpoint can lie after a crash, a hand edit, a rebase or a branch switch (the user's own edits are a recurring blind spot). assumption: checkpoint and reality drift often.
  Done when: a test that amends HEAD and edits a tracked file between kill and resume gets a printed diff of "checkpoint says / repo says" and resumes from the repo's side.

- **Make evidence and lease commands work inside the builder worktree** — FIX — value 5 — effort S — risk low — category: worktree
  Why: the request names this failure directly: they fail inside the worktree the harness put the agent in.
  Done when: every evidence and lease verb returns the same result from the main checkout, a lane worktree, and a nested subdirectory of each, checked by a matrix test.

- **Take over a dead holder's lease with proof of death** — FIX — value 4 — effort M — risk med — category: leases
  Why: a killed session leaves leases that block the resumed one. assumption: owner pid/host/start time are recorded.
  Done when: a lease whose owner process is gone is reclaimed on resume with a printed reason, while a live holder's lease is refused, both tested.

- **Re-inject a 40-line goal anchor at PreCompact and SessionStart** — FEATURE — value 5 — effort M — risk low — category: compaction
  Why: compaction is a named hazard, and the long tier shows 0/6 true done. The goal's words, open clauses and "what done means" must survive summarising.
  Done when: after a forced compaction in the long-tier harness, the first prompt context contains the anchor, and its size stays ≤ 40 lines.

- **Re-attach a moved or missing worktree on resume** — FIX — value 4 — effort M — risk med — category: resume
  Why: a stopped builder's work is kept by `fm lane resume`, but the worktree path can be gone or moved. assumption: this happens after reboots (/run/user is tmpfs here).
  Done when: deleting a lane's worktree directory and resuming rebuilds it from the lane branch with the uncommitted work recovered or reported lost.

- **Hold "done" as provisional, then re-run proofs from cold** — FEATURE — value 5 — effort M — risk low — category: done-gate
  Why: 6 false dones unchanged since gen 2. A cold replay in a fresh worktree catches evidence that only held in the old state.
  Done when: a planted false-done scenario is caught by the cold replay, and the real fixed scenarios stay green.

- **Kill the goal run at every plan step and compare with an uninterrupted run** — PERFORMANCE — value 4 — effort L — risk low — category: testing
  Why: resume bugs were found only after the fact. A systematic kill-point sweep finds them before.
  Done when: a long-tier scenario reports, per step, whether the killed-and-resumed final tree and verdict match the clean run.

- **Print a worktree-aware Next line on every failure** — FIX — value 3 — effort S — risk low — category: DX
  Why: when a verb fails in a worktree today the agent has nothing to act on.
  Done when: every failing evidence or lease verb run from a worktree prints a `Next:` command that itself parses and succeeds.

- **Wild: Fire drill, kill the session on purpose mid-goal** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: wild. The nightly drive kills its own session at a random step on a scratch goal and times how long the resumed one takes to return to the same step.
  Done when: a report lists time-to-recover and any lost clause over the last 7 drills.

- **Wild: A stranger finishes the goal from the handoff alone** — FEATURE — value 4 — effort M — risk low — category: handoff
  Why: wild. A tool-less cold child gets only the handoff note and checkpoint and must name the next three actions. If it cannot, the note is incomplete.
  Done when: the child's answer matches the real next steps on 5 of 6 long-tier replays.

- **Wild: Write a note-to-self in the agent's own words at each checkpoint** — FEATURE — value 3 — effort S — risk low — category: handoff
  Why: wild. Structured state misses intent and hunches; a free-text letter carries them across compaction.
  Done when: the resumed session's first read includes the letter, and a test shows it names the last decision and its reason.

Next question: When a resume disagrees with the checkpoint, does the user want the repo's state or the plan to win?
Next question: Which of the 6 false dones came from lost state versus a weak done check?
