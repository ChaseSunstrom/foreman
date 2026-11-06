# Brainstorm — lens: invented: drive that never stalls

- **Run the drive as an external supervisor, not a session** — FEATURE — value 5 — effort M — risk med — category: drive
  Why: stops appeared (0 to 0.1) and the drive's phantom-hold bugs (T-2873, T-2901) all stem from the drive living inside a process that dies or lags; the user wants overnight progress unattended. Assumption: a user systemd timer can re-enter `fm next`.
  Done when: killing the Claude process mid-night leaves the queue advancing within 2 minutes, shown in the drive ledger.

- **Type every stop with a cause and a self-heal** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: "drive stops appeared" is a gap, but a stop has no taxonomy beyond waits. Assumption: stops are currently untyped in the ledger.
  Done when: each stop row carries one of {usage-limit, dead-agent, phantom-hold, endpoint-down, user-only-grant, empty-queue} and the first four resume without a human in a replay test.

- **Verify every counted running agent against a live OS process** — FIX — value 4 — effort S — risk low — category: drive accuracy
  Why: T-2873/T-2901/T-0115 show the running set mixing engine lists and event scans; each error holds the drive. Done when: a planted dead agent id is dropped from the running set within one tick in a unit test.

- **Keep a never-empty ladder of unblocked work** — FEATURE — value 4 — effort M — risk low — category: queue
  Why: standing rule "keep working the rest of the queue"; blocked items (T-0325, T-0335, T-0352) must not stall the drive. Done when: with only blocked tasks open, the drive picks a local-model-safe item (audit, doc claim check, deferred backlog grooming) instead of stopping.

- **Fall back to the local model during a usage-limit wait** — FEATURE — value 5 — effort M — risk med — category: local models
  Why: user wants local models used "without limit for background volume"; real usage limits are currently waited out. Assumption: Smith on qwen3.8-27b can do S-sized tasks. Done when: a simulated limit wait results in at least one closed S task by the local arm, marked unwitnessed.

- **Add a progress watchdog with an escalation ladder** — FEATURE — value 4 — effort M — risk low — category: watchdog
  Why: a quiet drive is indistinguishable from a working one. Done when: no ledger movement for N minutes triggers retry tick, then agent reap, then a re-exec, each logged.

- **Re-exec the drive at an idle tick after code lands** — FIX — value 3 — effort S — risk med — category: self-update
  Why: the drive fixes (T-2900, T-2901) only help once the running drive loads them. Done when: after a ship touching drive code, the next idle tick restarts onto the new code with state intact.

- **Check the model endpoint before a swap and batch around it** — PERFORMANCE — value 4 — effort S — risk low — category: local models
  Why: steer says a llama-swap switch costs ~3 min with no detection; a mid-night swap looks like a stall. Done when: queued local jobs are ordered by resident model and a swap is logged as "swap", not stall.

- **Trip a circuit breaker on repeated failing tool calls** — FIX — value 4 — effort M — risk low — category: tool reliability
  Why: failed tool calls are up by half. Done when: three identical-signature failures in a lane stop that lane's retries and file one task with the signature.

- **Wild: Run a stall drill every night first** — FEATURE — value 3 — effort M — risk low — category: chaos — wild
  Why: assumption: stalls are found by users, not tests. Done when: a scratch drive is killed, phantom-held and limit-blocked nightly and must recover, with the result on the morning card.

- **Wild: Have a second drive audit the first** — FEATURE — value 3 — effort L — risk med — category: oversight — wild
  Why: assumption: a stall cannot be self-detected. Done when: a lightweight watcher process pages (one glyph in the status line) when the main drive's heartbeat stops while work is open.

- **Wild: Write a night plan the drive grades itself against** — FEATURE — value 3 — effort M — risk low — category: planning — wild
  Why: "overnight progress" is unmeasured. Done when: the morning card shows planned vs closed tasks and names the stop that cost the most time.

- **Replay the drive's last 50 ticks against a candidate fix** — CLEAN — value 4 — effort M — risk low — category: testing
  Why: three drive bugs in a row each slipped through; real engine shapes are the missing fixture. Done when: a recorded tick log replays through the running-set function and a regression fails red before the fix.

Next question: What fraction of past drive stops were caused by the host (session death, usage limit) versus Sampo's own counting, and does the ledger record enough to tell?
Next question: Which stops would the user rather be woken for than have auto-resumed?
