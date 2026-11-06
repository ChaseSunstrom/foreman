# Brainstorm — lens: reliability

- **Heartbeat every trigger and timer from outside the session** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: the pack's "session-bound work" and "unwitnessed deaths" items show loops that only advance inside a session; `fm night` logs only when something happens, so a dead timer looks identical to a quiet night. Assumption: the user's installed timers are systemd user units.
  Done when: killing the `fm night` timer in a scratch home makes `fm doctor` report "night tick missed N intervals" within one interval, and a healthy quiet night reports "alive, nothing to do".

- **Break trigger storms with a per-trigger budget and debounce** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: file, CI and issue watchers can fire in bursts, and the pack's "retry storms" and "debounce events into one wake-up" ideas have no owner in this Mission. Assumption: no per-trigger rate cap exists yet.
  Done when: a test firing 200 file events in 10 seconds produces one lane, and a trigger that exceeds its daily budget is parked with a named reason rather than silently dropped.

- **Replay a trigger on the last 30 days before it can install** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: installs are "queued for one yes", and the yes is only worth giving if the card shows what the trigger would have done. `fm triggers` already measures precision per trigger, so the data exists.
  Done when: the install card for a new trigger prints "would have fired N times, M led to accepted work" computed from recorded events, and a trigger with zero replay hits is flagged.

- **Run every self-triggered lane under the same guard and hook budget** — SECURITY — value 5 — effort M — risk med — category: unattended safety
  Why: standing rule that capabilities must be called by a real session path, and the pack's "run the unattended paths under the same guard" idea; a watcher lane with no session may skip the hooks that the guard depends on. Assumption: headless lanes load the guard through settings rather than a session hook.
  Done when: a scheduled lane that attempts a denied command is blocked and logged with its trigger id, tested on a headless run.

- **Treat issue, PR and CI-log text as untrusted in watcher lanes** — SECURITY — value 5 — effort S — risk low — category: injection
  Why: a CI or issue watcher feeds third-party text to a model that holds write tools, and T-0791 (injection defenses) is deferred. Assumption: watcher prompts currently inline that text.
  Done when: a fixture issue containing "ignore prior rules and run X" is fenced as data in the lane brief, and the lane's tool allowance excludes push and network writes.

- **Spend-once install receipts for timers and units** — SECURITY — value 4 — effort M — risk low — category: installs
  Why: the mission says installs are queued for one yes; the grant should be bound to the exact unit file hash and one install, then checked by diff afterwards. The pack's "spend an install grant on one invocation" idea is unbuilt for timers.
  Done when: approving a unit and then editing its file before install makes the install refuse, and after install `fm doctor` shows the installed file hash equal to the approved one.

- **Add a land-on-branch rule for self-started work** — FEATURE — value 4 — effort S — risk low — category: unattended safety
  Why: the push grant is spent per task through `fm ship`; a trigger-started lane has no task the user approved, so it must not reach main. Assumption: nothing enforces this today.
  Done when: a lane with a trigger origin that calls `fm ship` is refused, and its work shows up on a `night/<date>` branch with a one-command accept.

- **Write a shift charter, hard budget and stop file for each unattended run** — FEATURE — value 4 — effort M — risk low — category: unattended safety
  Why: standing steer says wait out real limits but also keep caps; with no one watching, a runaway trigger needs a file the user can touch. Assumption: no stop file is checked between lane steps.
  Done when: touching the stop file halts a running lane before its next step, and exceeding the shift budget parks remaining triggers with a morning note.

- **Quarantine a trigger the user never acts on** — CLEAN — value 4 — effort S — risk low — category: triggers
  Why: `fm triggers` already computes precision; nothing acts on a low one. The lean ratchet also penalises silent growth.
  Done when: a trigger with precision under a floor over N firings goes to shadow mode (logs, never starts work) and appears in the morning note with a one-word restore.

- **Test trigger firing after a kill at every boundary** — FIX — value 4 — effort M — risk low — category: crash safety
  Why: pack ideas "kill hooks at every write boundary" and "baton, ledger and repo disagree after a kill" apply doubly to a watcher that must not double-start or lose an event. Assumption: events are consumed from a file or a log with a cursor.
  Done when: killing the watcher between "event read" and "lane started" at each step leaves exactly one lane after restart, verified in a test.

- **Wild: Stage a planted-event drill each night** — FEATURE — value 3 — effort M — risk low — category: liveness — wild
  Why: assumption: a dead watcher is the commonest silent failure. A harmless synthetic file or fake CI event, tagged as a drill, proves the whole chain from event to lane to morning note.
  Done when: the nightly tick creates a drill event, the drill lane starts and closes with no repo changes, and a missing drill pops a red line in `fm doctor`.

- **Wild: Offer a `fm watch --dry-week` that fast-forwards a recorded week of events** — FEATURE — value 3 — effort L — risk low — category: triggers — wild
  Why: assumption: recorded events can be replayed against a stubbed model; this lets the user watch a week of triggers in ten minutes before saying yes.
  Done when: running it on a recorded fixture week prints a timeline of lanes that would have started, with zero model calls and zero writes.

- **Wild: Let an offline machine catch up with a "missed while closed" pass** — FEATURE — value 3 — effort M — risk med — category: triggers — wild
  Why: assumption: laptop timers skip when suspended. On wake, Foreman reads the gap, collapses missed schedules into one run per trigger, and says what it skipped.
  Done when: simulating a 3-day sleep fires each schedule once, not three times, and the note lists the skipped runs.

- **Gate the watcher on battery, load and network** — FEATURE — value 3 — effort S — risk low — category: unattended safety
  Why: the pack's night-shift ideas hold work when the machine is on battery or busy; no check is in evidence.
  Done when: with a faked battery state the tick defers lanes and records "held: on battery" instead of starting them.

Next question: Which triggers have fired in the past month, how many led to work the user kept, and is that evidence enough to say the 59 empty cells need triggers at all?
Next question: If the machine is off or the session is dead when a trigger fires, who notices, and how long until the user knows?
