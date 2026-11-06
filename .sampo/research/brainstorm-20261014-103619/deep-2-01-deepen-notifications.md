# Brainstorm — lens: deepen: notifications

- **Build an attention router that picks channel by presence** — FEATURE — value 5 — effort M — risk med — category: notifications
  Why: existing ideas list "route by presence" and "push only needs-you moments" separately; fuse them. Foreman already has tmux send-keys (bus), `fm notify` shell hook, and PushNotification unused. Assumption: presence is inferable from tmux client attach state, last keystroke time, and session idle time.
  Done when: with a tmux client attached and active, a blocked event only updates the statusline/band; with it detached for 5 min, the same event calls PushNotification; a test asserts both routes.

- **Make every notification an actionable decision card with a default and deadline** — FEATURE — value 5 — effort M — risk med — category: notifications
  Why: the user hates being handed commands and Foreman runs autonomously; a push saying "blocked" is a dead end. Assumption: replies come back via SendMessage/Artifact comments or a one-word answer typed on the phone.
  Done when: a needs-you event carries a question, a default answer and a deadline; when the deadline passes with no reply, Foreman applies the default, records it with `fm decide`, and the log shows "defaulted after Nm".

- **Collapse all pings into one in-place status notification** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: two listed ideas want a single updating notification. Assumption: PushNotification can't edit prior pushes, so use a stable tag and rate-limit, plus a living Artifact page for detail.
  Done when: a run with 20 state changes sends at most N pushes (configurable), and the one Artifact page shows the latest queue state when opened.

- **Add a notification budget with digest and quiet hours** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: more channels means more risk of annoying the user; the user's steers favour fewer, higher-value interruptions. Evidence: they push back on noise-like features.
  Done when: events below "needs human" are batched into one digest at the end of the night run, and a test shows a quiet-hours window suppresses all but critical blocks.

- **Stream long-running checks via Monitor and notify only on state transitions** — FEATURE — value 4 — effort M — risk med — category: notifications
  Why: Monitor is unused; test suites and `fm night` runs stall silently (user complaint T-0758: "doesn't sit idle"). Transition-only events (green→red, stalled for N min) replace polling.
  Done when: a background suite run raises a single event on first failure, and a run with no output for the stall threshold raises a "stalled" event, each covered by a test.

- **Detect idleness and notify when Foreman itself sits idle with queue work** — FIX — value 4 — effort S — risk low — category: notifications
  Why: T-0758 "make sure it doesn't sit idle like it is" and T-0759 (step not updating) show the user is the watchdog. Assumption: idle = no tool call for N min while tasks are queued and no block recorded.
  Done when: an idle session with queued work gets woken or flagged within the threshold, and the event names the task and step it was on.

- **Reply-by-notification: let phone responses resume the session** — FEATURE — value 4 — effort L — risk high — category: notifications
  Why: SendMessage/ListAgents and `fm bus` already wake sessions; closing the loop makes push two-way. Assumption: the reply path is Remote Control or Artifact comments, not raw push.
  Done when: answering "yes"/"no"/text on the artifact page is delivered to the waiting session within a minute and the step proceeds, verified in an e2e with a fake channel.

- **Fall back across channels when one is unconfirmed** — FEATURE — value 3 — effort M — risk low — category: notifications
  Why: "work with zero configuration" implies a chain: band → terminal bell → push → `fm notify` command. Escalate if unacknowledged after a deadline.
  Done when: simulating an unacknowledged event walks the chain in order with timestamps, and acknowledgement at any step stops it.

- **Wild: Give each notification a glyph grammar readable on a watch** — FEATURE — value 3 — effort S — risk low — category: notifications
  Why: wild. Two glyphs and ≤40 chars encode kind (✓ done, ? decide, ⚠ stalled, ✗ failed), task id and urgency, so a glance replaces opening anything.
  Done when: every notification renders under 40 chars matching the grammar, with a snapshot test over all event kinds.

- **Wild: Publish a live "night shift" Artifact as the notification's landing page** — FEATURE — value 4 — effort M — risk med — category: notifications
  Why: wild. Artifact supports a shared db and comments; one page shows the plan tree, evidence, and approve/redirect buttons, and every push links to it. It also serves the Frontier 11 cockpit ask.
  Done when: a push links to a page that renders current task, step, last evidence and pending decision, and a comment on it appears as a captured request.

- **Wild: Morning briefing assembled from the night's notifications** — FEATURE — value 4 — effort M — risk low — category: notifications
  Why: wild. Instead of many pings overnight, `fm night` ends with one briefing: what shipped, what defaulted, what needs you, ordered by cost of delay, scheduled with a cron or ScheduleWakeup.
  Done when: after a night run, one summary appears at a configured time listing every decision made on the user's behalf with its reversal command.

- **Wild: Let notifications learn from what the user ignores** — FEATURE — value 3 — effort M — risk med — category: notifications
  Why: wild; fits the learning flywheel (Frontier 12). Track which event kinds the user acts on within minutes versus never, and lower the priority of ignored kinds.
  Done when: after replaying a log where "done" pings were never acted on, the router demotes them to the digest, and the change is visible in `fm doctor`.

- **Redact and scope every outgoing notification** — SECURITY — value 4 — effort S — risk low — category: notifications
  Why: sending content to external services publishes it and may be cached; the project already redacts in `recall --ask`. Push and Artifact payloads should go through the same redactor and carry no paths, secrets or diffs by default.
  Done when: a test feeding a secret-bearing event produces a payload with the secret removed, and a setting is required to include more detail.
