# Brainstorm — lens: capability map

**Capability map: self-triggering**

Reference products: GitHub Actions (`workflow_dispatch`, concurrency groups), Dependabot/Renovate (grouped updates, schedules, auto-merge rules), Home Assistant (trigger, condition and action are separate), Airflow/Temporal (sensors, SLAs, backfill, pause), n8n/Zapier (test-fire, run history, replay), Hazel and `systemd.path` (file and machine-state events), and Copilot agent and Devin (an issue becomes a PR). The pack already covers catch-up, dry runs, storm breakers, one-yes install cards, heartbeats and drop folders. These are the capabilities it doesn't show.

- **Separate conditions from triggers** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: the pack's trigger table fires on events, but gates (battery, user-present, quiet hours) are scattered across separate ideas. Home Assistant's trigger/condition/action split keeps them reusable.
  Done when: one trigger row carries `when`, `only-if` (tree clean, branch is main, CI green, user idle, on AC) and `do`, and `fm triggers explain NAME` prints which condition vetoed the last non-fire.

- **Add run-now, snooze and skip-next verbs** — FEATURE — value 4 — effort S — risk low — category: control
  Why: assumption: every mature scheduler has `workflow_dispatch`, pause and skip-occurrence. The pack has only a global freeze file and `fm away`.
  Done when: `fm trigger run|snooze 2d|skip-next NAME` works, and the run is recorded with its origin as manual, snoozed or skipped.

- **Coalesce events by failure signature across sources** — FEATURE — value 4 — effort M — risk med — category: dedupe
  Why: the pack has count-based storm breakers and per-source watchers. It has nothing that merges a red CI run, an issue report and a local log line sharing a stack trace into one lane.
  Done when: three fixtures (CI log, issue body, tail line) with the same normalised trace start exactly one lane, and the other two attach to it.

- **Fire on machine-state events** — FEATURE — value 3 — effort M — risk low — category: triggers
  Why: `systemd.path` and udev-style events (resume from suspend, network up, AC plugged in, volume mounted) are standard. The pack only gates on battery. Heavy lanes could start at the right moment instead of being skipped.
  Done when: a trigger with `on: ac-plugged` starts a queued heavy lane within 60s of the event in a VM test, and does nothing on battery.

- **Check the trigger graph for cycles before install** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: the pack has self-output re-fire protection at runtime but no static check. Lane A filing an issue that trigger B watches, which starts A, should never reach the install card.
  Done when: a two-trigger loop fixture is refused at `fm yes` time, naming the cycle.

- **Reject over-scoped watcher tokens** — SECURITY — value 4 — effort S — risk low — category: credentials
  Why: the pack treats issue and CI text as untrusted but says nothing about the token that reads it. A watcher holding a write-scope PAT turns an injection into a push.
  Done when: installing a GitHub/CI watcher with a token that has write scopes is refused unless a user-signed override exists, and `fm doctor` reports the token's scopes.

- **Add a release-tag trigger that proves the artifact** — FEATURE — value 3 — effort M — risk low — category: release
  Why: the pack proposes "install the built artifact in a clean venv" as a proof kind and has no event that starts it. Renovate and Actions both fire on tag push.
  Done when: pushing a tag in a scratch repo starts a lane that builds, installs into an empty venv, runs the first-use path, and writes a receipt to the morning note.

- **Add expiry watchers for tokens, certs and keys** — FEATURE — value 3 — effort M — risk low — category: watchers
  Why: assumption: calendar-style "this will break in 14 days" events are a standard monitor (Dependabot-adjacent, cert-manager). Nothing in the pack watches things that expire.
  Done when: a fixture with a cert 10 days from expiry files one capture with the date, and does not refile it on later ticks.

- **Compute a start-by date for tasks with a due date** — FEATURE — value 3 — effort M — risk med — category: schedules
  Why: the pack has deferred tasks with revisit dates and "work backward from a deadline" for goals. Nothing turns a due date plus an S/M/L estimate into a self-armed start trigger.
  Done when: an L task due in 10 days gets a start trigger set from its size and history, visible in `fm triggers`, with a miss warning if the estimate is exceeded.

- **Add per-trigger service levels and misses** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: Airflow SLAs mean "expected by 07:00" is a checkable claim. The pack's heartbeat says the tick is alive but not that the promised result landed.
  Done when: a trigger with `expect: morning-note by 07:30` records an SLA miss in the next session's start note when the note is absent or empty.

- **Serve a loopback webhook receiver with HMAC** — FEATURE — value 3 — effort M — risk med — category: events
  Why: the pack polls only, which is right for local-first. A web UI already exists, so GitHub and CI webhooks through a user-owned relay could feed the same event envelope, off by default.
  Done when: a signed POST fixture creates an event, an unsigned or replayed one is rejected and logged, and the listener is off until `fm yes` enables it.

- **Wild: Subscribe to the fire schedule as an .ics feed** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. A local calendar file of upcoming fires and past results lets the user see the night shift in the calendar app they already open, with no new UI.
  Done when: the `.ics` file imports into a calendar app and shows tomorrow's expected fires with their names and dry-run results.

- **Wild: Compile a "when X, do Y" sentence into a trigger row** — FEATURE — value 4 — effort M — risk med — category: authoring
  Why: wild. The user says what should happen in words, and a cheap model drafts a row that goes through the existing replay, dry-run and install card. The pack lists this as a wild idea but no row shows a compile path with a safety fallback.
  Done when: five fixture sentences produce valid rows or a specific refusal, and none installs without the card.

- **Wild: Answer a grant by replying to a notification action** — FEATURE — value 3 — effort L — risk high — category: devices
  Why: wild. An ntfy-style push with Approve/Decline buttons writes to the grant ledger through a verb the model can't call. The card shows exactly the unit text, so one tap is an informed yes.
  Done when: tapping Approve in a local ntfy test installs the queued timer once, and a replayed tap does nothing.

- **Wild: Take a fire from the day's actual history** — FEATURE — value 3 — effort M — risk low — category: replay
  Why: wild. `fm trigger asof DATE` answers "would this have fired last Tuesday?" by replaying that day's recorded events, which makes bugs in a trigger's `only-if` visible before it arms.
  Done when: replaying a recorded day gives a fire list that matches the log, and a deliberately broken condition is flagged as a diff.

Next question: which of the 59 cells are covered by one mechanism (one probe per trigger family) and which need their own real-path check, and does the cell grid now double-count both?

Next question: what does a user who never opens the web UI see when a trigger misses or a SLA is breached, and through which surface do they learn it?
