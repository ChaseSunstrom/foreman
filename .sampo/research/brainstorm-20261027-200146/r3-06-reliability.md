# Brainstorm — lens: reliability

- **Pause a queue after the same gate fails twice** — FEATURE — value 4 — effort S — risk low — category: queue safety
  Why: a queue that repeats a failing gate burns usage and hides the cause. The pack shows gate failures that stalled runs and a gate lock held for over 40 minutes.
  Done when: a queue with two consecutive identical gate failures stops before the third attempt and prints the failing gate and its last output.

- **Give every hook a declared fail-open or fail-closed policy** — FIX — value 5 — effort S — risk med — category: hook safety
  Why: the guard hook must fail closed, while telemetry and the usage counter should fail open. The pack has no per-hook policy, and the bench shows hook latency already causing trouble under load (PreToolUse:Bash:script p95 ~310 ms against a 300 ms budget).
  Done when: each hook's manifest names its policy, and a test kills each hook and checks that the guard still blocks a dangerous command while telemetry still lets the tool call proceed.

- **Measure every wait with a monotonic clock, not wall time** — FIX — value 4 — effort S — risk low — category: timing
  Why: the defer-until bug fired at midnight instead of the 02:00 reset because it used wall-clock comparisons. The gate-lock wait and stall timers have the same exposure to clock jumps and DST.
  Done when: a test sets the wall clock back an hour during a gate wait, and the wait still ends at its monotonic deadline.

- **Share one deadline across a run's nested waits** — FIX — value 4 — effort M — risk med — category: timeouts
  Why: a full check can wait on the gate lock and then run its steps, each with its own timeout, so the total can exceed what the user expects. The pack shows a 15-minute gate wait stacking on top of check runtime.
  Done when: a run given a 20-minute budget with a 15-minute lock wait finishes or fails by minute 20 at the latest, and its receipt lists how the time was split.

- **Checksum every state file and fall back to the last good copy on mismatch** — FIX — value 4 — effort M — risk med — category: state integrity
  Why: a torn or edited backlog or journal stops `fm status` working. Atomic writes are already on the list, but nothing detects damage that happens after the write.
  Done when: a test corrupts the backlog's last byte, and `fm status` loads the previous copy, reports the recovery, and does not crash.

- **Make `fm task finish` idempotent after a crash** — FIX — value 4 — effort S — risk low — category: task close
  Why: a retried close can re-run follow-up capture and duplicate tasks. The pack already shows follow-up capture misfiring on "new playbook" and "n/a" entries, so it's not reliable when re-run.
  Done when: running `fm task finish` twice on the same task creates no second follow-up and leaves the first receipt unchanged.

- **Assign help positions from one generated registry** — CLEAN — value 3 — effort S — risk low — category: command registry
  Why: `fm dojo` and another command share help position 306, which fails `test_help`. Positions are hand-assigned, so collisions will keep happening.
  Done when: the build fails if two commands share a help position, and `fm help` lists every command once with a unique position.

- **Version the journal schema and migrate in-flight runs** — FEATURE — value 3 — effort M — risk med — category: upgrade safety
  Why: an upgrade that changes the journal layout can strand a run that was halfway through. The pack shows a broken test fixture (test_followups reading a split row) that is the same kind of format drift.
  Done when: a journal written by the previous schema version is read, migrated, and resumed in a test, and an unknown future version is refused with a clear message.

- **Preflight local resources before a queue starts** — FEATURE — value 4 — effort S — risk low — category: preflight
  Why: a queue that starts with a read-only state directory, no free disk, or a dead git lock fails after the model has already spent tokens. The pack shows the gate lock and state files are shared across projects.
  Done when: `fm run` with the state directory made read-only refuses before the first model call and names the path that failed.

- **Wild: seed a known-bad change nightly and distrust a gate that passes it** — FEATURE — value 5 — effort M — risk low — category: gate trust
  Why: a gate that stops failing is worse than no gate, and nothing in the pack checks that the gates still catch a real break. Assumption: a fixed, known-bad fixture in a throwaway clone is enough to prove the gate still bites.
  Done when: a nightly job applies the seeded break in a clean clone, and if `fm check` passes, the next `fm status` shows the gate as untrusted until a fresh run fails on the same break.

- **Wild: a dead-man's switch that halts the queue when no surface is watching** — FEATURE — value 3 — effort M — risk med — category: unattended safety
  Why: unattended queues run for hours while the user is away, and a hung TUI or a closed terminal leaves them in an unknown state. Assumption: a heartbeat written by the TUI and read by the queue is a cheap way to detect that the operator has gone.
  Done when: with the TUI killed and no heartbeat for five minutes, the queue stops at its next task boundary and writes a receipt that says it stopped because the operator was gone.

- **Wild: one-command rollback for every rules-file edit** — FEATURE — value 3 — effort S — risk low — category: rules safety
  Why: the rules file is trimmed and edited often, and a bad edit affects every run. The pack shows the file over budget and a dream pass proposed for future edits, so each change needs a way back.
  Done when: `fm rules undo` restores the previous rules file byte-for-byte, and a test edits the file, undoes it, and compares hashes.
