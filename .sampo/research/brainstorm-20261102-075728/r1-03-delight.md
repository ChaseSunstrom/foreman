# Brainstorm — lens: delight

- **Show a "you can now…" line on every row close** — FEATURE — value 4 — effort S — risk low — category: goal delight
  Why: the goal engine carries a plan over days, but a closed row is only a status flip; the user's stated need is knowing when it's "actually done". Ideas so far cover receipts and finish cards, not the per-row moment. A one-line capability sentence ("you can now resume after a crash") makes progress felt each time.
  Done when: closing a goal row prints one line starting "You can now" derived from the row's title and its passing probe, and a row without a probe prints none.

- **Ring a topping-out when the last must-row closes** — FEATURE — value 3 — effort S — risk low — category: milestones
  Why: assumption: plan rows are (or will be) tagged must/should/could; the pack lists the tiering idea but no moment of celebration for crossing it. The user gets one calm note: "Every must-row is proven. Remaining: N should, M could."
  Done when: closing the final must-row emits that note exactly once per goal, and reopening a must-row re-arms it.

- **Open a resumed goal with a three-line "where we were" story** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: the request says the plan survives days, crashes and compactions; the user's recurring need is not re-explaining. Story is rebuilt from baton, ledger and git only: last proof, what was in flight, the next row.
  Done when: after a kill-and-resume drill the first output has three lines naming the last closed row, the interrupted row and the next row, matching the files.

- **Print a finish certificate listing the proof behind every row** — FEATURE — value 4 — effort M — risk low — category: finish
  Why: "knows when it's actually done" is the core ask. A keepsake page (markdown, plus SVG for sharing) where each row shows the command that proved it and its date makes "done" feel earned rather than declared.
  Done when: `fm goal finish` writes a file with one line per row (id, title, proof command, pass date) and refuses a row with no proof.

- **Show the "you said / we built / not proven" receipt at finish** — FEATURE — value 5 — effort M — risk med — category: honesty
  Why: the user's words are captured verbatim; echoing them beside what exists and naming the unproven part is the delightful form of honest reporting. Stops "merely stopped" passing as done.
  Done when: the finish output has three sections, each user phrase maps to at least one row or is listed under "not proven", checked on a fixture goal.

- **Draw the goal as a ghost outline that fills in** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: surface is a web UI; a read-only goal page showing the finished version as a faint outline whose rows light up as proofs land makes progress visible across days. Scope growth shows as an extra ring, and reduced-motion users get a static version.
  Done when: the goal page renders every row as outlined, filled with proof, or ringed as added later, and respects prefers-reduced-motion.

- **Add a "try this first" card to the finish** — FEATURE — value 4 — effort S — risk low — category: handoff
  Why: finishing a goal leaves the user to guess what to do next. Three concrete commands from the rows' own probes let them touch the result within a minute.
  Done when: the finish card lists up to three runnable commands taken from probes, and each runs green on the fixture.

- **Write a one-line logbook entry per working day** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: multi-day goals lose their thread; assumption: a short dated line (rows closed, crashes survived, compactions) built from the ledger gives the user a diary to skim. It is a file the user can edit, not injected into sessions.
  Done when: a day with goal activity appends exactly one line to the goal's logbook, and a day without activity appends none.

- **Offer a "got N minutes" pick** — FEATURE — value 3 — effort S — risk low — category: pacing
  Why: assumption: rows carry effort sizes (S/M/L as tasks do). Saying "20 minutes" and getting the best-fitting unblocked row makes a long plan feel approachable.
  Done when: `fm next --minutes 20` returns an unblocked S row if one exists, and otherwise says so without suggesting an L.

- **Make the progress bar able to go backward, with the reason** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: it's delightful to trust a bar. When a row reopens or a probe stops passing, the bar drops and prints "−1: R7 probe failing since the dependency bump".
  Done when: failing a previously passing probe lowers the count and prints one reason line naming the row and the cause.

- **Wild: Seal a "what delight looks like" sentence at goal start and read it back at finish** — FEATURE — value 3 — effort S — risk low — category: wild goal
  Why (wild): vague goals carry an unspoken picture of success. Asking once, then returning the user's own sentence with a verdict beside it, catches a plan that met the letter but missed the point.
  Done when: finishing a goal that has a sealed sentence prints it unmodified next to a user-confirmed yes/no.

- **Wild: Let a tool-less child write the goal's postcard from the ledger alone** — FEATURE — value 3 — effort M — risk med — category: wild goal
  Why (wild): a cold child that never saw the build writes five lines on what a stranger would say was made. A mismatch with the receipt exposes overclaiming.
  Done when: the postcard is generated from files only, and a differing claim is listed under "claims the receipt doesn't support".

- **Wild: Replay the goal as a ten-second timelapse in the web UI** — FEATURE — value 3 — effort M — risk low — category: wild UI
  Why (wild): days of work become something the user shows others, built from timestamped ledger events, with crashes and compactions as visible ticks.
  Done when: a play control steps through closed-row events in time order and ends on the finish state, with a static fallback under reduced motion.

Next question: Which moments in a multi-day goal would the user actually show someone else, and does any surface capture them today?
Next question: Does the user read finish output at all, or only the status line, and what does the drop ledger say about which notes they ignore?
