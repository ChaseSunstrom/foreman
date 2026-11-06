# Brainstorm — lens: simplicity

- **Make one trigger table the only trigger surface** — CLEAN — value 5 — effort M — risk low — category: triggers
  Why: Mission asks for schedules, file, event, CI and issue triggers; the pack shows `fm night` ticks, `fm triggers`, `fm ci-watch` as three separate mechanisms. Assumption: they share no common record today.
  Done when: one file (`triggers.toml`) lists every active trigger with kind, action, budget and last-fired, and `fm night`, `ci-watch` and file watchers all read only it.

- **Use one tick, not many timers** — FEATURE — value 5 — effort S — risk low — category: scheduling
  Why: the user already installed the `fm night` timer; installs are queued for one yes, so each new timer costs a yes. Assumption: one tick can poll files, CI and issues cheaply.
  Done when: adding a schedule, file watch and CI watch installs zero new units; the existing tick fires all three in a test with a fake clock.

- **Poll instead of daemon-watch files** — PERFORMANCE — value 3 — effort S — risk low — category: file triggers
  Why: inotify watchers need a long-lived process (a unit to approve); a stat-compare per tick needs none. Assumption: sub-minute latency isn't needed for self-triggered work.
  Done when: editing a watched path causes a lane to be filed within one tick, with no new process running between ticks.

- **Cap every trigger with one budget line** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: standing rule says triggers must not storm; "Break trigger storms with a per-trigger budget" appears in earlier ideas but not as a field of the table. Assumption: not yet enforced.
  Done when: a trigger with `max_per_day=2` fires twice in a replay of ten events and logs the eight suppressed ones.

- **Queue installs as one `fm yes` card** — FEATURE — value 4 — effort S — risk low — category: installs
  Why: Mission text: "installs (timers, units) queued for one yes." Grants already exist (`fm ask --later`). Assumption: today each install is its own ask.
  Done when: three pending installs show as one list; one answer applies or refuses all, and the receipt names each unit file written.

- **Default every trigger to file-a-task only** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: the cheapest safe action is filing a task into the existing queue, which `fm next` already handles; no new runner is needed. Issue and CI text is untrusted input.
  Done when: a fired trigger produces a queue entry and no lane or edit; a flag `--run` is needed for anything more and is refused for issue-sourced triggers.

- **Dry-run a trigger on last week's events before it arms** — FEATURE — value 3 — effort M — risk low — category: validation
  Why: `fm triggers` already measures precision per trigger; reuse it as the arming gate. Assumption: the event history is stored.
  Done when: `fm trigger add` prints "would have fired N times" from the log and refuses to arm at N above its budget.

- **Delete a trigger that nobody acts on** — CLEAN — value 3 — effort S — risk low — category: triggers
  Why: `fm triggers` has precision; a trigger below a floor for 30 days costs a tick and attention. Assumption: precision data exists per trigger.
  Done when: a trigger with zero adopted firings in 30 days is moved to `triggers.retired` with a one-command restore.

- **Fill the 59 cells by rule, not by cell** — CLEAN — value 4 — effort M — risk med — category: coverage
  Why: the request says fill 59 empty cells, yet standing rule rejects templated cells. Assumption: most cells collapse to three real mechanisms (tick, table, queue) plus recorded n/a by nature (e.g. Desktop × operate).
  Done when: each cell names a concrete file path or a dated n/a with an adversary probe, and the templating linter reports zero duplicates.

- **Wild: Make the trigger table a single sentence per row** — FEATURE — value 3 — effort S — risk low — category: UX
  Why: wild. Rows read like "when CI on main goes red, file a fix task, at most 2 a day"; a parser maps the sentence to fields so the user edits plain text.
  Done when: five example sentences parse to the same records as their toml equivalents, and an unparsable sentence is rejected with the reason.

- **Wild: Let a missing tick be the alarm** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: wild. The night tick logs only on events, so silence is ambiguous. One heartbeat line per day proves it is alive without noise.
  Done when: killing the timer for 26 hours makes `fm doctor` print "no tick since …" and a restored tick clears it.

- **Wild: Make the whole self-trigger layer ~100 lines** — CLEAN — value 4 — effort L — risk med — category: simplicity
  Why: wild. Set a line budget for the feature; every new trigger kind must fit the same table row shape or be refused.
  Done when: schedule, file, CI and issue kinds all pass their tests with the trigger module under the budget, enforced in the lean ratchet.

- **Wild: Reuse the user's cron instead of owning timers** — FEATURE — value 2 — effort S — risk low — category: installs
  Why: wild. Emit one crontab line for the one tick rather than systemd units; fewer files, simpler uninstall.
  Done when: `fm trigger install --cron` prints the single line, and removal deletes exactly that line.

Next question: Does the existing night tick already poll anything besides the clock, and what is its measured cost per tick on an idle repo?
Next question: Which of the 59 empty cells are about triggers at all, and which are cells the Mission merely inherits from other surfaces?
