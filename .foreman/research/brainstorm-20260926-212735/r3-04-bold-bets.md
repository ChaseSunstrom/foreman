# Brainstorm — lens: bold bets

- **Squeeze noisy command output at the source** — PERFORMANCE — value 5 — effort M — risk med
  Why: assumption: test, build and lint logs are the largest single source of tool-result tokens. Foreman already recognises test and verify commands.
  Done when: a PreToolUse hook rewrites a recognised Bash test command to pipe through `fm squeeze` (pipefail, exit code preserved). Claude sees only failures plus a short tail and a full-log path, and a failing pytest run shows ≥80% fewer output tokens with an identical exit code.

- **Deny re-reads of unchanged files** — PERFORMANCE — value 4 — effort S — risk med
  Why: the pack's "outline-first guard" shapes first reads but does nothing about repeated ones. Assumption: repeated full reads within a session are common.
  Done when: PostToolUse keeps a per-session (path, mtime, hash, turn) ledger. A repeat full Read of an unchanged file gets denied with "unchanged since turn N; use offset/grep". PreCompact clears the ledger. A test shows the second read denied, and the read allowed again after an edit or a compaction.

- **Turn lessons into path-scoped tripwires** — FEATURE — value 4 — effort M — risk low
  Why: the pack says recurring failures are matched only after they happen, and lessons are recalled only via BM25 at focus.
  Done when: `fm task done` compiles each lesson into an optional trigger (scope glob + optional regex). PreToolUse emits a ≤200-char warning the first time a matching edit happens in a session. A test shows the warning firing once, and not for unrelated paths.

- **Add a stdlib symbol index with `fm where SYMBOL`** — FEATURE — value 4 — effort M — risk low
  Why: `fm map` and `fm impact` work at file level. Assumption: exploration is a many-grep, many-read loop.
  Done when: `fm where NAME` prints definitions and callers (`ast` for Python, regex for other languages) in ≤10 lines, refreshed incrementally by file hash. On the plugin's own repo it answers 10 sampled symbol lookups correctly in <100 ms.

- **A/B-test Foreman's own rules on real work** — FEATURE — value 4 — effort L — risk med
  Why: the pack has the improve skill (evals in a worktree) and `fm cost`, but nothing measures a rule or injection change on live tasks.
  Done when: a variant of a rule or injection is assigned to alternate tasks and recorded. After N tasks of each, `fm improve compare` reports median tokens, turns and gate failures per arm and proposes promotion behind one yes/no. A fixture run with fake cost logs picks the cheaper arm.

- **Park approvals without blocking `fm run`** — FEATURE — value 4 — effort M — risk low
  Why: the user only answers yes/no, and headless runs presumably stall or skip at consent points. Assumption: this is where autonomy breaks.
  Done when: `fm ask` writes a pending question with a safe default. `fm run` continues with independent tasks, and dependents are marked blocked. The next SessionStart shows one line, and "yes" resumes the parked task. It optionally calls `notify-send` if present. A test shows a run finishing three tasks while a fourth waits.

- **Compile acceptance criteria into failing checks before coding** — FEATURE — value 3 — effort M — risk med
  Why: criteria are prose plus a verify command, and red→green proof exists only for FIX. Assumption: FEATURE tasks often verify vacuously.
  Done when: for FEATURE tasks, `fm plan` requires each criterion's verify command to fail on the untouched tree (stored as baseline evidence). `fm task done` then requires it to pass. A criterion that already passes is flagged as vacuous at plan time.
