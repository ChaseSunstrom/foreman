# Brainstorm — lens: approaches

Lens: approaches. Every distinct way to get "work starts without the user" and fill the 59 cells, best first. Earlier rounds already cover the tick, the trigger table, the install card, replay, heartbeats, branch landing and drop folders, so these go to the less-covered corners.

- **Make `fm when` write one rule line into a plain file the tick reads** — FEATURE — value 5 — effort S — risk low — category: triggers
  Why: assumption: `fm night`'s tick already runs, and the user installed it, so a text file of `on <event> do <verb>` lines is the least new machinery. One yes installs nothing new, because the timer already exists.
  Done when: `fm when "ci fails on main" "fm ci-fix"` appends one line, the next tick fires it on a fixture failure, and `fm night` logs which line fired.

- **Derive the 59 cells from the trigger table by column rule** — CLEAN — value 4 — effort M — risk med — category: coverage
  Why: the pack's rule says a cell counts only if it names a concrete capability with no reused phrasing, and a column rule that stamps cells would be called templated. So each cell must cite its own probe output (the trigger family, the surface and the stage together), not a shared sentence.
  Done when: each of the 59 cells names a distinct probe command and its recorded output, and the templating lint passes on all 59.

- **Generalise `fm ci-watch` into a source-pluggable poller** — FEATURE — value 5 — effort M — risk med — category: watchers
  Why: ci-watch already settles 11 ship bets in a row, so issue, PR and review-comment sources are new adapters on a proven loop, not a new daemon. Every source files a capture and never runs work.
  Done when: a fixture issue and a fixture PR comment each produce one capture with an origin stamp, and the poller's replay test passes on a recorded response.

- **Install by committed `triggers.toml`, diffed against disk** — FEATURE — value 4 — effort M — risk med — category: installs
  Why: gen-0 says installs queue for one yes. A reviewable file whose exact unit text the card shows, plus a diff against what is on disk, makes that one yes auditable and repeatable.
  Done when: `fm doctor` reports "no drift" after an install, and a hand-edited unit is flagged by the diff.

- **Delegate scheduling to the host: emit one OS timer line per trigger** — FEATURE — value 3 — effort M — risk med — category: installs
  Why: this is the no-daemon approach, with systemd on this Linux box and launchd or Task Scheduler elsewhere. The trade-off is that every OS gets its own code path, but missed-run catch-up comes free with `Persistent=true`.
  Done when: a trigger renders valid unit text for systemd, and `systemd-analyze verify` passes on it.

- **Arm the CI watch from `fm ship` itself** — FEATURE — value 4 — effort S — risk low — category: ci
  Why: recent commits show `--last-ship` already exists, so the evidence is that the user is still arming it by hand. Shipping should start the watch with no extra yes, since the push was already granted.
  Done when: after a ship, a pending ci-watch row exists with the pushed commit, and it settles on the fixture run.

- **Start work from a drop folder and from git events, by polling** — FEATURE — value 3 — effort S — risk low — category: file triggers
  Why: assumption: polling in the existing tick avoids inotify and a daemon. The cost is latency of up to one tick, which is fine for work that is meant to run unattended.
  Done when: a file dropped in the folder yields one capture within one tick, and a repeat of the same file yields none (idempotency key).

- **Do less: leave schedules to the user's own cron and only document the line** — CLEAN — value 2 — effort S — risk low — category: scheduling
  Why: this is the minimal approach, and it is honest about the trade-off: no catch-up, no install card, no heartbeat. It is a fallback for headless boxes.
  Done when: `fm when --print-cron` outputs a line that a stranger can paste, with no files written.

- **Wild: compile a chat sentence into a trigger draft** — FEATURE — value 4 — effort M — risk med — category: natural language
  Why: wild. The user already types intent in plain words; "when CI fails on main, draft a fix" becomes a draft rule line shown on the one-yes card. A tool-less child parses it and the output is validated against the rule grammar.
  Done when: five sentences compile to the expected lines on a fixture set, and an unparseable one is refused with a reason.

- **Wild: mine shell and git history for the triggers the user would have written** — FEATURE — value 4 — effort M — risk med — category: discovery
  Why: wild. Repeated manual sequences are the strongest evidence of a wanted trigger. The mining runs locally only, and each proposal shows the number of times it was seen.
  Done when: a fixture history with a command run on a weekly cadence produces a proposed rule that cites its occurrence dates.

- **Wild: let a missing tick be the alarm** — RELIABILITY (FIX) — value 4 — effort S — risk low — category: liveness
  Why: wild. Today "the night tick logs only when something happens", so a silent tick looks the same as a dead one. A dead-man file touched every tick lets the next session say "no tick for 31 hours".
  Done when: a stopped timer on a fixture produces a stale warning in `fm doctor` and at session start, and a live quiet tick produces none.

- **Replay a candidate trigger on the last 30 days before it can arm** — SECURITY — value 4 — effort M — risk low — category: safety
  Why: it answers "would this have been noise?" using the user's real history. It also tests the earlier concern that triggers should earn their place, using precision from `fm triggers`.
  Done when: a rule with a fixture history reports its would-have-fired count and refuses to arm above a stated storm threshold.

- **Tag every self-started task with its trigger, and answer `fm why`** — FEATURE — value 3 — effort S — risk low — category: provenance
  Why: assumption: with several sources, the user will ask why something started. One origin field on captures and tasks makes "why did or didn't this fire" a lookup.
  Done when: `fm why T-NNNN` prints the rule line, the event and the time for a self-started task, and "user" for a typed one.

Next question: which of the 59 cells are cells where a self-started run is unsafe by nature (anything touching push or install), and can that be one recorded rule instead of 59 judgments?
Next question: does the user ever read the night tick's log, or only the final report, so that the morning note is the one surface this mission must get right?
