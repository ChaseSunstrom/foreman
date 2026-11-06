# Brainstorm — lens: delight

- **Open each resumed session with a three-line "where we were" story** — FEATURE — value 5 — effort S — risk low — category: resume
  Why: assumption: the goal is carried across crashes and compactions, but the user meets that only as a state dump. The story reads the baton and ledger as: last finished step, the step in flight, the next step and why.
  Done when: after a killed session, the next SessionStart prints exactly 3 lines naming the last closed step, the open step and the next step, and a test compares them to the ledger.

- **Add a finish-line trail to the status line and web UI** — FEATURE — value 4 — effort M — risk low — category: progress
  Why: assumption: a multi-day goal has no glanceable shape. The trail is one row of beads per contents row, each marked done, partial, unproven or untouched, with the current bead pulsing.
  Done when: `fm status` and the web UI show one bead per goal row, and flipping a row to unproven changes its bead in both.

- **Stamp "done" or "merely stopped" on every goal verdict** — FEATURE — value 5 — effort S — risk low — category: done-ness
  Why: the capability text says it "knows when it's actually done rather than merely stopped". assumption: the user only sees this distinction when it is named aloud. The stamp shows the reason (budget, crash or a row left unproven) beside a green "finished" seal, which appears only when every row is proven.
  Done when: a goal with one unproven row prints "stopped: 1 row unproven" and never "finished".

- **Show an honest finish-date band, redrawn daily** — FEATURE — value 4 — effort M — risk med — category: forecast
  Why: assumption: the user asks "when will this be done?" and gets a guess. The band comes from the goal's own row close times and shows "needs N more closes" until there are enough rows to trust it.
  Done when: a fixture goal with 10 closed rows yields a band, a goal with 2 closed rows prints "too early", and no band is shown without an evidence floor.

- **Count compactions and crashes survived on the goal** — FEATURE — value 3 — effort S — risk low — category: resilience
  Why: assumption: the carry-over machinery works invisibly, so nobody sees it earn its keep. A small "survived 2 compactions, 1 crash, 1 usage-limit wait" line on the goal card makes it visible.
  Done when: a goal that survived a forced compaction shows the count 1, and the count is read from the baton log rather than a new counter.

- **Draft a vague goal's finished version as a deck of parts the user can strike out** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: the capability says to turn a vague goal into what a finished, best-in-class version contains. A one-word-per-card reply (keep, drop, later) turns each card into a contents row, dropped cards go to the dropped ledger, and later cards go to deferred.
  Done when: a fixture goal produces 8 or more cards, and answers "keep", "drop" and "later" create a row, a ledger entry and a deferred item respectively.

- **Show a once-only milestone note** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: a long goal has no felt moments. It fires once, at the first proven row and the halfway row, as one plain line such as "first row proven; the other 11 are untouched".
  Done when: closing the first proven row prints the line once, and closing a second does not repeat it.

- **Draw scope growth as a ring on the goal card** — FEATURE — value 3 — effort S — risk low — category: scope
  Why: assumption: the contents of a goal grow as rows are added, and nobody sees by how much. The ring shows the original rows against added ones and names the biggest addition and the ask behind it.
  Done when: adding 3 rows to a 10-row goal shows "+3 since day 1" with each added row's source.

- **Write a day-end goal postcard** — FEATURE — value 3 — effort S — risk low — category: summary
  Why: assumption: a returning user wants a short human note, not logs. The postcard says what moved, what stalled and the first thing tomorrow, in 5 lines or fewer.
  Done when: ending a day with closed rows writes a postcard file of at most 5 lines naming the closed rows, and an idle day writes none.

- **Wild: Play the goal back as a timelapse in the web UI** — FEATURE — value 3 — effort L — risk med — category: web UI
  Why: wild; assumption: a screenshot is taken at each milestone for UI goals. The timelapse stitches them with row labels and respects reduced motion.
  Done when: a goal with 3 milestone screenshots plays them in order with their labels, and reduced-motion shows a static strip.

- **Wild: Print a finish certificate listing the proof behind every row** — FEATURE — value 3 — effort M — risk low — category: ceremony
  Why: wild; assumption: finishing a multi-day goal should feel like something. The page carries each row's claim, witness and "what this does not prove" line, and it exists only when all rows are proven.
  Done when: finishing a fully proven goal writes a certificate page with one entry per row, and a goal with an unproven row refuses to write one.

- **Wild: Let the user ask a goal row "why are you here?"** — FEATURE — value 4 — effort M — risk low — category: provenance
  Why: wild; assumption: rows sourced from a capability map or a brainstorm look arbitrary after days. The answer quotes the user's words, or says "tower-originated" if it came from nowhere the user said.
  Done when: `fm goal why ROW` prints a quoted user ask or "tower-originated" for every row of a fixture goal.

- **Show a ghost outline of the finished version that fills in as rows close** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: assumption: a goal page of rows has no sense of "how much of the whole thing exists". Each part of the best-in-class map starts as a dotted outline, fills when proven and stays hatched when unproven.
  Done when: the page shows one outlined slot per capability-map part, and closing a row fills exactly its slot.

Next question: Which moments in a multi-day goal would the user show someone else, and does any surface capture them without being asked?
Next question: When a goal resumes on a harness without hooks, which of these resume and done-ness outputs still reach the user?
