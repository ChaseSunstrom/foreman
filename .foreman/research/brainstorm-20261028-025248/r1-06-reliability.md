# Brainstorm — lens: reliability

- **Fence the gate lock with a token** — FIX — value 5 — effort M — risk med — category: lock safety
  Why: a full check waited 40+ minutes on a hung holder in another project (pack evidence). A holder that wakes after takeover can still write, so a stale lock can corrupt state.
  Done when: a test SIGSTOPs the holder, takes over the lock, resumes the old holder, and its write is rejected because its token is older than the current one.

- **Identify lock holders by PID and process start time** — FIX — value 4 — effort S — risk low — category: lock liveness
  Why: a dead holder whose PID was reused looks alive, so waiters stall. Assumption: the lock stores only a PID today.
  Done when: a test reuses a PID with a different start time and the lock is reclaimed without waiting.

- **Run each gate against a frozen snapshot of the tree** — FEATURE — value 5 — effort M — risk med — category: verdict integrity
  Why: an edit made during a check means the green verdict describes a tree that no longer exists. "Bind each proof to its diff" covers the close step, not the run itself.
  Done when: an edit during a gate run leaves the verdict unchanged, and the verdict records the snapshot hash it tested.

- **Judge stalls by transcript growth, not elapsed time** — FEATURE — value 4 — effort M — risk low — category: stall detection
  Why: run.py kills a class at a fixed 480 s, which also kills a slow but working build. Assumption: the transcript and output files grow while a run is alive.
  Done when: a run that keeps producing output for 10 minutes is not flagged, and one silent for 5 minutes is flagged with its last event.

- **Give every run a global retry budget** — FEATURE — value 4 — effort S — risk low — category: retry storms
  Why: each call backs off on its own, so parallel lanes can multiply retries during an API outage. Assumption: no run-wide cap exists.
  Done when: a simulated outage stops the run after its retry budget is spent and names the step that gave up.

- **Probe every hook at install and fail loudly without a journal line** — FIX — value 4 — effort S — risk low — category: install health
  Why: `fm quiet` ran with no stdin and reported exit 0 while doing nothing (pack evidence). Hooks can fail the same silent way.
  Done when: `fm install` sends a probe through each hook, and install fails if no journal entry appears within 2 seconds.

- **Inject write failures at the file seam in the test suite** — CLEAN — value 4 — effort M — risk low — category: fault testing
  Why: writes are atomic by design, but no test covers ENOSPC or EIO partway through. Assumption: the suite only tests success paths for state writes.
  Done when: the suite fails the Nth write in each state-file path and confirms the last good copy survives.

- **Tag each test with the environment it needs and refuse to run it elsewhere** — CLEAN — value 3 — effort M — risk low — category: test hermeticity
  Why: a crash test broke on Ubuntu 26's copied `sleep`, and browser tests crashed under parallel CI load. Tests fail by environment, not by code.
  Done when: each test declares its needs, and running one without them reports a skip with the missing requirement.

- **Use a monotonic clock for every deadline in the state machine** — FIX — value 3 — effort S — risk low — category: time safety
  Why: `defer --until` fired at midnight, two hours early, because it read local time. Wall-clock jumps can break other deadlines the same way.
  Done when: a test moves the wall clock back an hour mid-wait and the deadline still fires on schedule.

- **Wild: write a last-words note from every dying run** — FEATURE — value 4 — effort S — risk low — category: crash forensics
  Why: when a run dies, its final state is lost unless a surface happens to be watching. Assumption: signal handlers can write a small note before exit.
  Done when: killing a run with SIGTERM leaves a note that `fm why <id>` shows, with the last step and the held locks.

- **Wild: keep a crash corpus that every release must survive** — FEATURE — value 4 — effort M — risk low — category: regression memory
  Why: each fixed crash is a bug that can return silently. Closed-task replay exists, but nothing stores the crashing inputs themselves.
  Done when: each fixed crash adds a replayable case, and a release is blocked if any stored case reproduces its failure.

- **Wild: skew the wall clock mid-run in a chaos test** — CLEAN — value 3 — effort S — risk low — category: chaos testing
  Why: fake clocks cover fixed times, not jumps during a run. Assumption: a clock step is the realistic failure after sleep or NTP correction.
  Done when: a chaos run steps the clock forward and back by an hour and every run finishes with a correct state and no duplicate actions.
