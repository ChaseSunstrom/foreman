# Brainstorm — lens: reliability

- **Run compound operations as resumable sagas** — FEATURE — value 5 — effort M — risk med — category: durability
  Why: `fm lane merge`, `fm task done`, release, and `install-user` each change several files and refs in sequence. A kill between steps leaves a half-landed state. The lane-merge-beside-dirty-main fixes (T-0403) show this path is already fragile. Existing ideas cover crash-safe single-file writes, not multi-step operations.
  Done when: for each compound command, a test kills the process after every step; rerunning `fm resume` or the same command finishes or rolls back to a state where `fm doctor` is clean.

- **Pin each session to a Foreman version during upgrades** — FIX — value 5 — effort M — risk med — category: upgrade safety
  Why: assumption: `install.sh` and `fm evolve` rewrite files under `~/.claude/foreman` while live sessions import `plugin/lib/*.py`. Releases land often (1.2.8 to 1.2.16), so a hook can load a mix of old and new modules. Install into versioned directories and swap an atomic `current` link. Each session records its version at SessionStart, and old versions are garbage-collected once no session uses them.
  Done when: a test upgrades Foreman while a scripted session fires hooks in a loop, and no hook errors or runs mixed-version code.

- **Fault-inject the environment in CI** — FEATURE — value 4 — effort M — risk low — category: robustness
  Why: assumption: the 88 tests cover logic, not environment faults. Add a matrix of ENOSPC, read-only home, unset `$HOME`, non-UTF-8 locale, torn last ledger line, EMFILE, slow filesystem, offline network, and clock jumps or DST. For each fault, hooks must either allow the action or refuse with one clear line, never a traceback. Network features (`landscape`, `deps`, `share`) should degrade to cached results.
  Done when: `fm doctor --faults` runs the matrix and every case passes with no raw Python traceback in the output.

- **Put circuit breakers and retry classes on headless runs** — FEATURE — value 5 — effort M — risk low — category: unattended runs
  Why: `fm run`, `fm night`, and `fm serve` start fresh `claude -p` sessions. A task that crashes repeatedly, an API 529, or a rate limit can loop or burn budget. Classify failures as transient (backoff with jitter), deterministic (quarantine the task as blocked with its crash bundle), or environmental (pause the whole queue). Trip a breaker after N identical failures.
  Done when: with a fake `claude` that fails deterministically, `fm run` marks the task blocked after N tries and moves on. With one that fails transiently, it retries with backoff and then succeeds.

- **Send an external dead-man heartbeat for unattended work** — FEATURE — value 4 — effort S — risk low — category: monitoring
  Why: `fm night` and `fm serve` run while the user is away, and `fm notify` is a single command that can itself fail silently. A heartbeat to an independent channel the user configures (ntfy, a healthchecks-style URL, or a local file watched by systemd) alerts when the pings stop. The user opts in, and it sends nothing by default.
  Done when: killing a night run stops the heartbeat, and the configured sink gets an alarm within the grace period. With no sink configured, no outbound request is made.

- **Track hook SLOs and auto-degrade on burn** — FEATURE — value 4 — effort M — risk med — category: self-monitoring
  Why: `bench_hooks.py` measures latency only on demand. Track p99 hook latency, false-block rate, resume success rate, and crash count continuously against budgets. When the error budget burns fast, switch off the newest optional subsystem (by feature flag) and record why, instead of waiting for the user to complain through a downstream project.
  Done when: injecting a slow hook trips the budget, the flagged feature is disabled automatically, `fm status` says so, and `fm doctor` shows the recovery path.

- **Back up central state and rehearse the restore** — FEATURE — value 4 — effort M — risk low — category: recovery
  Why: all briefs, the ledger, decisions, and lessons live in one central place, and `fm sync` mirrors only an opt-in subset. Take rotating snapshots, run a scheduled restore drill into a scratch directory, and verify that `fm doctor` is clean and `fm resume` works there.
  Done when: deleting the state directory and running `fm restore` returns to the last snapshot, and the drill reports a pass or fail with a diff of what is missing.

- **Test Foreman beside popular plugins at runtime** — FEATURE — value 3 — effort M — risk low — category: interoperability
  Why: `fm plugins` only reports conflicts statically. Ship a matrix that runs a scripted session with Foreman plus each common hook-bearing plugin enabled. It checks hook ordering, `PreToolUse` input rewrites, and double `Stop` hooks that fight over keeping the session going.
  Done when: CI runs the matrix, and each plugin pair either passes the end-to-end roundtrip or has a documented conflict with a guard-side mitigation.

- **Contract-test the JSON surfaces that consumers read** — CLEAN — value 4 — effort S — risk low — category: API stability
  Why: the desktop app, UI mod, and MCP server consume `fm ui --json`, `fm projects --json`, and `fm mcp` tools. Earlier bugs such as the band stuck on step 1/5 came from state mismatches between producer and consumer. Add recorded consumer fixtures, with schema and golden files, that fail any producer change that breaks a field.
  Done when: removing or renaming a field in `fm ui --json` fails a named contract test that points to the consumer.

- **Wild: Probe rule retention inside live sessions** — FEATURE — value 4 — effort M — risk med — category: model reliability
  Why: assumption: long sessions and compactions silently erode vetoes, the single active task, and the "capture, don't chase" rule. At step boundaries, the hook asks a cheap side check ("what is the active task and which vetoes apply here?") and compares the answer with the ledger. A mismatch triggers a re-injection of the rules or a clean restart from the checkpoint. wild
  Done when: in a replayed long session where a veto was dropped from context, the probe detects it and re-injects the veto before the next edit.

- **Wild: Hold a monthly fire drill that destroys state on purpose** — FEATURE — value 3 — effort M — risk med — category: recovery
  Why: `fm night` can run a scripted disaster in a cloned sandbox project: delete the state, corrupt the ledger tail, kill mid-merge, and revoke a hook file. Foreman must recover using only its documented commands, and the run is scored on time-to-recover and manual steps. This turns recovery from something never exercised into something measured. wild
  Done when: the drill outputs a scorecard where each disaster maps to a recovery command, and a regression in any recovery path fails the drill.

- **Wild: Fuzz random lifecycle sequences with crash points** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: assumption: tests are mostly scenario-based. A stateful fuzzer would generate random sequences of `capture`, `focus`, `checkpoint`, `done`, `lane`, `compact`, and `resume`. It would also inject a kill at every file write and check the global invariants after each step: one active task, no lost briefs, resume point valid. Failing sequences shrink to minimal reproductions that become regression tests. wild
  Done when: a seeded run of 10,000 sequences passes, and a deliberately introduced non-atomic write is caught and shrunk to fewer than 10 commands.

- **Verify tool versions at startup, not just at install** — FIX — value 3 — effort S — risk low — category: environment
  Why: the installer enforces Python ≥ 3.12.7, but nothing re-checks it later. A system update, a PATH change, or a `uv` shim swap can silently change `python3`, and hooks would then fail in the middle of a session. Each SessionStart runs a cheap check of the interpreter, `git`, and `claude` versions against a manifest. On a mismatch it prints one actionable line and keeps hooks in a known-safe mode.
  Done when: running a session with `python3` shimmed to an older version produces a single clear warning naming the fix, and no hook raises a traceback.
