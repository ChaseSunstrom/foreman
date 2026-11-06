# Brainstorm — lens: invented: drive that never stalls

- **Write a typed stall record on every drive stop** — FEATURE — value 5 — effort S — risk low — category: drive
  Why: the request names "drive stops appeared (0 to 0.1)"; T-2900/2901 and the two later drive-miss fixes show stops being diagnosed by hand each time (phantom agents, re-push loops, a union that counted finished agents). Assumption: stops are not yet recorded with a cause.
  Done when: every transition from running to stopped writes one ledger row with a cause class (usage-limit, phantom-hold, tool-fail-loop, empty-queue, ward-block, host-exit, unknown), and `sampo drive why` prints the last one.

- **Release phantom holds against live OS processes** — FIX — value 5 — effort M — risk med — category: drive
  Why: three recent commits (T-2873, T-2900, T-2901) all fix the drive counting agents or shells that no longer exist. Counting from the host's list and an event scan keeps drifting. Checking pids is a signal the drive doesn't author.
  Done when: a test with a killed subagent pid and a stale background-task entry shows the drive releasing within one tick and logging the reason.

- **Run the drive under a supervisor outside the session** — FEATURE — value 5 — effort M — risk med — category: unattended
  Why: overnight progress is the ask, and a terminal closing, a resume or a host exit ends a session-bound drive. Assumption: the drive lives only inside a Claude Code session today. A user systemd timer plus a heartbeat file restarts it and runs `run-brief` headless.
  Done when: killing the session process at night causes a new drive to resume the queue within 2 minutes, with the stall record naming "host-exit".

- **Add a progress watchdog with an escalation ladder** — FEATURE — value 4 — effort M — risk low — category: drive
  Why: a drive can be "alive" yet hold with nothing advancing (the phantom-hold class). Define progress as ledger movement: a closed task, a new commit or a changed clause. After N quiet minutes: re-read the running set, then release holds, then restart the lane, then page.
  Done when: a planted hold with no real agent is cleared by rung 2 with no human input, and each rung is logged.

- **Trip a circuit breaker on repeated failed tool calls** — FIX — value 4 — effort M — risk low — category: reliability
  Why: failed tool calls up by half. A lane that retries the same failing call burns the night. Signature = tool + normalised args + error class; at three repeats, change approach, then fall to the next task.
  Done when: a replayed transcript with a repeated failing call stops after 3 tries, files a note and picks another task.

- **Keep a never-empty ladder of unblocked work** — FEATURE — value 4 — effort S — risk low — category: queue
  Why: Open work shows many deferred and blocked items, and `--round-first` holds Foreman-filed items back, so a quiet queue stops the drive. A ladder: user tasks, then held Foreman items whose blocker has flipped, then local-model backlog grooming, then the Exam sweeps.
  Done when: with the top queue empty, the drive picks a lower rung and logs which one, and only stops when every rung is empty or blocked on the user.

- **Fall back to local models during a usage-limit wait** — FEATURE — value 5 — effort M — risk med — category: local models
  Why: the standing rule says to wait out real usage limits, and the user wants local models used without limit for background volume. Waiting idles the night; the free arm can groom briefs, run finder passes and draft work held as unwitnessed.
  Done when: a simulated limit hit switches the drive to the local profile for allowed task kinds, marks outputs unwitnessed, and switches back at reset.

- **Split drive stops from drive waits in the ledger** — CLEAN — value 3 — effort S — risk low — category: observability
  Why: the 0→0.1 stop rate mixes real stops with intended waits (a usage limit, a ship gate), so the metric can't tell whether things got worse. Assumption: they are one counter.
  Done when: `sampo outcomes` reports stops and waits separately and the stop rate excludes waits.

- **Replay the drive's last 50 ticks against a candidate fix** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: the same class of bug returned three times in a week; each fix was tested on a hand-built shape. Recording tick inputs (engine list, event tail, process table) makes replay possible, and the real engine shapes are what slipped through.
  Done when: `sampo drive replay <ticks>` reproduces the T-2873 phantom hold on the old code and shows it cleared on the fix.

- **Wild: Run a second drive that audits the first** — FEATURE — value 4 — effort L — risk med — category: supervision — wild
  Why: assumption: a drive can't see its own blind spot. A tiny local-model sentry reads only the ledger and process table every 10 minutes and answers "should something be running?"; a mismatch wakes it.
  Done when: a seeded stall that the main drive ignores is flagged by the sentry within one interval.

- **Wild: Run a stall drill every night before the real work** — FEATURE — value 4 — effort M — risk low — category: unattended — wild
  Why: assumption: stalls are found at 3 a.m. otherwise. A scratch lane plants a phantom agent, a dead shell and a failing tool, and the drive must clear each before the night's plan is armed.
  Done when: the drill runs at arm time, the morning card shows "drill: 3/3 cleared", and a failure holds the night and says why.

- **Wild: Page the user by one glyph in the status line and phone push** — FEATURE — value 3 — effort S — risk low — category: notifications — wild
  Why: when the ladder is exhausted the user should learn it in one character, not by reading a log: ember lit (working), dim (waiting by design), cold (stopped, with cause).
  Done when: the glyph changes state within a tick of a stall record and a stalled drive sends one push, not repeats.

- **Write a night plan the drive grades itself against** — FEATURE — value 4 — effort M — risk low — category: unattended
  Why: "overnight progress" is the user's goal, and nothing yet says what progress was expected. A sealed list of task ids and rungs at bedtime, with the morning card showing planned versus done and stops by cause.
  Done when: the morning card prints "planned N, closed M, stalled K (causes)" from the sealed file.

- **Re-exec the drive at an idle tick after code lands** — FIX — value 3 — effort S — risk med — category: drive
  Why: the drive fixes (T-2873, T-2901) only take effect in a running drive once it restarts; a long-lived process keeps the old counting bug. Assumption: no restart on landing today.
  Done when: after a ship touching the drive module, the running drive restarts at its next idle tick and logs the new code hash.

Next question: Which of the 0.1 drive stops were real stops, and which were waits the metric miscounted, once causes are typed?
Next question: What does the user actually do in the first five minutes after a night where the drive stopped, and could the stall record have done it for them?
