# Brainstorm — lens: bold bets

Lens: bold bets for Mission 4 (#11 Self-triggering). The pack already holds hundreds of incremental ideas (dead-man beats, replay-before-arm, one yes card, branch landing). These go for whole new capabilities.

- **Compile standing orders from the user's own history** — FEATURE — value 5 — effort L — risk med — category: triggers
  Why: assumption: the user repeats manual sequences (the "asked" stream shows the same CI-watch, ship and steer patterns). `fm when` rules are drafted from shell, git and `fm` history, each with a replay of last month's hits and misses before it can ask for an install yes.
  Done when: on a fixture history with 3 planted repeated sequences, `fm triggers propose` emits 3 drafts, each showing replay precision, and installs none.

- **Make CI red on main a pre-briefed lane** — FEATURE — value 5 — effort M — risk med — category: watchers
  Why: `fm ci-watch` already settles ship bets; red runs only produce a note today (assumption: no lane starts from one). A red main run opens a worktree lane with the failing log fenced as data, the suspect commit and the likely test, and lands a fix on `night/<date>` only.
  Done when: a recorded failing run fixture creates one lane and branch, touches nothing on main, and a second identical event is deduped by its idempotency key.

- **Prove the whole chain with a weekly canary event** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: the night tick "logs only when something happens", so silence can mean alive or dead (the pack's own question). A harmless synthetic event runs the real path (event, dispatcher, lane, receipt) and times it end to end.
  Done when: killing the timer in a scratch home makes `fm doctor` report "chain dead since <date>" within one canary period, and a healthy run reports its latency.

- **Run a shift with a charter and a hard stop** — FEATURE — value 5 — effort M — risk med — category: unattended
  Why: Pillars say never idle, and the user's steer says wait out limits and resume. A charter file (budget, branch, allowed lanes, stop file) is written before each unattended run and a morning note is written to a file the first prompt reads.
  Done when: a simulated shift that exceeds its budget stops, the note names what ran and what is queued, and touching the stop file halts the next tick.

- **Replay a trigger on the recorded past before it arms** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: Mission 3's lesson was that briefs were built without checking the failure had occurred. Every trigger runs in shadow over the last 30 days of its event type and the install card shows would-have-fired counts.
  Done when: `fm triggers add` on a CI-failure rule prints a would-fire count from stored runs and refuses to arm below a set precision.

- **Queue every install as one exact-text yes card** — FEATURE — value 4 — effort M — risk low — category: installs
  Why: the Mission says installs get queued for one yes, and the user previously installed timers for `fm night`. One card shows the literal unit text, the diff against disk, the uninstall line and the work it unblocks; one word answers each.
  Done when: three queued installs render one card, "yes" installs exactly the shown bytes (hash-checked), and any changed text re-asks.

- **Fill the 59 cells by mechanism, with a probe per family** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: the standing rule demands cells name concrete, grounded capabilities with no reused phrasing. One probe per trigger family (schedule, file, git, CI, issue, drop folder) stamps its cells with real output, and a templating linter rejects duplicates.
  Done when: the sweep reports 0 empty and 0 templated cells, and each cell cites a probe whose rerun output matches.

- **Wild: Let a sentence become a trigger** — FEATURE — value 4 — effort M — risk med — category: natural language
  Why: wild, assumption: the user types intent in chat. "When CI fails on main, draft a fix" compiles to a trigger draft in a registry file, shown as one line, with a veto key.
  Done when: five sample sentences compile to the expected rows, and an ambiguous sentence yields one question rather than a guess.

- **Wild: A tripwire file that freezes everything** — FEATURE — value 3 — effort S — risk low — category: control
  Why: wild; the user's steers value autonomy but fear runaway. Touching one file in the state directory halts every trigger, lane and tick at the next boundary, and removing it resumes. The registry and the tick both check it with a single stat.
  Done when: after the touch no new lane starts within one tick, and removal resumes with no lost events.

- **Wild: Rehearse a recorded week in daylight** — FEATURE — value 4 — effort L — risk low — category: simulation
  Why: wild; the real night is unwatchable. A recorded week of events is fast-forwarded through the real dispatcher with a stub model, producing the morning note the user would have seen.
  Done when: replaying a fixture week emits a deterministic note and ledger, spending zero model tokens.

- **Fire on file and git events through one debounced envelope** — FEATURE — value 4 — effort M — risk med — category: triggers
  Why: the Mission names file and event triggers, and nothing in the pack shows them. A drop folder, a branch switch or a test saved red become one event type, deduped by identity rather than time.
  Done when: ten saves in two seconds yield one fire, and a restart mid-burst does not double-fire.

- **Coalesce missed schedules after sleep** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: laptop sleep skips ticks. After wake, missed runs execute once, capped, and the receipt says how many were folded.
  Done when: a simulated 3-day gap produces one run and a note reading "3 days folded".

- **Wild: Mine "while you were away" into a postcard** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild; the morning note should read like a person left it: what moved, what waits for one yes, and what was deliberately not done, with the cost.
  Done when: the first prompt after a shift shows at most 12 lines, led by the yes count and the minutes it unlocks.

Next question: which fires did the user ever act on, and what is each trigger family's act-on rate against a no-trigger baseline?
Next question: what does a trigger do when the world it was written for changes (host CLI update, moved repo, rotated token)?
