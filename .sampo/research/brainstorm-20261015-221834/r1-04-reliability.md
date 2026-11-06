# Brainstorm — lens: reliability

- **Write a resume manifest at every worktree-agent step** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: the user asked "worktree agents resume easily after a session stops"; T-1028 is only planned. Assumption: today a stopped builder leaves a branch but no record of its step, brief or last green check.
  Done when: killing a builder mid-task and running `fm resume` prints its worktree, branch, task id, brief and next step, and restarts it from there.

- **Journal tool intents before they run** — FEATURE — value 4 — effort M — risk med — category: crash recovery
  Why: assumption: a kill between an edit and its ledger write leaves state that disagrees with the tree. T-0798 (transcript repair, blackstart) is deferred, so no recovery path exists.
  Done when: a SIGKILL test mid-close leaves a journal entry, and the next start either completes or rolls back the step and says which.

- **Reconcile ledger against git on every SessionStart** — FIX — value 4 — effort S — risk low — category: state integrity
  Why: the user's stopped-session scenario, plus repeated stale-state bugs (swept snapshots with no by-pid record, T-1003). Assumption: tasks can say "in progress" while their branch is merged or gone.
  Done when: a fixture with a merged branch and an open task shows the task auto-flagged and one line naming the mismatch.

- **Heartbeat lanes and flag the silent ones** — FEATURE — value 4 — effort M — risk low — category: fleet liveness
  Why: the Agents graph shows lanes but nothing tells a hung child from a slow one. Assumption: lanes have no liveness signal beyond the process existing.
  Done when: a child stopped with SIGSTOP shows as "stalled 90s" in `fm ui` and `fm agents`, with resume or kill offered.

- **Make every fix hint carry a self-test** — FEATURE — value 4 — effort M — risk med — category: learned fixes
  Why: T-1032 ships git-carried hints learned from failure then success. Hints that travel to other clones can go stale, so they need to prove they still apply. Assumption: hints store only the fix text.
  Done when: each hint records a check command, and `fm doctor` marks a hint failing its check as stale and stops offering it.

- **Quarantine a task that fails the same way three times** — FEATURE — value 3 — effort S — risk low — category: loop safety
  Why: the "super recursive brainstorm, repeat until dry" request needs a stop for loops that never converge. T-0798 lists crash-loop quarantine as a later item.
  Done when: a seeded failing task is parked after three identical failures with the signature shown, and the queue moves on.

- **Test claude-binary lockout as a hard fixture** — FIX — value 4 — effort S — risk low — category: test isolation
  Why: T-0990's `~/.local/bin` fallback let tests reach the paid binary, and the user reported it. Assumption: other lookups (HOME, XDG) can bypass the lockout the same way.
  Done when: a test harness sets one sentinel that makes every claude lookup fail, and a canary test proves a spawn attempt errors.

- **Fence harness sessions from the Stop hook** — FIX — value 4 — effort S — risk low — category: isolation
  Why: shot.py's session was driven into the queue by the Stop hook and took focus from the working session (user report).
  Done when: sessions started with a harness env marker never read or write the real queue, shown by a test with a seeded queue left untouched.

- **Wild: Replay a crashed session from its ledger into a fresh worktree** — FEATURE — value 4 — effort L — risk high — category: time travel
  Why: wild; assumption: the ledger plus tool log hold enough to rebuild the plan, applied edits and proofs of a dead session.
  Done when: `fm replay <session>` recreates the worktree state at the last proven step and a diff against the original tree is empty.

- **Wild: Run a chaos mode that randomly kills hooks, children and writes** — FEATURE — value 3 — effort M — risk med — category: fault injection
  Why: wild; the roundtrip gate only covers the happy path. Assumption: no existing test kills a process mid-write.
  Done when: `fm chaos --runs 20` finishes with state passing `fm doctor` after each run, and prints any run that corrupted state.

- **Wild: Keep a hot-spare checkpoint ref per builder** — FEATURE — value 3 — effort M — risk low — category: resume
  Why: wild; a hidden git ref (`refs/foreman/ckpt/T-xxxx`) updated after each green step would let any clone fetch and resume a builder, which fits the user's wish for fixes and work to travel with git.
  Done when: after a green step the ref exists, and a fresh clone can run `fm resume T-xxxx` from the fetched ref alone.

- **Detect and repair the Bash env prelude growing on each compact** — FIX — value 3 — effort S — risk low — category: idempotence
  Why: SessionStart appends exports to the env file each start or compact, seen 8 times in the user's report.
  Done when: running SessionStart ten times leaves the env file byte-identical after the first run.

- **Write state files atomically with a version stamp** — FIX — value 3 — effort M — risk med — category: state integrity
  Why: a malformed ledger line already broke `gather()` (dropped item). Assumption: other state files use plain writes that a kill can truncate.
  Done when: a kill-during-write test leaves every state file either old or new, never partial, and a corrupt file is moved aside with one warning.
