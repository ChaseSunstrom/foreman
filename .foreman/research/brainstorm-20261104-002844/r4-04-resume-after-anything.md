# Brainstorm — lens: resume after anything

- **Resume from a ledger-derived checkpoint, not the model's memory** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: resume is the worst area (2 of 6 needed a later fix); T-2900 and T-2901 were both found by the user after a dead process left state behind. Assumption: a single deterministic reducer over existing ledgers (tasks, leases, grants, background list, git HEAD) can yield "where I am" with no model call.
  Done when: `sampo resume --json` run in a scratch home after SIGKILL at a random ledger write prints open clauses, held leases (with owner liveness), last verified evidence and the next command, and two runs on the same ledgers print identical output.

- **Kill the builder at every ledger write and compare verdicts** — FEATURE — value 5 — effort M — risk low — category: resume testing
  Why: two resume fixes landed only after the user hit them; the long tier is deferred, so nothing exercises crashes now. Assumption: ledger appends go through a small number of writer functions that a test harness can interpose.
  Done when: a test enumerates every append point on the goal path, kills there, resumes, and asserts the final done verdict equals an uninterrupted run's for all points; a planted torn write makes it fail.

- **Resolve state from the main repo inside any worktree** — FIX — value 5 — effort M — risk med — category: worktree
  Why: the request names evidence and lease commands failing inside the builder worktree the harness placed the agent in. Assumption: the cause is state-dir resolution from cwd; git's common dir is the stable anchor.
  Done when: in a harness-made worktree, `sampo evidence add`, `sampo lease take` and `sampo task finish` succeed and write to the same ledger the parent reads, verified for every verb on the goal path by a cwd-matrix test.

- **Print a resolution trace when a verb can't find its state** — FIX — value 4 — effort S — risk low — category: diagnosability
  Why: the worktree failure left the agent unable to self-heal; assumption: the error today lacks which path was tried and why.
  Done when: a failing verb in a worktree prints the cwd, git common dir, state dir tried and a `Next:` command that works, and the line parses as a valid command.

- **Reclaim a dead holder's lease with proof of death** — FEATURE — value 4 — effort M — risk med — category: leases
  Why: T-2900 shows dead processes leave open work that blocks the drive. Assumption: leases record pid, start time and session id.
  Done when: a lease whose pid is gone or whose start time mismatches is taken over by the resumed session with a ledger record naming the proof; a live holder is never taken over (test with a held pid).

- **Re-inject a 40-line goal anchor at PreCompact and SessionStart** — FEATURE — value 5 — effort M — risk med — category: compaction
  Why: the goal must survive days and compactions; false dones are unchanged since gen 2. Assumption: the anchor is built from clauses and evidence status, not prose summary, and fits a fixed budget.
  Done when: after a forced compaction in a scratch goal, the first turn's injected context contains every open clause id and the original goal sentence, and the anchor never exceeds 40 lines on a 100-clause goal.

- **Hold done as provisional, then re-run the proofs from cold in a fresh worktree** — FEATURE — value 5 — effort M — risk med — category: done-gate
  Why: 6 false dones unchanged; evidence made in a dirty or stale tree can pass once. Assumption: evidence commands are recorded with the tree hash.
  Done when: closing a goal marks it provisional, a fresh-worktree replay runs each recorded proof, and a planted proof that only passes in the original tree flips the goal back to open.

- **Fence evidence writes with a spool outbox inside the worktree** — FIX — value 4 — effort S — risk low — category: worktree
  Why: denied or unreachable state writes from a worktree lose evidence silently; assumption: the worktree is writable even when the main state dir is not.
  Done when: with the state dir made read-only, evidence is written to a worktree-local outbox, and merge on landing moves it into the ledger exactly once (idempotent on re-run).

- **Detect a split world between worktree and main checkout** — FIX — value 3 — effort S — risk low — category: worktree
  Why: the builder works in a tree the parent doesn't read. Assumption: HEAD and base can be compared cheaply at session start.
  Done when: starting a session in a worktree whose base is behind the goal's recorded base prints one warning line with the drift count and the rebase command.

- **Write a "where I stood" line before every risky call (wild)** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: assumption: a one-line pre-image (intent, target, expected result) makes a killed step resumable by skip-if-already-landed. Wild.
  Done when: killing during a multi-file edit and resuming skips steps whose post-check already holds and redoes the one that doesn't, shown in a scratch test.

- **Run an amnesia drill on a scratch goal every night (wild)** — FEATURE — value 4 — effort M — risk low — category: drills
  Why: resume regressions go unseen until the user hits them; assumption: a cheap Haiku or zero-token scripted goal can run in the tick. Wild.
  Done when: a nightly job kills a scratch goal at a random point, compacts, resumes, and files a task with the transcript if the done verdict differs from the control.

- **Hand a stranger model the goal mid-run (wild)** — FEATURE — value 3 — effort M — risk med — category: portability
  Why: any orchestrator must work (standing rule); assumption: the resume card is self-sufficient. Wild.
  Done when: a goal started under one model is resumed under another from the card alone and reaches the same clauses proven, scored by the long tier.

- **Write the goal as a plain GOAL.md any harness can resume** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: Codex, Gemini and opencode lack Sampo's hooks (T-0337); a file works without them. Assumption: clauses and status fit a diffable text format the ledger renders.
  Done when: deleting all ledgers and keeping GOAL.md plus git, `sampo resume` rebuilds clause status as unmeasured and lists what to re-prove.

Next question: which resume failures does the user hit that never touch a crash, such as a laptop suspend, a changed model, a moved repo path or a pulled branch, and does the resume reducer treat each as a first-class case?
Next question: when the reducer disagrees with the transcript about what is done, who wins, and where does the user see the disagreement?
