# Brainstorm — lens: reliability

- **Write a run journal and resume from it** — FEATURE — value 5 — effort M — risk med — category: durability
  Why: the user quit and the planner kept running orphaned; closed lids, kills and crashes lose the run today. Resume ideas exist only as one-liners ("Reattach to a live run from its event log"), and none defines a step-level journal with idempotent replay.
  Done when: `kill -9` of `fm code` mid-step, then `fm code --resume`, finishes the task with no step re-run that had already passed (the journal shows the skip), proven by a test with a fake runner.

- **Make one process group the unit of a run** — FIX — value 5 — effort S — risk low — category: process
  Why: T-1326 says stop kills children, but SIGKILL, a closed terminal and an exec'd grandchild escape a plain child list. Own the group (setsid and a registry file) so a later start can reap leftovers.
  Done when: after `kill -9` of the parent, a fake runner's grandchild is gone within 5 s, or the next `fm code` start reaps it and says so.

- **Add a silence watchdog with a named diagnosis** — FEATURE — value 5 — effort M — risk low — category: liveness
  Why: "it just isn't doing anything" for minutes at 66k–133k input tokens per call. A watchdog should tell a slow model from a hung child, a login prompt waiting on stdin, a rate limit, or a plugin-loading startup tax, then say which.
  Done when: four scripted fake CLIs (hang, stdin prompt, 429 loop, slow start) each produce a distinct one-line diagnosis within the watchdog window.

- **Fall back across runners on classified failures** — FEATURE — value 4 — effort M — risk med — category: failover
  Why: the runner registry (T-1328) finds CLIs, but nothing says what happens when one dies mid-run: quota, auth expiry, timeout. Classify the failure and retry the step on the next eligible runner while the harness still judges every turn.
  Done when: with runner A scripted to return a quota error on step 2, the run closes via runner B and the receipt names both, with the guard verdicts unchanged.

- **Reject nested Foreman with a depth marker** — FIX — value 4 — effort S — risk low — category: recursion
  Why: the user asked for no duplicate Foreman when Claude Code is a worker. T-1327 strips context, but a marker env var plus a process-ancestry check also catches a worker that spawns `fm code` itself, which could loop forever.
  Done when: a fake worker that runs `fm code "x"` gets a refusal naming the parent run, and the depth never exceeds 1 in a test.

- **Run every runner adapter against a misbehaving fake** — CLEAN — value 4 — effort M — risk low — category: testing
  Why: live verification of codex, gemini and opencode is blocked (T-0336). A scripted fake can emit truncated JSON, partial lines, ANSI noise, an early exit 0, an exit 1 with a good answer, and stderr floods. That tests every adapter without accounts.
  Done when: one table-driven test runs each adapter parser against 8 hostile transcripts and none hangs, crashes, or reports success on a failed turn.

- **Lock tasks across app instances and projects** — FIX — value 4 — effort M — risk med — category: concurrency
  Why: the home screen (T-1330) will run queued tasks from many projects, and a user may open two windows or run `fm code --task ID` beside Claude Code. Without a lease with a heartbeat and stale takeover, two runners can edit one task.
  Done when: two processes started on the same task ID leave exactly one running, and the loser says who holds the lease; a killed holder's lease is taken over after its timeout.

- **Snapshot each step to a shadow ref for instant rollback** — FEATURE — value 4 — effort M — risk med — category: rollback
  Why: the harness already undoes a commit and restores Git config, but a bad step in the middle of a run has no cheap undo. A private ref under `refs/foreman/` per step, never touching the user's branches, would give one.
  Done when: `fm code --rewind 2` restores the tree to the end of step 2 byte-for-byte and the user's branch and index are unchanged.

- **Write config atomically with a last-good copy and a doctor line** — FIX — value 3 — effort S — risk low — category: config
  Why: the user wants better config/setup and one config line to pick the default; a hand edit that breaks `models.json` should not stop the app from opening.
  Done when: a corrupt `models.json` makes `fm code` open with the last-good copy and a one-line warning naming the line, and a test proves it.

- **Run a canary of every request kind on every runner nightly** — PERFORMANCE — value 3 — effort M — risk low — category: regression
  Why: 7/7 request kinds closed only with the claude CLI; other CLIs' drift would go unseen. `fm code bench` exists to be scheduled, and a ratchet on the held-rate catches a CLI update that breaks an adapter.
  Done when: a scheduled run writes a per-runner pass table, and a deliberate adapter break turns one cell red and files a task.

- **Wild: Add a sentinel that watches the watchers** — FEATURE — value 3 — effort M — risk low — category: self-monitoring
  Why: assumption: the TUI, the watchdog and the home screen can each fail silently. A tiny separate process checks heartbeats from the harness and the renderer and rings the terminal bell if either goes stale.
  Done when: freezing the renderer with SIGSTOP makes the sentinel print a "renderer stalled" line to the plain log within 10 s.

- **Wild: Shrink any failed run to a minimal repro** — FEATURE — value 3 — effort L — risk med — category: debugging
  Why: assumption: a failure on a user's machine (the nixie hang) is hard to reproduce. Delta-debug the run's event log into the smallest fake-runner script that still shows the failure, redacted, and attach it to a filed task.
  Done when: a recorded stall log reduces to a script under 20 events that still triggers the same watchdog diagnosis.

- **Wild: Mutate real logs to fuzz the whole app** — SECURITY — value 3 — effort M — risk low — category: fuzzing
  Why: assumption: real event logs hold odd sequences the hand-written tests miss. Replaying logs with dropped, duplicated, reordered and truncated events against the reader and renderer finds crashes before users do.
  Done when: 1,000 mutated replays of a recorded run end with no traceback and a restored terminal, and any failure saves its seed.

- **Wild: Quarantine a crash loop into safe mode** — FEATURE — value 3 — effort S — risk low — category: recovery
  Why: assumption: a bad theme, extension or config can crash `fm code` at start every time, locking the user out of the app. After 3 crashes in 2 minutes, boot with no extensions, the default theme and plain text, and say why.
  Done when: a planted extension that raises at import crashes three starts, and the fourth opens in safe mode naming that extension.
