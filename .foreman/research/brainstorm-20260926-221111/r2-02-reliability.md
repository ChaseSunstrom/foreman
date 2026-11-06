# Brainstorm — lens: reliability

- **Make `fm check` prove its verify commands are pure** — FIX — value 4 — effort M — risk low
  Why: cached passes and evidence are keyed to an identical tree hash, but nothing shows a command leaves that tree unchanged. Commands that write files or leave servers running poison the cache.
  Done when: `fm check` hashes the tree and lists child processes and listening ports before and after each command. A test command that touches a file or leaves a process behind gets a named "impure" warning and is excluded from cached passes.

- **Order scope and evidence by sequence number, not mtime** — FIX — value 4 — effort S — risk low
  Why: the scope-drift check compares a "scope:" reason with an edit being "newer". File times break under git checkout, clock skew, coarse filesystems and copied state. Assumption: the check uses mtimes or timestamps.
  Done when: state entries carry a monotonic counter. A test that sets a file's mtime in the past or future still gets the correct drift verdict.

- **Pause on usage limits instead of failing** — FIX — value 5 — effort M — risk low
  Why: the user has burned 20% of their weekly usage, and `fm run` and `fm ideas` shell out to `claude -p`. Assumption: a limit or 429 currently looks like an ordinary child failure and gets retried or dropped.
  Done when: a stub `claude` that prints a limit message makes `fm run` stop cleanly. It parks the task, records the reset time, does not count it as a failure, and resumes after the reset. `fm ideas` reports the lens as "limited", not "empty".

- **Smoke-test the plugin whenever its version changes** — FEATURE — value 4 — effort M — risk low
  Why: the last-known-good snapshot and rollback exist, but nothing decides when to trigger them beyond doctor. A bad update fails on the user's next real task.
  Done when: the first `fm` call after a version stamp change runs a synthetic capture→done task in a temp state dir in under 2 s. Failure restores the snapshot and prints one line. The result is cached per version.

- **Rebind the task when the branch or HEAD changes mid-task** — FIX — value 4 — effort M — risk med
  Why: tree hashes, checkpoints, `--affected` and the scope preflight all assume one lineage. A checkout, rebase or stash pop silently invalidates them. Assumption: only outside edits are detected today, not HEAD moves.
  Done when: focus records the branch and HEAD. A per-turn note fires once after a HEAD change and names what it invalidated (cached passes, checkpoint base). `fm task done` refuses stale evidence after a rebase until it is re-run.

- **Inject IO faults into state writes** — CLEAN — value 4 — effort M — risk low
  Why: writes are crash-safe against kills, but there is no test for ENOSPC, read-only home, EACCES, non-UTF-8 paths, or a clock jump. A hook that dies here fails open silently.
  Done when: a table-driven test monkeypatches these faults across every `fm` write path. Each fault yields either a clear one-line error or a read-only degraded mode, never a traceback or a half-written brief. The suite also passes under `LANG=C` and on the oldest supported Python.

- **Check that checkpoints stand alone before compaction** — FEATURE — value 3 — effort S — risk low
  Why: PreCompact writes a checkpoint, but nothing verifies that a fresh session could rebuild "Next" from it. Anything that lives only in the conversation is lost.
  Done when: the PreCompact hook rebuilds the Next action from state alone and compares it to the live one. On a mismatch it appends the missing fact (a decision, a ruled-out approach) to the checkpoint and logs the gap. A test drops a fact and sees it added.
