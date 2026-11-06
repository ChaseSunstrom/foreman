# Brainstorm — lens: reliability

- **Back off with jitter and a breaker on API overload** — FIX — value 4 — effort M — risk low — category: resilience
  Why: the pack covers waiting out usage limits and failing over between providers, but not 429/529/5xx bursts, which are a different failure from a quota. Without a retry budget, a drive with several lanes will hammer an overloaded endpoint. assumption: today's retry is flat or per-call.
  Done when: a fake host returns 529 for 60s, and the test shows capped, jittered retries, one open-breaker note and no lane failing.

- **Run a pipe-flood and slow-reader fake agent** — FIX — value 4 — effort S — risk low — category: child handling
  Why: the pack has a hostile fake host and schema-validated child output, but nothing that tests stdout/stderr backpressure. A child that writes 50 MB to stderr, or never closes stdout, can deadlock a drive that reads one pipe at a time. assumption: children are read through pipes, not files.
  Done when: a fake child floods stderr and a second one hangs with stdout open, and the drive times both out, records the cause and keeps its other lanes running.

- **Shuffle the test order and print the seed on failure** — FIX — value 3 — effort S — risk low — category: test reliability
  Why: plugin/tests holds 414 files gating every `fm ship`. Order dependence and shared-state leaks go unseen while the order is fixed. The pack has flake rates, an env matrix and a fast/full split, but no order randomisation.
  Done when: `FM_TEST_SEED=N` reproduces the same order, the nightly full suite runs shuffled, and any failure prints its seed.

- **Isolate every `fm doctor` check** — FIX — value 4 — effort S — risk low — category: diagnostics
  Why: `fm doctor` is a named gate and has many checks. One crashing or hanging check shouldn't hide the rest. assumption: checks currently share one process and one failure path.
  Done when: a planted check that raises and another that sleeps forever each appear as "check failed to run: <reason>" (the third state) while all other rows still print.

- **Lint that every raised exception maps to an exit code and a Next line** — CLEAN — value 3 — effort S — risk low — category: CLI contract
  Why: T-2653 added Next commands to nonzero exits for PolicyError, LockTimeout, CorruptState and ValueError. A new exception class added later would silently fall back to a bare traceback.
  Done when: an AST test fails when an exception class raised under `plugin/lib` has no entry in the exit table, and passes once one is added.

- **Explain who holds a lock and for how long** — FEATURE — value 3 — effort S — risk low — category: concurrency
  Why: LockTimeout now prints a Next command, but the holder's identity and age are what let the user decide between waiting and clearing it. assumption: lock files don't record the owner's command line today.
  Done when: a held lock makes `fm` print the holder's pid, command, start time and age, and mark it dead if the pid is gone.

- **Post-push watch: follow CI for the pushed sha and file a revert-or-fix task** — FEATURE — value 4 — effort M — risk med — category: ship safety
  Why: `fm ship` pushes straight to main under a standing grant, gated by the local suite only. The test badge lives on GitHub, so a red remote run (a different Python or OS) would go unseen after the push.
  Done when: after a ship, a red Actions run on that sha produces an inbox task with the log tail and a one-line revert command, and a green run records the sha as confirmed.

- **Show a single persistent "running degraded" line** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the pack has many separate fallbacks (no `claude` on PATH, read-only state, stale installed copy, volatile paths, a dropped ledger class). Each is reported differently, so a user can't tell at a glance that Foreman is working at reduced strength.
  Done when: a registry of degraded reasons feeds one line in the session start, `fm status` and `fm doctor`, and the line disappears when the last reason clears.

- **Record the nondeterminism of every hook call so any failure replays bit-exact (wild)** — FEATURE — value 3 — effort L — risk med — category: replay
  Why: the pack replays hook inputs, but a failure that depends on clock, PID, env, hash seed or file listing order may still not reproduce. assumption: a failing run today can't be reproduced from its logged input alone.
  Done when: a hook crash writes a bundle of its input plus clock, random seed, env and directory listings, and `fm replay --exact BUNDLE` reproduces the same exception.

- **Run the guard under two Python versions and block when they disagree (wild)** — SECURITY — value 3 — effort M — risk med — category: guard
  Why: the pack proposes a 100-line shadow guard and an oldest-supported-Python matrix. Neither covers interpreter-dependent behaviour such as regex semantics, `shlex` and unicode, where the same rule can decide differently on two minor versions.
  Done when: a nightly job feeds the replay corpus to the guard on the oldest and newest supported Python, and any differing verdict becomes a task.

- **Pull a cable on a random subsystem during a real idle drive, with a kill switch (wild)** — FEATURE — value 3 — effort M — risk high — category: chaos
  Why: the pack's fault injection runs only in tests and drills. Production-shaped failures (the timer environment, tmpfs pressure, a half-installed upgrade) are only rehearsed in scratch homes. assumption: one safe idle window per week is available.
  Done when: a weekly opt-in job injects one reversible fault into the live drive, such as a read-only state dir for 30s. It records how the drive recovered and aborts on a HALT file.

Next question: which of Foreman's retry, wait and backoff paths share one policy, and which each carry their own constants that a single overload event could trip at once?
Next question: when `fm ship` pushes and the remote disagrees with the local verdict (CI red, a hook rejecting the push, a protected branch), what does the user see, and who files the follow-up?
