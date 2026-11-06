# Brainstorm — lens: reliability

Answering one earlier question first: the settled-bet and digest jobs need to run on time. Everything else can be eventual, so catch-up should run those two first.

- **Pin each closed goal row to its proving tests by id** — FIX — value 5 — effort M — risk low — category: done-detection
  Why: assumption: a row stays closed after its test is deleted or renamed. "Flag goals that finish by shrinking" catches size, not a disappearing proof.
  Done when: deleting a pinned test in a scratch copy reopens its row on the next goal read, and the read names the missing test.

- **Write an intent marker before every outward row step** — FEATURE — value 5 — effort M — risk low — category: crash safety
  Why: assumption: a crash between a push or publish and the ledger write can repeat or skip the effect on resume. The trigger layer has fire-intent rows, but goal rows don't.
  Done when: a kill between the effect and the close leaves a marker, and resume checks the remote and does not repeat the push (test).

- **Round-trip every hand-edited goal file** — FIX — value 4 — effort M — risk low — category: file robustness
  Why: the user can edit the goal as plain markdown (earlier idea), and a lossy parse could silently rewrite their edit.
  Done when: a 500-case fuzz of edits either gives parse→render→parse identity, or the write refuses with a line number and leaves the file unchanged.

- **Refuse a retry that repeats a failed approach** — FEATURE — value 4 — effort M — risk low — category: row retries
  Why: the standing Genesis rule says a failed spike gets 2 or more different approaches, then goes to not-yet with its blocker. Nothing enforces this at the row level.
  Done when: a second attempt with the same approach fingerprint is refused. After two distinct failures the row moves to not-yet with its blocker and a re-entry condition.

- **Quarantine probes that flip verdicts** — FIX — value 4 — effort M — risk low — category: verification
  Why: assumption: a finish oracle or row probe that passes once and fails once can close a row or reopen a goal at random.
  Done when: a probe that disagrees across 3 runs is marked flaky, can't close a row, and the finish read names it.

- **Degrade to read-only on a full or read-only disk** — FIX — value 4 — effort S — risk low — category: storage failure
  Why: this sandbox's path sits on /run/user (tmpfs), and "warn when goal state sits on volatile storage" only warns. Nothing covers ENOSPC or a read-only mount.
  Done when: with a zero-quota fixture, goal verbs print a banner and exit non-zero with no traceback, and a bookmark from a pre-reserved file is still readable.

- **Give plan rows ids from their meaning, not their position** — FIX — value 4 — effort M — risk med — category: replanning
  Why: assumption: replans that reorder or reword rows detach evidence and vetoes from the rows they belong to.
  Done when: a replan that reorders and rewords 3 fixture rows keeps all evidence attached, and the diff lists only the truly added or removed rows.

- **Attribute every dirty hunk at resume to a row or flag it orphaned** — FEATURE — value 4 — effort M — risk med — category: crash recovery
  Why: a crash mid-edit leaves uncommitted work that the ledger doesn't explain. "Reconcile baton, ledger and repo" is at the file level, not the hunk level.
  Done when: an unlogged edit planted in a fixture appears as one "unowned hunk" line on resume, and clears once it is attributed.

- **Prove every mutating goal verb is idempotent** — CLEAN — value 4 — effort M — risk low — category: idempotency
  Why: assumption: a double-run verb, or one interrupted at each write and re-run, leaves different state. The tick has a "double tick is a no-op" idea, but goal verbs don't.
  Done when: a harness runs each mutating verb twice and interrupted at every write, compares final state, and fails if a new verb has no entry.

- **Record the inputs behind every next-row pick** — FEATURE — value 3 — effort S — risk low — category: explainability
  Why: assumption: a surprising pick after a crash can't be audited. Earlier asks (why did or didn't a trigger fire) show the user wants this for triggers, and goals have no equivalent.
  Done when: `fm goal why-next` prints the stored inputs, and re-running the pick on them yields the same row.

- **Mutate the plan to test the completeness check (wild)** — FEATURE — value 4 — effort M — risk low — category: plan quality
  Why: wild. "Mutate the finish oracle" tests done-detection, but nothing tests whether a missing row is noticed.
  Done when: dropping a random must-row from each of 3 fixture plans, 20 times, prints a catch rate that is ratcheted.

- **Triple-store the bookmark and resume by majority (wild)** — FEATURE — value 3 — effort M — risk med — category: state redundancy
  Why: wild. Keep the bookmark in the goal file, a git ref, and a transcript line, so one corrupt or compacted copy can't mislead a resume.
  Done when: corrupting any one copy is detected and repaired, and the resume line says which copy lost.

- **Expire a closed row's proof when its covered files change (wild)** — PERFORMANCE — value 3 — effort M — risk med — category: proof freshness
  Why: wild. Stamp each proof with the tree hash of the files it covers. On resume after days away, re-run only the proofs gone stale instead of all or none.
  Done when: touching one covered file re-runs exactly that row's proof on resume and skips the others, and the resume read lists both counts.

Next question: Which closed goal rows in the real history would have turned out false, or had to be redone, if their proofs had been re-run a week later?
Next question: What does a goal verb do when its state file was written by a newer Foreman than the one reading it?
