# Brainstorm — lens: resume after anything

- **Make resume a single replayable "resume.sh" the harness runs before the agent speaks** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: resume is the worst area (2 of 6 needed a later fix); T-2900 and T-2901 were both found after a real resume went wrong. Today the agent re-derives state from scattered ledgers.
  Done when: killing a session at any of 10 seeded points and starting a new one makes `sampo resume --plan` print the same open clauses, lease owner, worktree path and next command as an uninterrupted run, byte for byte after timestamps are stripped.

- **Resolve state from the git common dir in every worktree** — FIX — value 5 — effort M — risk med — category: worktree
  Why: the request says evidence and lease commands fail inside the builder worktree the harness put the agent in; the ledgers are keyed to the main checkout path.
  Done when: in a `git worktree add` checkout, `sampo evidence add`, `sampo lease take` and `sampo task finish` write to the main repo's state and a test over all goal-path verbs passes in both checkouts.

- **Print a resolution trace when a verb can't find its state** — FIX — value 3 — effort S — risk low — category: diagnosability
  Why: the failure in the worktree is silent to the agent, which then gives up on evidence and claims done without it. assumption: the error today lacks the path it tried.
  Done when: running any state verb from an unrelated cwd prints the paths tried, the one chosen, and a `Next:` line that parses.

- **Take over a dead holder's lease with proof of death** — FEATURE — value 4 — effort M — risk med — category: lease
  Why: a killed session leaves its lease, and T-2900 shows dead processes hold open work. Reclaim needs more than a timeout.
  Done when: a lease whose pid/boot-id/start-time no longer matches is reclaimed by `resume` with a ledger record naming the evidence of death; a live holder is refused in a test.

- **Write a goal anchor at every tool boundary and re-inject it at PreCompact and SessionStart** — FEATURE — value 5 — effort M — risk low — category: compaction
  Why: the long tier is 0/6 with the same false dones since gen 2; the original goal words and open clauses are lost to compaction.
  Done when: after a forced compaction in the long-tier scenario, the next model turn's context contains the verbatim goal and the list of unmet clauses (40-line cap), checked in a test.

- **Reconcile on resume: diff git and ledgers against the last checkpoint** — FEATURE — value 4 — effort M — risk med — category: resume
  Why: T-2900/T-2901 are symptoms of ledger state that disagreed with reality after a death. Edits, branch switches and landed commits are not noticed.
  Done when: resuming after a manual commit and a branch switch prints "tree moved: N commits, branch X to Y" and marks steps whose change already landed as skipped.

- **Hold "done" as provisional and re-run the proofs from cold in a fresh worktree** — FEATURE — value 5 — effort M — risk med — category: done-gate
  Why: 6 false dones are unchanged; evidence is tied to a session, not a tree.
  Done when: closing a goal records tree hash plus clause-to-evidence bindings, and a replay in a clean checkout is run before the goal status leaves provisional; a planted stale proof flips the status back in a test.

- **Turn the six false dones into a zero-token regression corpus** — FIX — value 4 — effort S — risk low — category: exam
  Why: the long tier is expensive and deferred to the end of the run, so false dones can't be caught cheaply per generation.
  Done when: six fixtures with a transcript tail and a clause list each run in the finders/oracle arm and fail on the current gate until the gate is fixed.

- **Add a resume drill that kills the builder at every ledger write** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: resume is the worst area and each bug so far was found by a real session, not a test.
  Done when: `sampo drill --resume` kills a scratch goal at each write point and reports zero lost leases, zero duplicate pushes and zero orphan background tasks.

- **Wild: A "will" file the agent writes before each risky step and the resumer reads first** — FEATURE — value 3 — effort S — risk low — category: handoff
  Why: wild; assumption: a one-line statement of intent plus the undo is cheaper to reconstruct from than ledger archaeology. The builder was stopped mid-work in T-2851.
  Done when: killing a session between the will and the step makes resume print the will and whether the step's effect is visible on disk.

- **Wild: A nightly amnesia test on a live goal** — FEATURE — value 3 — effort M — risk low — category: drill
  Why: wild; compaction is the long tier's top failure and no real goal is checked for it. A cold child gets only the resume card and must name the next action; a diff against the true next action is scored.
  Done when: a nightly report shows the match rate per goal and files a task under a set threshold.

- **Wild: Hand the goal to a stranger model mid-run to prove the handoff is model-swappable** — FEATURE — value 3 — effort L — risk med — category: portability
  Why: wild; if a different model can finish from files alone, the resume does not depend on a lucky summary.
  Done when: in the long tier, switching model families at a compaction point yields the same clause outcome as no switch.

- **Resume from a plain GOAL.md any harness can read** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: Sampo is meant to work on Codex, Gemini and opencode too, whose hooks differ (T-0337 shows Gemini has no Stop).
  Done when: a goal started under Claude Code is resumed by a second harness reading only GOAL.md, with the clause list and next command intact.

Next question: which of resume's failures happen before any hook fires (a wrong cwd or a moved worktree), so none of the ideas above get to run?
Next question: after a resume, how often does the user re-state the goal in their own words, and does that measure a lost anchor?
