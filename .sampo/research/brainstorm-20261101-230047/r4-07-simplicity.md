# Brainstorm — lens: simplicity

- **Make `fm night`'s tick the only dispatcher** — CLEAN — value 5 — effort M — risk low — category: triggers
  Why: the night tick already runs, logs only on events, and the user installed it; every extra timer is another unit to queue, install, heartbeat and uninstall. One tick reading one table means one install yes ever.
  Done when: `fm triggers list` shows schedule, file, CI and issue triggers all fired by the same tick, and `fm doctor` counts exactly one installed timer.

- **Store triggers as one-line rules in a plain file** — FEATURE — value 5 — effort S — risk low — category: triggers
  Why: the pack's many table/registry/toml ideas collapse to a single readable format. Assumption: one line per rule (`when ci-fail main -> task draft-fix`) is enough for the 59 cells.
  Done when: adding a line to the file makes the next tick honour it, and a malformed line is named by line number in `fm doctor` without stopping other rules.

- **Limit every trigger's action to filing a capture** — SECURITY — value 5 — effort S — risk low — category: safety
  Why: CI, issue and PR text is untrusted, and the existing capture inbox plus `fm next` already turn work into lanes under the guard. Triggers that only file need no separate sandbox or budget system.
  Done when: a test feeds an issue body containing a command and a capture appears with the text fenced as data, and no process was spawned.

- **Extend `fm ci-watch` into the one poller for issues and PRs** — FEATURE — value 4 — effort M — risk med — category: watchers
  Why: ci-watch already settles 11 ship bets in a row; the poll-and-settle shape is proven. Adding two sources beats building a new watcher family.
  Done when: `fm ci-watch --source issues` files a capture for a new labelled issue exactly once across two ticks.

- **Show every queued install as exact unit text on one card** — FEATURE — value 4 — effort S — risk low — category: installs
  Why: the mission says installs get "one yes". Simplest honest form is a single file holding the literal text to be written, diffed against disk.
  Done when: `fm yes` prints all pending unit/timer texts with their target paths, and one answer installs them and nothing else.

- **Fill the 59 cells with one rule per column** — CLEAN — value 4 — effort M — risk med — category: coverage
  Why: standing rule says templated cells don't count, so the fill must name a concrete path per cell. Assumption: columns (stages) share a mechanism, so a probe stamps the cell from its output while each cell still names its own file.
  Done when: the coverage linter reports zero empty and zero templated cells, each citing a distinct file or probe output.

- **Catch up missed ticks once, with a cap** — FIX — value 4 — effort S — risk low — category: reliability
  Why: a laptop that sleeps misses timers; replaying N fires would be a storm. Run each missed schedule at most once on wake.
  Done when: a test that skips 3 days of ticks results in one fire per schedule.

- **Write a beat file on every tick** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: the pack notes the tick logs only on events, so silence can't be told from death. One timestamp file read at session start fixes it.
  Done when: killing the timer makes the next SessionStart print "tick silent for N hours".

- **Land self-started work on a `night/<date>` branch only** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: push grant exists but unattended work should never touch main. A branch name is the cheapest boundary.
  Done when: a triggered lane's commits are on `night/…` and `git log main` is unchanged.

- **Add `fm why TRIGGER`** — FEATURE — value 3 — effort S — risk low — category: explainability
  Why: assumption: users distrust silent automation; the fired/not-fired reason is already computed by the tick.
  Done when: the command prints the last decision and its reason for a named rule.

- **Wild: Let a missing beat be the alarm** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: wild — no extra monitor; the next session's start is the watchdog.
  Done when: a stale beat file produces a one-line warning and a captured task.

- **Wild: Make the whole trigger layer fit in 100 lines** — CLEAN — value 3 — effort M — risk med — category: lean
  Why: wild — the lean ratchet makes growth pay; a line budget forces reuse of the tick, capture inbox and ci-watch.
  Done when: a test asserts the trigger module stays under 100 lines and still passes the family probes.

- **Wild: Use the user's existing cron instead of owning timers** — APPROACH-as-FEATURE — value 3 — effort S — risk low — category: installs
  Why: wild — print one crontab line for the yes card and run no unit at all; fewer install kinds to verify.
  Done when: `fm yes` offers a single crontab line and the tick runs from it.

- **Wild: Compile a chat sentence into one rule line** — FEATURE — value 3 — effort M — risk med — category: triggers
  Why: wild — "when CI fails on main, draft a fix" becomes one file line, so the user never learns a syntax.
  Done when: `fm when "<sentence>"` appends a rule and echoes it for confirmation.

Next question: which of the 59 cells are only reachable by a session path no trigger calls, and would deleting those cells be simpler than filling them?
Next question: if the tick were removed, which trigger family would the user notice missing first?
