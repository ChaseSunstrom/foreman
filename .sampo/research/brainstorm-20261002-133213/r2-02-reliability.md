# Brainstorm — lens: reliability

- **Lock the record with a cross-process writer lock** — FIX — value 5 — effort M — risk med
  Why: the pack shows classic hooks (separate Python processes), `fm` CLI calls, `fm run` and soon a mod calling `$.process.run` all writing one per-project record concurrently; atomic writes were suggested, but not serialization (lost updates between read-modify-write). Assumption: fmcore uses plain read-modify-write without flock.
  Done when: a test spawning 20 parallel `fm task step` / `fm task evidence` calls on one brief leaves all 20 changes present and the file parses.

- **Detect and heal stage/step drift on resume** — FIX — value 4 — effort M — risk low
  Why: Foreman promises resuming at the exact step after /compact, yet Bash edits are invisible and a crash mid-transition can leave stage=executing with all steps done, or stage=verifying with no evidence. Assumption: no invariant checker runs on SessionStart.
  Done when: `fm doctor` and SessionStart flag a hand-corrupted brief (stage/steps/evidence mismatch) and `fm doctor --fix` repairs it in a test.

- **Make "done" evidence tamper-evident and fresh** — SECURITY — value 4 — effort M — risk med
  Why: gates refuse "done" without recorded evidence, but evidence is a text claim. Record the HEAD/tree hash and file mtimes with each evidence entry, and reject evidence older than the last edit of files in scope. Assumption: evidence currently stores only text and a timestamp.
  Done when: editing an in-scope file after `fm task evidence` makes `fm task done` fail with "stale evidence" until re-proved.

- **Add a hook-dispatch circuit breaker with a visible degraded mode** — FIX — value 4 — effort M — risk med
  Why: hooks must stay fast and fail-safe; there is a known 29 ms p50 but no tail-latency or repeated-crash policy. After N consecutive hook exceptions or timeouts, disable the failing handler for the session, surface it in the statusline/Pane, and keep the guard (fmguard) always fail-closed for dangerous commands.
  Done when: a test that injects an exception into a handler 3 times shows the handler skipped, a "degraded" marker in state, and the guard still blocking `rm -rf /`.

- **Run a mod-vs-classic contract test matrix in CI** — CLEAN — value 4 — effort M — risk low
  Why: mods are additive and classic hooks must work under `claude -p` and older builds; the tests (137 s) only cover the Python side. Test with `claude plugin test` using a mocked `$.process.run` that replays recorded `fm --json` fixtures, including fm failure, non-JSON output, and slow responses (timeouts).
  Done when: `claude plugin test` passes on fixtures for fm missing, exit≠0, malformed JSON, and 5 s hang, with the Pane showing an error state rather than crashing.

- **Make the test suite fast and tiered** — PERFORMANCE — value 3 — effort M — risk low
  Why: 137 s for the suite discourages TDD runs and rewards skipping; a flaky or slow suite is a reliability risk. Tag the slow e2e/bench tests, run a <15 s smoke tier by default, and cache the rest by changed-module.
  Done when: `fm check --fast` finishes in under 15 s and a CI target still runs the full tier.

- **Add a record snapshot and `fm undo` for destructive transitions** — FEATURE — value 3 — effort S — risk low
  Why: drive/full-autonomy mode mutates the queue unattended (`fm tidy`, `fm task finish`, section overwrites like T-0075), and there is no rollback. Keep the last N rotated snapshots of the record, restorable with `fm undo`.
  Done when: after `fm tidy` deletes a brief, `fm undo` restores it byte-identical, and snapshots are capped at N.

- **Make drive mode stall-proof with a watchdog and attempt budget** — FIX — value 4 — effort M — risk med
  Why: unattended `fm run` and `$.prompt.submit` wake-ups can loop on a task that keeps failing verification, burning tokens (the user is usage-sensitive). Assumption: there is no per-task retry cap. Record attempts per task and park the task into the inbox with the failure reason after K failures.
  Done when: a task whose verification always fails is parked after K attempts, the queue advances, and `fm digest` reports it.
