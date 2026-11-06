# Brainstorm — lens: reliability

- **Make every guard-state read fail loudly, with a ledger record** — FIX — value 5 — effort M — risk med — category: guard
  Why: open question "when the guard's rules file, grant store or last-good copy is missing or truncated at hook time, what does each unattended path do, and does anything record it?" The pack shows no answer.
  Done when: a test truncates each of rules, grants and last-good, runs a hook, and finds a `guard_degraded` ledger line naming the file and the chosen fail-open or fail-closed mode.

- **Declare fail-open or fail-closed per hook and crash-test it** — FEATURE — value 5 — effort M — risk med — category: hooks
  Why: the idea list proposes crash cards, but nothing enforces a declared mode per hook. assumption: hooks currently differ in behaviour on an exception.
  Done when: a table in the code lists every hook with its mode, and a test injects an exception into each and asserts the declared outcome.

- **Kill-point sweep across every ledger append** — FIX — value 4 — effort M — risk low — category: ledgers
  Why: T-2668's latency test and the drill faults cover shape, not torn writes at each fsync boundary. assumption: appends are not yet crash-tested at each write.
  Done when: a test kills a writer subprocess at N points per append and `fm verify-ledger` plus every reader open the file and report only the torn tail.

- **Give unattended spawns a credential allowlist, tested with a canary grant** — SECURITY — value 5 — effort M — risk med — category: authority
  Why: open question on which lanes, ticks, `fm code` tools and prover children inherit the push grant, credentials or the signing key.
  Done when: a canary grant and key are planted, each spawned process class is run, and a test fails if any can read or spend them.

- **Name the stall precisely: `fm run` records why and which step hung** — FEATURE — value 4 — effort S — risk low — category: drive
  Why: T-2669 added `--stall-usd`, but the ship gate and children still time out without naming the hung test or child. assumption: timeouts report only "timed out".
  Done when: a forced hang in a test child yields a receipt line with the step name, elapsed time and last output line.

- **Surface a sub-agent's allowlist block as its own outcome** — FIX — value 4 — effort S — risk low — category: agents
  Why: open question "what does a sub-agent do when its tool allowlist blocks the only way to finish?" The pack shows no distinct outcome.
  Done when: a child that needs a blocked tool ends with status `blocked_by_policy`, the one widening command printed, and the task not marked failed.

- **Fall back to the previous install generation on a hook import failure** — FEATURE — value 4 — effort M — risk med — category: install
  Why: hooks run Python from the installed copy; a bad upgrade breaks every session at once. assumption: no atomic generation swap exists yet.
  Done when: a test corrupts a hook module in the new generation and the next hook call runs the prior one and logs the fallback.

- **Heartbeat for every unattended path with a "last alive" line in doctor** — FEATURE — value 4 — effort S — risk low — category: liveness
  Why: T-2542 handled one liveness case and "dead timer vs sleeping machine" is open; failures here are silent.
  Done when: `fm doctor` lists each timer, tick and drive with its last-alive time, and a stopped one turns the row red.

- **Verdict hysteresis: a flaky proof is labelled, not flipped** — FIX — value 3 — effort S — risk low — category: proof
  Why: T-2657 records per-test fail rates, yet `fm prove` verdicts don't use them. assumption: a flaky pass reads as a plain pass.
  Done when: a test that fails 1 in 5 reruns yields "pass (flaky, 4/5)" in the receipt rather than "proven".

- **(wild) Replay a museum of tasks that once hung or crashed the drive** — FEATURE — value 4 — effort M — risk low — category: regression
  Why: assumption: past hangs (T-2668's nested `$(`) are single regression tests, not a standing corpus run against each release.
  Done when: `fm drill --museum` replays N recorded poison inputs under a timer, and any one over its bar fails the ship gate.

- **(wild) Run a silence drill that times who notices** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: question "when a capability is retired, who notices first?" Nothing measures time-to-notice for a silently dead part.
  Done when: a drill disables one random hook in a scratch home and reports minutes until a doctor row, ledger line or test names it.

- **(wild) Dual-run new hook code in shadow before it takes over** — FEATURE — value 3 — effort L — risk med — category: hooks
  Why: assumption: hook changes ship straight to the live path, so a regression hits every session first.
  Done when: for 50 real hook calls the shadow and live outputs are compared, and any difference is logged without affecting the session.

Next question: which unattended paths have never been run end-to-end on a real clock while the machine slept, suspended or lost its network?
Next question: what does the user see in the first minute after a silent fail-open, and is that moment ever tested?
