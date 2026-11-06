# Brainstorm — lens: reliability

Lens: reliability. Focus is on self-triggering that must not misfire, go silent, double-fire or run unseen. Many round-1/2 ideas already cover heartbeats, replay, storm breakers and idempotency, so these go to second-order failure modes.

- **Fence the tick with a monotonic clock guard** — FIX — value 4 — effort S — risk low — category: scheduling
  Why: assumption: `fm night` tick compares wall-clock times; suspend, NTP step or DST makes a window fire twice or never. Round 2 listed DST checks but not backward clock steps.
  Done when: a test that steps the fake clock back 2h and forward 6h yields exactly one fire per due trigger and a logged "clock jump" line.

- **Make trigger state append-only with a compacting reader** — FEATURE — value 4 — effort M — risk med — category: state
  Why: the pack shows ordering fuzzing of task-state writes as an idea but not trigger state; a killed tick mid-write can corrupt last-fired times (assumption).
  Done when: killing the tick at every write boundary (kill test) leaves a readable table whose replayed state equals the pre-kill state or the post-write one, never a mix.

- **Reconcile installed units against the queued yes on every tick** — FIX — value 5 — effort S — risk low — category: installs
  Why: the mission says installs are queued for one yes; if the user edits or removes a unit by hand, Foreman's record disagrees with disk (assumption).
  Done when: deleting an installed timer file makes the next tick log "drift: unit missing" and re-queue it as a yes, never silently re-install.

- **Give every watcher a blind-detector** — FEATURE — value 5 — effort M — risk low — category: watchers
  Why: ci-watch settled 11 held bets in a row; a watcher that returns "nothing new" because auth expired or the API changed looks identical to a quiet repo.
  Done when: a watcher whose fetch returns 401, a schema it can't parse, or zero events for 3x its normal cadence records a "blind" status that `fm doctor` shows in red.

- **Classify fire failures as transient, permanent or poison** — FEATURE — value 4 — effort M — risk low — category: retries
  Why: a trigger that fails the same way forever burns budget; one that failed once because the network blinked must retry.
  Done when: a fixture trigger that fails with exit class "permanent" is parked after one try with a reason, and a "transient" one retries with backoff up to a cap.

- **Cap a fired lane's lifetime with a deadline and a process-group kill** — FIX — value 4 — effort S — risk low — category: lanes
  Why: unattended lanes with no user to notice a hung child; orphan reaping is a deferred idea, not shipped.
  Done when: a lane that sleeps forever is killed with its children at the deadline, and its trigger row records "deadline".

- **Verify the tick can run before it is allowed to arm anything** — FEATURE — value 4 — effort S — risk low — category: preflight
  Why: T-2532 made hooks fall back to the committed library; the tick has no equivalent self-test shown (assumption).
  Done when: arming a trigger runs a no-op fire through the real path and refuses to arm if it fails or exceeds a latency bound.

- **Detect a trigger firing on its own output** — FIX — value 4 — effort M — risk med — category: loops
  Why: a file trigger on the repo plus a lane that writes the repo is a loop; a CI watcher that files a fix whose push goes red again is another.
  Done when: a synthetic trigger whose action touches its own watched path fires once, then is held with "self-caused" and no second lane starts.

- **Wild: Run a shadow tick that recomputes what should have fired and diffs it** — FEATURE — value 4 — effort M — risk low — category: assurance
  Why: wild. Silence is the hardest failure; a second independent implementation reading the same table catches missed and doubled fires.
  Done when: seeding a bug that skips one due trigger makes the shadow report "missed: NAME" within one tick.

- **Wild: Inject chaos into the tick on a schedule** — FEATURE — value 3 — effort M — risk med — category: chaos
  Why: wild. Weekly in a scratch state dir, inject ENOSPC, a read-only state directory, a clock jump and a killed child, and assert the tick degrades visibly.
  Done when: the chaos run exits 0 only if each injected fault produced a named log line and no corrupt table.

- **Wild: Fire a canary event through the real path weekly and time it** — FEATURE — value 4 — effort S — risk low — category: liveness
  Why: wild. A planted fake event proves watcher, dispatcher, lane spawn and note delivery are all alive end to end, which a heartbeat alone doesn't.
  Done when: removing any one stage makes the next canary report which stage dropped it.

- **Pin the trigger table schema and refuse to fire on an unreadable one** — FIX — value 3 — effort S — risk low — category: compatibility
  Why: an older installed `fm` reading a newer table, or the reverse after a rollback, could misread cadence fields (assumption).
  Done when: a table with a future schema version makes the tick log "unreadable, not firing" and fire nothing.

- **Make a trigger's first fire a visible dry run unless the user opts out** — FEATURE — value 3 — effort S — risk low — category: safety
  Why: replay on history is covered, but a live first fire still can behave differently from the replay.
  Done when: a newly armed trigger's first fire files a task marked "dry" with the would-be action and does not run it.

Next question: Which of the 59 empty cells describe a surface where a trigger's failure would be invisible to the user, and what detector would turn each from silent to named?
Next question: What does the tick do when two machines share one state directory, such as a synced home, and who holds the lease?
