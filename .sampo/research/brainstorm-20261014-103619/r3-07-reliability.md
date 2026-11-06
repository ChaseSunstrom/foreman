# Brainstorm — lens: reliability

- **Reconcile every user prompt against the inbox** — FIX — value 5 — effort M — risk low — category: capture
  Why: T-0756 is a truncated "also, the …", and T-0757 and T-0759 read as fragments of one message, so captures are losing or splitting text. Assumption: UserPromptSubmit can fail or truncate before the write lands.
  Done when: a test feeds 20 prompts through the hooks with one forced hook crash, and `fm doctor` reports 20 transcript prompts, 20 inbox dispositions and no unmatched ones.

- **Make step advances compare-and-swap** — FIX — value 5 — effort S — risk low — category: step pointer
  Why: the user saw Foreman start different steps without updating the step (T-0759). Parallel tool calls also fire hooks concurrently. `fm step advance` should take an expected-from step and a sequence number, and refuse stale or duplicate advances.
  Done when: two concurrent advances from the same step leave the pointer on exactly one new step, the loser gets a "stale" error, and a test proves it.

- **Require a typed disposition on every stop** — FEATURE — value 5 — effort M — risk low — category: idle
  Why: the user said "make sure it doesn't sit idle like it is" (T-0758). The Stop hook should demand one of done, needs-you (with a default), blocked (with a reason), paused or continuing. A stop with none of these is an idle bug: auto-continue and count it.
  Done when: a replay of 50 recorded stops shows zero silent stops, and a stop with queued work and no disposition triggers a continue.

- **Grant a wake lease to one waker at a time** — FEATURE — value 4 — effort M — risk med — category: liveness
  Why: Foreman has tmux send-keys, and Monitor, ScheduleWakeup, cron and SendMessage are all candidate wakers. Several at once would double-prompt a session. Each wake carries an idempotency token, and the session acks it.
  Done when: with all wake paths firing at an idle session, exactly one prompt arrives, the others log "lease held", and killing the holder hands over within one interval.

- **Put every outward native effect behind a durable outbox** — FEATURE — value 4 — effort M — risk low — category: delivery
  Why: Artifact publish, PushNotification, SendMessage and `fm notify` become outward calls, and a failure today vanishes with the turn. Assumption: these calls can fail or the network can drop. Each effect gets a dedupe key and at-least-once retry with a receipt.
  Done when: a push issued with the network blocked is delivered once after restore, a restart in between doesn't duplicate it, and `fm outbox` shows the receipt.

- **Add a wiring sentinel for `~/.claude` drift** — FIX — value 4 — effort S — risk low — category: install
  Why: other plugins, `claude plugin update` and CC itself rewrite settings. If Foreman's hooks, statusline or output style get dropped, discipline disappears silently. Hash Foreman's wiring blocks and check them at SessionStart.
  Done when: removing a hook entry from settings is detected and repaired at the next SessionStart, with a one-line notice and a test.

- **Quarantine crash-looping tasks** — FEATURE — value 4 — effort S — risk low — category: queue
  Why: the drive keeps going through the queue, so a task that wedges or crashes the session on every pickup can starve everything behind it. After N aborted pickups, move it to a dead-letter lane with its last failure and carry on.
  Done when: a seeded poison task is parked after 3 attempts, the next task runs, and `fm task list` shows the quarantine reason.

- **Auto-demote a native path on anomalies** — FEATURE — value 4 — effort M — risk med — category: adoption
  Why: the plan is to swap send-keys for Monitor/SendMessage and step tracking for the native todo list. Every adopted path needs a tripwire (missed wake, drift, hollow receipt) that flips it back to the proven path and records why.
  Done when: injecting 3 missed wakes on the native path switches `fm wiring` to the fallback, and the idle test still passes.

- **Record live hook payloads as scrubbed fixtures** — CLEAN — value 4 — effort M — risk low — category: contracts
  Why: the contract tests rest on payloads Foreman's authors believed in. Capture one redacted real payload per event and Claude Code version, and run the hooks against the whole archive.
  Done when: a fixture exists for each of the 14 events, a new CC version adds its own, and a field change fails the schema diff test.

- **Run a launcher-parity matrix** — FEATURE — value 3 — effort M — risk low — category: environment
  Why: hooks launched under tmux, cron/ScheduleWakeup, the desktop app, a worktree lane and a remote session see different PATH, cwd and python. Assumption: `python3` resolution already differs between them. Run the same hook inputs under each and diff the verdicts.
  Done when: `fm doctor` lists each launcher with a matching or differing verdict, and a broken PATH is flagged naming the launcher.

- **Wild: Plant a canary phrase in every injected context block** — FEATURE — value 3 — effort S — risk low — category: injection
  Why: assumption: injected state or briefs can be silently dropped by compaction, truncation or a hook failure. Each block carries a rotating phrase, children echo it in their return, and a missing echo means the contract never arrived.
  Done when: a child launched with injection disabled returns without the phrase and the return is rejected as "no context".

- **Wild: Bootstrap preamble for sessions Foreman never started** — FEATURE — value 4 — effort M — risk med — category: remote lanes
  Why: `isolation: "remote"`, cloud routines and a cloud sibling session run without Foreman's hooks, so discipline is absent without anyone noticing. The launch brief should carry a minimal kernel (brief, vetoes, evidence format), and the return should be checked for the hook receipts it should have.
  Done when: a remote lane's return lacking guard receipts is held as "unverified", and one with the preamble passes the close-out check.

- **Wild: Add `fm blackstart`** — FEATURE — value 3 — effort L — risk med — category: recovery
  Why: after a reboot or power loss there are no tmux panes, sessions or schedules, only central state. One command should rebuild the fleet from the ledger and reopen each session at its exact step, reinstalling crons and wakes.
  Done when: killing every claude and tmux process mid-queue and running `fm blackstart` resumes each task at the recorded step with no manual input.

- **Wild: Keep a nightly "old CC replay" fleet** — FEATURE — value 3 — effort M — risk low — category: compatibility
  Why: assumption: users and the cloud may run older or newer Claude Code than Foreman was built on. Replay the recorded payload archive through the current hooks, and the reverse (new payloads against the oldest supported hooks), as a compatibility matrix that gates releases.
  Done when: the release gate fails when a hook crashes on any archived payload version, and the matrix prints in `fm doctor`.
