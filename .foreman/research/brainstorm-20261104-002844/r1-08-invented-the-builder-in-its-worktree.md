# Brainstorm — lens: invented: the builder in its worktree

- **Resolve state from the common git dir in any worktree** — FIX — value 5 — effort S — risk low — category: worktree
  Why: the request says evidence and lease commands fail inside the builder worktree. Assumption: they find state through cwd or `.git` as a directory. In a linked worktree `.git` is a file, so `git rev-parse --git-common-dir` is the safe key.
  Done when: `fm evidence add` and `fm lease take` succeed from a linked worktree and write to the same state as from the main checkout (test compares the two).

- **Run every verb across a worktree matrix** — FIX — value 5 — effort M — risk low — category: testing
  Why: the failure was found by users, not by tests. Assumption: the suite only runs verbs from the main checkout.
  Done when: one parametrised test runs the evidence, lease, task, finish and prove verbs from main, linked worktree, subdir, detached HEAD and a worktree under `/run/user/…`, and all pass.

- **Pin state with an env var at lane spawn** — FIX — value 4 — effort S — risk low — category: lanes
  Why: the harness chooses where the builder works, so the builder shouldn't have to guess where state lives. Assumption: lane spawn already knows the main repo path.
  Done when: a builder started in a worktree outside the repo tree finds the state dir through `SAMPO_STATE` alone, and `fm doctor` names the variable's source.

- **Replay all evidence in a fresh worktree before accepting done** — FEATURE — value 5 — effort M — risk med — category: true done
  Why: tier 0/6 true done with 6 false dones, unchanged since gen 2. A builder's own worktree can hold uncommitted files that make the evidence pass.
  Done when: `fm task finish` creates a clean worktree at the final commit, re-runs every recorded evidence command there, and refuses done on any mismatch. A planted untracked-file fixture is refused.

- **Store the plan as clauses, each needing evidence at a reachable commit** — FEATURE — value 5 — effort M — risk med — category: plan and done
  Why: "a vague goal becomes a complete plan … knowing when it is actually done". Assumption: done is currently judged from a summary, not clause by clause.
  Done when: `fm goal status` lists each clause with the commit and command that proved it, and done is true only when every clause has one reachable from HEAD.

- **Add a handoff note the builder rewrites each step** — FEATURE — value 4 — effort S — risk low — category: resume
  Why: resume is the worst area (2 of 6 needed a later fix), and compaction drops context. A note kept in the common dir survives a worktree being deleted.
  Done when: after a forced compaction, a fresh builder reads the note and completes the next planned step without re-planning (long-horizon fixture).

- **Take over a stale lease safely on resume** — FIX — value 4 — effort M — risk med — category: leases
  Why: T-2900 shows resumed sessions left dead background work behind. Leases carry the same risk. Assumption: a lease records only pid and time.
  Done when: a lease records pid, worktree path and heartbeat. A resumed builder takes over only when the pid is dead and the heartbeat is old, and a live holder is refused (two tests).

- **Re-attach a moved or missing worktree on resume** — FIX — value 4 — effort M — risk med — category: resume
  Why: "WIP: builder stopped; work kept by fm lane resume" shows resume already works from commits. Assumption: a missing or relocated worktree path is not handled.
  Done when: deleting the lane's worktree dir mid-task, then resuming, recreates it from the WIP branch with no lost commits.

- **Print a worktree-aware Next line on every failure** — FIX — value 3 — effort S — risk low — category: diagnosability
  Why: a builder that sees an opaque error will retry or give up. Assumption: today's errors don't say which worktree and state dir were used.
  Done when: any verb failing inside a linked worktree prints the worktree, the resolved state dir and one corrective command.

- **Probe the verb classes at lane start** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: failures appear mid-task, after work is done. A 2-second `fm lane probe` that tries evidence, lease and finish in dry-run mode would catch them at the start.
  Done when: the probe fails a lane with a broken state path before any edit, and the failure is recorded in the lane ledger.

- **Wild: kill the builder at random and require the same verdict** — FEATURE — value 4 — effort M — risk med — category: resume drills
  Why: wild; resume is the weakest area. A seeded SIGKILL at a random step on a scratch repo, followed by resume, must reach the same done verdict as an uninterrupted run.
  Done when: 20 seeded kills all reach the same true/false done verdict, and the drill reports any divergence.

- **Wild: ghost builder tries to pass done without the work** — FEATURE — value 4 — effort M — risk low — category: false-done
  Why: wild; six false dones persist. A cold child gets only the plan and gate, and is scored on whether it can make `done` fire with a stub or a deleted test.
  Done when: the exam lists which false-done shapes the gate accepted, and each accepted shape becomes a failing test.

- **Wild: leave a "morning after" bundle for each multi-day goal** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild; goals span days, crashes and compactions. The user returns to a one-page bundle with clauses proven, clauses open, crashes survived and the exact replay command.
  Done when: the bundle is generated from ledger records alone with no model call, and a cold reader can name the next action from it.

- **Wild: score done-ness forecasts against the later outcome** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: wild; the system claims "actually done" but is never checked afterwards. Each done is sealed with a confidence, then marked wrong if the user reopens or re-asks within 14 days.
  Done when: `fm goal calibration` prints the false-done rate over closed goals using the existing close-survival record.

Next question: which of the six false dones were passed by evidence that only held in the builder's own worktree (uncommitted or untracked files), and which were gaps in the plan itself?
Next question: after a resume, does the new builder trust the old builder's recorded evidence, and what would show it that evidence has gone stale?
