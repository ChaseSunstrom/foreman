# Brainstorm — lens: bold bets

- **Compile a sentence into a trigger** — FEATURE — value 5 — effort M — risk med — category: triggers
  Why: wild. Assumption: users think "when CI fails on main, draft a fix", not cron or unit syntax. `fm when "<sentence>"` writes one row to a plain trigger table that the existing `fm night` tick reads, and the install, if any, goes to the one-yes queue.
  Done when: `fm when "when CI fails on main, draft a fix"` adds one row, `fm triggers` lists it with its source, action and budget, and a fixture CI failure makes the tick file one task tagged with that trigger.

- **Replay a trigger on last month before it arms** — FEATURE — value 5 — effort M — risk low — category: safety
  Why: `fm triggers` already scores captures by precision, and Mission 3 showed three of five briefs had no failure behind them. Assumption: enough recorded events exist to replay.
  Done when: a new trigger shows "would have fired N times in 30 days, M of them on events the user then acted on" before the install yes, and refuses to arm at 0 matches without an override.

- **Run a night shift that lands on a branch** — FEATURE — value 5 — effort L — risk med — category: unattended
  Why: self-started work must never touch the user's tree. A charter file sets budget, hours and a stop file. Work lands on `night/<date>`, with a one-command accept or discard.
  Done when: a timed shift run leaves the main tree byte-identical, produces a branch with a morning note, and `fm night accept` merges it through the normal gate.

- **Install every timer through one ranked yes card** — FEATURE — value 4 — effort M — risk low — category: installs
  Why: the mission says installs are "queued for one yes". Assumption: queued installs are currently separate items. The card shows exact unit text, the enable and uninstall commands, and a diff against what is on disk.
  Done when: three queued installs render as one card with one-word answers, and a "yes" writes only the unit text the card showed.

- **Beat every timer from outside** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: the night tick logs only when something happens, so silence can't be told from death. A dead-man file is checked at the next session start.
  Done when: killing the tick for 2 intervals makes the next SessionStart print one line naming the stale timer, and a healthy quiet tick prints nothing.

- **Mark untrusted issue and CI text as data in watchers** — SECURITY — value 5 — effort M — risk low — category: injection
  Why: issue watchers read text anyone can write. Watchers may only file captures, never run commands from that text. A fenced body goes into the lane brief.
  Done when: a fixture issue containing "run rm -rf" files a capture and a lane brief that quotes it as data, and no command from it reaches a Bash call.

- **Fire a trigger on a drop folder and on git events** — FEATURE — value 4 — effort M — risk low — category: file triggers
  Why: the mission names file triggers. Polling in the tick means no daemon. Each file gets an idempotency key from its content hash, and bursts debounce into one wake.
  Done when: three files dropped in 10 seconds make one task, and dropping the same file again makes none.

- **Hold fires while the user is mid-flow** — FEATURE — value 4 — effort S — risk low — category: etiquette
  Why: assumption: a lane that starts while the user is typing in the same repo is a nuisance. Check recent edit and prompt times, and defer and coalesce.
  Done when: with an edit inside the last 5 minutes, a due trigger waits, and afterwards a single fire runs, not one per missed interval.

- **Fill the 59 cells by trigger family, not by cell** — CLEAN — value 4 — effort M — risk med — category: coverage
  Why: the standing rule says templated cells don't count. Build a registry of five families (schedule, file, git, CI, issue). One probe per family emits grounded output that each cell cites.
  Done when: the 59 cells each name a concrete registry row and probe, and the templating lint finds no repeated phrasing.

- **Explain why a trigger did or didn't fire** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: a silent tick leaves the user guessing. `fm triggers why NAME` prints the last evaluation with its inputs, which gate held it and what comes next.
  Done when: for a trigger held by the budget cap, the output names the cap and the reset time.

- **Wild: Fire a weekly canary event through the real chain** — FEATURE — value 4 — effort M — risk low — category: liveness
  Why: wild. A harmless fake CI failure goes through the watcher, tick, lane and morning note, and times the whole path end to end.
  Done when: the weekly canary shows up in the morning note with a latency, and breaking the watcher makes the next canary report red.

- **Wild: Rehearse a recorded week in daylight** — FEATURE — value 4 — effort L — risk low — category: rehearsal
  Why: wild. `fm watch --dry-week` replays a recorded week of events at speed through the dispatcher with a stubbed model, so the user sees what a week of triggers would have done before any timer installs.
  Done when: the replay prints a timeline of fires, spend and tasks filed, and writes nothing outside a scratch directory.

- **Wild: Touch one file to freeze everything** — FEATURE — value 3 — effort S — risk low — category: control
  Why: wild. A tripwire file is the user's panic button. Every trigger and lane checks it, and no network or session is needed.
  Done when: creating the file stops a running lane within one tick and blocks new fires. Removing it resumes them, and the freeze shows in the status line.

- **Propose triggers from the user's own habits** — FEATURE — value 4 — effort L — risk med — category: discovery
  Why: assumption: the user repeats manual sequences (run tests, check CI, rebase) that nobody wrote down. Mine local shell and git history, with nothing sent out, and propose `fm when` rows with a replay count attached.
  Done when: on a fixture history with a command repeated weekly, the proposer drafts one trigger with its evidence and never installs it without the yes.

Next question: Which self-started lanes have the user actually accepted rather than discarded, and is that rate better than a coin flip?
Next question: What stops a trigger from firing on its own output, such as a CI watcher reacting to the CI run its own fix just caused?
