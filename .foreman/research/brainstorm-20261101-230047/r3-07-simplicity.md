# Brainstorm — lens: simplicity

- **Make one trigger file the only trigger surface** — CLEAN — value 5 — effort M — risk low — category: triggers
  Why: the pack's ideas pile up many trigger families (schedule, file, CI, issue, git) with no shared home; the 59 empty cells fill faster when one table is the thing they cite. Assumption: today triggers are scattered across fm night, fm triggers, and ci-watch.
  Done when: `fm triggers list` prints every active trigger from a single plain file, and a test fails if any watcher fires without a row there.

- **Reuse the existing night tick for every trigger** — FEATURE — value 5 — effort S — risk low — category: scheduling
  Why: the user already installed Foreman's timers and the tick logs only on events; adding a second timer per trigger multiplies installs that each need a yes. Assumption: one tick can dispatch all families.
  Done when: adding a file, issue and CI trigger installs zero new timers, and the tick log shows each fire.

- **Make every watcher file a capture and never run work** — SECURITY — value 5 — effort S — risk low — category: safety
  Why: issue and CI text is untrusted, and the capture inbox already exists with precision grouping (fm triggers). One output path keeps the guard and hook budget unchanged.
  Done when: a planted issue body containing a shell command produces a capture row and no process start, proven by a test.

- **Generalise fm ci-watch into the one poller** — CLEAN — value 4 — effort M — risk med — category: watchers
  Why: ci-watch already settles ship bets (11 held in a row), so it works on the real path. Issue and PR watching are two more sources on the same loop, not new machinery.
  Done when: `fm ci-watch --source issues` files a capture from a fixture feed, using the same code path as the CI source.

- **Queue every install as one exact-text card** — FEATURE — value 4 — effort S — risk low — category: installs
  Why: the mission says installs get queued for one yes; a single file holding the exact unit text, enable command and uninstall line is the smallest thing that is honest to approve and easy to diff against disk.
  Done when: `fm yes` shows all pending installs on one screen, and approving one writes exactly the shown text (byte-compared in a test).

- **Fill the 59 cells by one rule per column** — CLEAN — value 4 — effort M — risk med — category: coverage
  Why: the steers say templated cells don't count, but each column (surface × stage) shares a mechanism; one probe per trigger family can stamp its cells with real output. Assumption: most cells collapse to about 6 mechanisms.
  Done when: the templating lint passes on all 59 cells and each cell cites a probe output that a rerun reproduces.

- **Land all self-started work on a night branch only** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: the user's rule on outward actions; a trigger that never touches the user's tree or main needs no extra consent design.
  Done when: a triggered lane's commits exist only on `night/<date>`, and a test shows main and the working tree unchanged.

- **Dry-run a trigger on last week before it arms** — FEATURE — value 4 — effort M — risk med — category: triggers
  Why: the steers prize precision over volume and Mission 3's lesson was that unmeasured ideas fail; a replay shows noise before the user is asked for a yes. Assumption: past events are logged enough to replay.
  Done when: `fm when --dry` prints how many fires the trigger would have made in the last 7 days, with the test using a recorded fixture.

- **Cap every trigger with one spend line and a storm breaker** — PERFORMANCE — value 3 — effort S — risk low — category: budget
  Why: an unattended start with no ceiling is the main way self-triggering goes wrong, and the existing budget code can be reused.
  Done when: a trigger firing 20 times in a minute stops after its cap and logs the stop reason.

- **Wild: Add `fm when "<sentence>"` that writes one table row** — FEATURE — value 4 — effort M — risk med — category: usability — wild
  Why: assumption: users say "when CI fails on main, draft a fix" more easily than they edit a file; the verb only parses into the same row, so it adds no new engine.
  Done when: the sentence "when CI fails on main, file a task" produces a row that a dry-run accepts.

- **Wild: Make a missing tick the alarm** — RELIABILITY via FIX — value 4 — effort S — risk low — category: reliability — wild
  Why: the night tick logs only on events, so silence cannot be told from death. A dead-man file touched each tick, checked at session start, answers it with no new daemon.
  Done when: with the tick stopped for two intervals, the next session start prints one line saying so.

- **Wild: Let the user touch one file to freeze every trigger** — FEATURE — value 3 — effort S — risk low — category: control — wild
  Why: a physical off switch is the simplest consent story for work that starts without the user. Assumption: a stat on the tick path costs nothing.
  Done when: with `FREEZE` present, a due trigger does not fire and the log records why.

- **Wild: Replay a recorded week through the dispatcher in daylight** — FEATURE — value 3 — effort M — risk med — category: testing — wild
  Why: it lets the unattended path be exercised without waiting a night, using the same fixtures as the dry-run.
  Done when: one command replays a fixture week and prints each fire and skip with reasons.

Next question: Which trigger families would the user actually leave on for a month, judging by what fm triggers precision already shows?
Next question: Can the 59 cells be generated from the trigger table itself, so adding a trigger can't leave a cell empty?
