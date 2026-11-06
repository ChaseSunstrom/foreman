# Brainstorm — lens: simplicity

- **Make the tick a pure function with an injected clock** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the gap is "a week of live ticks graded waits on the user's install". The grade needs the tick's decisions, not systemd. Assumption: `fm night`'s tick can take `now` and a state dir as inputs.
  Done when: `fm night tick --at <ISO> --dry --state <dir>` prints the jobs it would run, and a 7-day replay finishes in under 60s on a machine with no timer unit.

- **Run due jobs from the sessions that already exist** — FEATURE — value 5 — effort M — risk med — category: self-trigger
  Why: Foreman already has SessionStart and Stop hooks, so a lazy tick needs no install. If the last tick is older than the interval, SessionStart runs the due jobs inline under a 2s cap and SessionEnd runs the rest. Assumption: the jobs can be bounded or detached cheaply.
  Done when: on a box with no Foreman timer, three sessions across two days append tick rows, at most one per interval, and the hook p95 stays inside `bench_hooks.py`'s budget.

- **Record who ticked: timer, session or replay** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: once ticks can come from several places, "alive" means nothing without a source. It is one field on the existing tick row, not a new store.
  Done when: `fm doctor` prints one line such as `ticks 14d: 9 session, 0 timer, 3 replay, last 6h ago`, and "never" is a distinct state from "stale".

- **Grade self-triggering from ledgers that already exist** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: `fm outcomes` already holds bets, tasks already carry an origin, and the dropped ledger already holds rejections. `fm night grade` would be stateless and join them: fires, kept, dropped, and a fire-to-kept rate with its denominator printed. This adds no new store to maintain.
  Done when: running `fm night grade` twice on the same state gives identical output, and deleting every file it does not read changes nothing.

- **Replay this repo's git history as the event stream** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: there are about 2,600 task commits with dates and the CHANGELOG, which is free labelled data for "should a trigger have fired here". The pure tick plus a fake clock walks the history and compares its fires with what the user actually asked for next. It sits beside the end-of-run exam as a cheap arm. Assumption: task ids in commit messages give a usable ground truth.
  Done when: the replay prints precision and recall of fires against the next-commit tasks over 30 simulated days, with zero tokens spent.

- **Add a null-tick arm to the exam** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: the standing rule says a free arm beating the session arm is a top gap. A tick that does nothing is the cheapest control for "does self-triggering add value", and it tells you whether the trigger and watch grades move at all.
  Done when: `fm exam scorecard` shows trigger and watch with the real tick next to the no-op tick on the same scenarios.

- **Let the web UI process be the timer while it is open** — FEATURE — value 3 — effort S — risk low — category: self-trigger
  Why: the web UI is a surface the user already runs, and it can call the same pure tick every N minutes with no unit file. Assumption: the server stays up through a normal workday.
  Done when: with `fm web` running and no timer, tick rows appear on schedule, tagged `source=web`, and stop when the server stops.

- **Collapse trigger gauges into one useful-fire rate** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: the pack shows gauges multiplying. One line, "fires kept by the user ÷ fires, last 30 days (n=…, excludes replay)", is the number that says whether self-triggering is paying for itself.
  Done when: `fm doctor` has exactly one self-trigger score line that states its denominator and exclusions, and a lint fails a second score for the same capability.

- **Wild: use each commit as the clock** — FEATURE — value 3 — effort S — risk med — category: self-trigger
  Why: wild. `fm ship` and `fm task finish` already run in the repo, so each one calls the lazy tick. Work cadence then sets tick cadence: busy days tick often and idle days never tick, which is the right shape for the dev loop and costs nothing when idle.
  Done when: finishing a task after 24h of silence runs due jobs once, and finishing two tasks within the interval runs them once.

- **Wild: a detached week-long sleep chain, no install** — FEATURE — value 3 — effort M — risk high — category: self-trigger
  Why: wild. A session starts one `setsid` process that sleeps until the next slot, runs the tick, re-arms itself, and exits after 7 days or at the first failure. It dies on reboot, and that bounded life is also the measurement. Risk: a hardened kernel may kill the process, and this is an outward-facing background process, so it needs a grant.
  Done when: with the grant set, the process produces tick rows for 48h, `fm halt` ends it, and a reboot ends it without leaving files behind.

- **Wild: keep ticks as a local git ref** — FEATURE — value 2 — effort M — risk low — category: portability
  Why: wild. Each tick is one note on a `refs/fm/ticks` ref, so the ledger is a tamper-evident chain that `git log` can read and that cannot be dropped by a state-dir cleanup. Tick history then survives a moved repo and is readable on any machine with no Foreman. Nothing is pushed unless a setting says so.
  Done when: `git log refs/fm/ticks --oneline` lists the last 20 ticks, and `fm night grade` rebuilds its table from that ref alone.

- **Delete the tick jobs that have never fired** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: after the tick is measurable, any job with zero kept fires in 30 days is dead weight in the lean ratchet. Pay for the lazy tick by removing one job or timer path.
  Done when: a job with no kept fire in 30 replayed days is listed by `fm doctor` as a removal candidate, and the PR adding the lazy tick removes at least one existing tick-related line of code or doc.

- **Wild: let a stub user decline every fire** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild. A scripted user who keeps 1 in 5 fires, and drops the rest, is run through the replay. The gauge must come out near 20%. Otherwise the useful-fire rate is measuring something else, and it is caught before a live week.
  Done when: planted keep rates of 0%, 20% and 100% each give a reported useful-fire rate within 5 points.

Answering one earlier question: the user would not notice a silent tick for a month. The "source" field and the one-line score answer it.

Next question: does the lazy tick change what the user sees at session start, and would they rather have no note on a tick that found nothing?
Next question: which fires are safe with no user present, and is that list one file small enough to read in under a minute?
