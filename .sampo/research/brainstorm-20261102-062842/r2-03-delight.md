# Brainstorm — lens: delight

- **Show a "tick tape" replay in the web UI** — FEATURE — value 4 — effort M — risk low — category: web UI, motion
  Why: the mission needs self-triggering measured without the user's install; a recorded tape of ticks, fires and skips is the evidence, and a scrubbable strip makes the invisible visible. Assumption: the tick log (or a replay tape) already has timestamps and outcomes.
  Done when: opening the page against a fixture tape shows a timeline where each fire, skip and "checked, nothing found" is a distinct mark, and scrubbing moves a cursor that updates the detail panel.

- **Open sessions with a one-line "while you were away"** — FEATURE — value 5 — effort S — risk low — category: session start
  Why: the user is told nothing when a lazy tick or shadow tick ran; quiet reads as dead. Done when: SessionStart prints one line naming ticks since the last session, how many fired, and the count "checked, nothing found", and prints nothing if no tick ran.

- **Write the morning note in a person's voice** — FEATURE — value 4 — effort S — risk low — category: copy
  Why: the nightly digest names the worst-calibrated bet kind; a digest that reads like a note left by a colleague is read, and an unread output proves nothing. Assumption: the digest is plain text today.
  Done when: the nightly digest passes a lint of at most 6 lines, first-person, ending in one suggested next command.

- **Ring a one-time "first self-started result" moment** — FEATURE — value 4 — effort S — risk low — category: celebration
  Why: the first time a tick starts work the user keeps is the proof self-triggering works, and it deserves marking once. Done when: the first fire whose task is later closed prints a single dated line, and a second such fire prints none.

- **Breathe a "next tick due" dot on the status line** — FEATURE — value 3 — effort S — risk low — category: status line
  Why: the user can't tell if a timer exists. Done when: the status line shows a dot that is green when the last tick is within three intervals, amber beyond that, and absent when no tick has ever run.

- **Pitch the timer with the user's own numbers** — FEATURE — value 4 — effort M — risk low — category: install card
  Why: the install waits on the user. A card saying "your last 8 sessions began with N hours of unattended-eligible work" gives a reason to say yes. Done when: `fm night` prints a counterfactual line computed from ledgers with the exact install command, and the line is absent when there is no data.

- **Give each trigger a name and a receipt line** — FEATURE — value 3 — effort S — risk low — category: naming
  Why: fires are anonymous task rows. Done when: each fired task title starts with the trigger's name, and `fm why <task>` prints "fired by <name> at <time>".

- **Show the stage rail's first step as a trigger glyph** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: the Foreman pane's stage rail shows work stages; self-started work should look different at a glance. Done when: a self-started task's rail begins with a distinct glyph, and a user-started one does not.

- **Fast-forward a replayed week as a ten-second timelapse** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: replaying a recorded week through the dispatcher is how self-triggering gets graded without waiting a week. Assumption: the replay produces ordered events. Done when: the page plays a 7-day fixture replay in under 12 seconds and ends on a summary of fires kept versus dropped.

- **Wild: Hatch a tick-egg on the status line** — FEATURE — value 2 — effort S — risk low — category: playful, wild
  Why: assumption: a tiny creature that grows with each on-time tick and rests when ticks are late makes liveness something people glance at and show others. Done when: the status line shows a stage glyph derived from the count of on-time ticks, and a missed tick resets it to the egg.

- **Wild: Sign the night's note as "the night watchman"** — FEATURE — value 2 — effort S — risk low — category: voice, wild
  Why: assumption: a persona with a consistent sign-off turns "checked, nothing found" from silence into reassurance. Done when: the note ends with a fixed sign-off line and a quiet night still produces a one-line note.

- **Wild: Replay last Friday evening as a ghost shift** — FEATURE — value 3 — effort M — risk low — category: demo, wild
  Why: assumption: showing the user what the tick would have done during hours they were away, using their own history, is more convincing than any claim. Done when: `fm night ghost` replays the previous evening's ledgers on a virtual clock and prints what would have fired, writing nothing to the task list.

- **Wild: Let a stub user decline every fire and report who noticed** — FEATURE — value 3 — effort M — risk low — category: measurement, wild
  Why: assumption: the delight is a confident number, "N fires would have been kept," which needs a baseline that rejects everything. Done when: a replay run with an all-decline stub reports a kept-rate of zero and a nonzero kept-rate for the real stub.

Next question: What does the user actually do with the nightly digest the morning after, and is there any trace of it being read?
Next question: Which moment would make the user tell someone else that Foreman ran while they slept?
