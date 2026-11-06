# Brainstorm — lens: user value

- **Show a "while you were away" morning card first** — FEATURE — value 5 — effort M — risk low — category: handoff
  Why: the mission is work that starts without the user, but the pack shows the night tick "logs only when something happens", so the user returns to silence. Assumption: the user reads one file before anything else.
  Done when: after a simulated night with 2 fires (one landed, one failed), the first prompt of the next session contains a ≤10-line card naming each fire, its trigger, its outcome and the one yes it needs.

- **Queue every install as one `fm yes` card** — FEATURE — value 5 — effort M — risk low — category: consent
  Why: the mission says "installs (timers, units) queued for one yes"; open items T-0325, T-0335, T-0418 are all blocked on a user grant. Several unrelated asks are waiting separately.
  Done when: with 3 pending installs, `fm yes` prints one card showing exact unit text, the enable command, the uninstall line and the work each unblocks; answering "y" installs only the ones marked.

- **Dry-run a trigger on the last 30 days before it arms** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: standing rules favour proof before presentation, and fm triggers already measures precision per capture trigger. A trigger that would have fired 40 times last week is something the user should see before saying yes.
  Done when: `fm when --dry <rule>` prints how many times it would have fired over recorded events, with cost, and refuses to arm a rule above a set storm threshold without an explicit flag.

- **Land self-started work on a `night/<date>` branch only** — SECURITY — value 5 — effort S — risk low — category: safety
  Why: the user's push grant is per task through fm ship, and self-started work has no ask behind it. Assumption: unattended edits on the user's working tree would be unwelcome.
  Done when: a trigger-started lane never writes to the checked-out branch or main; `fm night accept` merges the branch and `fm night undo` removes it.

- **Defer fires while the user is mid-flow and coalesce missed ones** — FEATURE — value 4 — effort M — risk low — category: etiquette
  Why: a lane starting while the user types in the same repo collides with their edits. Assumption: sleep and reboot cause missed schedules.
  Done when: a fire arriving while the repo has edits in the last 10 minutes waits, and 5 missed runs after a suspend run once.

- **Explain "why did or didn't this fire" in one command** — FEATURE — value 4 — effort S — risk low — category: transparency
  Why: the tick is silent unless something happens, so silence reads as either healthy or dead. Assumption: the user will otherwise assume the worst.
  Done when: `fm why-fire <trigger>` prints the last evaluation, its inputs, and the reason for firing or skipping, including "tick not running since X".

- **Watch CI and issues into the capture inbox, never straight into work** — FEATURE — value 4 — effort M — risk med — category: watchers
  Why: fm ci-watch already settles ship bets on main; extending it to red runs and new issues reuses a proven poller. Issue and CI text is untrusted, so watchers should only file tasks.
  Done when: a red main run files exactly one capture carrying its fenced log, and re-running the poll files no duplicate.

- **Cap each trigger's spend and break storms** — SECURITY — value 4 — effort S — risk low — category: budget
  Why: standing rules say a real usage limit is waited out and the budget cap stays; a self-starting rule with no ceiling can burn it unseen.
  Done when: a trigger over its per-day cap is paused, a one-line note names it, and the cap survives a restart.

- **Resume rate-limited lanes from a timer, not a session** — FEATURE — value 4 — effort M — risk med — category: unattended
  Why: the steer says wait out real usage limits and resume where stopped; today that waiting needs a live session. Assumption: nothing wakes a stopped lane while the user is gone.
  Done when: a lane stopped by a limit restarts after the window reopens with no session open, and the log shows both times.

- **Add a heartbeat so silence means alive** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: the night tick logs only on events, and a dead timer looks identical to a quiet one.
  Done when: a stopped timer is named in `fm doctor` and at the next session start within one cadence.

- **Wild: Compile "when CI fails on main, draft a fix" typed in chat into a trigger** — FEATURE — value 4 — effort M — risk med — category: authoring
  Why: wild; the user already states intent in sentences, and a cron string is a barrier.
  Done when: a sentence produces a draft rule showing its dry-run count and waits for one yes.

- **Wild: Offer to schedule what the user does by hand every week** — FEATURE — value 3 — effort L — risk med — category: discovery
  Why: wild; assumption: recorded events show repeated manual sequences the user never thought to automate.
  Done when: after the same manual sequence occurs 3 weeks, Foreman proposes one trigger with its dry-run result.

- **Wild: Touch one file to freeze every trigger** — SECURITY — value 3 — effort S — risk low — category: control
  Why: wild; a panic button the user can reach without a session, shell knowledge or the model.
  Done when: creating `~/.claude/foreman/HALT` stops all fires within one tick, and removing it resumes them.

- **Wild: Replay a recorded week through the dispatcher in daylight** — FEATURE — value 3 — effort M — risk low — category: rehearsal
  Why: wild; lets the user watch what a night would have looked like before trusting it.
  Done when: `fm night rehearse` replays stored events at speed and prints the fires, spend and landed branches.

Next question: What does the user actually do by hand in the repo each week that never reaches Foreman's event log?
Next question: Which fires would the user, on seeing the morning card, have wished never happened, and can that be learned from their next action?
