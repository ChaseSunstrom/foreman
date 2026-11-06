# Brainstorm — lens: bold bets

Round 3 is near saturation. These are the only ideas I'd call genuinely new, and everything else I could think of was a variant of an existing item.

- **Verify Foreman changes with the last-known-good runner** — CLEAN — value 4 — effort M — risk low
  Why: the pack shows Foreman being built by Foreman (474 tests, new gates in `fm task done`). A candidate's own broken gate can approve itself. Snapshot/rollback exists, but nothing says who runs the verdict. Assumption: the plugin is edited in place under a live session.
  Done when: a test that plants a gate which always passes in the candidate copy still gets a failing `fm task done` on that plugin task, because the gates ran from the pinned snapshot.

- **Add `fm refactor` (rename, move, change-signature) built on `ast` and `tokenize`** — FEATURE — value 4 — effort L — risk med
  Why: "suggest a codemod" and "atomic edit transaction" exist, but nothing does the structural edit itself. CLEAN work is many small Edit calls, each one a turn that re-reads context. Assumption: Python-first, with plain text fallback refused.
  Done when: renaming a function used in 12 files (including strings in `__all__`) is one `fm refactor` call, the affected tests pass, and a dry run prints the same diff without writing.

- **Sweep for dangling references to anything the diff removed or renamed** — FEATURE — value 3 — effort S — risk low
  Why: the "companion edit" idea uses git co-change history, and the public-surface diff covers exported symbols. Neither greps docs, CI files, Dockerfiles, config keys, env vars or CLI flags for the old token. Assumption: this is a common cause of "done" tasks that break later.
  Done when: deleting an env var from code while `README` and `ci.yml` still mention it makes `fm task done` list both file:line hits.

- **Find the culprit commit for FIX tasks with `fm bisect`** — FEATURE — value 3 — effort M — risk low
  Why: FIX tasks have red→green proof and a repro, but the pack's bisect ideas cover finished tasks and hunks, not commits. The culprit commit's diff is the smallest useful context for a regression. Assumption: the repro is stable and runs in a temp worktree with a timeout.
  Done when: on a fixture repo with a known bad commit, `fm bisect` names that commit and the brief's Evidence section gets the commit hash and its diff stat.

- **Nudge when independent read-only calls are issued one per turn** — PERFORMANCE — value 3 — effort S — risk low
  Why: the user reports a 20% weekly burn, and every extra turn re-reads the whole context. Existing ideas cover re-reads, thrash and noisy output, but none measure turns. Assumption: PostToolUse sees enough sequence data to spot 3 or more consecutive Read/Grep/Glob calls with no dependency.
  Done when: replaying a recorded trace with 5 serial reads emits exactly one "batch these" note, and `fm cost` reports turns per task.

- **Diff runtime call traces between the start tree and now** — SECURITY — value 3 — effort L — risk med
  Why: characterization snapshots and the public-surface diff only see outputs. A `sys.settrace` run of the suite would show which internal functions changed behavior or were newly reached, catching unintended side effects. Assumption: Python only, gated to CLEAN and L tasks, and it needs a noise filter for timing and randomness.
  Done when: a CLEAN task that accidentally changes an unrelated helper's return values gets flagged as "behavior changed outside scope", and a true no-op refactor produces an empty delta.

- **Attack risky diffs with a scratch-copy test writer** — SECURITY — value 3 — effort M — risk med
  Why: the read-only adversary lens and pre-authored holdouts exist, but no one generates new failing tests against the finished diff. Only run it for security-sensitive or L tasks, since it costs tokens. Assumption: a write-enabled `claude -p` in a throwaway copy is acceptable.
  Done when: on a fixture diff with a seeded off-by-one, the attacker produces a failing test that also fails when replayed on the real tree, and the finding is queued. A clean diff produces no finding.
