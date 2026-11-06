# Brainstorm — lens: delight

- **Open a new repo with one card that names a fact only its code shows** — FEATURE — value 4 — effort S — risk low — category: first run
  Why: assumption: a newcomer's first `fm init` ends with setup output, so the first delight is missing. `fm map` already knows the slowest gate and the least-touched directory.
  Done when: `fm init` on the fixture repo prints a card whose one fact matches a `fm map` field, and the card is absent on a second init.

- **Keep the half-typed request when fm restarts** — FEATURE — value 4 — effort S — risk low — category: prompt continuity
  Why: the user has dropped and re-sent requests (the "recreated with interpretation" drops). Losing a typed request on a crash or restart costs the same retyping.
  Done when: kill `fm code` with 40 characters typed, restart, and the prompt shows those 40 characters unchanged.

- **Say durations the way a person would ("a little under four minutes")** — CLEAN — value 3 — effort S — risk low — category: receipt wording
  Why: receipts print raw seconds such as `222 s`. Assumption: a rounded phrase reads faster, and the exact figure stays in `--verbose`.
  Done when: a 222 s task prints "a little under four minutes", and tests cover 8 s, 61 s, 222 s and 3,700 s.

- **Wrap receipts with a hanging indent at the pane's width** — CLEAN — value 3 — effort S — risk low — category: layout polish
  Why: the pane wraps receipt lines raggedly and splits words. Assumption from the demo's narrow pane.
  Done when: at 40 columns every continuation line aligns under its label and no word is split.

- **Open a failed gate by saying what passed** — FEATURE — value 3 — effort S — risk low — category: failure tone
  Why: a gate failure currently leads with the failing line. Naming the passes first tells the user how little is actually broken.
  Done when: a gate with 3 passes and 1 failure prints "3 passed" before the failing assertion.

- **Credit the test that caught the bug, by name, on its receipt** — FEATURE — value 3 — effort S — risk low — category: close receipt
  Why: receipts show proof but not which test did the catching, the one thing a user would want to credit.
  Done when: a fix whose first red test was `test_x` prints "caught by test_x" on close, and a fix with no red run prints nothing.

- **Postmark each receipt with the commit's local time and zone** — wild — FEATURE — value 2 — effort S — risk low — category: receipt charm
  Why: assumption: a receipt that reads like a letter, stamped with where and when it landed, is the kind of small touch people show others.
  Done when: the receipt's postmark matches the offset in the commit's `%ci`, and a commit with no timezone gets no postmark.

- **Flick a backlog row to throw it into the next run** — wild — FEATURE — value 2 — effort M — risk low — category: queue motion
  Why: assumption: reordering the queue is drag-and-drop today, which is slow and fiddly. A flick gesture gives it weight and motion that explains the change.
  Done when: a fast drag in the web UI moves the row to the top of the queue within one frame, and the reorder is written to the journal.

- **Nudge a run stalled for ten minutes with one question it has not asked itself** — wild — FEATURE — value 3 — effort S — risk med — category: stall recovery
  Why: assumption: stalls often mean the model is looping on one approach. The stalled card exists, but nothing offers a different angle. Risk: a nudge can derail a run that was about to finish, so it is steered, not forced.
  Done when: a run stalled for 10 minutes gets exactly one nudge line appended to its steer journal, and a second stall does not repeat it.

- **Fill the empty queue with a single line about the last thing you finished** — FEATURE — value 2 — effort S — risk low — category: empty state
  Why: assumption: an empty queue currently shows nothing useful. The last closed task is already in the journal and makes a warmer empty state.
  Done when: with no open tasks, `fm status` prints one line naming the last closed task and its close time, and with no closed tasks it prints the usual empty message.

- **Wild: let the pane's cursor blink in the rhythm of the model's typing speed** — wild — FEATURE — value 2 — effort S — risk low — category: motion tempo
  Why: assumption: the work bar pulse exists, but a cursor that matches the model's output tempo ties the pane's motion to real activity instead of a timer.
  Done when: the cursor blink interval follows the measured tokens-per-second over the last 5 seconds, and it is steady when output has stopped.

- **Wild: have the close line change with the shape of the day** — wild — FEATURE — value 2 — effort S — risk low — category: close voice
  Why: assumption: one fixed closing sentence gets tuned out. Choosing among a few lines by the day's pattern (busy, quiet, first run of the week) keeps the close fresh without adding content.
  Done when: a day with 6+ closes uses the busy line, a day with 1 close uses the quiet line, and a test pins each rule.
