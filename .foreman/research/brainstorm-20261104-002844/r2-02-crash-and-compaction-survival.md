# Brainstorm — lens: crash and compaction survival

- **Run a resume-point audit that kills the builder at every ledger write** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: resume is the worst area (2 of 6 needed a later fix); T-2900 and T-2901 were found only after real use. Related ideas exist (kill-point sweep on writers), but none ties the sweep to the goal path: kill, resume, compare the final verdict to an uninterrupted run.
  Done when: a test kills a scratch goal run at each of N recorded write points, resumes it, and asserts that the same clauses end up proven as in the uninterrupted run, with zero duplicated or lost ledger rows.

- **Make evidence and lease commands resolve state from the main repo inside any worktree** — FIX — value 5 — effort M — risk med — category: worktree
  Why: the request names this directly: evidence and lease commands fail inside the builder worktree the harness put the agent in. Assumption: the cause is state dir derivation from the cwd toplevel rather than the git common dir.
  Done when: from a fresh `git worktree add` directory, `fm evidence add`, `fm lease take` and `fm lease release` succeed and write to the same ledger the main checkout reads.

- **Write the goal charter as one file the model can't compact away** — FEATURE — value 5 — effort S — risk low — category: compaction
  Why: a vague goal must survive days and compactions. The pack shows compaction handling through hooks but no durable restatement of the user's words plus the clause list.
  Done when: after a forced compaction in a scratch session, the first turn contains the verbatim goal and every open clause (from SessionStart/PreCompact injection, ≤40 lines), verified by a transcript check.

- **Bind each done-clause to evidence by tree hash and re-check at close** — FEATURE — value 5 — effort M — risk med — category: true done
  Why: tier 0/6 true done, 6 false dones unchanged since gen 2. Assumption: false dones stem from evidence that was valid at its commit but stale or never run against the final tree.
  Done when: `fm goal done` refuses when any clause's evidence tree hash differs from HEAD's relevant paths, naming the clause, and the 6 known false-done scenarios each get refused.

- **Turn the six false dones into a permanent regression corpus run by the zero-token arm** — FEATURE — value 4 — effort M — risk low — category: true done
  Why: false dones have not moved in two generations, which suggests nothing measures them cheaply between end-of-run exams. Standing rules allow only free arms per generation.
  Done when: `fm exam` free arm replays 6 recorded false-done transcripts and reports pass/fail per case in under 60 seconds, without a model call.

- **Take over a dead holder's lease only with proof of death** — FIX — value 4 — effort S — risk med — category: leases
  Why: a crash leaves a lease and the resumed session either blocks or steals it blindly. Related T-2900 closed dead background work, so the same pid/session-start evidence is available.
  Done when: a lease whose owning pid and session id are gone is reclaimed automatically with a ledger note, and one whose owner is alive is refused, tested both ways.

- **Journal intent before result for each plan step and resume from the journal** — FEATURE — value 4 — effort M — risk med — category: resume
  Why: a crash between "started editing" and "recorded result" leaves ambiguous state. Assumption: plan steps are currently recorded only at completion.
  Done when: killing between intent and result yields on resume a "step X was in flight" card, and the step is re-verified rather than assumed done or skipped.

- **Hold done as provisional for a time window and re-run the proofs** — FEATURE — value 4 — effort S — risk low — category: true done
  Why: multi-day goals are where false dones hide; a decayed re-check catches regressions from later steps. Matches the known "decayed" idea but ties it to goal close specifically.
  Done when: a closed goal shows "provisional" until the re-run passes at +24h (settable), and a seeded regression flips it back to open with the failing clause named.

- **Make a cold, different-model child list unmet clauses before any done is accepted** — FEATURE — value 4 — effort M — risk med — category: true done
  Why: standing rules favour signals Foreman didn't author; false dones are self-graded today. The child sees only the goal words and final evidence.
  Done when: for the 6 false-done cases the child names at least the missed clause in 5 of 6, and for a truly done scratch goal it lists none.

- **Reconcile on resume by diffing git and ledgers against the last checkpoint** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: a resumed session today trusts its recorded state; commits, branch switches or hand edits made while away go unnoticed.
  Done when: resume prints a one-screen diff (commits since, dirty files, moved worktrees, open leases) and a test with a hand-made commit shows it.

- **Wild: Run an amnesia drill on the live goal each night** — FEATURE — value 3 — effort M — risk low — category: compaction — wild
  Why: assumption: compaction survival is only proven in tests, never against the user's real goal. A scratch copy of the session is force-compacted and a cold child must say what remains, scored against the ledger.
  Done when: a nightly report lists the clauses the child missed after compaction, and a deliberately deleted charter line is caught.

- **Wild: Write the goal's "I'd know it's done when…" sentence first and test against it at the end** — FEATURE — value 4 — effort S — risk low — category: true done — wild
  Why: a vague goal needs a stated finish line before work; false dones come from the agent inventing the bar late. The sentence is sealed at intake.
  Done when: intake stores a sealed done-sentence with a hash, and `fm goal done` quotes it back with each clause's evidence beside it.

- **Wild: Make a stranger finish the goal from the handoff alone** — FEATURE — value 3 — effort L — risk med — category: resume — wild
  Why: assumption: if a fresh model with only the handoff note and charter can continue correctly, the real resume path is sufficient. Scored against what the original session did.
  Done when: a weekly job hands a fresh child the handoff for a scratch goal at a random midpoint, and it completes the remaining clauses with no questions about prior context.

- **Wild: Fork a probation self for every change to the done-gate** — FEATURE — value 3 — effort L — risk high — category: self-edit
  Why: gate edits are the likeliest way to move the unchanged 0/6; they should be proven on the replay corpus before going live. Assumption: self-edits to the gate exist today.
  Done when: a gate change is applied to a probation copy, run over the six false-done cases and the long-tier replays, and promoted only if it improves one and regresses none.

Next question: which of the six false dones were truly the agent's mistake and which were an unreadable or stale evidence record (a "could not run" read as pass)?
Next question: when the harness puts the agent in a builder worktree, which of the other verbs that touch state (not just evidence and lease) also silently resolve to the wrong directory?
