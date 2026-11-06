# Critique — Mission 4, self-triggering (gen 2, #11)

Tasks: T-2542 (done). Mission: gen-2/mission-self-triggering.md.

## Closed vs planned
- The one planned brief is closed. Installed timers known alive (T-2542): `fmnight.liveness()` reads systemd's own
  record for each installed foreman-night/tick timer: the timer's LastTriggerUSec, and the service's Result and
  ExecMainStatus. It names a timer with no trigger in three intervals (a never-fired one is judged by its unit file's
  age) and a failed last run. fm doctor's night-timers row WARNs with journalctl --user -u UNIT, or says how many
  timers are firing. The Stop hook's foresight sweep caches the finding, and SessionStart prints it among its Watch
  items. fm night --install starts the tick once and reports that first run.
- Grounded before filing, and not rebuilt: file and schedule triggers (fm orders), CI and issue watching on the user's
  yes, staged one-yes installs, trigger budgets and storm caps, sleep catch-up (Persistent=true), heartbeats for runs
  that wedge. Mission 3's lesson held: one brief, no drops at planning.

## Outside signals
- systemd on this host, a record Foreman doesn't write: fm doctor --json reads "2 installed timer(s) firing, last runs
  ok (systemd)" for the real foreman-tick (fired within the hour) and foreman-night (installed today, not yet due).
- The failing-unit drill (a throwaway systemd-run unit that exits 1) was blocked by the guard as a system action.
  Foreman doesn't grant itself categories (gen-0's NEVER), so it is queued for the user's yes (fm ask T-2542 system
  --later). The failed path is pinned by unit tests over a fake systemctl until then.
- CI on main: green on cef5811. a0ba95a (T-2536 to T-2541) was being watched when this was written.

## What failed
- The Mission's first draft graded the liveness check only by tests Foreman wrote against its own fake. The cold
  reader refused that. The real-systemd check replaced it, and half of it (the failing unit) still waits on a grant.
- The cold reader also caught that a check reachable only through fm doctor reaches no one while the user is away.
  The foresight cache fixed that. The first draft had missed how its own finding would surface, which is the point of
  #11.

## What the next Seed should change
- For any capability meant to work while the user is away, the Mission names the unprompted path a finding takes to
  the user (a cache SessionStart reads, the digest, a notification) before naming the check itself.
- Ask for the system grant for local, reversible drills (a throwaway user unit) up front in the Seed's grants list, so
  real-world checks don't wait until the end of the run.
