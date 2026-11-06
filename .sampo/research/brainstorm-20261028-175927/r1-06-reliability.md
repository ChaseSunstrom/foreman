# Brainstorm — lens: reliability

- **Fail any fm command that exits 0 having done nothing** — FIX — value 5 — effort M — risk med — category: honesty
  Why: the first "asked" item: `fm quiet` ran a heredoc script with no stdin and reported exit 0. The same shape (a verb succeeds while doing nothing) is likely elsewhere, e.g. `fm task defer`, `fm edit` with a no-op block.
  Done when: a test table of verbs given empty/no-op input shows each exits non-zero with one sentence naming what was skipped, and `fm quiet` with a heredoc reads the script or refuses.

- **Pin every hook to a declared fail-open or fail-closed policy, tested by injected faults** — FEATURE — value 5 — effort M — risk med — category: hooks
  Why: the guard hook is the product's safety claim, and the user's bypass mode depends on it. The pack shows "risk budget tripped" from guard collisions, but nothing says what happens when the hook itself crashes, times out or reads a corrupt rules file. Assumption: policy is implicit today.
  Done when: a fault-injection test (corrupt rules, timeout, missing interpreter) shows the guard denies destructive-looking commands and allows read-only ones, and each hook's policy is listed in `fm doctor`.

- **Reap a dead run's edit leases, gate lock and children together** — FIX — value 5 — effort M — risk med — category: recovery
  Why: the user's recurring complaints are the 20-minute edit-lease timer, the machine-wide gate lock blocking `--affected` checks, and a zombie in the crash-hygiene tests. All share one cause: ownership is time-based, not liveness-based.
  Done when: `kill -9` on a run frees its leases and lock within 5 s (test), and the lock file records PID plus process start time so PID reuse can't hold it.

- **Make a gate that ran zero tests fail** — FIX — value 4 — effort S — risk low — category: proof
  Why: the product's claim is "prove its work with commands it actually ran". `fm quiet` exiting 0 on nothing shows empty runs can look like proof. Assumption: gates are judged on exit code alone.
  Done when: a gate whose output reports 0 tests collected (pytest "no tests ran", empty glob) is recorded as `unable`, not `pass`, with a test.

- **Make state writes crash-proof with checksums and last-good fallback** — FIX — value 4 — effort M — risk med — category: state
  Why: the pack notes `set_panic` already uses write_atomic, but backlog, journal and the task ledger are not shown to share it, and `fm drill` covers detectors, not torn writes. Assumption: not every state file is atomic.
  Done when: a lint test fails on any state-file write not going through write_atomic, and a kill-at-every-write test leaves the ledger readable or restored from the previous copy.

- **Classify CI failures by cause before filing a task** — FIX — value 4 — effort M — risk low — category: CI
  Why: asked items show chromium crashing under parallel load, a 20-minute job cap hiding a hang, a flaky hook bench, and a macOS job able to cancel main's tests. Each looked like a real failure first.
  Done when: a CI-failure intake labels runs as timeout / cancelled / infra-crash / real test failure, reruns the first three once, and only files a task for a repeat or a real failure.

- **Refuse a queue that cannot finish before the usage reset** — FEATURE — value 4 — effort M — risk low — category: budget
  Why: the user said Foreman should have noticed its own usage burn without being told; `defer --until reset` exists but nothing predicts the queue's cost against the reset clock.
  Done when: `fm run` prints the projected cost versus remaining headroom and, if it will not fit, starts only the tasks that do and parks the rest with the reset time.

- **Make the hook bench a median-with-load verdict** — FIX — value 3 — effort S — risk low — category: tests
  Why: the user already had `FOREMAN_DOCTOR_BENCH` skipping the bench in release-check because it was flaky under parallel load; a skip hides regressions.
  Done when: the bench records the machine load average, reports median over N runs, and fails only if the median exceeds budget at low load; the skip flag is removed.

- **Rehearse crash recovery nightly on the user's own finished runs** — FEATURE — value 3 — effort M — risk low — category: recovery
  Why: `fm drill` exercises detectors only. Journaled resume is claimed but not rehearsed on real data. Assumption: resume has no scheduled check.
  Done when: a scheduled job kills a copied run at a random journal point, resumes it, and diffs the final state against the original; a mismatch files a task.

- **Wild: Plant a seeded known-bad change nightly and distrust a gate that passes it** — FEATURE — value 4 — effort M — risk low — category: gates
  Why: the "fails closed" claim is only as good as the gates; mutation-testing the gate itself is untested in the pack. Assumption: gates are trusted when green. Wild.
  Done when: a nightly job applies a known-bad patch in a scratch clone and fails loudly, filing a task, if `fm check` stays green.

- **Wild: Keep a last-known-good Foreman install that boots when the new one fails its first gates** — FEATURE — value 4 — effort L — risk med — category: install
  Why: the release path covers plugin, CLI, desktop and mod, and version skew is a known risk (installed foreman-ui is behind, T-0418). A bad update on an unattended run has no way back. Wild.
  Done when: after an update, the first three gates failing causes automatic rollback to the previous copy and one line in session start saying so.

- **Wild: Write a "last words" note from every dying run** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: stalled and dead runs are explained by the user's `fm code why` asks, but a SIGKILL leaves nothing. A sidecar written on each journal step (current step, open leases, last command) survives it. Wild.
  Done when: after `kill -9`, `fm code why <id>` names the last step, last command and which leases were held, from the sidecar alone.

- **Reconcile backlog against journal at session start and list drift** — FEATURE — value 3 — effort M — risk low — category: state
  Why: the pack shows closed tasks still referenced (the session-start CI line pointed at a closed task) and a large deferred pile. Two stores with no cross-check will drift.
  Done when: session start prints one line per mismatch (task closed in journal but open in backlog, or the reverse) with the fix command, and prints nothing when consistent.

- **Make a rerun that passes a flake entry, then quarantine on repeat** — FEATURE — value 3 — effort M — risk low — category: tests
  Why: crash-hygiene fake git, chromium crashes and load-sensitive benches all came up as intermittent; nothing records reruns that flipped result.
  Done when: a flake ledger records each test that failed then passed on rerun, and a test that flips three times in 30 days is quarantined with a filed task rather than blocking main.
