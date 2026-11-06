# Brainstorm — lens: resume after anything

- **Resume from a single checkpoint file, not scattered ledgers** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: resume is the worst area (2 of 6 needed a later fix); T-2900 and T-2901 were both resume bugs found after the fact. Assumption: state is spread over several ledgers, so each resume path re-derives it differently.
  Done when: killing the session at 10 random points in a scripted goal and resuming yields the same `fm next` output as an uninterrupted run, in a test.

- **Make evidence and lease commands work inside the builder worktree** — FIX — value 5 — effort S — risk low — category: worktree
  Why: the request names this failure directly: the harness puts the agent in a builder worktree where evidence and lease commands fail. Likely cause (assumption): the commands resolve the state dir from cwd, not from the main repo's identity.
  Done when: `fm evidence` and `fm lease` run from a linked worktree and write to the same ledger as from the main checkout, tested in a fixture.

- **Write a "where I was" handoff note at every compaction and kill** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: goals run over days, crashes and compactions. Assumption: the agent loses the plan's intent after compaction, not just the task list.
  Done when: after a forced compaction, the first injected note names the current step, the next command and the last evidence, and a cold child can state them.

- **Keep a plan ledger with a per-step "done means" check** — FEATURE — value 5 — effort M — risk med — category: true done
  Why: long tier scores 0/6 true done and 6 false dones, unchanged since gen 2. Assumption: dones are declared from agent claims, not from a check run against each plan step.
  Done when: a goal cannot close while any plan step's check has no passing run recorded, and a planted false done in the long tier is caught.

- **Re-run every step's check at goal close, from cold** — FEATURE — value 5 — effort M — risk low — category: true done
  Why: false dones survive because earlier passes are trusted. A final cold replay catches regressions made later in the same goal.
  Done when: a long-tier scenario where step 2 is broken by step 5 reports not-done, naming step 2.

- **Replay the goal's original words at every resume** — FEATURE — value 4 — effort S — risk low — category: intent
  Why: a vague goal becomes a plan, and the plan drifts from it over days. Assumption: only the plan is carried, not the user's sentence.
  Done when: the resume note quotes the verbatim goal and lists the clauses with no step against them.

- **Add a resume drill that kills at every ledger write** — PERFORMANCE — value 4 — effort M — risk low — category: resume tests
  Why: two resume bugs were found late, which suggests no systematic fault matrix. Extends the idea of a kill-point sweep to the goal flow.
  Done when: the drill passes at every write point of `fm goal` start, step close and finish, with no duplicate or lost step.

- **Detect a dead owner of a lease and reclaim it safely** — FIX — value 4 — effort S — risk med — category: leases
  Why: lease commands failing in worktrees points at stale-lease handling being brittle. T-2900 shows dead processes leaving work open.
  Done when: a lease held by a killed pid is reclaimed on the next resume, and a live owner's lease is never taken.

- **Estimate remaining work and say "not done" with a number** — FEATURE — value 3 — effort S — risk low — category: done signal
  Why: the user needs to know when it is actually done. Assumption: a count of unproven steps is a cheap, honest proxy.
  Done when: every goal status line prints "k of n steps proven" and agrees with the ledger.

- **Wild: Hold a goal "fire drill" that kills the session on purpose mid-goal** — FEATURE — value 3 — effort M — risk med — category: chaos (wild)
  Why: assumption: seeded interruption during real goals finds resume bugs before the user does.
  Done when: a nightly run on a scratch repo kills the drive at random and the goal still finishes with all checks green.

- **Wild: Make a stranger finish the goal from the handoff alone** — FEATURE — value 4 — effort M — risk low — category: continuity (wild)
  Why: a cold child with no history reading only the checkpoint is the strictest test of whether the carried plan is complete.
  Done when: a fresh child with only the checkpoint file completes the next step correctly in 4 of 5 trials.

- **Wild: Write the goal's "I'd know it's done when…" sentence first and test against it at the end** — FEATURE — value 4 — effort S — risk low — category: true done (wild)
  Why: false dones come from the agent grading itself. Assumption: a sentence written before the work resists drift.
  Done when: the sentence is stored at intake, sealed by hash, and the close step reads it back and attaches a command for each clause.

- **Warn when the worktree and the main checkout disagree about the goal** — FIX — value 3 — effort S — risk low — category: worktree
  Why: the harness puts the builder in a separate tree; plans edited in one are invisible in the other.
  Done when: a goal edited in main appears in the worktree's next `fm next` within one call.

Next question: Which of the 6 false dones in the long tier were a missing check, and which were a check that passed vacuously?
Next question: Does any resume path read the transcript rather than the ledger, and does a compaction change what it sees?
