# Brainstorm — lens: beautiful UI and motion

Round 4 ideas from the beautiful UI and motion lens. None repeat the list above; each is a second-order or combined idea.

- **Ship a motion budget linter for the web UI** — CLEAN — value 3 — effort S — risk low — category: motion
  Why: earlier ideas add many animations ("one pulsing element per screen", "stage rail", "hard hat wink") but nothing stops them piling up. Assumption: web UI CSS lives under `plugin/templates/web/`.
  Done when: a test fails if a screen has more than one infinite animation or any animation ignores `prefers-reduced-motion`.

- **Render every receipt state from one verdict component with a state table** — FEATURE — value 4 — effort M — risk low — category: design system
  Why: "proven / unproven / overridden" and "hatched third state" are proposed in several places, but the web UI, the pane and the CLI will each draw them differently. Assumption: they currently don't share a renderer.
  Done when: one table maps each state to glyph, hatch pattern, colour token and text, and web, pane and CLI snapshot tests all read it.

- **Add a "settle" transition when a number changes** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: Today charts, work bar and bets update in place. Assumption: they redraw instantly. A short count-and-tint on change shows what moved since you last looked.
  Done when: a changed gauge shows a 400 ms tint, and the tint is off under reduced motion (tested).

- **Design the "nothing here yet" screen per web view, each with the one command that fills it** — FEATURE — value 4 — effort S — risk low — category: empty states
  Why: new users and fresh repos hit empty History, Agents and Today panes first. Assumption: they currently show blank or zero charts.
  Done when: every web view has a snapshot for empty, loading and error, and the empty one names a real `fm` verb.

- **Show a diff-of-state scrubber on the stage rail** — FEATURE — value 3 — effort M — risk med — category: timeline
  Why: the rail shows current stage only, while the session history already exists in the ledgers. Dragging back shows the plan, edits and proof as they stood.
  Done when: dragging the rail to a past stage shows that stage's recorded step list without a network call.

- **Add a "since you looked" ribbon at the top of every surface** — FEATURE — value 4 — effort M — risk low — category: orientation
  Why: T-1344 asks for a changed-since line on the code home; the need is wider, because the user leaves for hours with overnight timers. Assumption: no surface stores a last-seen mark.
  Done when: reopening the web UI after a night shows a ribbon counting closed tasks, settled bets and new blockers since the stored last-seen time, and it clears on dismissal.

- **Give the guard block a designed "stop" card with the safe alternative** — FEATURE — value 4 — effort M — risk low — category: guard UX
  Why: the guard is the headline feature, yet its block is likely a plain text refusal. A card with the rule, the command, why and a safer form makes it feel like protection, not friction.
  Done when: a blocked command renders a card with rule id, quoted command and one alternative, in terminal and web.

- **Ship a contrast and colour-depth gate for all themes** — FIX — value 3 — effort S — risk low — category: accessibility
  Why: T-1217 shows the docked pane's #262626 background was only noticed by eye. Assumption: no automated contrast check exists.
  Done when: CI fails if any text and background token pair falls under 4.5:1, and each theme renders in 16-colour and truecolor.

- **Typeset the daily report as a printable one-page broadsheet** — FEATURE — value 2 — effort M — risk low — category: reports
  Why: the "daily report" and "weekly receipt" ideas have no layout. One grid with a lead item, a column of closed tasks and a corrections box turns a log into something shown to others.
  Done when: `fm report --print` produces a single A4 page HTML with print CSS, and it has no overflow at 6 or 40 tasks.

- **Wild: Make the guard a visible tripwire that snaps in the pane** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: a blocked command could draw a taut line across the pane that snaps and shows what it stopped. Assumption: the pane can animate over a few frames.
  Done when: a guard block triggers a one-second snap animation in the pane, plus a static fallback when motion is off.

- **Wild: Let the web UI become an ambient dashboard on a spare monitor** — FEATURE — value 3 — effort M — risk low — category: ambient display
  Why: the work bar, rail and bets can be a calm wall display with slow breathing colour: green idle, amber waiting on you, red blocked. Nobody asked, but overnight runs make it useful.
  Done when: `/ambient` shows one full-screen state colour, changes within 5 seconds of a state change, and carries a text label for colour-blind use.

- **Wild: Print a tiny sparkline "heartbeat" of the drive in the terminal prompt** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: a drive can run for hours silently. A 12-character sparkline of tasks closed per hour in the shell prompt shows it is alive.
  Done when: `fm prompt` prints under 20 characters with a sparkline, and it reads from existing ledgers in under 50 ms.

- **Make every chart keyboard- and screen-reader-navigable with a data-table twin** — FEATURE — value 3 — effort M — risk low — category: accessibility
  Why: Today, calibration and Agents graphs are visual only. Assumption: no text alternative exists.
  Done when: each chart has a toggle that shows the same numbers as a table, and arrow keys step through points announcing values.

Next question: which screens of the web UI has the user actually opened, and is there any record of what they looked at first?
Next question: does the docked pane share a renderer with the web UI, or must every visual idea be built twice?
