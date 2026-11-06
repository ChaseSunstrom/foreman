# Brainstorm — lens: delight

- **Write the morning note like a person left it** — FEATURE — value 5 — effort S — risk low — category: delight
  Why: the night tick "logs only when something happens", so a quiet night is indistinguishable from a dead one; the user returns to nothing. Assumption: a single file `morning.md` is the only place self-started work is announced first.
  Done when: after a simulated night with two fires and one skip, `fm night note` writes a ≤120-word first-person note naming each fire, the skip's reason and the one yes waiting.

- **Show the install queue as one card with one-word answers** — FEATURE — value 5 — effort M — risk low — category: consent
  Why: the mission says installs are "queued for one yes"; many timers, units and hooks each asking separately would defeat that. Assumption: the queue exists as separate rows today.
  Done when: `fm yes` prints every pending install with exact unit text, the enable and uninstall lines, and `yes`, `no` or `later` per row works from one prompt.

- **Celebrate the first self-started success exactly once** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: the first time work starts and lands without the user is the whole point of #11 and passes unmarked. Assumption: a trigger-origin stamp on lanes exists or is cheap to add.
  Done when: the first lane carrying a trigger origin that passes its gate prints a one-time receipt ("started by CI red on main, landed on night/<date>") and never prints it again.

- **Explain why a trigger did not fire** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: the pack shows silence as a repeated worry (heartbeat, "make the watcher tell you when it goes blind"). Delight is a straight answer. Assumption: the tick can record a skip reason per trigger.
  Done when: `fm why-not <trigger>` names the last evaluated time, the event seen or not seen, and the reason (debounced, user mid-flow, over budget, quiet hours).

- **Preview a trigger on last week before it arms** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: replay-before-install recurs in earlier ideas but its payoff is felt at the install card: "this would have fired 3 times, 2 useful". Assumption: ci-watch and the capture log hold enough history.
  Done when: the install card for a CI trigger shows a count of would-have-fired events from the last 30 days, each with a one-line outcome.

- **Offer a quiet-hours dial instead of a cron string** — FEATURE — value 3 — effort S — risk low — category: ergonomics
  Why: cron syntax is the unfriendly part of timers. Assumption: the user would rather say "not before 7, not while I'm typing".
  Done when: `fm night hours 23-7` is stored, the tick holds fires outside it, and `fm night` prints the window in words.

- **Tell the user kindly when a trigger has never helped** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: `fm triggers` already measures precision per trigger. Assumption: a gentle one-line offer to retire beats a silent dead timer.
  Done when: a trigger with ≥10 fires and zero accepted results appears in the morning note with "retire? `fm yes`", never auto-removed.

- **Draw the night as a timeline strip in the web UI** — FEATURE — value 4 — effort M — risk low — category: UI and motion
  Why: the web UI is the only surface found, and it already has Activity lanes. Assumption: tick events are readable by the page.
  Done when: the page shows one horizontal strip per night with fires, skips and lanes as marks, an empty state ("nothing needed doing") and a keyboard-reachable tooltip for each mark.

- **Wild: Compile a sentence into a trigger** — FEATURE — value 5 — effort M — risk med — category: wild
  Why: wild. The user says "when CI fails on main, draft a fix" and gets a trigger draft with a replay and an install card, not a cron line.
  Done when: `fm when "when CI fails on main, draft a fix"` writes one row in the trigger table in shadow mode and prints its would-have-fired count.

- **Wild: Play the night back as a ten-second timelapse** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: wild. Overnight work is invisible; a replayable strip of lanes opening, gates going green and branches landing makes it something to show others. Assumption: lane events carry timestamps.
  Done when: a "play" button on the night page replays one night in 10 seconds with reduced-motion users getting a static step list.

- **Wild: Touch one file to freeze everything** — FEATURE — value 4 — effort S — risk low — category: wild
  Why: wild. A calm, physical off switch (`touch ~/.foreman/hush`) makes unattended work feel safe to leave on. Assumption: the tick can check one stat per run.
  Done when: with the file present no trigger spawns work, the tick logs "hushed", and removing it resumes within one tick.

- **Show "what would wake me" on the status line** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user can't see what is armed. Assumption: the trigger table is cheap to read.
  Done when: the status line shows a short count like "3 armed" and `fm triggers` expands it, with nothing injected into model context.

- **Wild: Leave a postcard from the lane** — FEATURE — value 3 — effort S — risk low — category: wild
  Why: wild. A finished self-started lane signs off with one line in the lane's own words ("fixed the flaky timeout; test went red first") appended to the morning note.
  Done when: each landed night lane contributes one ≤20-word line, taken from its closing receipt, to the note.

Next question: What does the user do in the first minute after returning from a long absence, and which single screen or file would they open first?
Next question: Which trigger would the user be upset to find had fired without a visible trace, and does every fire path leave one?
