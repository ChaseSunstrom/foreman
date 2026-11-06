# Brainstorm — lens: crash and compaction survival

Lens: crash and compaction survival. Mission: a vague goal becomes a complete plan carried over days, crashes and compactions, knowing when it is actually done. Gaps cited: resume is worst (2 of 6 needed a later fix), evidence/lease commands fail inside the builder worktree, 6 false dones unchanged since gen 2.

- **Resolve the state dir from the git common dir, not the cwd** — FIX — value 5 — effort S — risk low — category: worktree
  Why: the pack says evidence and lease commands fail inside the builder worktree the harness puts the agent in. A worktree has its own `.git` file, so any path built from cwd or toplevel misses the main repo's ledgers.
  Done when: in a fresh `git worktree add`, `fm evidence add`, `fm lease take` and `fm task finish` read and write the same ledger as the main checkout, and a test runs all three from a worktree.

- **Write a goal charter file at intake that survives compaction** — FEATURE — value 5 — effort M — risk low — category: goal-state
  Why: the goal is a vague sentence that must reach "complete plan". Compaction summaries paraphrase it and drift. The charter holds the verbatim goal, the clauses extracted from it, and the plan items, and is re-injected at SessionStart (source compact or resume).
  Done when: after a forced compaction, the first turn's injected note quotes the original goal verbatim plus the count of clauses still open, and a test asserts both.

- **Make every done-claim a clause-by-clause receipt** — FIX — value 5 — effort M — risk med — category: true-done
  Why: long tier is 0/6 true done with 6 false dones unchanged since gen 2, so the finish check is not tracking the goal. Each charter clause needs a command or file evidence id, and `task finish` refuses while any clause is unmatched.
  Done when: replaying the 6 false-done scenarios, `fm task finish` refuses on all 6 with the unmatched clause named, and the long tier shows fewer than 6 false dones.

- **Stamp a checkpoint at every tool-boundary, not just at Stop** — FEATURE — value 4 — effort M — risk med — category: crash-resume
  Why: resume is the worst area, 2 of 6 needing a later fix (T-2900 and T-2901 were both resume bugs). A killed process never reaches Stop, so a checkpoint written only at Stop is lost. Append one small record (current step, files touched, open agents, last evidence id) after each plan step.
  Done when: SIGKILL of a session mid-step, then resume, shows the next prompt naming the exact step in flight, tested with a kill-point sweep.

- **Reconcile on resume: re-derive state from git and ledgers, then diff against the checkpoint** — FIX — value 5 — effort M — risk low — category: crash-resume
  Why: T-2900 shows a dead process leaves open background work. The same class applies to leases, half-written tasks and uncommitted trees. A single `resume reconcile` pass closes stale leases, flags uncommitted files by the step that made them, and prints one "you were here" card.
  Done when: planting a dead lease, a stale agent record and a dirty file, then resuming, closes the first two and attributes the third to a plan step, all in one printed card.

- **Run a compaction drill as a long-tier fault** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: the long tier has planted faults (forced compaction, killed session), yet resume still needed fixes after the fact. Make the drill a gate: compact at a random step, then require the agent to name its next step correctly without rereading the transcript.
  Done when: `fm exam long` includes a compaction at a seeded random point, and the score records whether the next step matched the plan's.

- **Keep a plan ledger with per-item states and dependencies** — FEATURE — value 4 — effort M — risk med — category: plan
  Why: "complete plan carried over days" needs more than a todo list. Each item carries state (open, in-flight, done-with-evidence, blocked-by), so a resumed session picks the next unblocked item rather than re-deriving it.
  Done when: killing the session twice at different points yields the same next item as an uninterrupted run, checked by a test.

- **Detect goal drift after compaction by diffing the agent's restated goal** — FEATURE — value 3 — effort S — risk low — category: goal-state
  Why: assumption: compaction summaries shift wording. On resume, ask the agent to restate the goal in one line and compare it to the charter by clause overlap, flagging a mismatch.
  Done when: a planted paraphrase that drops one clause raises a drift warning naming that clause.

- **Wild: Hold a "dead-man done" hold for 24 hours** — FEATURE — value 3 — effort S — risk low — category: true-done
  Why: wild. A multi-day goal closes provisionally, then a cold re-check re-runs all its evidence a day later and only then marks it done. This catches false dones that pass once.
  Done when: a goal whose evidence later fails moves from provisional to reopened with the failing clause named.

- **Wild: Stage a nightly "amnesia test" on the live goal** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: wild. A tool-less child receives only the charter and plan ledger, then predicts the next step. Disagreement with the real next step means the saved state is too thin.
  Done when: the nightly run logs agreement per active goal and files a task when it falls under a set rate.

- **Wild: Leave a "note to self" letter at each checkpoint in the agent's own words** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: wild. State fields lose intent. A three-line letter ("what I was about to try and why") written before risky steps is re-read on resume, with the structured state as backup.
  Done when: after a kill, the resume card quotes the letter, and a test shows it present in 100% of kill points.

- **Replay a crash into a scratch worktree before trusting the resume fix** — PERFORMANCE — value 3 — effort M — risk low — category: reliability
  Why: resume fixes landed late because bugs showed up only in live runs. Record a real session's event stream and replay it with kills injected.
  Done when: a recorded stream with 20 kill points replays in CI and every resume produces a card matching the golden one.

- **Pin the clause-to-evidence binding by content hash** — SECURITY — value 3 — effort S — risk low — category: true-done
  Why: assumption: evidence that later changes (a file edited after the proof) makes a done stale. Hashing the files each evidence item covers lets finish notice.
  Done when: editing a covered file after evidence is recorded marks that clause stale and blocks finish.

Next question: which of the 6 false dones came from a clause that was never extracted from the goal, and which from a clause whose evidence was weak?
Next question: when a resume fix lands late, was the missing scenario in the drill list or present and unscored?
