# Brainstorm — lens: deepen: measurement

- **Build a tick tape and replay harness with a virtual clock** — FEATURE — value 5 — effort L — risk med — category: measurement
  Why: the week of live ticks waits on the user's install; the existing ledgers (dropped, outcomes, dated deferrals, git, CI timestamps) already hold a recorded week. Merges "replay a recorded week", "tick as pure function with injected clock" and "key tapes by patch-id".
  Done when: `fm tick replay --tape <week>` runs the real dispatcher against a virtual clock with no timer or network, and two runs on one tape give byte-identical fire lists.

- **Hold out a share of fires as a causal control and report the lift** — FEATURE — value 5 — effort M — risk med — category: measurement
  Why: assumption: a fire count says nothing on whether the tick helped. Combines "hold out one in five", "null-tick arm" and "randomise across repos". Held-out fires are logged as would-have-fired and later compared on time-to-notice and time-to-close.
  Done when: with `--holdout 0.2` about a fifth of fires are logged but not delivered, and `fm tick grade` prints median lateness for delivered against held-out with an n and an interval.

- **Grade the tick with one sentence a day and a power gate** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the user acts on outputs without outside checks (earlier question) and wants no new dashboards. Merges the "one sentence per day" idea with "gate on statistical power" and "sequential test naming missing evidence".
  Done when: the digest holds one line such as "tick: 6 fires, 4 acted on; need 14 more fires to call useful", and `fm tick grade` refuses a verdict below the stated sample size.

- **Pin every grade to its clock class and refuse pooled numbers** — FIX — value 4 — effort S — risk low — category: measurement
  Why: replayed, session-borne, edge (Stop/SessionEnd) and real timer ticks differ in kind. A pooled hit rate would be quietly wrong, the same fault the CHANGELOG-baselines steer (T-2591) was filed for.
  Done when: each tick grade row carries a clock class, and the grade command prints a separate row per class and fails on a request to pool them.

- **Settle every self-filed task by line survival and the dropped ledger** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the pack's own ledgers list tasks the user dropped, such as the gen-2 review items and the sweep red. Retro-grading each self-filed task as kept, dropped or dismissed gives a precision for self-triggering with no install. Add git line survival for kept ones.
  Done when: `fm tick grade --retro` prints precision per source (ci, self, discovered) from existing ledgers, with a count for each.

- **Seed the grader with planted mutants and calibrate the cold judge** — TEST (FIX) — value 4 — effort M — risk low — category: measurement
  Why: the cold-read rule says a FAIL only counts when it quotes a line. Plant known-good and known-bad tick outputs, measure the grader's miss and false-alarm rates, and publish them next to each grade. Replaces "grade the tick's grader with mutants".
  Done when: a planted set of 20 labelled tick outputs gives a stored grader accuracy, and any tick grade without a fresh calibration is flagged "uncalibrated".

- **Backtest the finders on the parent of every past FIX commit** — FEATURE — value 4 — effort L — risk med — category: measurement
  Why: this gives recall for fm find and the tick's detectors from history, a signal Foreman didn't author (steer), and it needs no live week. Report per language and bug type, as the standing #1 rule requires.
  Done when: `fm tick backtest` checks out each FIX parent in a scratch worktree and prints detection rate per language and bug type over at least 30 commits.

- **Report backlog age and time-to-notice per job with a freshness SLO** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: assumption: fire counts reward noise, while age rewards timeliness. Backfill from dated deferrals (30 "later: needs…" items) and give each job (night, sweep, maintain) an SLO whose burn shows in fm doctor.
  Done when: fm doctor lists each tick job's oldest unserved item and SLO burn, and a seeded stale deferral turns the row amber.

- **Prove the install chain with a one-shot transient timer** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: the real week waits on the install, and the timer-liveness check (T-2542) only reads units that exist. `systemd-run --user --on-active=10s` exercises the same path with no permanent install.
  Done when: `fm tick selftest` schedules a transient unit, sees it fire within 30 seconds, and reports the exit status, then removes it.

- **Estimate the no-install baseline from natural session gaps** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: assumption: session starts already run maintenance, so the gap between events and the next session start is the lateness a timer would remove. Merges "lateness as a natural experiment" and "awake windows".
  Done when: fm doctor prints the median and p90 event-to-notice latency from the last 30 days, and "a timer would add nothing" when p90 is under an hour.

- **Wild: let the tick play a tournament against itself** — FEATURE — value 3 — effort L — risk med — category: measurement
  Why: wild. Run N tick-policy variants (cadence, finder sets, thresholds) over the same replay tape; rank them by Brier on actually-needed events and keep the winner, ranking on a split of the tape to avoid overfit.
  Done when: `fm tick tournament` ranks at least 3 variants on one tape and prints held-out scores that differ from the train scores.

- **Wild: seal a predicted morning card and settle it at wake** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild. Before night, the tick writes what it expects will need the user in the morning (red CI, stale branch, expired deferral). At wake it is scored against reality, giving a Brier per prediction and a bet-kind row in fm outcomes.
  Done when: a sealed card file is stamped before midnight and the morning digest shows hits, misses and a Brier value.

- **Wild: add a stub user who declines every fire** — FEATURE — value 2 — effort S — risk low — category: measurement
  Why: wild. A deterministic stub user acting on none, all, or a random half of notes stress-tests the grader: an "acted on" metric must read zero for the decliner and fail loudly otherwise.
  Done when: replay with the decline-all stub yields acted-on 0 and a grade of "no value", and the all-accept stub cannot yield a perfect score without a flagged ceiling.

- **Score "acted on" by echo in the user's next prompt** — FEATURE — value 3 — effort S — risk med — category: measurement
  Why: assumption: a note the user used shows up in their wording or in a follow-up verb. This is a cheap proxy that needs no new input channel, and it is validated against the stub-user and mutant sets above.
  Done when: each delivered note gets an acted-on flag from phrase overlap with the next prompt, with a stored agreement rate against 20 hand-labelled pairs.

Next question: which tick outputs can be settled against something outside Foreman's ledgers (forge events, CI, the user's commits), and which are only ever graded by Foreman itself?
Next question: if the install never happens, which of these grades would still be enough to decide keeping or retiring each tick job?
