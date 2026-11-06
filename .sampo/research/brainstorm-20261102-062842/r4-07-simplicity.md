# Brainstorm — lens: simplicity

- **Record the install as a declined-by-default costly decision** — FIX — value 4 — effort S — risk low — category: process
  Why: the gap says it "waits on the user's install", which breaks the standing rule not to block on the user for process questions. Run `fm decide --kind costly` as "no timer; session-edge ticks are the baseline", with a revisit date. The mission's gap then closes.
  Done when: `fm genesis check` no longer lists the install as a wait, and `fm decide` shows the record with its revisit date.

- **Assert the tick makes zero model calls** — CLEAN — value 3 — effort S — risk low — category: tick safety
  Why: assumption: the tick is meant to be free, since it runs unattended and the budget steers say nothing may block. One test stubs every spawn path and fails if a tick job reaches a model call. This is simpler than a cost gauge.
  Done when: a red-first test injects a spawn-recording stub, runs a full tick, and passes only with zero spawns.

- **Grade self-triggering as one sentence per day** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: the pack shows many gauges and no single readable result. Append one line per local day to an existing ledger: "N jobs due, N ran, worst lateness Xm, source session-edge". The weekly grade is then the count of green lines out of seven.
  Done when: after 7 simulated days, `fm night status` prints a "k/7 days on time" line read from that one file.

- **Name the one consumer of every tick job's output** — CLEAN — value 3 — effort S — risk low — category: reach
  Why: the standing rule says a capability must be called by a real session path. For each tick job, the table in the registry gets a `consumer` field naming the session path that reads its output. A job with no consumer is listed for removal.
  Done when: a test fails on a job entry with an empty or unresolvable `consumer`, and the failure names the job.

- **Make "overdue" the only tick alarm** — FEATURE — value 3 — effort S — risk low — category: notice-when-missing
  Why: assumption: a user who never installed a timer can still tell "late" from "dead". SessionStart prints a tick line only when a job is past 2× its interval, and says nothing otherwise. No new ledger is needed, since last-run times already exist.
  Done when: a fixture with one stale job produces exactly one SessionStart line, and a fixture with none produces zero bytes.

- **Reuse the exam's end-of-run as the first week of ticks** — FEATURE — value 4 — effort M — risk med — category: exam
  Why: the pack says the tick is "unmeasured until the end-of-run exam grades trigger and watch". Replace a real week with seven virtual days, each calling the same `tick()` function with an injected clock over a planted-event fixture repo. The exam then grades a known timeline.
  Done when: `fm exam` has a tick scenario with 7 virtual days that reports expected and actual fires per day, and a deliberately broken job turns it red.

- **Add a null arm: the same planted week with no tick** — FEATURE — value 3 — effort S — risk low — category: control
  Why: a result like "the tick caught 6 of 7 planted events" means nothing without the baseline of what a session would have caught anyway. This follows the standing rule that a free arm beating the session arm is a top gap. Run the planted week once with ticks off and report the delta.
  Done when: the scorecard prints "tick caught X, no-tick caught Y" for the same fixture.

- **Cut the tick table to the jobs that fired in the last 30 days** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: assumption: some jobs have never produced a result the user acted on. List the never-fired jobs in `fm doctor` with "no fire in 30 days" and let the sweep file one removal task per job.
  Done when: `fm doctor` lists zero-fire jobs after 30 simulated days, and removing one passes the existing suite.

- **Wild: use the git shim as the clock** — FEATURE — value 2 — effort M — risk med — category: clock
  Why: wild; assumption: the user runs git constantly and `fm` already owns `fm ship`. An opt-in `git` wrapper in `~/.local/bin` runs the lazy tick, detached, before delegating to the real git. It needs a PATH entry but no systemd unit, and it ticks at the frequency the user actually works.
  Done when: running the shim logs a tick with `source=git-shim` and returns the real git's exit code unchanged.

- **Wild: let a commit trailer be the schedule** — FEATURE — value 2 — effort M — risk med — category: trigger
  Why: wild. A trailer such as `Fm-Wake: 2026-11-09 re-run bench` in a commit makes the next tick on or after that date file the task. The commit is the only record, so the schedule reviews, diffs and travels with the repo and needs no registry.
  Done when: a fixture commit with the trailer yields a filed task on the first tick at or after the date, and none before.

- **Wild: tick on the user's own failed command** — FEATURE — value 2 — effort M — risk med — category: trigger
  Why: wild; assumption: the user's shell can call a hook after a non-zero exit. The tick runs only then, and files a capture holding the command and its exit code. It ticks exactly when something went wrong, and each fire has an obvious cause to check it against.
  Done when: a scripted failing command produces one capture, and a succeeding command produces none.

- **Print a verify line on every self-started result** — FEATURE — value 3 — effort S — risk low — category: external check
  Why: this answers the earlier question about outputs the user acts on unchecked. Each tick-filed item ends with one copy-paste command that checks its claim outside Foreman, such as `git log -1 <ref>` or `curl -sI <url>`.
  Done when: every item filed by the tick in a fixture run contains a `Verify:` line that exits 0 when its claim holds.

- **Make the tick source a required field, enforced by the writer** — CLEAN — value 3 — effort S — risk low — category: ledger
  Why: assumption: the tick will be driven from the timer, session edges and replay, and a ledger row that doesn't say which is useless for grading. The ledger writer rejects a row with no `source`, so no grade ever mixes the three.
  Done when: a test writing a row without `source` raises, and the grade splits its counts by source.

Next question: What is the smallest event the user would act on within a minute of seeing it, and does any tick job produce one?
Next question: If the tick were removed entirely, which result would the user notice missing first, and is that result already in the ledger?
