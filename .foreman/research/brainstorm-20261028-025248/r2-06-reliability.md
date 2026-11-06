# Brainstorm — lens: reliability

- **Fire each deferral exactly once with a fired-token ledger** — FIX — value 4 — effort S — risk low — category: deferrals
  Why: `fm task defer --until` came back at the wrong time once (T-1802). A restart or a second surface reading the same deferral can wake it twice. Assumption: nothing records that a deferral already fired.
  Done when: a deferral whose trigger fires twice, with a restart between, runs its task once and logs one wake.

- **Escalate SIGTERM to SIGKILL on a timed ladder and journal the rung that worked** — FIX — value 4 — effort S — risk low — category: process kill
  Why: `run.py` kills a hung test class after 480 s, and a stalled check in another project held the gate for 40+ minutes. The kill path has no recorded escalation, so a stubborn child can outlive its parent unnoticed.
  Done when: a child that ignores SIGTERM is killed within the grace period, and the journal records `sigkill` as the rung that worked.

- **Auto-disable a hook that blows its budget twice, and say so in the glance line** — FIX — value 4 — effort M — risk med — category: hook safety
  Why: the PreToolUse:Bash:script p95 ran 310 ms over its 300 ms budget with no action taken. A slow hook should degrade visibly, not silently slow every command.
  Done when: a stub hook that sleeps 2 s is disabled after two timeouts, and the glance line shows "guard off: slow" until it is re-enabled.

- **Shed optional checks under memory or CPU pressure using PSI** — PERFORMANCE — value 4 — effort M — risk low — category: load shedding
  Why: CI runners hit a crashing chromium under parallel load (T-1806), and the hook bench varies with machine load. Assumption: Foreman has no signal of host pressure before it starts optional work.
  Done when: with a synthetic memory-pressure stall in `/proc/pressure`, browser and shot checks are skipped with a named reason and required checks still run.

- **Buffer proofs in memory when the journal disk is full, then flush on recovery** — FIX — value 4 — effort M — risk med — category: durability
  Why: a full disk currently fails a write and can drop a proof. Assumption: the write path has no fallback when the disk fails.
  Done when: with the journal directory on a full tmpfs, a proof is held in memory, the command reports it as pending, and it lands on disk once space returns.

- **Publish a per-command reliability SLO from the journal and alert on budget burn** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: session-start checks catch CI and cost problems, but no check tracks whether `fm` commands succeed or how long they take over time. The journal already has the raw data.
  Done when: `fm slo` prints success rate and p95 per command for the last 7 days, and a 1-hour burn above threshold adds one line to session start.

- **Roll back to the last working Foreman install when the new one fails its first gates** — FEATURE — value 4 — effort M — risk med — category: release safety
  Why: version skew between the plugin and the CLI is a known risk. A bad `/plugin update` currently stays installed until someone notices.
  Done when: a deliberately broken build fails its first three gates, the previous install is restored automatically, and the journal records the swap.

- **Fire a weekly fire drill that kills one lane and times the recovery** — FEATURE — value 3 — effort S — risk low — category: resilience testing
  Why: the recovery paths (leases, deferrals, journal replay) are tested in isolation but never under a live kill. Assumption: a real kill has never been timed end to end.
  Done when: the drill kills a lane mid-task, the next run resumes it, and the report shows the recovery time against a 60-second target.

- **Enumerate crash points automatically and kill at each one in CI** — CLEAN — value 4 — effort M — risk low — category: crash testing
  Why: recovery bugs appeared in crash-hygiene tests (T-1807), and the leases bug shows that cleanup after a death is easy to miss. Hand-written crash cases cover only the points someone thought of.
  Done when: the suite lists every journal write in `fm task finish` and, for each, kills the process there and checks that the next command restores a consistent state.

- **Keep the last known-good state snapshot and restore it when a run leaves a bad one** — FEATURE — value 3 — effort M — risk med — category: state recovery
  Why: a stuck run has left stale leases and a bad backlog entry (the lease and the refused edit reports). Recovery today edits state by hand.
  Done when: after a simulated corrupt backlog write, `fm doctor --restore` brings the backlog back to the last snapshot and lists what changed.

- **Wild: run every gate on two simulated machines with different CPU counts and fail when verdicts disagree** — FEATURE — value 3 — effort L — risk low — category: determinism (wild)
  Why: flakiness has come from timing and load, not from code. Assumption: most gates pass on the developer's own box and fail elsewhere.
  Done when: a timing-sensitive test that passes at 8 CPUs and fails at 2 is flagged as nondeterministic before it merges.

- **Wild: a standby Foreman that takes over a run only when the primary's heartbeat stops and the journal shows no progress** — FEATURE — value 3 — effort L — risk high — category: failover (wild)
  Why: a run that dies mid-task waits for a manual restart. Assumption: the journal already holds enough state to resume.
  Done when: killing the primary mid-task causes the standby to resume the task within 90 seconds, with one journal entry and no duplicate edits.

- **Wild: a dead-man's pager that sends a local notification when a run goes silent for 20 minutes** — FEATURE — value 2 — effort S — risk low — category: alerting (wild)
  Why: a stalled run is noticed only when someone reads the status screen. Assumption: the user is away from the terminal during long runs.
  Done when: a run with no journal write for 20 minutes raises one desktop notification, and a run that resumes clears it.
