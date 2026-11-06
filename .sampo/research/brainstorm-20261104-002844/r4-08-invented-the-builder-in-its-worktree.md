# Brainstorm — lens: invented: the builder in its worktree

- **Resolve state from the main repo inside any worktree** — FIX — value 5 — effort M — risk med — category: worktree state
  Why: the request names "evidence and lease commands fail inside the builder worktree the harness put the agent in"; the lane's `.sampo` dir doesn't exist there. Assumption: the failure is state resolved by cwd rather than by git common dir.
  Done when: in a fresh `git worktree add` checkout, `fm evidence add` and `fm lease take` write to the main repo's state and `fm evidence list` run from the main checkout shows them.

- **Run a worktree parity matrix in CI** — FIX — value 4 — effort M — risk low — category: testing
  Why: the failure was only found by a long-tier run; nothing tests every verb the goal path calls from a worktree.
  Done when: a test runs each goal-path verb from main, a linked worktree and a worktree under a symlinked path, and fails if any verb's result differs.

- **Print a resolution trace on every worktree failure** — FEATURE — value 4 — effort S — risk low — category: diagnosability
  Why: the builder gets an error but not which path it looked in. Assumption: current errors name the verb, not the resolved state dir.
  Done when: a failing `fm evidence` run in a worktree prints cwd, git common dir, state dir tried and a `Next:` line that works.

- **Spool evidence to a worktree-local outbox, merge on landing** — FEATURE — value 4 — effort M — risk med — category: evidence
  Why: when the harness sandbox denies writes outside the worktree, evidence must still be captured, or the false-done problem returns. Assumption: some harnesses deny writes to the main repo's state dir.
  Done when: with the main state dir made read-only, `fm evidence add` succeeds into `<worktree>/.sampo-outbox`, and `fm lane land` moves it into the ledger with hashes intact.

- **Detect a dead lease holder from inside the worktree** — FIX — value 4 — effort M — risk med — category: leases
  Why: resume is the worst area and crashed builders leave leases behind. Assumption: the lease records pid and worktree path but resume does not check either.
  Done when: killing a builder with SIGKILL and starting a new session in the same worktree reclaims the lease and prints the proof of death, and a live holder is never taken over.

- **Preflight the closing path at task start** — FEATURE — value 5 — effort S — risk low — category: builder flow
  Why: today the builder learns at the end that `fm task finish` fails, after hours of work. Assumption: the failure is detectable at the start.
  Done when: `fm task start` in a worktree runs a dry write of evidence, lease and finish and refuses with a plain reason if any would fail.

- **Keep a shadow ref of the worktree's work** — FEATURE — value 3 — effort S — risk low — category: crash recovery
  Why: the log says "builder stopped; work kept by fm lane resume", so a killed builder's work is held only by that path. A ref under `refs/sampo/shadow/<task>` survives worktree deletion.
  Done when: after deleting the worktree directory by hand, the last tool-boundary snapshot is recoverable with one command.

- **Overlay main's state read-only under the worktree** — FEATURE — value 3 — effort M — risk med — category: worktree state
  Why: the builder in a worktree can't see the steers, lessons or goal clauses, so it plans without them. Assumption: those live in the main repo's untracked state.
  Done when: in a worktree, `fm steers` and `fm goal show` print the same content as in main, and a write attempt goes through the broker or fails with a named reason.

- **Fence edits to the assigned worktree** — SECURITY — value 3 — effort M — risk med — category: guard
  Why: a builder with a stale cwd can edit the main checkout and corrupt the parent's work. Assumption: the guard doesn't compare edit paths to the lane's worktree.
  Done when: an Edit or Write by a lane builder on a path in the main checkout is blocked with a `Next:` line, and one inside its worktree passes.

- **Say which Sampo code is running** — FIX — value 3 — effort S — risk low — category: diagnosability
  Why: worktrees hold their own copy of `plugin/`, so a builder may run the old verbs while editing new ones. Assumption: the hooks and `fm` resolve to the installed copy.
  Done when: `fm doctor` in a worktree prints the source of `fm`, the hooks and the state dir, and flags a mismatch with the worktree's own `plugin/`.

- **Wild: Run a ghost builder through a harness worktree each night** — FEATURE — value 4 — effort M — risk low — category: drill
  Why: wild — a scripted builder that calls the harness's real worktree call, takes a lease, records evidence, finishes and tries to close without real work, so a regression shows overnight rather than in a long-tier run.
  Done when: a nightly run reports pass for the honest path and a refusal for the no-work path, and a planted worktree-state bug turns it red.

- **Wild: Have a builder write "where I stood" before every risky call** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: wild — one line per risky call, written to the shadow ref, which a resumed session reads first; it covers the gap between checkpoints at tool boundaries.
  Done when: killing the builder at a random point and resuming shows the last line in the resume card, and the next action matches it.

- **Wild: Heal a failed verb through the parent, then log it** — FEATURE — value 3 — effort L — risk high — category: worktree state
  Why: wild — when `fm evidence` fails in a worktree, the verb asks the parent session to run it and writes a ledger row saying a heal happened, so the builder never stalls and the user can see how often it did.
  Done when: with the main state dir unwritable from the worktree, the verb succeeds via the parent and a "healed" row appears in the ledger with the reason.

- **Wild: Warn when a worktree outlives its task** — CLEAN — value 2 — effort S — risk low — category: hygiene
  Why: wild — a janitor on the tick lists worktrees with no open lease or task and offers a trash-with-TTL removal after checking nothing unlanded is inside.
  Done when: a worktree whose task closed 3 days ago is listed by `fm doctor` with its unlanded-commit count, and removal moves it to the trash.

Next question: which harnesses (Claude Code, Codex, Gemini CLI, opencode) create the builder worktree, and does each give the agent the same cwd, env vars and write permissions?
Next question: when a builder finishes inside a worktree, which of its records (evidence, lease, lessons, ledger rows) must reach the main repo to survive, and which are safe to lose?
