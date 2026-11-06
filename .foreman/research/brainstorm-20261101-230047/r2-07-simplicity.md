# Brainstorm — lens: simplicity

- **Fill the 59 cells by one rule per column, not one prose cell each** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the pack's rule says templated cells don't count, yet 59 are empty. Self-triggering cells collapse to ~4 real mechanisms (tick, git hook, poll, drop folder). Cells then cite the mechanism's file and probe, so each names a concrete path.
  Done when: `fm genesis sweep` reports 0 empty #11 cells and no templated or duplicate flag, each cell naming a distinct file or recorded n/a.

- **Use one tick and one trigger table as the only trigger surface** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: `fm night` already ticks and logs only on events; schedules, file, CI and issue watchers can all be rows in one plain file that the tick reads. No new daemon.
  Done when: adding one row to the table makes the next tick fire it, and `fm triggers` lists every row with its last fire.

- **Default every trigger to "file a task" only** — SECURITY — value 5 — effort S — risk low — category: safety
  Why: issue and CI text are untrusted. A watcher that only captures an inbox item cannot run injected text. The existing capture inbox and `fm triggers` precision already exist.
  Done when: a test feeds a poisoned issue body to the watcher and the result is one captured task with fenced text and no process spawned.

- **Queue every install as one `fm yes` card** — FEATURE — value 4 — effort S — risk low — category: consent
  Why: the mission says installs queue "for one yes". Timers, units and hooks are generated as text, shown with the enable and uninstall lines, and spent once.
  Done when: three queued installs show as one card; answering once installs exactly those three and logs a receipt.

- **Poll instead of watching: ci-watch and issue watch share one poller** — SIMPLIFY — type CLEAN — value 4 — effort M — risk low — category: watchers
  Why: `fm ci-watch` exists and settles bets; an issue watcher is the same shape (fetch, diff against last seen, emit). Sharing one poller avoids two code paths.
  Done when: both watchers run through one function and the existing ci-watch tests pass unchanged.

- **Dry-run a trigger on last week's events before it arms** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: the pack's precision data (`fm triggers`) shows triggers vary in value; a replay prints "would have fired N times, M you acted on" before the yes.
  Done when: `fm when --dry NAME` prints a fire count over 7 days from recorded events without starting any work.

- **Cap every trigger with one budget line** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: storms and repeat fires are the main failure of self-triggering. One per-trigger cap (fires per day, dollars) in the table covers a storm and a runaway cost.
  Done when: a synthetic burst of 50 events yields at most the capped number of lanes and a single "capped" log line.

- **Delete a trigger nobody acts on** — CLEAN — value 3 — effort S — risk low — category: triggers
  Why: the lean steers want subtraction by evidence. `fm triggers` already measures precision; below a floor for N fires the tick proposes removal, never silently.
  Done when: a trigger with 0 of 10 acted-on fires appears in the next morning note as a one-word remove proposal.

- **Catch up missed schedules once, coalesced** — FIX — value 3 — effort S — risk med — category: schedules
  Why: assumption: timers on a laptop miss runs during sleep; N missed fires should become one run.
  Done when: simulating three missed daily slots produces one run and one log line stating how many were coalesced.

- **Wild: Let a missing tick be the alarm** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: wild. Silence from a log that logs only on events looks identical to a dead timer. A heartbeat file's age checked by `fm doctor` distinguishes them without any planted event.
  Done when: stopping the timer makes `fm doctor` name "tick last ran X ago" within one expected interval.

- **Wild: Make the whole self-trigger layer about 100 lines on top of cron** — CLEAN — value 3 — effort M — risk med — category: simplicity
  Why: wild. Generate one crontab or systemd timer line that runs `fm night tick`, and put all logic in the table-reading tick. The OS owns scheduling, Foreman owns nothing resident.
  Done when: the install card shows a single line, and removing it leaves no Foreman process or file other than the table.

- **Wild: A `fm when "<sentence>"` verb that writes one table row** — FEATURE — value 3 — effort M — risk med — category: triggers
  Why: wild. A plain-English line like "when CI fails on main, file a task" is compiled to a row and shown for confirmation; no config language to learn.
  Done when: three sample sentences produce the expected rows, and an ambiguous one asks a single question.

- **Land self-started work on a `night/<date>` branch only** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: unattended work never touching main or the user's tree is the simplest safe rule and fits the standing merge-protection steers.
  Done when: a triggered lane's commits exist only on the branch, and `fm accept` is the sole way to merge them.

Next question: Which of the 59 cells are n/a by mechanism, and can one rule record that for every row at once?
Next question: What does the user do within five minutes of the morning note, and should the note be shaped by that instead of by the night's output?
