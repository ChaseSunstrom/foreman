# Brainstorm — lens: delight

- **Show a finish-line bar that fills as contents rows close** — FEATURE — value 4 — effort S — risk low — category: goal surface
  Why: assumption: the goal's contents list already has per-row state; the pane has a work bar and stage rail but the pack shows no goal-level "distance to finished" bar. Users seeing a goal inch toward done over days get a reason to come back.
  Done when: `fm goal` and the pane print a bar with closed/total rows and it changes after one row closes.

- **Confetti-free closing receipt in plain words** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: T-0795 (plain receipts, landing ladder) is deferred; the user keeps shipping "clean receipt" work (Initiative pipeline), so a human-readable "here is what is now true" closing page is the natural next thing.
  Done when: closing a goal prints a ≤10-line receipt naming each contents row, its evidence command, and the day count, and the same text appears on the site goal page.

- **Name each goal by a one-line headline the user can say aloud** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption: multi-day goals are referred to by task ids (T-2217); the user's own words are sentences. A generated headline on every surface makes "what's left on the mailbox goal?" answerable.
  Done when: every goal has a headline ≤60 chars shown on the pane, status line and `fm goal list`, editable with one command.

- **Show "since you left" on the first prompt of a resumed goal** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: the goal spans days and crashes; the user returns cold. A 3-line welcome-back (rows closed, one thing that surprised, next move) feels like a colleague, not a log.
  Done when: a resumed session's first output starts with that three-line note, derived only from ledger files, and a kill/resume test shows it.

- **Make the stage rail celebrate a first-time-green row** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: the demo already shows a rail and live tree; a small one-frame flash on a row that passed first try (T-0217 confidence idea) rewards the behaviour Foreman wants.
  Done when: the pane renders a distinct glyph for first-try rows, respecting reduced-motion, verified by a snapshot test.

- **Give an abandoned goal a dignified "parked" card** — FEATURE — value 3 — effort S — risk low — category: empty states
  Why: stopped-vs-done is the pack's core theme; a parked goal should read as "paused, here's how to wake it", not as a failure. Assumption: today it just disappears from the pane.
  Done when: a goal idle >7 days shows a parked card with its last row, reason and the single resume command.

- **Print the plan as a one-page "what finished looks like" poster** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: users judge a plan better when it reads like the finished product's feature list than a task tree; the goal prompt is vague by definition.
  Done when: `fm goal poster` outputs a one-page markdown of contents rows grouped by capability, each with a plain-word "you can…" sentence.

- **Wild: Play the goal back as a 30-second timelapse on the site** — FEATURE — value 3 — effort L — risk low — category: site
  Why: wild; Genesis already has a live tower graph page and demo/live.svg exists, so a scrubbable replay of rows appearing, closing and being added is within the site's idiom.
  Done when: a finished goal's site page has a play control that animates its ledger events in order, no network calls.

- **Wild: Let the user name the goal's mascot hard hat mood** — FEATURE — value 2 — effort S — risk low — category: personality
  Why: wild; the logo is a hard hat with a check mark. The pane's corner hat could be hopeful with rows open, tired on a stall, and tipped when done. Small, shareable, memorable.
  Done when: the pane and site show three distinct hat states mapped to open, stalled and done, with a setting to turn it off.

- **Wild: Generate a "foreman's postcard" when a multi-day goal ends** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: wild; the README leans on demo visuals and people show them. A single-image summary (days, rows, tasks, first-try rate, one proud diff) made locally as SVG is something to post.
  Done when: `fm goal postcard` writes an SVG with those five facts, no external fonts or requests, readable at 1200px wide.

- **Ask one friendly question when the goal is vague, not five** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the request is "turn a vague goal into a complete plan"; the user's own intake style is short lines. One sharpest question, with a suggested default to accept by pressing enter, keeps flow.
  Done when: a vague goal yields at most one question with a default; accepting it produces the plan without more prompting.

- **Say what the planner added that the user didn't ask for, with a veto key** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: open question about one-line vetoes; showing "+7 rows I added (from lessons/neighbours)" with a drop-by-number command makes the plan feel collaborative.
  Done when: the plan view lists added-not-asked rows separately, and `fm goal drop N` removes one and records it as a steer.

Next question: What does the user feel in the first 30 seconds after a goal closes, and is anything on screen yet telling them it is truly done rather than stopped?
