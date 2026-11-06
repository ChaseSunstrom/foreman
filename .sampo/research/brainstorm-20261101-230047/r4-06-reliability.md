# Brainstorm — lens: reliability

- **Fence the tick with a single-writer lease** — FIX — value 5 — effort M — risk med — category: trigger state
  Why: `fm night` already ticks from a user-installed timer, and Mission 4 adds more dispatchers (ci-watch, issue watch, file triggers); two overlapping ticks (a slow tick plus the next timer fire, or a session plus the timer) can double-fire a lane. Assumption: no lease exists today.
  Done when: a test starts two ticks concurrently on one state dir and exactly one fires the trigger; the other logs "lease held" and exits.

- **Derive idempotency keys from event identity** — FEATURE — value 5 — effort S — risk low — category: dedupe
  Why: CI runs, issues and commits have natural ids (run id, issue number+updated_at, sha). `fm ci-watch --last-ship` and the ship-bet settling show re-fire risk after a crash. Assumption: keys are not stored today.
  Done when: replaying the same recorded CI event twice, including across a kill between "fire" and "mark done", starts one lane.

- **Write a fire-intent row before acting, reconcile on tick start** — FIX — value 5 — effort M — risk med — category: crash safety
  Why: the pack's open reliability asks ("kill hooks at every write boundary", "fuzz the ordering of task-state writes") show crash boundaries are a known weak spot; a trigger that dies between spawning a lane and recording it either loses or duplicates work.
  Done when: a kill-at-each-boundary test (intent written, lane spawned, result recorded) leaves exactly one lane and one closed intent after the next tick.

- **Beat every timer from outside so silence is distinguishable from death** — FEATURE — value 5 — effort S — risk low — category: liveness
  Why: "the night tick logs only when something happens" (Measured now). A tick that has not run for three days looks identical to a quiet tick. Assumption: no heartbeat file exists.
  Done when: each tick touches a beat file; `fm doctor` reports "last tick 3d ago, expected 15m" red, with a test that fakes the old beat.

- **Verify the tick can run before it arms anything** — FIX — value 4 — effort S — risk low — category: preflight
  Why: T-2532 showed a working copy that fails to import silently disabled hook events; a timer unit pointing at a broken tree is the same failure, unattended. The unit runs from the committed library with a self-test.
  Done when: an install card refuses to arm when `fm night --selftest` fails, and a deliberately broken working copy still ticks from the committed library, logged.

- **Classify fire failures as transient, permanent or poison** — FEATURE — value 4 — effort M — risk low — category: retry policy
  Why: usage-limit pauses, rate limits and bad payloads need different handling; a poison event (an issue body that crashes the lane) must not retry forever. Assumption: current handling is uniform.
  Done when: tests show a rate-limit retries with backoff, a malformed event goes to a dead-letter list after 2 tries, and the digest names it.

- **Bound each fired lane with a deadline and process-group kill** — FIX — value 4 — effort S — risk med — category: runaway control
  Why: unattended lanes have no user to notice a hang; "reap orphaned child processes" and "cap lane memory" appear as unbuilt ideas. Assumption: no per-fire wall clock exists.
  Done when: a stub lane that sleeps forever is killed at its deadline along with its children, and the fire is recorded "timed out".

- **Reconcile queued installs against the live system every tick** — FIX — value 4 — effort M — risk med — category: install drift
  Why: Mission asks installs "queued for one yes". The yes can go stale: a unit edited by hand, deleted, or written for an older library version. Assumption: no diff of queued vs installed text.
  Done when: editing an installed unit file makes the next tick and `fm doctor` name the drift with a diff.

- **Make trigger state append-only with a compacting reader** — CLEAN — value 3 — effort M — risk low — category: state integrity
  Why: overlapping writers and kills corrupt rewrite-in-place JSON; an append-only log tolerates a torn last line.
  Done when: truncating the last line mid-record still loads every earlier record and the tick continues.

- **Refuse to fire on an unreadable trigger-table schema version** — FIX — value 3 — effort S — risk low — category: upgrade safety
  Why: the pack asks for "version goal files and test an N-1 reader"; a timer from an older install reading a newer table could misfire.
  Done when: a table with a future version makes the tick log "schema newer, not firing" and `fm doctor` flags it.

- **Wild: Chaos tick** — TEST — value 4 — effort M — risk low — category: fault injection
  Why: wild. A nightly test-only mode injects clock jumps, ENOSPC, a read-only state dir and a SIGKILL mid-fire, asserting no double fire, no lost event.
  Done when: the chaos run passes on the suite and fails when the lease from the first idea is removed.

- **Wild: Shadow tick that recomputes what should have fired** — FEATURE — value 4 — effort M — risk low — category: self-audit
  Why: wild. A second pure function replays the event log against the trigger table and diffs against what actually fired; a mismatch is a missed or phantom fire. Catches bugs no unit test imagines.
  Done when: deleting a fire record from a fixture makes the shadow report "missed: <event id>".

- **Wild: Weekly synthetic canary through the real chain** — FEATURE — value 4 — effort M — risk low — category: end-to-end liveness
  Why: wild. A harmless fake CI failure enters the same watcher, fires a dry-run lane and is timed end to end; it proves the watcher, dispatcher and lane path are alive when no real event has come.
  Done when: the canary appears in the digest with its latency, and disabling the watcher turns the canary red within a week.

- **Classify the clock: monotonic guard and DST test** — FIX — value 3 — effort S — risk low — category: time
  Why: schedules fire on wall-clock time; sleep, reboot, NTP jumps and DST can skip or double-fire. Assumption: no skewed-clock test exists (the pack lists it as an idea).
  Done when: the suite replays a spring-forward and a backward clock jump and each schedule fires exactly once.

Next question: Which triggers have actually fired in the user's installed `fm night` log, and what fraction produced work the user kept?
Next question: When two trigger families (CI watcher and issue watcher) report the same failure, which one owns the lane and who proves it?
