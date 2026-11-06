# Brainstorm — lens: delight

- **Write the morning note like a person left it** — FEATURE — value 5 — effort S — risk low — category: morning note
  Why: the mission is "work starts without the user"; the user's first contact with that is whatever they read on return. Pack ideas mention a "while you slept" card and a morning ledger but none specifies voice. assumption: plain first-person sentences ("CI went red on main at 2:10; I drafted a fix on night/1101, tests pass, one yes to merge") land better than a table.
  Done when: after a seeded night with one fired trigger, `fm` prints a ≤6-line note that names what fired, what it produced, what it cost, and the single yes needed, and a cold read finds no jargon or ids without a plain label.

- **Celebrate the first self-started success exactly once** — FEATURE — value 4 — effort S — risk low — category: first win
  Why: the first time a trigger starts work that the user keeps is the product's proof moment. assumption: no one-time marker exists today.
  Done when: the first adopted self-started lane prints a single warm line and a receipt; a second adopted lane prints nothing extra; a test checks the once-only flag survives a restart.

- **Show every queued install as one card with one-word answers** — FEATURE — value 5 — effort M — risk low — category: yes card
  Why: the request says installs "queued for one yes". Showing exact unit text, enable command and uninstall line on one screen with `yes`/`no`/`later` makes it a pleasure, not a chore.
  Done when: with three queued installs, `fm yes` renders one card listing each unit's text and its undo line, and a single word applies or defers each, with the result echoed.

- **Name each trigger and print a one-line receipt when it fires** — FEATURE — value 4 — effort S — risk low — category: trigger receipts
  Why: the night tick logs only when something happens, so most of the time the user sees nothing; a named, human receipt ("Tidy-Tuesday woke at 03:00, filed 2 tasks") makes the layer feel alive.
  Done when: each fire appends a receipt naming the trigger by its user-given name, and `fm triggers` shows the last receipt beside each name.

- **Draw the night as a timeline strip in the web UI** — FEATURE — value 4 — effort M — risk low — category: web UI motion
  Why: the only surface found is the web UI, and the pack's UI pillar wants states that move. A strip of dots for fires, lanes, waits and yeses, with the current moment gently pulsing, explains state without text. assumption: the tick log has timestamps to plot.
  Done when: a screenshot of the page after a seeded night shows fire, lane and wait marks in order, with an empty state ("nothing woke me") and an error state both rendered.

- **Offer a quiet-hours dial instead of a cron string** — FEATURE — value 3 — effort S — risk low — category: scheduling
  Why: users rarely love writing schedules; a slider-style "work between 11pm and 6am, not while I'm typing" is friendlier. assumption: the tick can read a start/end pair.
  Done when: `fm night hours 23-6` (or the UI dial) sets the window, and a fire attempted at 14:00 is held with the reason "outside quiet hours" in its receipt.

- **Tell the user kindly when a trigger has never helped** — FEATURE — value 3 — effort S — risk low — category: trigger hygiene
  Why: `fm triggers` already measures precision; a gentle "this one fired 9 times and you never used the result; retire it?" turns a metric into a courtesy. 
  Done when: a trigger with 0 adopted fires in 7 days shows a single retire-or-keep prompt in the morning note, and a "keep" answer silences it for 30 days.

- **Show "what would wake me" on the status line** — FEATURE — value 3 — effort S — risk low — category: status line
  Why: invisible automation makes people nervous; a tiny glance at armed triggers builds trust. assumption: the status line has room for ~20 chars.
  Done when: the status line shows `⏰ 3 armed` and `fm triggers` lists them; with none armed the segment is absent.

- **Wild: Let the night shift leave a postcard from each lane** — FEATURE — value 3 — effort M — risk low — category: wild delight
  Why: wild. A lane's last line becomes a short, signed postcard ("Lane 2, from the 2am CI failure: found it, one-line fix") stacked in the morning card, so the night feels like a crew reporting in.
  Done when: each night lane writes a ≤140-char postcard on stop, and the morning view shows them in order, each linked to its branch.

- **Wild: Play the night back as a ten-second timelapse** — FEATURE — value 3 — effort M — risk low — category: wild delight
  Why: wild. Replay the strip of events at 100× in the web UI with the stage rail advancing, something people would show a colleague. assumption: events are timestamped and retained.
  Done when: a "Replay night" button animates the recorded events in ≤10 s, and honours reduced-motion by showing the final state instead.

- **Wild: Knock twice to cancel everything** — FEATURE — value 3 — effort S — risk low — category: wild delight
  Why: wild. A single `fm hush` (or touching one file) freezes every trigger and held lane, with a cheerful confirmation and a one-word `fm resume`; the safety valve people want before they feel safe enough to install anything.
  Done when: creating the hush file stops the next tick from firing anything and the morning note says "hushed since 22:14"; removing it resumes on the next tick.

- **Give the first dry run a visible rehearsal** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: a trigger's first fire as a clearly labelled "rehearsal" (what I would have done) lets the user watch it work before it touches anything, matching "queued for one yes".
  Done when: a newly armed trigger's first fire writes a rehearsal receipt with no branch or task created, and `fm triggers` shows "rehearsed, awaiting go".

- **Say why a trigger didn't fire, in a sentence** — FEATURE — value 4 — effort S — risk low — category: explain
  Why: the night tick logs only when something happens, so silence is ambiguous; "didn't fire: you were typing in the repo until 03:40" turns a mystery into a feature.
  Done when: `fm why-not <trigger>` prints one plain sentence naming the blocking condition (quiet hours, mid-flow, budget, hush, no event) for the last evaluation.

Next question: What does the user feel in the first 30 seconds after the first trigger fires without them, and which surface do they see it on?
Next question: Which of the 59 cells describe a moment of delight versus a moment of mere plumbing, and does anything measure whether the delightful ones get noticed?
