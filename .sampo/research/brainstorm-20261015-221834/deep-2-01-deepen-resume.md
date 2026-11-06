# Brainstorm — lens: deepen: resume

- **Resume the whole fleet with one verb (`fm resume --all`)** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: the user asked that stopped worktree agents "resume easily"; the Agents graph already lists worktrees and T-1028 is planned for single builders. Combining the manifest, git reconcile and checkpoint ideas into one triage pass is the natural next step.
  Done when: with three killed builders in different states (clean, dirty, merged), `fm resume --all` prints a table with a verdict per builder (continue, salvage, discard-merged) and relaunches only the continuable ones, each in its own worktree.

- **Reconcile before resuming: classify each stopped builder against git** — FEATURE — value 5 — effort S — risk low — category: resume
  Why: a stopped worktree may have uncommitted edits, commits already merged to main, or a branch that has diverged. Offering a blind resume would redo or clobber work. Assumption: the branch and task id are recoverable from the worktree name or ledger.
  Done when: a test fixture with merged, diverged, dirty and untouched worktrees gets the correct verdict for each from `fm resume --plan`, and none of them is mutated.

- **Checkpoint builders to a hidden git ref on every step** — SECURITY — value 4 — effort M — risk low — category: resume
  Why: a killed session loses uncommitted edits. A commit written to `refs/foreman/ckpt/<task>` with a temporary index leaves the branch and working tree untouched, and the ref travels with git when pushed. Without that a resume can't survive a crashed disk or another clone.
  Done when: after `kill -9` on a builder mid-edit, `fm resume` restores the uncommitted file contents from the ref, and the builder's branch history is unchanged.

- **Write a resume capsule: brief, plan, next step, failing proof** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: "instructions that survive compaction and new sessions" is the top research ask. The capsule is a small file holding the brief, the acceptance criteria, the steps done, the last red command and its output, and the lessons recalled. A fresh session then needs about 1k tokens of context instead of re-scanning the repo.
  Done when: a resumed builder's first prompt contains the capsule, and a test shows it can name the next step without reading any file the capsule already summarised.

- **Offer resume at SessionStart and in the pane** — FEATURE — value 4 — effort S — risk low — category: resume
  Why: nobody remembers to run a resume command. The Agents graph already shows worktrees, so stopped nodes can be drawn dimmed with a "resume" action, and SessionStart can print one line such as "2 builders stopped: fm resume".
  Done when: with a stopped builder present, SessionStart output contains the resume line, and the pane's Agents graph marks the node as stopped.

- **Make resume idempotent with a lease and heartbeat** — FIX — value 4 — effort M — risk med — category: resume
  Why: two sessions might resume the same worktree, and a slow "stopped" agent might still be alive. Builders write a heartbeat and the resumer takes a lease, so a live builder is never double-driven. The earlier incident where the UI harness session was driven by the Stop hook into the queue shows that cross-session interference already happens here. Assumption: PID or timestamp liveness is sufficient.
  Done when: running `fm resume` twice at once on one worktree starts exactly one agent, and a builder with a fresh heartbeat is refused with a clear message.

- **Carry resume capsules and checkpoints across machines through git** — FEATURE — value 4 — effort M — risk med — category: resume
  Why: the user steered that fixes must travel with git so other sessions, clones and teammates use them. The same applies to a stopped task: push the capsule and checkpoint ref, and another clone runs `fm resume T-xxxx`.
  Done when: in a second clone, after `git fetch`, `fm resume T-xxxx` recreates the worktree from the pushed ref and prints the capsule.

- **Learn why builders stop and pre-empt it** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: this joins the resume idea to the user's "learn a fix once" request. Record the stop cause (trust prompt, budget cap, killed session, test red loop) with the fix that worked, and apply it automatically on the next resume, for example by pre-accepting the trust prompt or raising the cap. Fixes are kept as git-carried hints in the repo.
  Done when: after a resume that fixed a trust-prompt stall once, the next resume applies the fix without a prompt, and a hint file appears in the repo.

- **Show resume cost before committing: tokens to catch up** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: the research notes that cost matters, and the user wants least token use. Estimate capsule size against redoing the work, and let `fm resume --plan` recommend resuming versus restarting fresh from the brief.
  Done when: the plan output shows a token estimate and a resume-or-restart recommendation for each builder.

- **Wild: Rewind a builder to any past step (time-travel resume)** — FEATURE — value 4 — effort L — risk med — category: resume
  Why: wild. With a checkpoint ref per step, a user can pick "go back to before step 3 and try another approach". That gives a branching tree of attempts, which could be drawn in the Agents node graph. The checkpoint refs make it cheap.
  Done when: `fm resume T-x --at 3` restores the tree as of step 3 in a new worktree, and the original branch is kept intact.

- **Wild: Resume from another harness (cross-agent handoff)** — FEATURE — value 3 — effort L — risk high — category: resume
  Why: wild. The capsule is plain text and git state, so a stopped Claude builder could be continued by Codex, Gemini or opencode, which matters because T-0335 to T-0337 show those adapters are blocked. Assumption: the capsule format stays harness-neutral.
  Done when: `fm resume T-x --on codex` launches Codex with the capsule as its brief, with the agent noted as a fallback.

- **Wild: Self-healing fleet supervisor that auto-resumes overnight** — FEATURE — value 4 — effort L — risk high — category: resume
  Why: wild. A watcher notices a builder that died or hit a rate limit and resumes it when the limit resets, with crash-loop quarantine after N failures (see T-0798 on recovery and T-0793 on overnight work). The user would wake up to finished work.
  Done when: with a builder killed at random, the supervisor resumes it within one interval, and after three crashes in a row it quarantines the builder and reports why.

- **Salvage and hand back partial results when resume is not worth it** — FEATURE — value 3 — effort M — risk low — category: resume
  Why: some builders stopped with useful partial work, such as a passing test, but the plan is stale. Salvage cherry-picks the green commits and files the remainder as a new task with the brief updated. This relates to T-0831 on partial results from capped children.
  Done when: `fm resume --salvage T-x` creates a branch containing only the verified commits and a new queue task describing what remains.
