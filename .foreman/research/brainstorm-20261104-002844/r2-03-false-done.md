# Brainstorm — lens: false done

- **Make "done" require one real-path firing** — FEATURE — value 5 — effort M — risk low — category: false done
  Why: the standing rule says every capability must be called by a real session path, and the long tier has 6 false dones that ran no such path. A goal that adds a verb, hook or skill often ends "done" with only a unit test.
  Done when: closing a goal that adds a capability fails until the ledger holds one record of that capability firing through a hook, skill, `fm next` or the drive. A planted test with no such record is refused.

- **Spool evidence to a lane-local outbox** — FIX — value 5 — effort M — risk med — category: worktree and resume
  Why: the request says evidence and lease commands fail inside the builder worktree. The assumption is that a failed evidence write ends as a skipped record and a done claim anyway. Resolving the path helps, but an outbox also survives a crash.
  Done when: in a builder worktree with the main state dir unreachable, `fm evidence` appends to a file in the worktree. The land step merges it into the ledger, and the done gate counts it. A kill mid-write loses no record.

- **Harvest false dones from the user's follow-up words** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the 6 false dones have not moved since gen 2, and the standing rule prefers signals Foreman did not author. The user's own "still", "you didn't" and "not working" after a close are such a signal.
  Done when: a zero-token matcher over the next user message after a close files a `false-done` label with the task id. Run over the last 60 closes, it reproduces the known 6 or names the ones it missed.

- **Detect proof that touched something else** — FEATURE — value 4 — effort M — risk med — category: false done
  Why: assumption: some false dones pass a real command that never touched the clause's files or symbols. A clause about parser X is "proven" by an unrelated green suite.
  Done when: each clause-to-evidence link records the paths and symbols the command exercised, from the diff plus coverage or a trace. A link with zero overlap with the clause's nouns becomes `unmeasured`. A planted unrelated pass is caught.

- **Floor the test count on every pass** — FIX — value 4 — effort S — risk low — category: vacuous pass
  Why: assumption: a green run with 0 tests collected, or fewer than the parent commit, is a classic false pass. The vacuous-pass sentence idea covers wording only, not a count.
  Done when: evidence records the tests-run count parsed from the runner output. A count of 0, or a drop against the parent without a stated reason, gives `unmeasured`. A planted deselected suite fails the gate.

- **Turn mid-run user messages into clauses** — FEATURE — value 5 — effort M — risk med — category: resume and intake
  Why: the user steers while a goal runs ("also…", "and not X"). After a compaction the builder keeps the sealed plan and misses the amendment, so it declares done against a stale goal.
  Done when: a user message arriving during an open goal is classified. An addition or change appends an `amended` clause to the goal capsule with the quote and time, and the capsule is re-injected at the next PreCompact and SessionStart. Done is refused while the clause is unproven.

- **Hold done on hedge words in the final message** — FEATURE — value 3 — effort S — risk med — category: false done
  Why: assumption: finish text such as "should work", "not tested" or "I couldn't run" often precedes a false done. A zero-token scan is cheap, and the idea of mining caveats earlier was only for predicting asks.
  Done when: the Stop gate scans the final message for a short hedge list. A hit holds the close and quotes the phrase, and the agent clears it with evidence or by naming it as left out. False holds are counted in `fm doctor`.

- **Keep clause tombstones for any dropped or weakened clause** — FEATURE — value 4 — effort M — risk low — category: scope shrink
  Why: a vague goal becomes a plan, and the plan can silently lose a hard clause. Sealing and diffing the plan is only partly covered.
  Done when: removing or rewording a sealed clause writes a tombstone with old text, new text and a reason. The done card lists every tombstone, and a close with an unexplained one is refused.

- **Require a failing parent receipt for a close with no code change** — FIX — value 4 — effort S — risk low — category: false done
  Why: assumption: "already satisfied, nothing to do" and tiny diffs are a false-done route. Outcome-differs-on-parent exists for briefs, not goal closes.
  Done when: a goal close whose diff misses the clause's files must cite a predicate that passes on HEAD and fails on a named earlier commit. If it passes on both, the close is held as vacuous.

- **Build denominators for "all" and "every" with grep** — FEATURE — value 4 — effort M — risk low — category: false done
  Why: goals like "update all callers" end done after the first few. This is a zero-token sibling sweep wired into the done gate, not only into briefs.
  Done when: intake finds quantifier clauses and builds the member list by grep. Done requires each member to be changed or marked n/a, and a planted missed caller blocks it.

- **Turn the saboteur's winning cheat into a new clause check** (wild) — FEATURE — value 4 — effort L — risk med — category: adversarial
  Why: a ghost builder trying to pass done without the work was proposed, but its output was not fed back. Each win then closes a hole for good.
  Done when: a nightly cold child tries to satisfy a scratch goal's checks without doing the work. Each success files a task and a regression scenario that fails on that cheat, and the cheat count falls over weeks.

- **Require a recorded demo of the feature in use** (wild) — FEATURE — value 3 — effort M — risk med — category: evidence
  Why: assumption: a transcript of a fresh process using the new thing is stronger than a test the builder wrote. A cold child can also read it later.
  Done when: closing a user-facing goal stores a terminal capture of a fresh process using the feature, linked from the done card. A child given only that capture and the goal answers whether the goal was met, and a mismatch holds the close.

- **Build a memorial wall of false-done mechanisms** (wild) — FEATURE — value 3 — effort M — risk low — category: delight, false done
  Why: the 6 false dones are unchanged since gen 2 because they are not named. A card per mechanism (proxy proof, stale resume, scope shrink, vacuous pass) with its replay test makes recurrence visible.
  Done when: the site and pane show one card per mechanism, with a planted replay and a count of recurrences in the last 30 days. Any recurrence turns its card red.

Next question: which of the 6 known false dones were caused by an agent that could not write evidence (tooling) versus one that chose not to (judgement), and does the fix differ?
Next question: after a resume, which claims in the first message are re-derived from state and which are just remembered, and where is the difference recorded?
