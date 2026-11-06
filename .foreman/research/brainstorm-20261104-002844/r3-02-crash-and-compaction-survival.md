# Brainstorm — lens: crash and compaction survival

- **Write the resume card from the ledger, not from the model** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: resume is the worst area (2 of 6 needed a later fix); T-2900 closes dead background work only after the fact. Assumption: a PreCompact/SessionStart card built mechanically (open clauses, last evidence, held leases, last 5 tool outcomes) is more reliable than a model-written summary.
  Done when: after a forced compaction in a scratch goal, the first SessionStart line lists every open clause and the lease owner, and a test diffs it against the ledger with zero omissions.

- **Resolve state from the main repo inside any worktree** — FIX — value 5 — effort M — risk med — category: worktree
  Why: the request says evidence and lease commands fail inside the builder worktree the harness put the agent in. Assumption: they resolve `.sampo` from cwd rather than from `git rev-parse --git-common-dir`.
  Done when: `sampo evidence add` and `sampo lease take` succeed from a harness-made worktree, and a matrix test runs every goal-path verb from main, a linked worktree and a subdirectory with the same result.

- **Spool evidence to a worktree-local outbox, merge on landing** — FIX — value 4 — effort M — risk med — category: worktree
  Why: when the shared store is unreachable (sandbox, read-only mount), evidence is lost and the done gate sees none. Assumption: some failures are permissions, not path resolution.
  Done when: with the main state dir made read-only, a verb writes to the outbox, prints "spooled", and `sampo task finish` counts the spooled evidence after a merge step.

- **Kill the builder at every ledger write and compare verdicts** — PERFORMANCE — value 5 — effort L — risk low — category: crash testing
  Why: gen 4's long tier has 0/6 true done and planted faults are the measured weakness; torn tails and double-spent grants are untested. Assumption: ledger appends are not all atomic.
  Done when: a sweep that SIGKILLs a scratch goal at each append point yields, after resume, the same done verdict as an uninterrupted run in at least 95% of points, and each failure lists its write site.

- **Make the leases fenced and self-describing for takeover** — FIX — value 4 — effort M — risk med — category: leases
  Why: a crashed session leaves a lease the next one cannot safely claim. Assumption: leases store only an owner id.
  Done when: a lease records pid, host, boot id, session id and a fencing counter. A resumed session takes over one whose pid is dead, and a stale holder's later write is rejected, both proven in tests.

- **Re-inject a 40-line goal anchor at PreCompact and SessionStart** — FEATURE — value 5 — effort S — risk low — category: compaction
  Why: false dones persist since gen 2, which suggests the agent forgets the goal's original words and unmet clauses after compaction. Assumption: the summary currently drops them.
  Done when: after a compaction the transcript contains the verbatim goal text and the open-clause list, and the amnesia drill (below) agent restates all clauses.

- **Run a nightly amnesia drill on a scratch goal** — SECURITY — value 4 — effort M — risk low — category: drills — wild
  Why: assumption: compaction loss is only found when a real goal fails. A scratch goal is compacted, then the agent is asked what remains.
  Done when: `sampo drill amnesia` reports clauses recalled versus open, fails below 100%, and writes a line to the ledger.

- **Hold done as provisional, then re-run the proofs cold** — FEATURE — value 5 — effort M — risk low — category: true done
  Why: 6 false dones unchanged since gen 2. Assumption: many were proofs that passed in the builder's warm state.
  Done when: a closed goal is marked provisional, and a timer or the next session start re-runs every recorded proof in a fresh worktree. A planted warm-state-only proof flips it to reopened in a test.

- **Turn each false done into a replayable regression scenario** — CLEAN — value 4 — effort M — risk low — category: true done
  Why: the six false dones are known but not a permanent zero-token corpus. Assumption: their transcripts and ledgers exist.
  Done when: six scenarios run in the free arm and fail on the current gate, then pass after the fixes, with their ids cited in the gate code.

- **Reconcile on resume by diffing git and ledgers against the last checkpoint** — FEATURE — value 4 — effort M — risk med — category: resume
  Why: a dead session may have committed, half-edited or moved a worktree without recording it. Assumption: the checkpoint is written only at Stop.
  Done when: resume prints a three-way diff (checkpoint, git, ledger) and skips steps whose change already landed. A test with a commit made after the last checkpoint is not redone.

- **Write a "where I stood" line before every risky call** — FEATURE — value 3 — effort S — risk low — category: handoff — wild
  Why: assumption: the intent of a killed step is the information most often lost. A one-line will is appended before pushes, deletes and long commands.
  Done when: after a kill mid-step, resume shows the last will line and whether its result record exists.

- **Make a stranger finish the goal from the handoff alone** — FEATURE — value 4 — effort L — risk low — category: resume — wild
  Why: assumption: a different model with no history proves the handoff is sufficient, and doubles as a model-swap continuity test.
  Done when: a cold child given only the resume card and the repo completes a scripted three-step goal, and the check fails when the card is truncated.

- **Dead-man done: a cold different-model child lists unmet clauses before closing** — FEATURE — value 4 — effort M — risk med — category: true done — wild
  Why: self-judged done is the repeated failure. Assumption: a child reading only the goal text and the evidence will catch clauses the builder skipped.
  Done when: closing is refused when the child cites an unmet clause with a quoted goal line, and a planted-skip scenario is caught.

Next question: which of the six false dones were caused by lost context after compaction versus by a weak proof, since the fixes differ?
Next question: what does the host's own resume and compaction already preserve, so Sampo's card adds only the difference?
