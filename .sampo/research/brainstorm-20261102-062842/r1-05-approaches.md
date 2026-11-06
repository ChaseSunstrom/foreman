# Brainstorm — lens: approaches

Answering the earlier question about outputs the user acts on unchecked: tick-filed tasks are one. Idea 1 grades them from drop history, without waiting for new ticks.

- **Retro-grade every self-filed task from the dropped ledger** — FEATURE — value 5 — effort S — risk low — category: measurement
  Why: the pack's drop history already labels Foreman-filed items (origins ci, self, discovered): closed means useful, dropped means noise, and gen-2 sweep tasks dropped as already queued are duplicates. No new tick is needed to grade a week of them. Assumption: filed tasks keep an origin field.
  Done when: `fm exam` or `fm outcomes` prints per-origin kept/dropped/duplicate counts over the last 60 days, and a fixture ledger with 3 dropped and 1 closed shows precision 0.25.

- **Backtest the tick's finders on the parent of every past FIX commit** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the repo has hundreds of T-numbered FIX commits. Checking out each parent in a worktree and running the tick's finders gives labelled recall for free. The standing rule asks for signals Foreman didn't author, and git history is one.
  Done when: a run over the last 50 FIX commits reports the share where a finder flagged the file the fix touched, split per finder.

- **Hand the tick to the drive as its clock** — FEATURE — value 4 — effort S — risk low — category: session path
  Why: the drive loop already runs unattended between tasks, and a standing rule requires every capability to have a session path. The drive calls the due-tick check at each task boundary and logs "due at / ran at".
  Done when: after a drive of 3 or more tasks, `fm night --log` shows tick rows stamped source=drive with lateness in minutes.

- **Run a lazy tick at Stop and SessionStart with a lateness ledger** — FEATURE — value 4 — effort S — risk med — category: hooks
  Why: it is cron-by-use, with no install and no daemon. It is measurable (catch-up debt per gap) and useful (a filed morning note). The trade-off is that it only fires while the user is present, and the hook-latency ratchet must not move. Assumption: the tick's cheap half fits a p95 budget.
  Done when: `python3 plugin/tests/bench_hooks.py --runs 20` stays within budget and a simulated 20-hour gap yields exactly one coalesced catch-up tick.

- **Add tick scenarios to the zero-token exam arms** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the gap says triggering is unmeasured until the end-of-run exam. The per-generation rule allows the finders, oracle and empty arms on all scenarios. A tool-less child writes trigger and watch scenarios (red CI on main, stale branch, a dropped file), and the oracle arm grades them.
  Done when: `fm exam` lists a trigger kind with at least 6 child-authored scenarios and the empty arm scores below the oracle arm.

- **Score the tick against a dumb baseline** — FEATURE — value 4 — effort M — risk low — category: control arm
  Why: a standing rule makes the free arm beating the session arm a top gap. The baseline is just `fm find` plus a CI poll on a fixed schedule, and only filings the baseline lacks count as the tick's value.
  Done when: the tick scorecard shows "unique findings vs baseline" and prints a top-gap line when it is zero over 14 simulated days.

- **Soak the tick on logical time with planted faults** — FEATURE — value 4 — effort M — risk low — category: simulation
  Why: a scratch clone with an injected clock moves a simulated week in seconds. A script plants a red test, a stale branch and a DST jump at known ticks, so detection latency is graded against ground truth. This tests code paths, not real-world precision, so it complements ideas 1 and 2.
  Done when: the soak prints per-plant detection latency in ticks and fails if any plant goes undetected for more than 2 ticks.

- **Run the tick as a scheduled GitHub Actions workflow on a log branch** — FEATURE — value 4 — effort M — risk med — category: real clock
  Why: the repo already has `test.yml`, so a cron workflow gives a real week of wall-clock ticks with no install by the user. It writes a tick log to a `tick-log` branch. The trade-offs are an outward push (it goes through `fm ship` under the push grant) and CI minutes. This is a cheap slice of T-0793. Assumption: the repo's Actions are enabled.
  Done when: after 3 days, `fm night --remote-log` lists at least 3 tick rows fetched from the branch.

- **Host the tick in the web UI or Desktop process** — FEATURE — value 3 — effort S — risk low — category: surface
  Why: the user already leaves `fm web` or Foreman Desktop running, so a thread there is a clock needing no unit file. It fires only while the app is open, which the ledger records. Assumption: the web server is long-lived.
  Done when: with the web UI running 2 hours at a 30-minute interval, the tick log shows 4 rows with source=web.

- **Wild: use `core.fsmonitor` as an install-free heartbeat** — FEATURE — value 2 — effort M — risk high — category: unconventional
  Why: wild. git runs the fsmonitor hook on every `git status`, which the user and the status line run constantly. A repo-local config line makes the tick fire on repo activity, with a rate limit. It is invasive and touches git config, so it needs an explicit yes.
  Done when: in a scratch repo with the hook set, ten `git status` calls cause at most one tick and add under 20 ms p95.

- **Wild: schedule a weekly cloud routine that runs the tick on a fresh clone** — FEATURE — value 3 — effort M — risk med — category: cloud
  Why: wild. A remote routine is a clock owned by the host, not by Foreman, and a fresh clone also tests that a stranger's checkout works. Assumption: routine scheduling is available to this account. It sends repo content out, so it needs an explicit setting.
  Done when: one routine run posts its tick summary to the inbox, and `fm doctor` shows it as alive.

- **Wild: tick against a stranger's open-source history with real issue-to-fix pairs** — FEATURE — value 3 — effort L — risk low — category: external benchmark
  Why: wild. Foreman didn't author the labels, so the grading can't be gamed by Foreman's own habits. A pinned clone of a small public repo is stepped commit by commit, and the tick must flag the file before the fix lands.
  Done when: a pinned repo's 30 issue-to-fix pairs produce a recall figure per finder, reproducible offline from a bundle.

- **Do less: grade only the claim "a tick ran when due"** — CLEAN — value 2 — effort S — risk low — category: minimal
  Why: if no install exists, the honest measure is lateness against the due schedule from the existing beat file. Calling the rest "unmeasured" in docs beats a placeholder.
  Done when: `fm doctor` prints "ticks due 14, run 0, installs: none" and no grade figure.

Next question: Which of these grades would the user actually trust, a backtest on past FIX commits or a live week, and do they ever read either?
Next question: When the tick files something and the user drops it, does the drop record carry which finder produced it?
