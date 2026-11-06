# Brainstorm — lens: crash and compaction survival

- **Run a compaction-survival drill as a long-tier fault with a recall quiz** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: resume is the worst area (2 of 6 needed a later fix); the long tier is 0/6 and compaction is only named as a planted fault, not scored on what the agent remembers afterwards.
  Done when: `fm exam long` forces a compaction on a scratch goal, then asks a tool-less child five questions (goal, open clauses, last decision, steers, next step) from only the post-compaction context. The score is printed, and a planted forgotten clause fails it.

- **Write a goal capsule at every tool boundary and re-inject it at PreCompact and SessionStart** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: the Stop-only checkpoint loses everything between Stop events. Crashes and compactions happen mid-turn, and the ideas list asks for tool-boundary stamps without a size budget.
  Done when: killing the session at a random tool call leaves a capsule of 40 lines or fewer that is at most one tool call stale. A fresh session's first context contains the capsule's open-clause list.

- **Resolve state from the main repo inside any worktree** — FIX — value 5 — effort M — risk med — category: worktree
  Why: the pack says evidence and lease commands fail inside the builder worktree the harness put the agent in. The cause is probably state resolved by cwd, not by the git common dir.
  Done when: from a harness-created worktree, `fm evidence add`, `fm lease` and `fm task finish` read and write the same ledger as from the main checkout. A doctor probe covers it, and an unresolvable case prints the paths it tried.

- **Spool denied evidence writes to a worktree-local outbox, merged on landing** — FIX — value 4 — effort S — risk low — category: worktree
  Why: when the state dir is read-only or unreachable from the worktree, evidence is lost, which means false dones or false "unproven" states.
  Done when: with the state dir made unwritable, evidence recorded in the worktree appears in the main ledger after `fm lane resume` or landing, each record exactly once, with an explicit note naming what was replayed.

- **Make leases fenced and reclaimable with proof of death** — FIX — value 4 — effort M — risk med — category: lease
  Why: a crash leaves leases whose holder is gone, and the resumer cannot tell a live builder from a dead one. The ideas list has "take over a stale lease" without the fencing token.
  Done when: each lease records pid, host, boot id and a monotonic token. After SIGKILL, resume reclaims it only if the pid is gone, and a late write from the old holder is rejected by its stale token. Both are tested.

- **Kill the goal run at every ledger write and compare the final verdict to an uninterrupted run** — PERFORMANCE — value 4 — effort L — risk low — category: resume testing
  Why: resume needed a fix twice, so the failures are in the gaps between writes. A kill-point sweep finds the remaining ones before a real crash does.
  Done when: a harness injects SIGKILL after the Nth write for every N on a scratch goal, then resumes. Every run ends in the same done verdict and clause set as the control, and any divergence names the write index.

- **Hold done as provisional and re-run its proofs from cold in a fresh worktree** — SECURITY — value 5 — effort M — risk med — category: true done
  Why: 6 false dones are unchanged since gen 2. Evidence recorded in a dirty or cached session passes without being reproducible after a crash or compaction.
  Done when: `done` first marks the goal "provisional". A fresh checkout of the final commit re-runs every clause's proof, and only then does it become "done". A planted stale-pass clause fails the replay.

- **Bind each clause's evidence to a tree hash and the files its command read** — FIX — value 4 — effort M — risk low — category: true done
  Why: evidence recorded before a later edit, or before a compaction summary claimed success, still counts as proof.
  Done when: editing a file that a clause's command read marks that clause "decayed" and blocks done until it is re-run. Editing an unrelated file leaves it proven.

- **Strip unproven "completed" claims from handoff notes and compaction summaries** — FIX — value 4 — effort S — risk low — category: compaction
  Why: after a compaction the summary says "done" for items that were only attempted, and the next context treats that as fact.
  Done when: the resume card lists each item as observed (backed by a ledger record) or asserted (not backed). An asserted "tests pass" line with no evidence record is shown as unproven in the first post-compaction context.

- **Reconcile on resume by diffing git and ledgers against the last capsule** — FEATURE — value 4 — effort M — risk med — category: resume
  Why: a crash can leave a commit with no ledger record, or a ledger record for work that never landed. Resume currently trusts one side.
  Done when: resume prints a three-line diff of the capsule, HEAD and the ledger and skips plan steps whose change already landed. A planted half-landed step is detected and not redone.

- **(wild) Run a nightly amnesia drill on a scratch goal and open a self-edit task when it fails** — FEATURE — value 4 — effort M — risk low — category: drills
  Why: assumption: regressions in resume appear only after hook or skill edits, so a nightly guard against silent loss is cheaper than the next manual discovery.
  Done when: each night a scratch goal is killed, compacted and resumed, and its quiz and verdict are logged. A failed drill files a task naming the commit range since the last pass.

- **(wild) Have the agent write a "where I stood" line before every risky call and have the resumer read it first** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: assumption: intent is the one thing ledgers and git cannot reconstruct. A one-line will per risky step is cheap, and it covers the gap between a decision and its first write.
  Done when: a PreToolUse hook on a risky class appends the line to a journal. After a kill, the resume card shows the last line and whether its result record exists.

- **(wild) Hand a half-finished goal to a stranger model, with only the capsule and ledgers, as the handoff test** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: if a different model can finish the goal from the capsule alone, the capsule is complete. If it cannot, the gap is named.
  Done when: a scratch goal is cut at a random turn, a different-model child resumes it from the capsule only, and its first five actions are scored against a control run's. The missing facts are listed.

- **(wild) Plant a dead-man hold: before done is accepted, a cold child must list unmet clauses and cite none** — SECURITY — value 4 — effort S — risk med — category: true done
  Why: false dones persist because the agent grades itself, and a cold read with a different model is a signal Foreman does not author.
  Done when: a close with a planted unmet clause is blocked by the child's named clause. A clean close passes with an empty list and the child's verdict recorded.

Next question: Which of the six false dones would a capsule plus a cold re-run have caught, and which need a signal that exists only outside the session?
Next question: At which exact point in a compaction does the agent lose the open-clause list, and can a PreCompact hook run in time to preserve it?
