# Brainstorm — lens: 2030 worked back

- **Run a cheap pilot of the plan in a scratch clone before committing days** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: tier 0/6 true done and evidence commands that fail inside the worktree show the plan's proof commands were never exercised before the work began. Assumption: a 20-minute local-model pass can find them.
  Done when: for a seeded goal whose proof command cannot run, the pilot flags that clause as "unrunnable" before the first edit, and a goal with runnable proofs gets no flag.

- **Record a replayable world bootstrap** — FEATURE — value 4 — effort M — risk med — category: resume
  Why: resume is the worst area, and evidence silently goes stale when a dev server, database, env var or seed from day 1 died with the session. Assumption: the commands that built that world can be captured from the Bash tool calls.
  Done when: after killing the session and its services, resume rebuilds the services from the recorded list and the clause proofs that need them run green again.

- **Sweep for orphaned done-claims** — FIX — value 5 — effort S — risk low — category: done-gate
  Why: Stop never runs when a session is killed right after "done". Compaction summaries can also carry completed claims that no gate saw. The 6 false dones are unchanged since gen 2. Assumption: some of them came from this path.
  Done when: a planted transcript with "done" and no gate record is listed as ungated at the next SessionStart, and the goal reopens as provisional.

- **Hand over a remainder packet when the goal is done except for user-only steps** — FEATURE — value 5 — effort S — risk low — category: user value
  Why: "knowing when it is actually done" fails when the last clause needs a human (publish, credentials, a physical check). Today that clause is either faked or blocks forever. Assumption: the "split user-held steps" idea applies at goal level and is not built there.
  Done when: a goal with one user-held clause closes as "done except N", printing the exact commands or clicks and each step's expected result, and re-checks that clause when the user says they did it.

- **Snapshot the red tests at goal start** — FIX — value 4 — effort S — risk low — category: done-gate
  Why: "all green" and "no regressions" claims need a baseline, or inherited failures get blamed on the goal or hidden by it. Assumption: not already recorded per goal.
  Done when: the done receipt lists the failures that were already red at intake and the new ones separately, and a planted new failure blocks done while an inherited one does not.

- **Compute an amendment's blast radius when the goal changes on day 3** — FEATURE — value 4 — effort M — risk med — category: multi-day
  Why: multi-day goals get reworded by the user; tombstones and mid-run-message clauses exist, but nothing says which finished clauses and evidence the change invalidates. Assumption: clauses carry file and evidence links.
  Done when: after an amendment, the pane lists clauses as kept, invalidated or new, and only invalidated ones are re-planned.

- **Stamp evidence with an environment fingerprint and tell drift from regression** — FEATURE — value 4 — effort M — risk low — category: evidence
  Why: evidence re-run a day later fails for two different reasons, a changed toolchain, lockfile or service versus a code change. Today both read as "unproven".
  Done when: a re-run that fails with an unchanged tree but a changed fingerprint is labelled "world drifted", naming the field that changed.

- **Re-anchor evidence after a history rewrite** — FIX — value 3 — effort M — risk med — category: resume
  Why: evidence is bound to tree hashes, which dangle after an upstream force-push or rebase over several days. Assumption: hash-bound evidence exists as built or planned.
  Done when: after a rebase of the goal branch, evidence whose patch-id is unchanged is re-bound automatically, and evidence that no longer applies is marked stale.

- **Keep every plan prefix shippable** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: working back from a future where goals run for weeks, the plan must survive a stop at any milestone. Assumption: milestones are not currently required to leave main green.
  Done when: a test kills a seeded goal at each milestone boundary, and the repo passes the ship gate every time.

- **Lint open goals against each other for conflicting clauses and files** — FEATURE — value 3 — effort M — risk low — category: portfolio
  Why: parallel lanes and several open goals are the norm, and the idea list so far only checks briefs against each other. Assumption: goals have clause text and file reach.
  Done when: two goals with a planted contradiction (one clause removes an API, the other uses it) raise a conflict at filing.

- **Wild: Delta-debug the finished diff to its smallest passing form** — FEATURE — value 3 — effort L — risk med — category: done-gate
  Why: wild. The idea list has hunk-attribution and ablation but never asks "what in this diff is unnecessary for done?". Delta debugging against the clause proofs answers that, and "done" would then mean nothing removable.
  Done when: on a seeded diff with one clause-irrelevant hunk, the minimiser names that hunk and the proofs still pass without it.

- **Wild: Rehearse the undo at done** — FEATURE — value 3 — effort M — risk low — category: done-gate
  Why: wild. A multi-day goal that can't be rolled back isn't done. This rehearses the revert in a scratch clone and requires the clause proofs to fail then pass again, instead of trusting a verified-undo verb.
  Done when: a goal whose revert leaves a broken tree stays provisional, and one with a clean revert closes with the rehearsal recorded.

- **Wild: Agree the acceptance demo before any work** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: wild. A vague goal becomes a plan, but the user never approves what "I'd see it working" looks like. Agree a short demo script up front; the final proof is that script replayed, and the user's objection to it is the cheapest false-done filter. Assumption: users answer a 3-line demo faster than a clause list.
  Done when: intake emits a demo script the user can strike lines from, and done fails if any retained line doesn't run and match its stated expectation.

Next question: which of the 6 false dones in the long tier did the done-gate never see because the claim came after a kill or a compaction, not at Stop?
Next question: when the user returns after a gap of days, what do they ask first, and does the resume card answer that before the agent speaks?
