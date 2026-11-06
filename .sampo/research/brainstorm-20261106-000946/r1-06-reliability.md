# Brainstorm — lens: reliability

Thinking through the reliability lens, the pack shows a system with massive parallelism (20+ agents, lanes, worktrees, triggers, self-edits, hooks, local models, cloud endpoints, migrations) and several explicit failure classes: hook latency, silent cuts, guard false-positives, state size (2.4 GB), worktree split-brain, lease races, fail-open, and "done" that doesn't hold. The user's words lean hard toward unattended correctness, "still get done quick and not expensive," and push grants that keep landing. So reliability = unattended runs that hold, fail loudly but not falsely, and recover deterministically.

I'll go deep on failure-mode correctness rather than breadth.

- **Give every verdict a provenance proof-chain, and refuse "done" without it** (FEATURE) — value 5 — effort M — risk low — category: correctness
  Why: The pack's false-dones and "could-not-run" states recur; claims are only as good as their evidence. A chain (clause → command → output hash → tree hash) makes a close replayable and lets a cold reader verify it without trusting the builder.
  Done when: `sampo verify T-id` re-derives each clause verdict from stored outputs on a fresh checkout and matches, or flags exactly the drifted clause.

- **Turn the Ward's false-refusal into a first-class, measured class, not a mystery** (FIX) — value 5 — effort M — risk low — category: safety
  Why: T-2967 and the pgrep bracketed-pattern incident show the Ward blocks the *literal text* of a command, not its intent. That's a reliability hole in both directions: over-refusal stalls work, and it's unmeasured.
  Done when: `sampo ward audit` prints the 7-day over/under-refusal counts with the exact commands and a "would-have-been-safe" flag, and a regression case proves the bracket-pattern class no longer self-matches.

- **One canonical state resolver: every verb, hook and lane reads paths from git's common dir, never a literal** (FIX) — value 5 — effort M — risk med — category: state
  Why: The migrated-home bug (T-2967) and the worktree split-brain (36 sites naming `.foreman/`) share one root: code compares literal paths. A single resolver kills the whole class, not one instance.
  Done when: a fuzz run over {real path, symlink, worktree, moved home, deleted cwd} yields identical guard and ledger decisions for every verb.

- **Kill-lease fencing: no two holders of a task or lane can both write, provably** (FEATURE) — value 4 — effort L — risk med — category: concurrency
  Why: With 20 agents, leases and "take over a dead holder" recur. A git-ref or monotonic epoch fence makes takeover safe even if the old holder is only *slow*, not dead.
  Done when: a split-brain drill with two drives on one repo ends with exactly one commit and a logged, correct loser, with no lost write.

- **Ledger writers are kill-safe by construction, proven by a kill-point sweep** (PERFORMANCE) — value 5 — effort M — risk med — category: durability
  Why: Unattended night runs meet SIGKILL, suspend and ENOSPC. A sweep that kills each writer at every write boundary and requires a clean, resumable state makes "the drive died at 3 a.m." a non-event.
  Done when: the sweep across all writers leaves no torn file; `sampo doctor` shows every ledger consistent after a mid-write kill.

- **Fail-loud, then fail-quiet: distinguish "I can't read this" from "nothing to report" everywhere** (CLEAN) — value 4 — effort S — risk low — category: observability
  Why: The pack repeatedly collapses a blank into a pass. A three-state verdict (proven / unmeasured / could-not-run) with a plain cause line stops silent false-dones and respects the user's "fail loud with a named cause."
  Done when: no UI, status line or close card can render a missing reading as a pass; every "could-not-run" names its cause and the command that would clear it.

- **Reconcile on resume: rebuild state from git + ledgers, then diff against the checkpoint** (FEATURE) — value 5 — effort L — risk med — category: recovery
  Why: Compaction, killed sessions and migrations all risk a session believing a stale world. Re-deriving and diffing before the first action catches drift the model would otherwise carry forward.
  Done when: a resume after a forced compaction shows a "reconciled: N deltas" line, and a planted drift is caught and reported before any edit.

