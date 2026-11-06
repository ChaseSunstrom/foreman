# Brainstorm — lens: deepen: self-trigger

- **Build one "edge-driven scheduler" every edge calls** — FEATURE — value 5 — effort M — risk med — category: self-trigger
  Why: the category lists session-start, every-`fm`-verb, commit and web-UI triggers as separate ideas; the bet-settling ask (fm night's tick runs fmoutcomes.maintain) and the timer-liveness ask (T-2542) both presume a tick that may never fire. One `fmtick.due()` with a lock file, a per-job last-run stamp and a cost cap lets every edge (session hook, verb, commit hook, web UI) call the same code, so a second edge is a one-line registration.
  Done when: with no timer installed, running any `fm` verb, opening a session, or making a commit each runs a due job exactly once within its interval (a lock stops double runs), and `fm tick status` lists the edge that ran it.

- **Record every tick with its trigger source and measure lateness** — FEATURE — value 5 — effort S — risk low — category: self-trigger
  Why: the Mission gap is "a week of live ticks graded" waiting on an install. A ledger row per tick (source: timer/session/verb/commit/ui, due-at, ran-at, jobs, outcome) makes self-triggering measurable from day one. assumption: a tick ledger doesn't exist yet in a form that carries the source.
  Done when: `fm tick report` prints, per source, the count and the median lateness against the due time over the last 7 days, from the ledger.

- **Replay a simulated week of edges against the scheduler** — FEATURE — value 4 — effort M — risk low — category: self-trigger
  Why: nobody can wait a week to see whether the self-trigger works. Feed recorded session-start, verb and commit timestamps from this repo's history into the scheduler with a fake clock and grade the result: longest gap with no tick, jobs missed, jobs doubled.
  Done when: `fm tick simulate --days 7` prints the longest unticked gap and the missed/doubled counts, and a test fails if the longest gap exceeds 2× the interval for a normal activity trace.

- **Grade the quiet gaps: say what the tick could not cover** — FEATURE — value 4 — effort S — risk low — category: self-trigger
  Why: edges only fire when the user is active, so a weekend away leaves jobs overdue. Surface "last tick 41h ago, 3 jobs overdue, caught up now" at the next edge, and make `fm doctor` name the max gap as the honest cost of having no timer.
  Done when: after a faked 40-hour idle gap, the next session start prints one line naming the gap and the jobs it caught up, and `fm doctor` reports the longest gap in the last 30 days.

- **Catch up in priority order under a time budget** — FEATURE — value 4 — effort M — risk med — category: self-trigger
  Why: hooks have a p95 budget (bench_hooks gate), so a backlog of due jobs at session start can't run inline. Rank jobs (bet settling, sweep, digest), run what fits in a hook-safe slice, and detach the rest as a background child that outlives the hook.
  Done when: with five jobs due, a session start adds under the hook budget in `bench_hooks.py`, and the remaining jobs finish in the background and appear in the ledger.

- **Give red sweep rows a wake-condition** — FEATURE — value 4 — effort M — risk med — category: self-trigger
  Why: the gen-2 sweep's "tasks is red" row cleared only because open tasks closed, and a person had to know to rerun it. A row that stores "rerun when T-2600, T-2603 and T-2601 close" lets the task-close edge trigger the rerun without a timer.
  Done when: closing the last task a red row waits on reruns that row within the same command, and the ledger shows the trigger as "task-close".

- **Add `fm since`, the pull form of every tick** — FEATURE — value 3 — effort S — risk low — category: self-trigger
  Why: a pull verb works with no scheduler: it runs what is due, then prints what changed since the user last looked (bets settled, sweep rows, drops). Pull and push share the scheduler's ledger, so the digest cannot disagree with the tick.
  Done when: `fm since` after a faked 2-day gap runs due jobs and prints at most 10 lines of changes, and a second call immediately after prints "nothing new".

- **Offer the trigger the user just did by hand** — FEATURE — value 3 — effort S — risk low — category: self-trigger
  Why: if the user runs the same maintenance verb by hand three times at similar intervals, that is evidence of a missing schedule. Offer once, with the observed cadence, to register it as a job. assumption: verb invocations are logged with timestamps.
  Done when: after three hand runs of one verb over a faked 3 days, the next run prints one offer line naming the cadence, and declining records a steer so it never offers again.

- **Show "checked, nothing found" so quiet reads as alive** — FEATURE — value 3 — effort S — risk low — category: self-trigger
  Why: a tick that finds nothing leaves no trace, which looks identical to a dead tick. A one-line receipt ("checked 6 jobs at 09:14, nothing due, next edge-run by 15:00") in the session's Watch line, tied to the ledger, separates alive from broken.
  Done when: a session start after a no-op tick prints exactly one such line, and `fm doctor` fails the check when the newest ledger row is older than three intervals.

- **Let the tick pace itself from the data** — FEATURE — value 3 — effort M — risk med — category: self-trigger
  Why: a bet-settling job that finds nothing for ten ticks does not need running as often, and one that finds something each time may deserve more. Per-job interval backs off on empty runs and tightens on hits, bounded by a floor and ceiling.
  Done when: a job with ten empty runs in the ledger has an interval at least double its base, and one hit resets it, shown by `fm tick status`.

- **Wild: use each commit as the clock** — FEATURE — value 3 — effort S — risk med — category: self-trigger
  Why: wild. A post-commit hook calls the scheduler, so the repo's own heartbeat drives jobs, and the work cadence sets the tick cadence with no timer. Commits also give a natural "what changed since the last tick" diff for the job.
  Done when: committing in a test repo with a job overdue runs that job once in the background within the hook budget and records source "commit".

- **Wild: a detached week-long sleep chain, no install** — FEATURE — value 2 — effort M — risk high — category: self-trigger
  Why: wild. The first session spawns a detached `setsid` process that sleeps to the next due time, runs the tick, and re-arms itself, with a pidfile so only one chain exists and a ledger row each time it wakes. It gives real timer behavior until reboot and costs no systemd install; the fallback is the edges.
  Done when: after starting the chain with a 2-second test interval, three ticks appear in the ledger with source "chain", a second start does not create a second process, and killing it is reported by `fm doctor`.

- **Wild: let the tick wake from the user's other tools** — FEATURE — value 2 — effort M — risk med — category: self-trigger
  Why: wild. The shell prompt hook, an editor save, or a git fetch in any repo can nudge the scheduler through a tiny local socket or touch file, so activity anywhere on the machine counts as an edge. This closes the weekend gap when the user is working but not in a Foreman session.
  Done when: sourcing the one-line shell snippet and running three commands in an unrelated directory triggers one due-job run, recorded with source "shell", and the snippet adds under 5 ms per prompt.

- **Wild: have the tick prove itself with a canary job** — FEATURE — value 3 — effort S — risk low — category: self-trigger
  Why: wild. A no-op canary job writes a timestamp each run, and the exam grades "did the canary run on schedule" per trigger source. That gives the end-of-run exam a free, side-effect-free measure of trigger coverage without needing real bets or digests to be due.
  Done when: `fm exam` includes a trigger line reporting the canary's on-time rate per source, and removing all edges but one changes the printed rate in a test.

Next question: Which of the user's real working patterns (nights, weekends, long gaps between sessions) leave every edge silent, and what is the longest such gap in the actual session history?

Next question: Which jobs does the user need run on time (settled bets, digest) versus merely eventually, so the catch-up order and budget are set by need rather than by guess?
