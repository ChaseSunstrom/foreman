# Brainstorm — lens: bold bets

- **Run gates in the background while the next step starts** — PERFORMANCE — value 5 — effort M — risk med — category: speed
  Why: gates are 18.8 of 125 hours, and one project's `cargo test` takes a median of 8 min about once per task. The session sits idle waiting. Start the gate as a background process the moment the last edit lands, let planning or capture for the next queue item proceed, and only block on the result when "done" is claimed. Assumption: tasks in the queue are independent enough to overlap.
  Done when: on a task with an 8-minute gate, the next task's planning starts before the gate returns, and `fm task done` still refuses until the gate result is recorded.

- **Cache gate results by tree hash** — PERFORMANCE — value 5 — effort M — risk low — category: speed
  Why: the same `cargo test` runs about once per task, even when a retry or a docs-only close-out leaves the tree unchanged. Key the result on a hash of the tracked files plus the command, and reuse a passing result that is still valid. Assumption: the tests are deterministic enough for a cached pass to be trusted.
  Done when: running the gate twice on an unchanged tree executes the command once, and the second run reports "cached pass @ <hash>".

- **Run only the tests the diff can affect** — PERFORMANCE — value 4 — effort L — risk med — category: speed
  Why: full-suite gates dominate wall time. Map the changed files to test targets (cargo/pytest selection), run those on every step, and keep the full suite for the final close-out only. Assumption: the target projects have maps that are cheap to derive.
  Done when: a one-file change runs a subset in under 20% of the full-suite time, and the full suite still runs once before "done".

- **Triage tasks with a Haiku pre-pass that skips ceremony** — PERFORMANCE — value 4 — effort M — risk med — category: token cost
  Why: the median task makes 18 bookkeeping calls, and planning has the highest call count. A cheap model call classifies each request (typo, rename, config, real feature) and picks a fast lane, which uses one plan call, no audit lenses and a single gate. This also cuts tokens, which matters to a usage-sensitive user. Assumption: misclassifications can be corrected by escalating the lane.
  Done when: trivial-class tasks finish with at most 4 fm calls, and an escalation test shows a wrongly lane-classified task upgrading to the full ceremony.

- **Run a "stale fact sweeper" at each task boundary** — FEATURE — value 4 — effort M — risk low — category: context rot
  Why: the user wants long sessions without out-of-date information or stale docs. Record each fact or doc claim with the file hashes it depended on. At a task boundary, re-check the ones whose files changed and flag or fix the stale ones. Assumption: claims can be tied to files at capture time.
  Done when: editing a file that a recorded fact depends on causes that fact to show up as stale at the next boundary, with a one-line diff.

- **Run a "what did I forget to ask" brainstorm against the diff history** — FEATURE — value 4 — effort M — risk low — category: brainstorming
  Why: the user says brainstorms miss "things I want but don't know how to say". Mine past corrections, reverts and re-asks in the ledger for repeated patterns (for example, "L, T, M mean nothing" followed by "clean up your output"). Turn each pattern into a proposed standing preference. Assumption: the ledger keeps enough of the user's phrasing.
  Done when: running it on the 287 tasks produces at least 5 preference proposals, each citing the corrections that support it.

- **Make a "Foreman weather report" at session start** — FEATURE — value 3 — effort S — risk low — category: orientation
  Why: after days of a long session or a new session, the user has to rebuild context. One animated card shows what changed since last time, what is blocked on them, what is at risk, and a time estimate for the queue based on history. Assumption: the view model has enough history for estimates.
  Done when: opening a session on a project with a non-empty queue shows the card with an estimate that is within a stated range of the later actual time.

- **Wild: Run a speculative twin that pre-executes the next queue task in a git worktree** — FEATURE — value 5 — effort L — risk high — category: parallelism
  Why: tasks take hours and the queue is long. While the user's current task is in gates or review, a forked agent starts the next task in an isolated worktree. If the files don't overlap, it merges; otherwise it is discarded. Assumption: the queue has independent tasks, and the user accepts the extra usage in exchange for time.
  Done when: two non-overlapping queued tasks complete in less wall time than serial runs, and an overlapping pair discards the twin cleanly without touching the main tree.

- **Wild: Add a "Foreman dreams" idle-time worker that refactors the rules and playbooks** — FEATURE — value 3 — effort M — risk med — category: self-improvement
  Why: the rules diet (T-0085) and the playbooks both depend on knowing which rules and playbooks actually change outcomes. While idle, a cheap-model job replays past tasks, finds rules that never fired and playbooks that were never used, and proposes a pruned set in the inbox. Assumption: the ledger records which rules or playbooks were active.
  Done when: the job produces a proposal listing at least some unused rules with usage counts, and applying it passes the existing test suite.

- **Wild: Let the user talk to the Foreman mascot as a voice of the queue** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: the mascot already lives in the pane. Clicking it opens an Input where the user asks "what's blocking me?" or "why is this slow?" and a Haiku call answers from `fm ui --json` with a one-line reaction animation. This gives the user a natural-language way into the data they have otherwise had to ask for in commands. Assumption: `model.complete` is cheap enough for short answers.
  Done when: asking "why is this slow?" returns an answer that cites the measured gate and ceremony times for the current task.

- **Wild: Add a token and time budget per task that the plan must fit** — FEATURE — value 4 — effort M — risk med — category: cost control
  Why: the user is usage-sensitive and tasks take hours, but nothing says up front what a task is allowed to cost. Estimate the budget from similar past tasks at the plan step, show it on the band, and warn or ask once at 80% instead of silently overrunning. Assumption: the usage API gives per-task totals.
  Done when: a task that crosses 80% of its budget triggers exactly one warning, and the final summary shows the budget against actual use.