- **A deterministic "replay any closed task" from the ledger alone, no network, no GPU** (FEATURE) — value 5 — effort M — risk low — category: auditability
  Why: Genericity and "proves its work with commands it really ran" both depend on replay. A hermetic replay is the cheapest, strongest reliability proof and the backbone of every future regression.
  Done when: `sampo replay T-id --offline` reproduces the same verdict on a fresh clone, byte-for-byte on the evidence hashes.

- **Hook self-bait at every start: plant one benign command the Ward must block, silent unless it fails** (FEATURE) — value 4 — effort S — risk low — category: liveness
  Why: The guard going quiet is the most dangerous silent failure and currently invisible. A 1-token canary per session start makes "the Ward is off" impossible to miss without adding noise.
  Done when: a test disables the hook and the start line shows a named, red "guard canary failed" within one turn.

- **wild — A "dead-man done" hold: before any unattended close, a cold, different-model child must list unmet clauses and cite none** (wild) — value 4 — effort M — risk med — category: adversarial
  Why: The user grants push-without-asking, so a wrong close ships itself. A cheap, adversarial gate that only blocks on an *unmet* clause adds safety without adding cost on clean work.
  Done when: a seeded false-done is caught and held with the specific clause named, and a clean close passes with zero extra user turns.

- **wild — Run the drive's own worst day as a standing fixture: a recorded 3 a.m. ledger replayed through every surface on each ship** (wild) — value 4 — effort L — risk med — category: chaos
  Why: The pack has many one-off incidents (CI timeout, core.bare leak, deploy-page timeout, ENOSPC). A single replayed "worst day" turns scattered scars into one regression that ships nothing unless the night holds.
  Done when: the ship gate includes the worst-day replay and fails on any surface whose behavior regressed versus the recorded outcome.

- **wild — Self-surgery rehearsal: a throwaway nightly clone where Sampo applies its most recent self-edit and is judged only by outcomes, never by intent** (wild) — value 3 — effort M — risk high — category: self-modification
  Why: The user steers Sampo to advance itself, and self-edits to guard/hook files are the highest-risk change class. Rehearsing in a clone with an outcome-only judge catches a self-edit that *claims* to help but makes outcomes worse, before it lands.
  Done when: a self-edit that worsens a held-out outcome set is auto-reverted by the rehearsal with a one-line "reverted: reason" in the ledger.

- **A single, content-addressed "last good" snapshot per capability class, restorable in one key** (FEATURE) — value 4 — effort M — risk low — category: rollback
  Why: Migrations, renames and self-edits all risk an unrecoverable state. A content-hash-pinned last-good snapshot makes "undo the last change to the guard" deterministic instead of best-effort (homemove._undo already breaks on a changed hash).
  Done when: after any state change, `sampo restore <class>` returns the exact prior snapshot and `sampo doctor` confirms the guard and ledgers match it.

- **wild — A "Sampo is gone" morning: weekly, disable every Sampo capability for one live session and log what the user had to do by hand** (wild) — value 3 — effort S — risk low — category: counterfactual
  Why: The user's core question is whether Sampo still earns its tokens. A recurring bare-host session measures the *actual* reliability delta (what breaks without it) that no self-report can claim.
  Done when: the week's bare-session log names each hand-done step, and Sampo's next pack lists which one it could have automated.

- **Budget the night by yield-knee: stop when marginal progress per token drops, and say so** (PERFORMANCE) — value 4 — effort M — risk low — category: efficiency
  Why: The user explicitly wants "done, not burning a fortune, and quick." A yield-knee stop (rather than a clock) spends tokens only where they still move the goal, and logs the stop reason.
  Done when: two runs on the same night stop at different yields with a logged knee value, and total spend tracks the curve rather than a fixed budget.

Next question: What is the single longest unattended window this user actually runs Sampo (overnight, multi-day, or multi-machine), and is there a recorded incident at its *boundary* — so we know whether the reliability target is "survive a night" or "survive a week"?
Next question: Which silent failure has cost this user the most real time so far — a false "done" that shipped, a stall that looked like progress, or a state corruption that needed a full rebuild — because that is the one the dead-man and worst-day ideas should target first?
