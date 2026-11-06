# Brainstorm — lens: reliability

- **Make the gate lock die with its holder** — FIX — value 5 — effort S — risk low — category: gate locks
  Why: a hung check in another project held the machine-wide gate lock for over 40 minutes, and the user asked for a 15-minute cap, so waiters still stall until that cap expires. Assumption: the lock records no owner PID or heartbeat, so a crashed holder is only detected by timeout.
  Done when: killing a `fm check` mid-run releases the lock within one heartbeat interval, and a test shows a waiter proceeding without the 15-minute wait.

- **Expire edit leases with their run** — FIX — value 5 — effort S — risk low — category: fm code leases
  Why: the user reported that a model run's edit leases outlive it, because `drop_session` runs only for worker runs, so the next run on the same code is refused for 20 minutes.
  Done when: a finished or killed model run releases its leases, and a test starts a second run on the same files right after the first ends and it is not refused.

- **Make `fm quiet` fail loudly on empty stdin** — FIX — value 4 — effort S — risk low — category: CLI honesty
  Why: the user reported that `fm quiet` runs with no stdin, so a heredoc script does nothing and the command exits 0.
  Done when: piping a script into `fm quiet` either runs it or exits nonzero with a message, and a test covers both paths.

- **Fix the midnight defer bug with a reset-time test** — FIX — value 4 — effort S — risk low — category: scheduling
  Why: deferrals set with `--until reset` came back at midnight, two hours before the 02:00 weekly usage reset (T-1802).
  Done when: a test sets a defer with `--until reset` and asserts the wake time equals the configured reset time in local time, with a DST-boundary case included.

- **Quarantine flaky tests instead of letting them block main** — CLEAN — value 4 — effort M — risk med — category: test reliability
  Why: `test_followups.Docs` raised IndexError on main after a split, `test_help` broke because two commands shared help position 306, and `test_session_care` failed on a snapshot of last release's defaults. Each failure blocked a push.
  Done when: each recurring failure has a named owner test, a check that flags any new red test on main within one run, and a CI record of pass/fail history over 20 runs.

- **Gate the site deploy on the same checks as the build** — FIX — value 4 — effort S — risk med — category: release safety
  Why: pushing `foreman/build` to main published the site, but the work's criterion was pinned to an old commit (235932b8) before the test fix moved build to e021641f, so the pass record no longer matched what shipped.
  Done when: a deploy refuses to run unless the commit it publishes is the same commit that passed the gate, and a test checks the SHA match.

- **Measure the hook budget under load, not once** — PERFORMANCE — value 3 — effort S — risk low — category: hook benchmarks
  Why: the PreToolUse:Bash:script p95 read about 310 ms against a 300 ms budget, but on a quiet machine a 20-run bench gave a median of 266.5 ms and a p95 of 272.3 ms. The budget failure is a measurement artifact, not a regression.
  Done when: the bench reports the machine load beside each number and fails only if the budget is exceeded at load below a stated threshold.

- **Recover runs that die mid-task without losing their place** — FEATURE — value 5 — effort M — risk med — category: crash recovery
  Why: the stalled-run card offers wait, kill and switch-runner actions, which means a stall currently ends with a human choice. Assumption: a run that dies mid-edit has no checkpoint that a fresh run can resume from.
  Done when: killing a run during an edit and starting `fm code` again resumes from the last journal step and the final diff matches an uninterrupted run.

- **Notice your own usage burn and act on it** — FEATURE — value 5 — effort M — risk med — category: self-monitoring
  Why: the user said, "I shouldn't have even had to tell you about the usage things, foreman should've figured it out itself," and Foreman still required a manual pass to find and cut the burn.
  Done when: when a session's context per reply rises above the budget (about 140k), Foreman compacts or switches model without being asked, and the event shows up in `fm cost`.

- **Lock the rules file under its budget in CI** — CLEAN — value 3 — effort S — risk low — category: doctor budgets
  Why: the rules file went over the doctor's 6,400-character budget (6,416 characters) and stayed there until the user asked for a trim.
  Done when: a commit that pushes the rules file over 6,400 characters fails CI, and the doctor prints the remaining headroom.

- **Crash-proof the TUI with a last-known-good state** — FIX — value 3 — effort M — risk low — category: TUI resilience
  Why: the app shows several live cards (work bar, stall, activity), so a failed render of one card has no fallback. Assumption: a single exception in a card would take down the whole pane.
  Done when: forcing an exception in one card leaves the other cards rendering and shows a placeholder for the failed card.

- **Run a rolling soak test of the gate and lease system** — RESEARCH — value 4 — effort M — risk low — category: soak testing
  Why: the gate-lock stall and the lease outlive bug were both found by use, not by a test, and both showed up only under overlapping runs.
  Done when: a soak runs 50 overlapping `fm check` and `fm code` jobs with random kills, and it finds zero stuck locks and zero refused leases.

- **Pin every run's environment and check it on start** — FEATURE — value 3 — effort S — risk low — category: reproducibility
  Why: a test failed when the Claude Code env from `fm install-user` was inherited, causing a 200k window and 10 bench failures.
  Done when: a run refuses to start if an inherited variable differs from the pinned value, and the refusal names the variable.

- **Wild: a black-box flight recorder for every run** — FEATURE — value 4 — effort L — risk low — category: wild observability (wild)
  Why: `fm code why ID` already rebuilds a run from its journal, so a continuous, replayable recording of every run, including the input, the gate state and each lease, would let any stall be diagnosed after the fact. Assumption: journals don't yet capture lock and lease state.
  Done when: replaying a recorded run to a chosen step reproduces the same lock and lease states as the original.

- **Wild: a standby run that takes over a stalled one** — FEATURE — value 3 — effort L — risk med — category: failover (wild)
  Why: `fm run` already fails over after a usage limit, so the same mechanism could hand a stalled run to a warm standby without waiting for the user to press k or m.
  Done when: a run stalled for longer than its threshold is handed to a standby, and the handoff completes with the same final diff in a test.

- **Wild: a chaos day for Foreman's own gates** — RESEARCH — value 3 — effort M — risk med — category: chaos testing (wild)
  Why: the reliability failures so far were all found in real use, so a scheduled run that kills locks, drops leases and corrupts a journal on purpose would find them before the user does.
  Done when: a weekly chaos run injects at least three faults, and every fault is either recovered automatically or reported with a named cause.
