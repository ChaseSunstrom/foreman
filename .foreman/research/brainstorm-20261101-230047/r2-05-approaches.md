# Brainstorm — lens: approaches

Lens: approaches. These are distinct ways to solve "work starts without the user; installs queued for one yes; fill the 59 empty cells", best first. Ideas already listed in the pack (trigger table, replay before install, one-yes card, drop folder, heartbeats) are not repeated; each item below is a different way to get there.

- **Reuse the host's scheduler: generate one cron/systemd-timer line per trigger, run no daemon** — FEATURE — value 4 — effort S — risk low — category: scheduling
  Why: assumption: the night tick already exists (`fm night` is installed and logs only on events), so a second timer family adds weight against the lean ratchet. A generated unit that just calls `fm tick --only NAME` makes the OS the scheduler and survives sessions dying.
  Done when: `fm trigger add` writes a unit file to a staging dir, nothing is enabled until the one-yes card is accepted, and `systemd-analyze verify` passes on it.

- **Make the capture inbox the only trigger output: every watcher files a capture, never runs work** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: pack shows `fm triggers` already groups captures by trigger with precision, and the round-first steer already holds Foreman-filed items. Reusing that path means CI, issue and file watchers get the existing hold, dedupe and precision stats for free.
  Done when: a fake failing CI run produces one capture tagged `trigger=ci`, appears in `fm triggers` with precision, and starts no lane until `fm next` offers it.

- **Fill the 59 cells by mechanism: one probe per trigger family that stamps all its cells** — CLEAN — value 4 — effort M — risk med — category: coverage
  Why: the standing rule forbids templated cells, so the family probe must emit distinct output per cell (surface x stage), not shared wording. Assumption: the 59 cells fall into about 6 families (schedule, file, git, CI, issue, install).
  Done when: `fm genesis check` reports 0 empty cells and the templating lint finds no two cells sharing a sentence.

- **Do less: make `ci-watch` the generic watcher and add issue/PR as two more sources** — FEATURE — value 4 — effort S — risk low — category: watchers
  Why: `fm ci-watch --last-ship` exists and settles 11 ship bets in a row. Extending its poll loop to issues and review requests is smaller than new infrastructure.
  Done when: `fm ci-watch --source issues` files a capture from a labelled test issue against a recorded fixture.

- **Gate each new trigger on a replay of the last 30 days of its own event type** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: Mission 3's lesson was that briefs were built or had no failure behind them. Replaying first shows the trigger would have fired on real failures before the user is asked for a yes.
  Done when: the install card shows "would have fired N times, M led to a task you kept" computed from logs, and a trigger with N=0 is refused.

- **Install queue as one append-only file of exact unit text, diffed against disk** — SECURITY — value 4 — effort S — risk low — category: installs
  Why: the standing intent says installs wait for one yes; the user needs to see exact bytes. Assumption: a checksum of the staged unit is stored and `fm doctor` flags disk drift from the approved text.
  Done when: editing an installed unit by hand makes `fm doctor` name it as drifted from the approved text.

- **Compile a declared `triggers.toml` in the repo, reviewed like code** — FEATURE — value 3 — effort M — risk med — category: config
  Why: assumption: team and multi-machine use want triggers versioned. The cost is a new file format, so it should be second to the capture route.
  Done when: a toml with two triggers round-trips to the trigger table, and a malformed key is named by `fm doctor`.

- **Add a per-trigger spend and storm breaker enforced in the tick** — RELIABILITY→FIX — value 4 — effort S — risk low — category: safety
  Why: a trigger that fires on its own output is the classic failure; the pack's pace/budget steers say waits are fine but cost caps stay.
  Done when: a trigger that fires 5 times in 10 minutes is disabled with a named reason and one line in the morning note.

- **Wild: Treat the user's repeated manual sequences as the trigger source, proposing `fm when` rules from shell history** — FEATURE — value 3 — effort L — risk med — category: discovery
  Why: wild; assumption: shell history is readable locally and never leaves the machine. It answers "what will they want next" without asking.
  Done when: given a fixture history with the same three commands each Monday, it proposes one weekly trigger with its replay.

- **Wild: Fire a harmless fake failure weekly through the real chain to prove it is alive** — FEATURE — value 3 — effort M — risk low — category: liveness
  Why: wild; answers the pack's "guard that never fires: alive or silent?" question for triggers. A planted event, labelled as synthetic, must reach a capture.
  Done when: the weekly drill's capture appears tagged `synthetic`, and a missing one turns `fm doctor` red.

- **Wild: Let a plain sentence in chat ("when CI fails on main, draft a fix") compile to a trigger draft** — FEATURE — value 4 — effort M — risk med — category: authoring
  Why: wild; the user already speaks steers in prose, and `fm decide --check` turns steers into checks, so the same intake can emit triggers.
  Done when: the sentence yields a draft trigger plus a replay preview, with nothing installed until yes.

- **Wild: Make a missing tick itself the alarm, via a dead-man file checked by the next session** — RELIABILITY→FIX — value 3 — effort S — risk low — category: liveness
  Why: wild; silence is the dominant failure of schedulers, and the night tick logs only on events, so quiet and dead look identical.
  Done when: stopping the timer for 2 intervals makes the next `fm status` print "tick silent since T".

Next question: Which of the 59 cells are about surfaces the user has never opened, and could a real trace of what they touch shrink the list before filling any?
Next question: When two triggers want the same lane while the usage window is closed, which one waits, and who decides without asking the user?
