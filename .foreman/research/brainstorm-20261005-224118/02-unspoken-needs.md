# Brainstorm — lens: unspoken needs

- **Add a "Yes/No inbox" with one-key consent** — FEATURE — value 5 — effort M — risk med — category: consent
  Why: The user wants Claude to run everything with only yes/no from them; Home has "Waiting on you" but grants can only come from the user's reply in an agent session. Assumption: the app can show pending asks and jump to the exact session composer with the question pre-focused (never granting itself), plus j/k/Enter navigation across devices.
  Done when: With 3 pending items across 2 devices, pressing j/k/Enter moves between them and opens the relevant session at the question, and no fm command outside the allow-list is run.

- **Show plan-usage forecast on every start action** — FEATURE — value 5 — effort M — risk low — category: usage
  Why: They watch plan limits and built pace-based subagent budgeting (T-0320) plus a sidebar meter. Assumption: Start, Session here and Drive could display "ahead/behind pace, est. cost" from fm cost/budget before confirming.
  Done when: Clicking Start on a queue item shows a pace badge and estimated cost sourced from `fm cost`/`fm budget`, and warns when usage is ahead of pace.

- **Surface fm friction and digest as a Improve tab** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: They asked for recursive self-improvement ("fm friction --every 3", T-0329 app rounds), but friction, digest, doctor and research list are listed as unused CLI surfaces. Done when: A project's Improve tab renders the latest fm friction and fm digest output with a button to capture each finding into the queue.

- **Add global search across sessions, inbox, decisions and recall** — FEATURE — value 4 — effort M — risk low — category: navigation
  Why: "Able to scroll/view all inbox/queue items, everything", plus fm recall exists unused and Ctrl+K only jumps to pages. Done when: Ctrl+K with a query returns hits from sessions, queue/inbox, decisions and recall, grouped by device, and Enter opens each.

- **Add a Doctor and drift banner per device** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: Multi-device ssh, guard wiring issues (bash -lc miss, config protection) and installs of foreman-ui versions across devices ("Install foreman-ui 0.6.0 for other sessions") suggest drift. Done when: Devices page shows fm doctor results and the Foreman/app version per device, flagging mismatches.

- **Make a capture box with type and tier** — FEATURE — value 3 — effort S — risk low — category: capture
  Why: fm capture with types/tiers isn't in the app; the user keeps filing ideas as asks. Done when: Ctrl+Shift+N opens a one-line capture dialog that files an item with a chosen type/tier and it appears in Inbox.

- **Group live sessions by "needs me" state** — FEATURE — value 4 — effort M — risk med — category: sessions
  Why: Many sessions across devices, including SDK/print-mode runs that were once mistaken for the user's own (dropped capture). Assumption: label automated runs distinctly, and sort stalled/waiting ones first. Done when: Sessions list hides or badges headless/SDK runs by default and a "waiting" filter lists only sessions awaiting input.

- **Wild: Daily "standup" screen narrated from the ledger** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild; they want less manual reading. Combine fm digest, decide --list and activity into a one-screen "what happened overnight, what needs a yes".
  Done when: Opening the app after 8h away shows a summary card listing completed tasks, costly decisions and pending yeses, dismissible.

- **Wild: Tray/menu-bar pulse with quick yes-routing** — FEATURE — value 4 — effort M — risk med — category: ambient
  Why: wild; notifications exist only on session finish. A tray icon colored by pace and waiting count, whose menu lists waits and deep-links into the app.
  Done when: The tray icon shows the waiting count, and clicking an entry focuses the app on that item.

- **Wild: Replay timeline scrubber for a session or task** — FEATURE — value 3 — effort L — risk med — category: observability
  Why: wild; fm task log, ledger and conversation exist separately, and they distrust autonomy ("Decisions" flagged costly/outward). One scrubbable timeline merges tool calls, decisions, gate runs and file/image changes.
  Done when: A task's page shows a timeline where dragging the scrubber highlights the matching conversation turn and decision.

- **Wild: Cross-device "move this session" handoff** — FEATURE — value 3 — effort L — risk high — category: devices
  Why: wild; they manage many devices and Remote Control units. Assumption: package a session's brief and recent context to continue on another device via fm session start. Done when: Choosing "Continue on <device>" starts a Foreman session there seeded with the task brief and last summary, and links both.
