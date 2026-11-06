# Brainstorm — lens: reliability

- **Make state writes crash-safe and race-safe** — FIX — value 5 — effort M — risk med
  Why: assumption: hooks, `fm run`, `fm serve` and `fm watch` can write the same brief and queue concurrently, and only `fm` writes state, so one atomic-write path covers everything. Use temp file + fsync + rename, a per-project lock, and a tiny write-ahead journal that `fm doctor` replays or repairs.
  Done when: a test that kills the writer mid-write still leaves a parseable brief, and two concurrent `fm` writers lose no log or evidence entries.

- **Bind evidence and cached passes to a tree hash** — FIX — value 5 — effort M — risk low
  Why: the pack has auto-recorded evidence and "cached pass on an identical tree". Stale evidence would let `fm task done` pass on code that has since changed. The cache key should include the gate command, tool versions, untracked files and lockfiles. Done should reject evidence older than the last edit to a scope file.
  Done when: editing an untracked in-scope file after recording evidence makes `fm task done` refuse and `fm check` miss the cache.

- **Flag vacuous verify commands at done** — FEATURE — value 4 — effort M — risk med
  Why: gaps named in the pack are that gates are exit codes and that red→green proof exists only for FIX. Run each new criterion's verify command against the base tree in the temp worktree that already exists for FIX proof. A command that passes there, or that collects zero tests, is flagged as vacuous.
  Done when: a criterion of `true`, or of pytest collecting 0 tests, is flagged, and a genuine failing-before check is not.

- **Detect thrash in PostToolUse and emit one note** — FEATURE — value 4 — effort M — risk low
  Why: the pack says "nothing notices thrash" (same file edited 5×, same test failing with different errors). Keep counters in per-task state and inject one note of at most 400 chars, once per pattern, suggesting a stop-and-hypothesize step. This adds no prompts otherwise.
  Done when: a fixture of 5 edits to one file yields exactly one note, and a normal edit sequence yields none.

- **Carry a "ruled out" digest across handoffs** — FEATURE — value 4 — effort S — risk low
  Why: the pack says `fm run` and resumed sessions get only the brief and resume note. Auto-collect failed commands and reverted approaches, add an `fm note --ruled-out` option, and include the digest, capped at 300 chars, in the resume note and the `fm run` prompt.
  Done when: a resumed fixture session shows the previous dead ends, and the digest stays under its cap.

- **Harden `fm run` against crashes and stalls** — FIX — value 4 — effort M — risk med
  Why: assumption: headless `claude -p` sessions can hang or die mid-task. Add per-task wall-clock and token budgets, a stall watchdog, and idempotent resume that reads the journal instead of restarting the task.
  Done when: killing a run mid-task and rerunning it resumes the same task with no duplicated log entries, and a hung session is stopped at the budget.

- **Self-monitor hooks with fail-open and a latency log** — FIX — value 3 — effort S — risk low
  Why: the constraints are p50 of about 30 ms and a fail at p95 above 150 ms. Wrap each hook in try/except that fails open, log the exception and duration to a bounded file, and have `fm doctor` report the p95 and the error count. A broken hook must never block the user's session.
  Done when: an injected exception in a hook leaves the tool call allowed and appears in `fm doctor`, and a timing test asserts p95 under 150 ms.
