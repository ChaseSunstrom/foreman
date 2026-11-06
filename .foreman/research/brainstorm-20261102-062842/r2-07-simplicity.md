# Brainstorm — lens: simplicity

- **Keep job state as one empty file's mtime** — CLEAN — value 4 — effort S — risk low — category: tick state
  Why: assumption: tick state is parsed from a ledger, so a torn write or an unreadable schema can block the exam. Due-ness becomes `now - mtime(job file) > interval`. There is nothing to parse and nothing to corrupt, and `ls -lt` is the dashboard.
  Done when: a test truncates and garbles the state dir, and the tick still computes the due set and exits 0.

- **Run due jobs from every `fm` verb, like `git gc --auto`** — FEATURE — value 5 — effort S — risk med — category: self-trigger
  Why: the gap is that nothing measurable happens until the user installs a timer. Any `fm` call stats one file (under 1 ms) and detaches a tick if a job is overdue. This differs from session-edge ticks because the user runs verbs all day. Assumption: verb entry is cheap enough to host the gate.
  Done when: with no timer installed, a fixture running `fm status` after the interval leaves a fresh mtime, and `bench_hooks.py` p95 does not move.

- **Stop warning about a missing timer once session ticks work** — FIX — value 3 — effort S — risk low — category: doctor
  Why: the timer install is something the user hasn't done, and a standing WARN for it reads as failure. Doctor should say `tick: session-driven, last 3h ago (ok)` and show the timer as an optional upgrade, with its measured lateness benefit if any.
  Done when: `fm doctor` on a fixture with no timer and a recent session tick prints no WARN for the tick.

- **Grade due-ness with a table of 12 real cases** — FEATURE — value 4 — effort S — risk low — category: exam
  Why: the pack says trigger is unmeasured until the end-of-run exam. A golden table of `(mtimes, clock) → due set` rows, taken from the repo's own past state, grades the decision procedure with zero tokens and no install. Assumption: past states can be reconstructed from git history of the ledgers.
  Done when: `fm exam tick` prints `12/12` and fails with a named row when the decision function changes.

- **Hard-code one interval table of at most 6 jobs** — CLEAN — value 3 — effort S — risk low — category: scope
  Why: knobs mean more things to measure and to get wrong. One constant table holds settle bets, digest, resume, doctor and so on, and a test caps its length. A new job must displace one.
  Done when: a test fails if the table exceeds 6 rows or any interval comes from a setting.

- **Allow exactly one function to spawn tick jobs** — CLEAN — value 3 — effort S — risk low — category: single path
  Why: the timer, hook edges and verb gate must not drift into separate code paths. The ledger line records `via=timer|session|verb`, and a grep test asserts only one call site starts job runners.
  Done when: the test passes, and a second call site added in a scratch copy fails it.

- **Measure backlog age instead of fire count** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: this answers whether self-triggering is useful without a week of ticks. Per job, report the age of the oldest unserviced item (oldest unsettled bet, oldest undigested day). The data already exists and is read at the start of a window and again at the end.
  Done when: `fm doctor` prints one `backlog` line per job, and a fixture with a 3-day-old unsettled bet shows 3d.

- **Mention the tick in SessionStart only when something is overdue** — PERFORMANCE — value 3 — effort S — risk low — category: lean
  Why: the lean ratchet is a standing concern, and a quiet tick should cost zero injected chars.
  Done when: a session with no overdue job injects 0 tick bytes, and one with an overdue job injects one line.

- **Retire jobs whose backlog stays at zero without ticking** — CLEAN — value 3 — effort M — risk med — category: subtraction
  Why: this combines backlog-age with the repo's "pay for growth with a deletion" rule. A job that is never behind is a candidate for pull-on-read.
  Done when: the report names at least one job as lazy-able or states that none qualify.

- **Wild: delete the scheduler and compute on read** — FEATURE — value 4 — effort M — risk med — category: pull not push
  Why: wild; assumption: bets can settle when `fm outcomes` is looked up, and the digest can build when asked. The tick then has nothing to measure because nothing is scheduled. The user's own words, repeatedly, ask for less machinery.
  Done when: one job runs with its tick entry removed and its output is identical at read time.

- **Wild: let the model be the cron** — FEATURE — value 3 — effort S — risk med — category: agent clock
  Why: wild. When a job is overdue, the one-line SessionStart note says `run fm tick`, and the agent complies at a natural pause. The tick ledger records `via=agent` and the compliance rate. This works on any harness that reads the note.
  Done when: a scripted session given the note runs `fm tick` in at least 8 of 10 trials.

- **Wild: print a seven-day strip from a time-warped fixture** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. `fm tick --week` touches mtimes in a temp state dir, replays seven days of verb and session activity, and prints `✓✓·✓✓✓·`. Each glyph is a day that ran on time. It is a one-glance answer to "does self-triggering work?" with no install.
  Done when: the command exits non-zero if any day that had activity shows a miss.

Next question: Which job in the tick does the user act on when it fires, and can backlog-age show that without any firing log?
Next question: If verb-gated ticks cover the user's active days, what share of due jobs are only ever due while no session is open?
