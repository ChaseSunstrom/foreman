# Brainstorm — lens: event and file triggers

- **Add a durable event spool with `sampo event emit`** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: drive stops and resumed sessions (T-2900, T-2901) show a trigger held only in a live process is lost on death. Every source (git hooks, CI, a shell one-liner, another harness) should write one file into a maildir-style spool. The drive consumes files by atomic rename and acks only after the task is filed. Each event carries an idempotency key of source plus id.
  Done when: killing the drive mid-event and restarting files exactly one task, and emitting the same key twice files one.

- **Make triggers edge-triggered on predicates with hysteresis** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: a persistently red main or a full disk would otherwise refire every tick. Assumption: current polling is level-based. A trigger fires on the transition to true, re-arms only after the predicate has been false for N minutes, and prints "still red since …" instead of refiring.
  Done when: a replayed 6-hour red CI stretch yields one task, and flapping red/green/red inside the window yields one.

- **Fire a prune plan when a state class crosses its byte budget** — FEATURE — value 4 — effort S — risk low — category: state hygiene
  Why: the 2.4 GB project state grew unnoticed. A size watcher on the state dir emits an event, and the lane runs `prune --plan` only. Apply stays behind the one yes.
  Done when: pushing a state class past its budget in a scratch home files a plan task and deletes nothing.

- **Turn `sampo:` code comments into briefs on save** — FEATURE — value 4 — effort M — risk med — category: editor surface
  Why: assumption: users leave "fix this later" comments and then re-ask in chat. A file watcher spots `# sampo: …` or `// sampo: …` and files a dormant brief carrying file:line and the comment text. Comment text is fenced as data, and the task is picked up only at a quiet time.
  Done when: saving a file with a marker creates one brief naming the line, and removing the marker withdraws it.

- **Add a git-hook event source** — FEATURE — value 4 — effort S — risk low — category: triggers
  Why: file watching cannot tell a hand commit, merge, checkout or rebase apart, and lane landings and the user's own commits are the useful events. `sampo hooks install` adds post-commit, post-merge and post-checkout stubs that only call `event emit`. They add under 20 ms and never block git.
  Done when: a hand commit in a test repo yields a spool event with the sha, and a hook failure never fails the commit.

- **Receive forge and CI callbacks on a loopback webhook with HMAC** — FEATURE — value 3 — effort M — risk med — category: CI watchers
  Why: polling CI costs tokens and latency, and the request names CI and issue watchers. A tiny listener bound to 127.0.0.1 (a tunnel is the user's choice) verifies a signature and spools the event. Payload bodies go through the Ward as untrusted text.
  Done when: a signed POST spools one event, an unsigned or oversized one is rejected and logged, and it never binds beyond loopback.

- **Coalesce events into open tasks by a subject key** — FEATURE — value 4 — effort M — risk low — category: queue
  Why: a CI-red on a branch already being fixed, or the same file saved ten times, should append evidence to the open task, not file another. Key is repo + branch + failure signature. Assumption: dedupe exists for asks but not for events.
  Done when: three CI-red events with one signature produce one task with three evidence lines.

- **Watch lockfiles and manifests and queue the audit plus its installs** — FEATURE — value 3 — effort M — risk med — category: dependencies
  Why: the request says installs are queued for one yes. A change to a lockfile or manifest triggers a read-only audit and a drift check, and any needed installs join the single overnight yes card.
  Done when: editing a manifest in a scratch repo yields an audit task, and a proposed install appears only as a queued item.

- **Quarantine flaky gates automatically when a ship gate fails intermittently** — FIX — value 4 — effort M — risk med — category: reliability
  Why: failed tool calls are up by half, and a flaky gate stops the drive and wastes the night. A gate failure that passes on rerun emits an event, and a lane reruns it N times and records a flake rate with the failing seed. It files a fix task and never silences the gate.
  Done when: a planted 1-in-3 flaky test is labelled flaky with its rate, and the gate stays enforced.

- **Start and stop the night on logind lock and unlock** — FEATURE — value 4 — effort S — risk low — category: presence
  Why: the user wants overnight progress unattended, and the idle signal already exists on the box. Screen-lock begins the night shift, and unlock yields the GPU and local model and shows the morning card. It reads the logind signal and never guesses from ledger gaps.
  Done when: locking the session starts the queue within a minute, and unlocking pauses new picks and prints the card.

- **Wild: Add a drop-folder inbox that a phone can sync into** — FEATURE — value 4 — effort S — risk low — category: devices
  Why: a synced `inbox/` (Syncthing or similar) turns a text file, voice-memo transcript or screenshot from the phone into a brief, so file names set priority. Nothing leaves the owner's hardware, and wild because it needs no app. Done when: a file dropped in the folder becomes a filed brief and moves to `inbox/done/` with the task id.

- **Wild: Plant tripwire files that fire when anything touches them** — SECURITY — value 3 — effort S — risk low — category: Ward
  Why: decoy files like `.env.sampo-canary` in each repo and lane worktree, watched via inotify or fanotify. A read by a lane, trigger-born session or unknown process emits a high-priority event and pauses the triggers.
  Done when: a scripted `cat` of the decoy pauses triggers and names the process, and normal work never touches it.

- **Wild: Fire a hardware lane when a USB device is plugged in** — FEATURE — value 2 — effort M — risk med — category: devices
  Why: assumption: some users build for boards and probes. A udev rule emits a "device attached" event, and a lane runs the repo's declared flash or hardware test card on it. Done when: a fake udev event runs the declared card in a dry run.

- **Wild: Schedule heavy local work into the user's calendar busy blocks** — FEATURE — value 3 — effort M — risk low — category: scheduling
  Why: while the user is in a meeting, the GPU and CPU are free. A watched local `.ics` file turns busy blocks into windows for the background queue, and a block ending triggers a yield. Done when: a test `.ics` with a busy hour opens a window that closes five minutes before the end.

Next question: which trigger source would the user cut first after a week, and does the trigger ledger record the "ignored" signal to say so?
Next question: when two spooled events from different sources describe one real incident, who owns the merged task and its provenance chain?
