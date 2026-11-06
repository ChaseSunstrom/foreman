# Brainstorm — lens: reliability

Reliability lens, round 2. These avoid the ideas already listed and focus on how Foreman behaves when something around it misbehaves.

- **Make recovery the only startup path** — CLEAN — value 4 — effort M — risk med — category: crash-only
  Why: assumption: verbs and `fm run` have separate "normal start" and "after crash" code, and the second is rarely run. T-2668 (a guard hang) shows paths that only break under odd input.
  Done when: a test kills `fm run`, `fm ship` and `fm lane` at 20 random points; each restarts through the same entry function with no separate recovery branch, and `fm doctor` is green.

- **Number every ledger record with a sequence beside the wall clock** — FEATURE — value 4 — effort M — risk low — category: ordering
  Why: c12 (T-2632 era) routes windowed readers through one clock because wall-clock windows are fragile. Suspend, NTP steps and two machines can still misorder records.
  Done when: a test appends records across a faked backwards clock jump; readers order them by sequence, and `fm verify-ledger` names any gap or duplicate in the sequence.

- **Shuffle and duplicate recorded hook events into the session readers** — FIX — value 3 — effort S — risk low — category: reader robustness
  Why: assumption: readers such as `fm burden`, `fm outcomes` and the done-gate assume ordered, once-only events. T-2667 shows they already misread one delivery shape (`hook_success` stdout).
  Done when: a property test permutes and duplicates events from 5 real transcripts, and every reader gives the same totals or names the anomaly.

- **Bind a guard verdict to the command's hash and check it afterwards** — SECURITY — value 4 — effort M — risk med — category: guard integrity
  Why: assumption: the guard judges the command at PreToolUse. Nothing re-checks that what ran matches what was judged, for example after a hook-input rewrite or a symlink swap between check and exec.
  Done when: a fixture where the executed command differs from the judged one is flagged by PostToolUse, and `fm doctor` counts mismatches.

- **Give every outward call an idempotency class** — CLEAN — value 4 — effort M — risk low — category: retries
  Why: `fm ship`, publish and `fm genesis live` push outward, and the retry/queue ideas elsewhere in the list assume safe replay. Assumption: no single place records which calls are safe to retry.
  Done when: each outward call site declares safe, keyed or never-retry. A lint fails on an undeclared call, and a test replays each call twice against a fake remote with at most one effect.

- **Hold a sleep inhibitor across critical sections** — FEATURE — value 3 — effort S — risk low — category: device power
  Why: the drive is unattended on a laptop-class machine. Suspend mid-ledger-rewrite or mid-push is the likeliest uncontrolled interruption. Assumption: no inhibitor is taken today.
  Done when: `fm ship` and ledger rewrites run under `systemd-inhibit` (or are skipped with a recorded reason when it is absent), and a test shows the inhibitor present during the section.

- **Attribute a killed child to OOM, cgroup limit or signal** — FEATURE — value 3 — effort M — risk low — category: diagnosability
  Why: lanes, provers and `fm code` tools can die with no cause shown, and the receipt then shows only a stall. Assumption: only the exit status is recorded.
  Done when: a child killed by a cgroup memory limit in a test is recorded as `oom` with the limit, and the task receipt says so.

- **Assign stable error codes and keep a failure census** — FEATURE — value 3 — effort M — risk low — category: diagnosability
  Why: refusals and warnings are free text, so classes can't be counted across weeks. This is a different thing from "every exception maps to an exit code".
  Done when: every `die()` and refusal carries an `FM-E####` code resolvable via `fm why`, and `fm doctor --codes` prints 30-day counts per code.

- **Warn before credentials expire** — FEATURE — value 3 — effort S — risk low — category: unattended
  Why: the drive pushes and calls models unattended. A lapsed `gh` login, Claude login or push grant stops it at the worst moment. Preflight checks exist, but a forecast does not.
  Done when: `fm doctor` and the drive's start receipt show days left for each credential. Any expiring before the planned run end stops the run with a named reason.

- **Run the suite under `-X dev -W error` once a night** — PERFORMANCE — value 3 — effort S — risk low — category: latent faults
  Why: assumption: unclosed files, leaked fds and deprecation hits never fail the normal suite, and long-running drive processes are where they accumulate.
  Done when: the nightly job lists new ResourceWarnings or fd growth per test file, and a planted leak makes it fail.

- **Detect a second live session on the same repo** — FEATURE — value 3 — effort M — risk low — category: concurrency
  Why: the user opens several terminals and lanes run in parallel. Claim heartbeats cover tasks, but not two sessions editing the same files outside a lane.
  Done when: a session start or edit that touches a file under another live session's claimed task prints the other session id and task, and a test with two fake sessions proves it.

- **(wild) Double-fire canary** — SECURITY — value 3 — effort S — risk low — category: determinism
  Why: wild. Run 1 in 200 hook calls twice in a throwaway process and compare decisions. Any difference exposes hidden state, clock use or hash-order dependence in the guard.
  Done when: a hook with a planted time-dependent branch is flagged within 1,000 calls, and a clean hook never flags.

- **(wild) Auto-stress and shrink every flaky test** — FEATURE — value 3 — effort M — risk low — category: flakes
  Why: wild. When a test lands in `flakes.json` (T-2657), rerun it 50 times under CPU stress and a shifted clock, then record which condition flips it.
  Done when: a planted order- or time-dependent test is recorded with its cause (stress, clock or order), and `fm doctor` shows that cause beside the fail rate.

- **(wild) Prognosis letter scored against what happens** — FEATURE — value 3 — effort M — risk low — category: prediction
  Why: wild. A tool-less child reads `fm doctor` output and the ledger tails (hook p95, ledger size, disk, quota, error codes) and predicts which fault is likeliest this week. Later records settle it.
  Done when: each prediction is stored with a sealed time, settled at 7 days, and a running hit rate against a "nothing happens" baseline is shown.

Next question: which of Foreman's own failures did the user find out about from something other than Foreman, and how long after they happened?
Next question: what is the longest interval an unattended path can be broken before any surface the user looks at shows it?
