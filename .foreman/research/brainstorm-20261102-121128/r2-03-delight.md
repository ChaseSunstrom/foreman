# Brainstorm — lens: delight

Lens: delight. Round 2 ideas, avoiding the listed ones (hard hat moods, replay clip, proof card, stage-rail animation, clickable ids, guided first win, Friday recap, train timetable, and similar are already taken).

- **Show a "close call" shelf for the guard** — FEATURE — value 4 — effort M — risk low — category: guard delight
  Why: the guard is the product's identity, but its saves are invisible once blocked. Assumption: guard decisions are already logged.
  Done when: `fm guard saves` lists the last 10 blocked commands, each with the rule that caught it and what it would have done, and the web UI home shows the count this week.

- **Give every task a one-line headline written at close** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: the recent commit log is dense (`T-2610: calibration reads compare like with like: a close or a task or choice bet counts only once…`). Close-out legibility sits deferred in T-0795. A plain headline is what people show others.
  Done when: closing a task stores a headline of 80 characters or fewer with no task ids or jargon, and `fm next` and the web UI list it in place of the long title.

- **Add a "why this one next" whisper to fm next** — FEATURE — value 4 — effort S — risk low — category: queue
  Why: the queue holds 30+ deferred items plus hold rules (round-first, depends-on). The user's steers show they keep asking why things wait (T-2462, T-2441). Assumption: the reasons already exist in code.
  Done when: each row from `fm next` ends with a 6-word reason such as "unblocked by T-2441", and a held item shows what it waits on.

- **Make the demo SVG regenerate from the latest real session** — FEATURE — value 3 — effort M — risk med — category: showcase
  Why: the README leads with `demo/live.svg`, recorded against Claude Code 2.1.301. Stale demos quietly lose trust. Assumption: the recording script is reproducible.
  Done when: `fm demo record` rebuilds `demo/live.svg` from a fresh run, and `fm doctor` warns when the SVG is older than the installed Claude Code version.

- **Name each settled bet in the feed with a tiny result line** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: bets now settle unattended through the night tick (the first ask in the user's words), so nobody witnesses them settling. The calibration stays abstract unless a single settlement is felt.
  Done when: the session start note includes "You were right on 3 of 4 bets overnight: T-2601 held" at most once per session, and the web UI shows the same line.

- **Offer a `fm doctor --calm` view that prints one line when all is well** — FEATURE — value 3 — effort S — risk low — category: doctor
  Why: doctor checks keep growing (timer liveness, steer checks, sweeps). A wall of OKs hides the one WARN.
  Done when: with no WARN or FAIL, `fm doctor --calm` prints a single line, and with any WARN it prints only the failing rows.

- **Let the web UI theme follow the host terminal palette** — FEATURE — value 3 — effort M — risk low — category: UI polish
  Why: T-1217 notes Claude Code paints the pane at #262626 while Foreman's background differs, which is a visible seam. Matching the palette removes it. Assumption: the palette is readable from the terminal.
  Done when: the pane background equals the host's measured background in a screenshot test, and a manual override setting exists.

- **Wild: Write the weekly changelog as the project's own release notes in the project's voice** — FEATURE — value 3 — effort M — risk low — category: storytelling — wild
  Why: assumption: users who see the last seven days of closed tasks as notes, in the voice of their own README, will share them. It also gives a free check on whether the headlines are readable.
  Done when: `fm notes --week` writes a markdown file with at most 10 bullets, each traceable to a closed task id.

- **Wild: Let the user "adopt" a lesson by naming it** — FEATURE — value 3 — effort S — risk low — category: lessons — wild
  Why: lessons are stored with no personality (T-0217 wants confidence on them). A name such as "the Tuesday migration rule" makes the lesson something people refer to. Assumption: lessons have stable ids.
  Done when: `fm lesson name L-12 "…"` stores the name and later recall notes quote it.

- **Wild: Offer an end-of-day "tool belt" screen that shows only the three verbs you used** — FEATURE — value 3 — effort S — risk low — category: simplicity — wild
  Why: the verb count keeps growing (the lean ratchet counts it), and the user keeps asking for less ceremony (T-0794 Lite mode). A personal belt shows the product is smaller than it looks.
  Done when: `fm belt` lists the user's three most-used verbs of the week with their counts and one verb they have never tried.

- **Play a soft chime or terminal bell when a long run finishes with a pass** — FEATURE — value 2 — effort S — risk low — category: notifications
  Why: assumption: long drives and night runs finish while the user is elsewhere. T-0325 (tray icon) is blocked, so a terminal bell is the cheap path.
  Done when: a setting `notify.bell on` makes a finished drive print a single BEL, and it is off by default.

- **Print the cost of each finished task in plain money and minutes** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: the project is about the duel on cost and time (T-1231) and about close-out legibility (T-0795). Seeing "this fix took 4 minutes and $0.31" is what a user shows others.
  Done when: the finish receipt ends with "4 min, $0.31, 1 retry", and the numbers match `fm cost` for that task.

Next question: Which single line of Foreman output does the user already screenshot or paste elsewhere, and can every other output be made as quotable?
