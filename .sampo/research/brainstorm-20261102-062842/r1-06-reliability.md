# Brainstorm — lens: reliability

- **Prove the tick under a real systemd with a transient timer** — FEATURE — value 5 — effort M — risk low — category: self-trigger proof
  Why: the week of live ticks waits on the user's install, but `systemd-run --user --on-active=5s` (or a `--scope` run) executes the real tick body in systemd's stripped environment (minimal PATH, no TTY, no shell rc) without installing any unit. That grades what the install would do. Assumption: user systemd is available on this host (Linux, per the pack).
  Done when: `fm night prove` runs the tick via a transient unit, exits 0, and records one tick row with `source=transient`, `exit`, `duration` and the PATH it saw; a deliberately broken PATH fixture makes it fail with the missing binary named.

- **Verify the rendered unit text without installing it** — FEATURE — value 4 — effort S — risk low — category: install check
  Why: the install card shows exact unit text, but nothing checks it. `systemd-analyze --user verify` plus `systemd-analyze calendar` give a syntax check and the next five elapse times, which show the cadence the user would get. Assumption: `systemd-analyze` is on PATH.
  Done when: a test renders each unit, runs verify, and fails on a planted bad `ExecStart`; `fm doctor` prints the next elapse time from the rendered text.

- **Measure staleness at session start as the no-install baseline** — FEATURE — value 5 — effort S — risk low — category: measurement
  Why: with no timer, the honest question is how long the oldest actionable item sat before any session touched it. SessionStart can record the age of the oldest unsettled bet, unscored outcome and due deferral. That is a measurable self-triggering score from live use, with no wait for the exam. Assumption: those items carry timestamps.
  Done when: each session start appends `{oldest_age_s, kind}` to a ledger, and `fm night report` prints the median and p95 for the last 14 days.

- **Run a compressed-week soak with an injected clock** — PERFORMANCE — value 5 — effort M — risk low — category: soak test
  Why: a week of ticks can be simulated in minutes on fixture state with a fake clock (10,080 one-minute ticks). The grade is slopes, not pass/fail: state-dir growth, open fds, leftover tmp dirs, ledger size and duplicate fires per tick.
  Done when: `python3 plugin/tests/soak_tick.py --ticks 10080` finishes in under 5 minutes, prints each slope, and fails if any slope is above zero by a set bound; a planted fd leak fails it.

- **Isolate tick steps with a timeout and one outcome enum each** — FIX — value 4 — effort M — risk med — category: fault isolation
  Why: assumption: the tick runs its steps in sequence, so one corrupt task file or one hung step would stop the later ones. Each step (settle bets, digest, ci-watch, maintain) should run in its own try block and time box, with an outcome of `ok`, `skipped`, `failed` or `timeout`.
  Done when: a test that corrupts one step's input still sees the other steps `ok`, and the tick row lists a per-step outcome and duration.

- **Prove a double tick is a no-op, and recover stale locks by PID and start time** — FIX — value 4 — effort S — risk low — category: concurrency
  Why: assumption: a session-piggyback tick and a timer tick can overlap. A lock left by a `kill -9`'d tick must not block ticks forever, and a recycled PID must not be mistaken for a live one.
  Done when: running two ticks concurrently makes exactly one do work; a lock owned by a dead PID, and one with a mismatched start time, are both reclaimed, each in its own test.

- **Add a session-piggyback tick that is graded like the timer's** — FEATURE — value 4 — effort M — risk med — category: no-install fallback
  Why: the earlier "prompt-time tick" idea was wild and unmeasured. Go further: at SessionStart, if the last tick is older than the interval, run only the cheap safe steps under a 2-second budget, tagged `source=session`. The same grader then covers both paths.
  Done when: with no timer, `fm night report` shows `source=session` ticks and the hook p95 bench stays under its existing budget (`bench_hooks.py --runs 20`).

- **Bound the tick ledger and read it tolerantly** — FIX — value 3 — effort S — risk low — category: durability
  Why: assumption: beats and tick rows are append-only and unbounded, and a kill mid-append leaves a torn last line. The reader should skip torn lines, and the ledger should rotate at a size cap.
  Done when: a test truncates the last line mid-record and the report still reads every other row; a ledger over the cap rotates and keeps the newest N rows.

- **Alert when tick duration approaches its interval** — PERFORMANCE — value 3 — effort S — risk low — category: capacity
  Why: assumption: a tick that takes more than about half its interval will eventually overlap with the next one, and nothing reports duration against interval. Doctor should show p95 duration as a share of the interval.
  Done when: `fm doctor` prints `tick p95 4s / 15m` and WARNs above 50%; a synthetic slow step trips the WARN.

- **Show the cost of not installing in one doctor line** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: users skip the install because nothing tells them what they're missing. From the ledger, doctor can say "no tick for 3d; 4 bets unsettled, 2 deferrals due". This is the product-side companion to the staleness metric.
  Done when: with the tick absent, doctor prints that line with real counts; with a fresh tick it prints nothing.

- **Wild: run the tick confined to the state dir and prove it writes nowhere else** — SECURITY — value 3 — effort M — risk med — category: confinement
  Why: wild. A bwrap (or landlock) run with everything read-only except the state dir turns "the unattended tick can't touch your repo" from a claim into a test, and any stray write becomes a failing diff. Assumption: bwrap is installable on this hardened kernel.
  Done when: the tick runs under bwrap with the repo mounted read-only and exits 0; a planted write to the repo makes the confined run fail.

- **Wild: hash-chain tick receipts so a missing tick is provable after the fact** — FEATURE — value 3 — effort S — risk low — category: tamper-evidence
  Why: wild. Each tick row carries the hash of the previous row and a monotonic counter. A reboot gap, a deleted row and a silent stop then look different, and the report can say which.
  Done when: removing a middle row makes `fm night verify` report a chain break at that counter; a clean ledger verifies.

- **Wild: shuffle input order every run and require identical outcomes** — FIX — value 3 — effort S — risk low — category: determinism
  Why: wild. Shuffling the order of tasks, bets and events (seeded) before each soak tick catches ordering bugs, the same class as the `hash % len` selection issue the pack already hit with exam items.
  Done when: the soak runs with 5 different seeds and all produce the same set of fires and settlements; a planted order-dependent step fails it.

Next question: which tick step has never failed in a recorded run, and is that because it is robust or because nothing exercises its failure path?
Next question: if the user never installs the timer, what is the smallest in-session behaviour that would make them notice a missed tick on their own?
