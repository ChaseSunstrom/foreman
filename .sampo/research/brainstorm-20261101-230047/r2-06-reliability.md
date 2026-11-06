# Brainstorm — lens: reliability

Lens: reliability, Mission 4 (#11 Self-triggering). Every idea below is about whether triggers keep working, fire once, and fail visibly. None repeats the ideas-so-far list (heartbeats, catch-up, replay, dry-run, storm breakers are already there), so these go to second-order failure modes.

- **Fence trigger state with a single-writer lease and fencing token** — FIX — value 5 — effort M — risk med — category: concurrency
  Why: assumption: the night tick, a live session and a lane can all reach the trigger table. A stale lease holder after a suspend or a slow tick could fire twice or overwrite a newer state.
  Done when: a test runs two tick processes against one table, pauses one past lease expiry, and shows its late write is rejected with a logged fence mismatch.

- **Write a fire-intent row before acting and reconcile on startup** — FEATURE — value 5 — effort M — risk low — category: durability
  Why: assumption: a kill between "decided to fire" and "lane started" is unrecorded (existing ideas cover kill-at-boundary tests, not the intent/outcome pair). T-2525-style premise bugs show how such gaps hide.
  Done when: killing the tick at each of three points leaves an intent row that the next tick resolves to exactly one of started, abandoned or retried, and a test asserts no duplicate lane.

- **Derive idempotency keys from the event's identity, not its time** — FIX — value 4 — effort S — risk low — category: dedupe
  Why: assumption: CI and issue watchers re-deliver (a re-run, an edited issue, a force-push). A time-bucket key either misses duplicates or drops real new events.
  Done when: replaying the same CI run id three times, and an edited issue body, each yield one lane; a force-pushed new SHA yields a new one.

- **Pin the trigger table to a schema version and refuse to fire on an unreadable one** — FIX — value 4 — effort S — risk low — category: compatibility
  Why: the pack's lessons show state-format drift (older `fm` reading newer files); assumption: timers run the installed `fm`, which can lag the working copy.
  Done when: a table written at version N+1 makes the tick log "refusing: newer schema" and fire nothing, and `fm doctor` names it.

- **Run the tick from the committed library with a self-test before it may spawn work** — FEATURE — value 4 — effort M — risk med — category: boot safety
  Why: T-2532 made hooks fall back to the committed library when the working copy fails to import; the unattended tick has no human to notice the same failure.
  Done when: breaking an import in the working copy leaves the tick running from the committed code, logged with its reason, and a self-test failure suppresses all fires.

- **Make a silent tick distinguishable from a dead one with an external beat check** — FEATURE — value 5 — effort M — risk low — category: liveness
  Why: the pack says the night tick "logs only when something happens", so quiet and dead look identical (the guard-alive question has the same shape).
  Done when: `fm doctor` reports last beat age from a file the tick touches each run, red past 2 intervals, and a stopped timer turns it red in a test.

- **Classify each fire failure as transient, permanent or poison and back off accordingly** — FEATURE — value 4 — effort M — risk low — category: retry
  Why: assumption: a failing trigger retried every tick burns budget (usage limit, bad config, deleted branch). The pack's "retry storm" idea has no taxonomy.
  Done when: a permanent failure disables its trigger after one try with a reason, a transient one backs off exponentially with jitter, and both are shown in the trigger inventory.

- **Bound a trigger's lifetime with a per-run deadline and a process-group kill** — FIX — value 4 — effort S — risk low — category: resource
  Why: assumption: an unattended lane that hangs holds the lease and blocks every later fire.
  Done when: a lane stub that sleeps past its deadline is killed with its children, the lease is released, and the next tick fires normally.

- **Reconcile queued installs against the live system on every tick** — FEATURE — value 3 — effort M — risk low — category: drift
  Why: the request says installs are queued for one yes; once approved, a timer file can be deleted, edited or masked by the user and nothing notices.
  Done when: deleting an approved unit makes the next tick report "installed but missing" and re-queue it for a yes, without re-installing silently.

- **Wild: Run a chaos tick that injects clock jumps, ENOSPC and a read-only state dir** — FEATURE — value 4 — effort M — risk low — category: fault injection
  Why: wild; assumption: real failures (a suspended laptop, a full tmpfs under `/run/user`) are rarer than tests, so nobody has seen them.
  Done when: a nightly test run in a scratch copy shows each injected fault yields a logged degraded mode and zero duplicate or lost fires.

- **Wild: Keep a shadow tick that recomputes what should have fired and diffs it** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: wild; the pack's rule that signals Foreman didn't author count most suggests an independent recomputation from the raw event log, not the table's own record.
  Done when: a planted missed fire is caught by the shadow diff within one day and appears in `fm doctor` as a named discrepancy.

- **Wild: Fire a synthetic canary through the real path weekly and time it end to end** — FEATURE — value 3 — effort M — risk low — category: liveness
  Why: wild; a trigger that is installed and quiet proves nothing, and the existing idea of a planted event is a drill, not a measured latency.
  Done when: the canary produces a task tagged as synthetic that auto-closes, and its fire-to-start latency is logged; a missing canary goes red.

Next question: which trigger failure would the user only discover by noticing absent work days later, and what is the cheapest independent signal of that absence?
Next question: what happens to every trigger and queued install when `fm` itself is upgraded, rolled back or moved between the user's machines?
