# Brainstorm — lens: reliability

- **Add a write-ahead step journal with fsync'd intent records** — FEATURE — value 5 — effort M — risk med — category: durability
  Why: earlier ideas say "journal every step" but not the intent-before-effect ordering; a crash between a tool's side effect and its log line leaves state and ledger disagreeing (assumption: `fm code` will execute edits itself).
  Done when: a test kills the loop with SIGKILL after the intent record and before the edit lands, and `fm code --resume` replays or skips that step exactly once, with the working tree matching the journal.

- **Make tool calls idempotent with step IDs and effect receipts** — FEATURE — value 4 — effort M — risk low — category: idempotency
  Why: resume and replay across workers (already proposed) double-apply edits or commands unless each call carries a stable ID and a recorded receipt (assumption).
  Done when: re-running a journal containing a completed edit step produces zero file changes and a "skipped: receipt exists" event, tested for edit, bash and commit steps.

- **Run a guard fail-closed canary at every session start** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: the constraint is "the guard must never fail open"; recent commits show constant guard parsing fixes (T-1194, T-1195, T-1204), and non-Claude hosts (opencode TS plugin) can silently lose the hook.
  Done when: at start, `fm code` and each `fm agents` host send a known-forbidden command through the real tool path, and the session refuses to proceed if it isn't blocked; a test with the hook disabled sees the refusal.

- **Quarantine unverified worker claims behind an independent evidence re-run** — FIX — value 5 — effort M — risk low — category: verification
  Why: T-1208 shows a criterion whose verify command named a nonexistent test module; weaker or foreign workers will report "done" with similar hollow proof.
  Done when: at close, Foreman re-runs each criterion's command itself in a clean checkout of the diff, and a fixture where a worker claims pass but the test is missing or fails ends in a rejected close.

- **Detect and heal state-ledger divergence from the git tree** — FIX — value 4 — effort M — risk med — category: consistency
  Why: T-1203 (guard mine reads the wrong worktree's transcripts) and the dirty-files-at-focus request show state and worktree drifting; multiple workers writing in parallel lanes make it worse.
  Done when: `fm doctor` flags a task marked done whose commit is absent or whose files differ from the evidence, and `--fix` re-opens it; a fixture with a hand-reset branch triggers the finding.

- **Add per-backend circuit breakers with automatic model failover mid-task** — FEATURE — value 4 — effort M — risk low — category: availability
  Why: the worker health-probe idea is in the list, but not the policy: when to trip, how to carry the half-finished slot state to the next backend, when to close again (assumption: network and local servers fail often).
  Done when: a fake provider returning 5xx three times trips the breaker, the task continues on the fallback with the same journal, and a half-open probe restores the primary after the cooldown.

- **Bound every external CLI worker with a process-group watchdog** — FIX — value 4 — effort S — risk low — category: process control
  Why: codex, gemini and aider as workers can hang on a prompt or spawn orphans; T-0831 (salvage partial results from capped children) shows capped children already lose work.
  Done when: a fake worker that ignores SIGTERM and spawns a child is killed as a whole group at the deadline, its partial diff is kept in a salvage lane, and no pids remain.

- **Snapshot the worktree and rewind on any gate regression** — FEATURE — value 4 — effort M — risk low — category: rollback
  Why: "atomic edits with rollback" is proposed per edit; a gate-level rule is missing: if a later step turns a previously green gate red, auto-revert to the last green snapshot and retry differently.
  Done when: a scripted weak-model run that breaks a passing test is rolled back to the green snapshot automatically, and the event log shows the regression and the revert.

- **Wild: Run a continuous soak harness that replays old sessions against every release** — FEATURE — value 4 — effort L — risk low — category: regression
  Why: recorded replay fixtures exist as an idea; using the whole corpus of the user's real guard refusals (`fm guard mine`, guard_cases.jsonl) as a release gate over `fm code` too would catch drift before 1.2.35. wild
  Done when: `fm release` fails when any replayed session's guard verdicts or gate outcomes differ from the recorded ones without an approved update.

- **Wild: Add a deterministic "fault dial" that makes any model act like a flaky one** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: weak local models are the target user's goal, but tests with a strong model never exercise malformed JSON, truncation, or repeated edits; a dial that corrupts replies at set rates proves the repair loop. wild (assumption: slot validator exists).
  Done when: running the e2e roundtrip with 30% corrupted slot replies still finishes the task with bounded repairs and reports the repair count.

- **Wild: Seal each closed task with a reproducible-proof bundle anyone can re-verify offline** — FEATURE — value 3 — effort M — risk low — category: auditability
  Why: users distrust agent "done" claims; the pack shows a heavy emphasis on evidence. A bundle holding diff, commands, outputs and environment hash lets `fm verify-bundle` re-run it elsewhere. wild
  Done when: `fm verify-bundle FILE` on a clean machine reproduces the recorded pass for a fixture task, and fails if one byte of the diff is changed.

- **Cap and report non-determinism by running flaky gates N times** — FIX — value 3 — effort S — risk low — category: flake control
  Why: the dropped item "retry a red criterion once" was premised wrongly, but the existing `fm check` single-rerun already hides flakiness (T-0047); with weaker models, a flaky pass is indistinguishable from real progress.
  Done when: a gate that passes 2 of 3 runs is recorded as "flaky", not "pass", and blocks the close unless the user overrides it.

- **Enforce a global lease on the main checkout for all non-Claude workers** — SECURITY — value 4 — effort S — risk low — category: isolation
  Why: T-1196 had to add "stay out of the main checkout" to the builder brief — text only; foreign CLIs ignore briefs. Enforcement must be mechanical (read-only bind or a path guard).
  Done when: a fake worker that writes to the main checkout path is blocked or the write is detected and reverted, with a logged violation.
