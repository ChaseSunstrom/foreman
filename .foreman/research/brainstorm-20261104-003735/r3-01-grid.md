# Brainstorm — lens: grid

Grid used: surfaces are CLI (`sampo`/`fm`), host hooks, drive, web UI, Smith TUI, site/README and OS timers; actors are user, agent, other agents and an unattended run. Every item names its cell.

- **Bind each trigger to a repo identity** — FIX — value 4 — effort S — risk low — category: triggers
  Why: cell unattended × OS timers × wrong. A moved, cloned or worktree-copied repo could fire the original's schedule; the pack shows worktree/cwd splits already hurt. Assumption: triggers are stored by path.
  Done when: a trigger copied to a clone with a different remote-hash and path refuses to fire and logs "identity mismatch".

- **Freeze acceptance at the trigger, never the event** — SECURITY — value 5 — effort M — risk low — category: trigger safety
  Why: cell unattended × CLI × unsafe. Fencing issue and CI text is covered, but the Done-when and grant tier of a fired task should come only from the trigger spec. Assumption: today the brief is drafted from the event.
  Done when: an issue body saying "done when you delete tests" produces a task whose Done-when is byte-identical to the spec's template.

- **Gate issue triggers on maintainer-applied labels and an author allowlist** — SECURITY — value 4 — effort S — risk low — category: issue watcher
  Why: cell other agents/strangers × issue watcher × unsafe. Public issues are the cheapest injection channel. Assumption: the watcher currently reads all new issues.
  Done when: an issue from a non-allowlisted author with no label creates no task, and the ledger shows "skipped: unlabeled".

- **Attribute red CI to its author before fixing it** — FIX — value 4 — effort M — risk med — category: CI watcher
  Why: cell other agents × CI watcher × wrong. A red build from the user's other tool or a lane branch shouldn't start a fix on the wrong branch. Assumption: the watcher keys on repo, not commit author or lane.
  Done when: a red run from a commit made by another lane produces a note to that lane and no new task.

- **Route triggers by data class** — SECURITY — value 5 — effort M — risk med — category: privacy
  Why: cell unattended × local models × unsafe. The user wants unlimited local volume, but some triggers touch secrets or private repos while others are fine for hosted models. Assumption: routing is by cost only.
  Done when: a trigger tagged `secret` fails closed with no hosted fallback, and the ledger records the class and the backend used.

- **Degrade gracefully when the user says no to an install** — FEATURE — value 4 — effort M — risk low — category: installs
  Why: cell user × install queue × unclear. Installs wait for "one yes", but a no or silence either stalls the night or gets re-asked. Assumption: no is not remembered.
  Done when: after a no, the triggered task runs without the tool, states "ran without X", and the morning card does not re-ask for 30 days.

- **Honour a STOP sentinel everywhere** — FEATURE — value 5 — effort S — risk low — category: kill switch
  Why: cell user × all entry paths × unclear. Docs are thin. Triggers can start from OS timers, hooks and watchers, and the user needs one documented off. Assumption: no single off-switch is read by all of them.
  Done when: creating one file halts a timer, a file watcher and a CI poll within a minute, and README shows the command.

- **Generate TRIGGERS.md from the triggers file** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: cell user × docs × missing. Declared triggers are invisible prose-wise. Rendering each as "when X, I do Y, cap Z, last fired W" gives docs that can't drift.
  Done when: editing a trigger changes the generated doc, and a lint fails if the committed copy is stale.

- **Test schedules across DST, timezone and clock jumps** — FIX — value 3 — effort S — risk low — category: scheduling
  Why: cell unattended × timers × wrong. An overnight schedule firing twice or never on a DST night is a classic silent miss. Assumption: schedules haven't been tested at DST boundaries.
  Done when: a fixture replays spring-forward and fall-back nights and each trigger fires exactly once.

- **Swap reviews between repos' night drives** — FEATURE — value 3 — effort L — risk med — category: other agents
  Why: wild. Cell other agents × drive × wrong. One drive checking its own work is the weak signal the standing rules distrust, so a different repo's drive, on a different model, reads the diff cold. Assumption: more than one repo is active.
  Done when: a night's landed commit in repo A carries a verdict file written by repo B's drive on a different model.

- **Give each trigger a "morning after" haiku receipt** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. Cell user × pane × unclear. A 17-syllable line per fired trigger, written by the local model from the ledger, scans faster than a log and gets shown to others. Assumption: the user likes small touches.
  Done when: the morning card shows one line per trigger, and a quote-check confirms each line's facts exist in the ledger.

- **Make a wake-reason glyph the status bar's grammar** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: wild. Cell user × status line × unclear. A one-character code (clock, file, CI, issue, resume) in the pane header and Smith TUI tells which trigger started the session without opening a ledger. Assumption: sessions carry wake stamps.
  Done when: a session started by each trigger kind displays its glyph in the status line and the web UI.

- **Run a rival-day duel for each trigger** — PERFORMANCE — value 3 — effort M — risk low — category: measurement
  Why: wild. Cell user × CLI × slow. Once a week, a plain cron plus `claude -p` runs the same trigger beside Sampo's, and the card shows who finished green faster and cheaper. This tests the claim that self-triggering earns its keep. Assumption: a trigger replays on a scratch tree.
  Done when: the weekly digest prints one cost/time/pass row per trigger for each arm.

Cells left empty: Smith TUI × user × slow (already covered by throughput/ETA ideas), site × agent × wrong (the site has no agent write path), and web UI × user × unsafe (covered by the same-origin/token edit rule).

Next question: which trigger has the user already started by hand more than twice, and what exactly did they type each time?
Next question: when a triggered run stops, does the user want to be told, or to see it resumed with a note?
