# Brainstorm — lens: approaches

- **Generate one OS timer line per trigger, run no daemon** — FEATURE — value 5 — effort S — risk low — category: scheduling
  Why: the user already installed `fm night` timers and the tick works; the pack asks for "installs (timers, units) queued for one yes". Reusing cron/systemd means no new long-lived process to guard, budget or heartbeat.
  Done when: `fm when add` on a fixture trigger prints the exact unit text, and after the yes `systemctl --user list-timers` (or the cron fixture) shows it, with no new resident process.

- **Make the capture inbox the only watcher output** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: `fm triggers` already groups captures by trigger with precision, and the standing rule says self-filed items are held until the round's seed. Watchers (CI, issue, file) that only file captures can't run untrusted issue text.
  Done when: a fixture issue containing an injected command produces one capture row, and no lane or command starts from it.

- **Generalise `fm ci-watch` into a generic watcher with issue and PR sources** — FEATURE — value 4 — effort M — risk med — category: watchers
  Why: `ci-watch` settles ship bets (11 held in a row) and `--last-ship` exists (T-2527), so the polling, auth and settle code is proven. Adding sources reuses it instead of building a second poller.
  Done when: `fm watch issues` against a recorded API fixture files one capture per new issue and none on a second poll.

- **Replay a candidate trigger on the last 30 days before it may install** — FEATURE — value 5 — effort M — risk low — category: precision
  Why: Mission 3's lesson was that briefs were built or never had a failure behind them; `fm triggers` already measures precision per trigger. A replay shows the fire count and hit rate on real history before the one yes.
  Done when: `fm when preview` prints would-have-fired count and precision for a trigger, and a trigger below a stated floor is refused with the numbers.

- **Declare triggers in one committed `triggers.toml`** — FEATURE — value 4 — effort M — risk low — category: registry
  Why: the 59 empty coverage cells need concrete, non-templated entries; one registry means a cell can cite a row (assumption: cells are filled per trigger family, and a registry is the cheapest stable thing to cite).
  Done when: `fm doctor` lists each registry row with last-fired time and fails on a row naming a missing action.

- **Land self-started work on a `night/<date>` branch only** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: the user's rules say pushes go through `fm ship` and merges are user-only; unattended work with a branch limit can't touch main or the user's working tree.
  Done when: a triggered fixture lane commits only to `night/<date>`, and a test that attempts a push to main from it is denied.

- **Add a dead-man beat so a silent tick is distinguishable from a dead one** — FIX — value 4 — effort S — risk low — category: reliability
  Why: "the night tick logs only when something happens" means a dead timer and a quiet night look identical (the pack's own unanswered question about a guard that never fires).
  Done when: killing the timer in a fixture makes the next `fm doctor` or session start print "tick silent for N h", and a quiet healthy night does not.

- **Fill the 59 cells by mechanism: one probe per trigger family stamps its cells** — CLEAN — value 4 — effort M — risk med — category: coverage
  Why: the standing rule rejects templated cells, and a probe's output gives each cell a distinct, grounded sentence (file, event, count) rather than swapped words.
  Done when: each of the 59 cells names a distinct file or probe output, and the sweep's templating check passes.

- **Cap each trigger's spend and break storms** — SECURITY — value 4 — effort S — risk low — category: budget
  Why: assumption: file and event triggers can burst; the standing rules say no spawn without a cost ceiling and wait out real limits rather than skip work.
  Done when: a fixture firing 50 events in a minute yields one coalesced run, and a trigger over its budget parks with a named reason.

- **Wild: compile a typed sentence ("when CI fails on main, draft a fix") into a trigger draft** — FEATURE — value 4 — effort M — risk med — category: natural language
  Why: wild; the user's steers are already sentences. Assumption: a restricted grammar over known event kinds avoids a model dependency.
  Done when: the sentence yields a `triggers.toml` row shown on the install card, and an unparseable sentence is refused with the nearest valid form.

- **Wild: propose triggers from the user's own repeated manual sequences** — FEATURE — value 4 — effort L — risk med — category: mining
  Why: wild; the "asked" stream and shell history show what the user does by hand. Assumption: local history is readable and stays on the machine.
  Done when: on a fixture history with one sequence repeated 5 times, `fm when suggest` proposes exactly that trigger with its count.

- **Wild: run a daylight rehearsal that fast-forwards a recorded week through the dispatcher** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: wild; installs are irreversible-ish and a rehearsal checks storms, catch-up and coalescing without waiting a week.
  Done when: replaying a recorded fixture week in under a minute prints fires, skips and spend per trigger, matching expected counts.

- **Wild: a tripwire file the user touches to freeze every trigger** — FEATURE — value 3 — effort S — risk low — category: control
  Why: wild; the pack has no single stop for unattended work, and the user's rule is that autonomy shouldn't need a session to halt.
  Done when: creating the file makes the next tick fire nothing and log "frozen", and removing it resumes.

- **Do less: make `fm night`'s tick the only dispatcher and defer other timers** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: one installed tick already works; adding timers per trigger multiplies install yeses. Trade-off: coarser timing, and ticks are the only schedule granularity.
  Done when: three registry rows produce zero new installed units and fire from the one tick in a fixture.

Next question: Which triggers would the user actually say yes to, judging from the shape of the `fm triggers` captures they acted on versus ignored?
Next question: What happens to a trigger's queued install yes if the user is away for a week, and does an unanswered card age into something visible?
