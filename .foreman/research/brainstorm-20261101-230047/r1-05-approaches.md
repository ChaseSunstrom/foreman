# Brainstorm — lens: approaches

Lens: approaches to self-triggering (#11). Every distinct way to make work start without the user, best first. Evidence is the pack's: fm night's tick already runs, fm ci-watch settles bets, fm triggers groups captures with precision, and installs are queued for one yes.

- **Run one event-envelope dispatcher inside the existing `fm night` tick** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: the tick already exists and logs only when something happens; schedules, file changes, CI results and issue changes can all be polled there as normalised events. This adds no new daemon, timer or unit, so there is nothing extra to install.
  Done when: a fixture file touch, a fake CI result and a fake issue each produce one envelope row in the tick log, and a second tick over the same inputs produces none.

- **Add a trigger table with a shadow mode before any trigger may start work** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: `fm triggers` already measures precision per trigger. A new trigger logs "would have started X" for N ticks and goes live only past a precision floor. Assumption: the precision metric is computed from the user's accept/ignore of captures.
  Done when: a new trigger stays in shadow, writes would-fire rows, and the first live fire happens only after the floor is met in a test.

- **Replay a candidate trigger on the last 30 days of recorded events before asking for its install yes** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: the install card then carries "this would have fired 6 times, 5 of them on things you later did by hand". The approach replaces guessing with the user's own history. Assumption: the event log keeps 30 days of ci, git and capture events.
  Done when: `fm triggers replay NAME` prints a count of fires and hits over a stored fixture history.

- **Bundle every install (timer, unit, hook) into one ranked yes card** — FEATURE — value 4 — effort S — risk low — category: installs
  Why: the mission says installs are queued for one yes, and the pack shows grants split across push, publish and install queues. One card shows each item's exact file diff and the work it unblocks.
  Done when: three queued installs render as one card, answering "yes" applies all three, and each can be reverted by one command.

- **Use git hooks and a path watcher instead of a poller for file and commit triggers** — FEATURE — value 3 — effort M — risk med — category: file triggers
  Why: an approach that trades the tick's delay for immediacy. Costs: hooks must be installed (queued for a yes), and they run on the user's critical path, so they must only write an event file and return within the hook budget.
  Done when: a commit writes an event envelope in under the hook latency budget and does nothing else.

- **Delegate scheduling to cron or systemd timers by generating the unit and never running a daemon** — FEATURE — value 3 — effort S — risk low — category: schedules
  Why: the user already installed Foreman's timers. The cheapest schedule approach is one generated timer per cadence that only calls `fm night tick`. This is less work than an in-process scheduler, with a diffable unit file for the yes card.
  Done when: `fm triggers install` emits a unit file and a dry-run diff, and refuses to write without a recorded grant.

- **Treat issue and CI text as untrusted and let watchers file tasks only, never run them** — SECURITY — value 5 — effort S — risk low — category: watchers
  Why: `fm ci-watch` already reads CI output, and issue text is attacker-controlled. The watcher's only action is to file a capture with fenced text; a lane starts later through the normal gate.
  Done when: a test issue body containing a shell command and an instruction produces a fenced task and no command execution.

- **Cap what a trigger may spend with a per-trigger budget and a storm breaker** — FEATURE — value 4 — effort S — risk low — category: safety
  Why: the "do nothing silently" failure of unattended work is the cost. A burst of 40 file events must debounce to one wake-up and stop at a budget.
  Done when: 40 events inside a window start one lane, and a second wake-up in the window is refused with a named reason.

- **Do less: a single `fm when` verb that writes a rule line into a plain file the tick reads** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: the minimal approach to schedules. Rules like "on ci red, draft fix" live in one text file, not a database. It reuses the tick and adds only a parser. Trade-off: less expressive than a full trigger table.
  Done when: a rule added with `fm when` fires once in a fixture tick and appears in `fm doctor`.

- **Land triggered work only on a morning branch with a one-command accept** — FEATURE — value 4 — effort S — risk low — category: safety
  Why: it removes the need to trust the trigger before it has earned it, since nothing reaches main unreviewed. Done when: a triggered lane's output is on `night/<date>`, main is unchanged, and `fm accept` merges it through `fm ship`.

- **Wild: Let a webhook-free "tripwire file" stop every trigger when the user touches it** — FEATURE — value 3 — effort S — risk low — category: safety
  Why: wild. The cheapest panic button is a file path that works from any shell, phone sync folder or file manager. Done when: creating the file makes the next tick skip all triggers and log one line.

- **Wild: Mine the user's own shell and git history to propose the triggers they would have written** — FEATURE — value 4 — effort L — risk med — category: discovery
  Why: wild. People repeat "pull, run tests, look at CI" at the same times. Foreman proposes a trigger from that pattern with its replay score. Assumption: shell history is readable locally and is never sent anywhere.
  Done when: given a fixture history, it proposes one trigger with a precision figure and files it in shadow mode.

- **Wild: Run a "daylight rehearsal" that replays a recorded night through the dispatcher** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: wild. It lets the whole self-triggering path be verified on the real path, as pillar 5 asks, without waiting for an actual night. Done when: a stored recorded-night file replays in minutes and its outputs match a golden log.

Next question: Which of the triggers the user already installed (fm night, ci-watch) have ever started work the user did not later revert or redo, and is that rate known?
Next question: Does the user want triggered work to wait for them on a branch, or to land on main under the existing push grant, and has that been said anywhere?
