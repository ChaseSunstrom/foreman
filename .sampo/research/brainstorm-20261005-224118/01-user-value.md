# Brainstorm — lens: user value

- **Triage "Waiting on you" with one-key yes/no** — FEATURE — value 5 — effort M — risk low — category: triage
  Why: the user wants to "only give yes/no consent" and to scroll all inbox/queue items. Home already lists waits. Assumption: j/k to move, y approves a plan or starts an item, n drops it, Enter opens the brief. Guard grants (fm ask) only deep-link to the agent session and are never granted from the app.
  Done when: with 5 waiting items, a keyboard-only user clears them all without the mouse, and an fm ask item shows "answer in session" with no approve button.

- **Add a Cost & Budget page with pace projection** — FEATURE — value 5 — effort M — risk low — category: usage
  Why: the user watches plan limits, and fm cost and fm budget are unused. The sidebar meter shows only the current usage.
  Done when: the page shows spend per project and task per device, plus a "weekly limit reached around <time> at this rate" line that matches fm budget output.

- **Show "safe to start" on Start buttons** — FEATURE — value 4 — effort S — risk low — category: usage
  Why: T-0320 made subagents wait while usage runs ahead of pace. Assumption: the same pace signal can be shown before the user starts a task or session.
  Done when: Start shows an amber "ahead of pace" hint when usage exceeds the even-pace mark, and Start still works after the user confirms.

- **Add a weekly Review page (friction + digest)** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: the user asked to "recursively improve" and runs fm friction every 3 tasks. Neither fm friction nor fm digest appears in the app.
  Done when: the page renders both outputs, and each friction item has a "Capture as task" button that calls fm capture.

- **Add a global quick-capture overlay** — FEATURE — value 4 — effort S — risk low — category: capture
  Why: fm capture has types and tiers, and the palette exists. Assumption: users often have an idea mid-session in another window.
  Done when: a global shortcut opens a one-line box with type/tier chips, and Enter creates an inbox item on the chosen device and project.

- **Add a Health page and sidebar dot from fm doctor and fm check** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: multi-device ssh setups drift, and agent wiring and the Gates tab already exist. Doctor isn't surfaced.
  Done when: a device with a failing doctor check shows a sidebar dot, and clicking it lists the failures with suggested fixes.

- **Add global search across tasks, decisions, research and sessions** — FEATURE — value 4 — effort M — risk low — category: search
  Why: the user wants "everything" viewable. fm recall and fm research list exist. Ctrl+K only navigates.
  Done when: searching a phrase from an old decision returns that decision, a session and a research note, grouped by type.

- **Run the queue overnight within a pace budget (wild)** — FEATURE — value 5 — effort L — risk high — category: autonomy
  Why: wild. The user wants Claude to run everything while they give consent. Assumption: one upfront yes ("run these 4 items, stop at 70% of weekly pace, no outward actions") could cover a night's work, and a morning summary lists what was done and what is waiting.
  Done when: a dry-run mode shows the plan and its pace cap, and a run stops at the cap and leaves a summary on Home.

- **Scrub a session like a video (wild)** — FEATURE — value 3 — effort L — risk med — category: replay
  Why: wild. Conversations, tool calls, images and scratchpad files are already shown. A timeline scrubber would sync them, so scrubbing shows the conversation, files and images as they were at that moment.
  Done when: dragging the scrubber to a past point shows the transcript and scratchpad file list as of that time.

- **Add a tray glyph that breathes when something waits (wild)** — FEATURE — value 3 — effort M — risk low — category: ambient
  Why: wild. The user wants animation without noise, and notifications already exist for finished sessions. Assumption: the tray stays quiet unless the waits count is above zero, and then pulses amber slowly. Its menu offers Approve next and Open.
  Done when: the tray icon changes state when waits go from 0 to 1 and back, and the menu shows the top item.

- **Show devices as a live constellation (wild)** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. The Devices and Home pages are plain tables. A restrained graphite map with devices as nodes and active sessions as slow amber pulses would give an at-a-glance view of "everything". The user asked for a "beautiful" app and "less AI made".
  Done when: the view lists every connected device with a pulse per live session, respects reduced-motion, and clicking a node opens that device.
