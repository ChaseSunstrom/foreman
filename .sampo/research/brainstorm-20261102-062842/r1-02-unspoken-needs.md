# Brainstorm — lens: unspoken needs

Answers to earlier questions my lens can reach:
- **First hour after an unattended mistake:** the user would look for what started it and a way to undo it. Neither has a single verb today.
- **Output acted on unchecked:** the morning or tick summary. Nothing outside Foreman verifies it.

- **Host the tick inside the running drive** — FEATURE — value 5 — effort M — risk low — category: self-triggering
  Why: the tower already runs continuously (the "advances itself" rule), yet the tick waits on a systemd install. A process that's alive can run `fm night`'s tick every N minutes. Assumption: the tick function can be called in-process.
  Done when: after a 3-hour drive with no timer installed, the tick ledger shows at least 6 ticks tagged host=drive, each graded by the same grader as timer ticks.

- **Grade the triggers already live** — FEATURE — value 5 — effort S — risk low — category: measurement
  Why: the sweep re-runs on task close, fix tasks are filed on a red sweep, the next Seed starts, and usage-limit waits resume. These are real event-driven self-starts with a week of history, but none is counted as trigger evidence.
  Done when: `fm night ticks --live` lists each of those starts with event, latency and outcome, and the trigger exam row counts them.

- **Measure the manual-world baseline first** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: "useful" has no yardstick. Before any tick exists, compute from git and the ledgers how long red CI, overdue deferrals, blocked tasks and inbox items sat before a human or session touched them.
  Done when: `fm night baseline` prints the median and p90 wait in hours for four classes over the last 30 days, and the trigger exam reports the tick's gain against them.

- **Settle shadow ticks against the user's own hand actions** — FEATURE — value 5 — effort M — risk low — category: grading
  Why: with no install, a shadow tick can still record "I would have started X". If the user later does X by hand, that's a hit and its lead time is how much sooner the tick would have acted. If nobody does, it's a false alarm. The user's own behavior is a signal Foreman didn't author (steer 3).
  Done when: a recorded shadow row closes as hit with a lead time after a matching manual `fm task new`, and as miss after 7 days with no match.

- **Seal the shadow week now and reconcile after the install** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: the gap is "a week of live ticks graded". Sealing today's shadow predictions means the first live week gets compared with them instead of starting from nothing. Assumption: shadow runs are deterministic enough to compare.
  Done when: a sealed file with a hash exists before install, and `fm night reconcile` prints a concordance percentage after one live week.

- **Run a scheduled tick on CI, off the user's machine** — FEATURE — value 4 — effort M — risk med — category: scheduler
  Why: the repo already has a GitHub Actions workflow (the tests badge). A cron workflow can run the free-arm tick (`--no-model`) daily and upload a ledger artifact. That's a real external scheduler needing no user install, shipped through `fm ship` and the existing push grant. Assumption: the tick works headless on a clean clone.
  Done when: 7 consecutive scheduled runs each upload a tick artifact that `fm night grade` accepts.

- **Refuse a "waits on the user" gap with no substitute measure** — CLEAN — value 4 — effort S — risk low — category: process
  Why: this Mission exists because a gap was recorded as waiting on an install. That contradicts "never block on the user". `fm genesis check` should reject a gap labelled user-dependent unless it names a no-user stand-in measure.
  Done when: a fixture gap saying "waits on the user's install" and naming no substitute fails the check, and passes once it names one.

- **Give the trigger exam a one-line-cron control arm** — FEATURE — value 4 — effort S — risk low — category: exam
  Why: plain Claude never self-starts, so it's a trivial baseline. The honest control is a cron line running `fm next`, and the tick must beat it on held-out timelines (steer 10, free arm vs session arm).
  Done when: `fm exam scorecard` prints the tick next to the cron arm, and a loss to cron is listed first.

- **Author the exam week blind** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: steer 3 requires scenarios from a separate tool-less child. That child writes a week-long event timeline (red CI, an issue, a limit pause, a quiet day) with expected responses, never seeing the code, and the oracle arm grades the tick on it.
  Done when: the timeline file's provenance records a child with no repo access, and per-event recall and precision appear in the exam line.

- **Differential-test the tick across hosts** — CLEAN — value 3 — effort S — risk low — category: reliability
  Why: once the tick can run from the drive, a session or a timer, different hosts could decide differently on the same state.
  Done when: the same fixture state run through each host yields identical decision lists, and a mismatch fails `fm doctor`.

- **Probe the scheduler with a 20-second transient timer** — FEATURE — value 3 — effort S — risk med — category: scheduler
  Why: today nobody knows whether this machine can run a timer, or whether linger is off, until the user installs. `systemd-run --user --on-active=20s` writes no unit file. Run it only on a granted probe, then clean up.
  Done when: `fm night probe` prints scheduler, linger and fired=yes/no within 60 seconds and leaves no unit behind.

- **Wild: cold-read the week's tick log** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: a tool-less child sees only the tick log and writes "what happened this week". Facts that don't match the ledger mean the log is unreadable to a stranger, which is the user's position at 7am.
  Done when: a fixture week scores at least 90% fact agreement and a deliberately garbled log scores lower.

- **Wild: rent a cloud tick** — FEATURE — value 3 — effort L — risk high — category: scheduler
  Why: T-0793 (deferred) points at cloud routines. Assumption: the host offers scheduled remote runs. A remote routine would run the free-arm tick against a repo bundle and return a ledger, reusing one existing path.
  Done when: one remote run's tick ledger imports through `fm night grade` with host=cloud.

- **Wild: ship the tick log as an orphan git branch** — FEATURE — value 2 — effort M — risk med — category: portability
  Why: tick rows committed to a `fm-ticks` ref travel with clones and CI. The graded week then survives a reboot, a tmpfs wipe or a second machine.
  Done when: a fresh clone's `fm night grade` reads the previous machine's ticks from the ref.

Next question: which Foreman starts already happen with no human present (sweep re-runs, drive resumes, limit waits), and which of them does no ledger yet count as a trigger?
Next question: if the tick were never installed, which of its promised outputs would the user still notice missing after a week, and by what signal?
