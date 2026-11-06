# Brainstorm — lens: delight

- **Replace "S/M/L" with a one-line "what this will cost" chip** — FEATURE — value 5 — effort M — risk low — category: plain words
  Why: the user said "L, T, M mean nothing as letters"; size words shipped, but the user cares about time and usage. Measured data (median task time, gate minutes, bookkeeping calls) can turn a size into "~25 min, ~1 gate run, light usage".
  Done when: `fm ui --json` and the band chip show an estimate from this project's own history for any planned task, and a project with no history shows "no estimate yet".

- **Show a "back from the gate" micro-win line after slow steps** — FEATURE — value 4 — effort S — risk low — category: feedback
  Why: gates take 8 min each and the user feels the slowness. A short line like "tests passed, 8m02s, 3 faster than your median" turns dead waiting into visible progress.
  Done when: after any gate finishes, one quiet row shows duration versus the project median, and nothing appears for runs under 10 s.

- **Add a "tell me like I'm skimming" digest on return** — FEATURE — value 5 — effort M — risk low — category: return card
  Why: multi-day Volt sessions and "hours" of work imply the user steps away. Existing "while you were away" and "morning digest" ideas describe the concept, but not the form. Proposal: three lines (done, needs you, next), each with a single-key jump.
  Done when: when the user's first keystroke follows more than 30 minutes idle, a card with ≤ 3 lines and key hints is shown, and dismissing it takes one key.

- **Let the user rate a finished task with one key to teach taste** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: the user said brainstorms miss "things I want but don't know how to say". Ratings (👍/👎 plus an optional word) on ideas and finished tasks give the signal that the taste-profile idea lacks.
  Done when: pressing one key on an idea card stores a rating in the record, and the next brainstorm pack includes the liked and disliked titles.

- **Make every error say what to do, in plain words, with a fix key** — FIX — value 4 — effort M — risk low — category: error UX
  Why: "clean up your output" plus "no commands handed to them". Gate refusals and hook failures should end with an action Foreman can take itself ("Retry", "Capture as task"), not a command to copy.
  Done when: each of the top 5 refusal messages shows a plain sentence and one actionable button, and a test asserts no message contains a raw `fm ...` command for the user to run.

- **Add a "scope creep meter" on the band during execution** — FEATURE — value 3 — effort M — risk low — category: awareness
  Why: the user pushes for captured-not-chased requests. Show files touched versus files the plan named, and turn amber when work wanders.
  Done when: editing a file outside the plan's listed files raises the meter, and the dashboard card shows "3 of 4 planned, 2 extra".

- **Wild: Hold a "Foreman standup" at session start, in the mascot's voice** — FEATURE — value 3 — effort S — risk low — category: personality
  Why: wild. The mascot exists but only reacts; a 4-line spoken-style recap (yesterday, today, blockers, one joke-free observation) makes the system feel like a colleague. Voice is configurable and off by default.
  Done when: a session start with the setting on prints a ≤ 4-line standup built from the ledger, and the setting off prints nothing.

- **Wild: Put a "hall of fame" of the fastest and cleanest tasks in the dashboard** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. Gamifying the measured numbers (fewest bookkeeping calls, shortest gate, zero audit findings) gives the user a reason to enjoy trimming overhead, and a visible record that "faster" is working.
  Done when: the dashboard lists the top 3 tasks by a chosen metric, and the list updates after a task closes.

- **Wild: Offer "undo the last hour" as a visual scrub bar** — FEATURE — value 4 — effort L — risk high — category: safety
  Why: wild. Autonomous overnight runs are scary. A scrubbable timeline of git snapshots plus record state, with a preview of each point, lets the user rewind safely. It combines the `fm undo`, snapshot and replay ideas into one gesture.
  Done when: scrubbing to a past point shows its diff summary and restoring it returns files and record to that state, verified by a test.

- **Add a "teach Foreman" capture that turns a complaint into a rule or test** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: the user's recurring complaints (slow, rot, quiet output) were fixed one at a time. Typing "that was annoying" should file a task, propose a regression check, and link it back, so complaints aren't lost between sessions.
  Done when: capturing a message flagged as a complaint creates a task with the quoted words and a proposed check, and the check appears in the verification list.

- **Wild: Draw a "queue weather map" that forecasts when the queue will finish** — FEATURE — value 3 — effort M — risk low — category: forecasting
  Why: wild. The band shows queue progress but not the finish time; with measured medians, a "done around 4 pm, 70% confident" line with a range bar answers "how long will this take?" before it's asked.
  Done when: the queue row shows a finish-time range from history, and the range narrows as tasks complete.
