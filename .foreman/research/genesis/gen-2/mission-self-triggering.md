# Mission 4 — self-triggering (gen 2, #11)

Task: T-2542 (brief 1).

Parent: gen-2/seed.md row 4 → gen-0.md #11: "Self-triggering. Schedules, file and event triggers, CI and issue
watchers, so work starts without me. Installs (timers, units) get queued for one yes." gen-0's goal, MUSTs and NEVERs
are quoted in the seed and apply here unchanged.

## Capability
Work that starts without the user, and a trigger layer that is known to be alive. Grounded before filing (Mission 3's
lesson), most of #11 is already built: standing orders that capture on a schedule or when a file changes (fm orders,
T-0452), the hourly model-free tick and the nightly run (fm night, T-2356), a CI fetch and issue watching only where
meta `watch` records the user's yes (with a cap of 20 issues per repo a day), timers staged under state and installed
on one yes (fm night --stage / --install, T-2357), trigger routes, budgets and precision (fm triggers, T-2276, T-2355),
and heartbeats that catch a run that wedged or was killed (fmserve.beat). Units run with Persistent=true, so a machine
that was asleep at the hour runs the job when it wakes. Measured now: the installed tick last fired at 23:00 with
Result=success, and the nightly timer has not fired yet.
What it lacks: nothing tells the user or the session that an installed timer stopped firing, or that its runs fail.
The tick logs only when something happens, and a run that never starts leaves no heartbeat, so a dead timer looks the
same as a quiet night. An interpreter upgrade that removes the ExecStart python, a unit that systemd disabled, or a
tick that exits 1 every hour all fail silently. systemd already records each timer's last trigger and each run's
result. Foreman doesn't read either.

## Gaps this Mission targets (coverage: #11, 59 empty cells; the I cells below are planned, open until the exam closes them)
- Liveness of installed triggers: operate × headless/server, verify × headless/server, operate × CLI (fm doctor reads
  systemd's last trigger and last result for every foreman-* unit), find × headless/server (a failed run is found the
  same day, not when its work is missed).
- Proof at install: ship × headless/server, build × CLI (fm night --install starts the tick once and reports its
  result, so the user's yes is followed by a run that is seen to work).
- Not in this Mission (grounded as built or with no failure behind them): file and schedule triggers (fm orders),
  CI-red briefs (fm ci-watch), issue watching, storm caps, sleep catch-up (Persistent=true), battery yield (this host
  has no system battery), a weekly canary event (no chain failure on record). They stay idea cells.

## Approaches
1. Read systemd's own record. For each installed foreman-* timer, fm doctor runs systemctl --user show for
   LastTriggerUSec and the service's Result and ExecMainStatus. A trigger older than three intervals, or a result
   other than success, is a WARN that names the unit and journalctl --user -u UNIT. fm night --install starts the tick
   service once and prints its result. Fails if: a machine without systemd (the crontab path) has no such record. The
   answer: there the row says it can't tell, and names the cron log.
2. A beat file written by every tick, judged by age. Fails if: it duplicates what systemd records, and a tick that
   crashes before writing it reads the same as one that never started.
3. A weekly canary event through the full chain (order → capture → inbox). Fails if: it proves the chain but not the
   timer's environment, and nothing on record says the chain breaks.
4. Use what exists: check_night_timers already walks the installed units under fmserve.unit_dir(), and fmserve already
   calls systemctl --user (_loginctl, the serve unit). Approach 1 extends that check, with no new store.
5. Do less: document `systemctl --user list-timers` in the install card and leave the checking to the user. Fails if:
   the user is away, which is the whole point of #11.

Choice: 1 on 4 (85%). systemd holds the truth already. The doctor's night-timers row is where the other timer
problems already show, and the foresight cache carries the same finding to the next session with no one asking. The
15% doubt is the cron path, which can only say it can't tell.

## Exam
#11's exam kinds are trigger ("Make the tests run every night on their own, without me starting them") and watch
(work started from replayed events, against a hidden key). This Mission adds no exam kind. Unit tests with a fake
systemctl pin the parsing, but they don't decide done. The deciding check runs against the real systemd on this host:
a throwaway user unit named foreman-tick-drill (systemd-run --user, a command that exits 1, removed afterwards) must
show up as a failed run with its exit status, and the real foreman-tick timer must read as alive. Both are read from
systemd's own record, which Foreman doesn't write. The drill is local and reversible, and its output is the step's
evidence. Zero-token arms run each generation; the session arms run at the end-of-run exam (rule 6).

## Long-horizon goal (end of run)
Across the long-horizon goals, every installed Foreman timer that stopped firing or failed is named by fm doctor
within one day, and no self-started run fails silently.

## Lean
No new verb. The same liveness read reaches the user and the session without anyone running fm doctor: the Stop
hook's detached foresight sweep (fmforesight.refresh, at most every 10 minutes per project, off the hook's own path)
caches a dead or failing timer, and SessionStart prints the cached line among its Watch items, as it already does for
CI red on main. fm doctor shows the same row. No hook runs systemctl itself. fm night --install gains one start of
the tick service. Hook p95 and rules size don't grow. Injected context grows by one Watch item, only while a timer is
dead or failing.

## Tier share
Brief 1 is tier 3, a capability Foreman lacks: knowing that its own triggers are alive. One of one, 100%.

## Done when
fm doctor, and the next session's Watch line through the foresight cache, name an installed foreman-* timer whose last
trigger is older than three intervals, or whose last run's result isn't success, with the unit and the journalctl
command. fm night --install reports the first tick's result. Without systemd, the row says it can't tell.

## Briefs (fm intake)
```
FEATURE: installed timers known alive: a liveness read of every installed foreman-* unit from systemd (LastTriggerUSec, Result, ExecMainStatus) WARNs on a trigger older than three intervals or a failed last run, naming the unit and journalctl --user -u UNIT, in fm doctor's night-timers row and, cached by the Stop hook's foresight sweep, in SessionStart's Watch line; fm night --install starts the tick once and prints its result; without systemd it says it can't tell
```
