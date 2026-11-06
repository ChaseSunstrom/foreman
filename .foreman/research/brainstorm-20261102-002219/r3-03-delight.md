# Brainstorm — lens: delight

- **Write a bookmark sentence at every stop** — FEATURE — value 4 — effort S — risk low — category: resume
  Why: assumption: a resume that opens mid-stride feels better than one that opens with a status table. At crash, compaction or day end, the goal stores one sentence in the user's voice, "Next I was about to wire the tier column into the sweep," and the next session opens with it.
  Done when: after a kill mid-row, the next `fm next` prints that sentence first, and it names the file or row being worked.

- **Offer a "got N minutes" pick** — FEATURE — value 4 — effort M — risk low — category: goal flow
  Why: assumption: users drop in with a short window and pick nothing because every row looks big. `fm goal short 15m` returns the one open row whose past duration (recorded estimate versus actual) fits, or says plainly that none does.
  Done when: with rows of mixed sizes, the verb returns a row under the budget, and prints "nothing fits, closest is X" otherwise.

- **Print a "you can now…" line on every row close** — FEATURE — value 4 — effort S — risk low — category: progress
  Why: assumption: closing a row says "row 7 done," which tells the user nothing they can try. A line like "You can now run `fm goal short` and get a row" is a capability sentence, taken from the row's own done-when.
  Done when: closing any row prints a line starting "You can now", and a row with no done-when is refused for lacking one.

- **Show You said / We built at finish** — FEATURE — value 5 — effort M — risk low — category: finish card
  Why: assumption: the vague goal's value is that it was vague, and showing the original sentence beside the shipped parts is the proof. The finish card prints the user's verbatim goal on the left and the delivered capabilities on the right, with unmatched words from the goal flagged.
  Done when: finishing a fixture goal prints both columns, and a goal word with no matching row shows a "not covered" mark.

- **Add a "Not quite" button on the finish card** — FEATURE — value 5 — effort S — risk low — category: finish card
  Why: assumption: a user who dislikes the result today has to write a fresh ask. `fm goal notquite "the colours are wrong"` reopens the goal and turns the complaint into a new row without ceremony, and records which "done" was wrong.
  Done when: after a finish, one command reopens the goal with the complaint as an open row, and the earlier finish is marked "reopened".

- **Keep a trail of paths tried and turned back** — FEATURE — value 3 — effort M — risk low — category: goal page
  Why: assumption: abandoned approaches are invisible, so effort looks wasted. The goal page marks each dead end with "turned back here, because …" next to the row it belonged to, from the not-yet and drop notes.
  Done when: a row with a dropped approach shows the marker with its recorded reason on the goal page.

- **Collect "found along the way" wins on the finish card** — FEATURE — value 3 — effort S — risk low — category: finish card
  Why: assumption: goals often turn up fixes the user never asked for, and they get lost in the commits. Builders tag such a change at close, and the finish card lists them in one short shelf.
  Done when: a task closed with `--bonus` appears under "found along the way" and is excluded from the goal's own contents count.

- **Keep a diary of the hard hat** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: assumption: the web UI has a logo but no personality. The hard hat on the goal page changes pose by state: napping during compaction or a usage-limit wait, tapping a watch when stuck, and a nod when a row closes.
  Done when: the page shows a distinct hat state for working, waiting, stuck and finished, and `prefers-reduced-motion` switches it to static labels.

- **Make row titles pass a read-aloud lint** — CLEAN — value 3 — effort S — risk low — category: plan wording
  Why: assumption: rows written in tower jargon ("wire stage-surface matrix cell") are unreadable at a glance. A lint refuses rows over about 12 words or with an internal verb name, and suggests a plain rewrite.
  Done when: a row titled with a function name is refused with a suggested plain sentence.

- **Wild: draw the goal as a metro map** — FEATURE — value 3 — effort L — risk med — category: web UI
  Why: wild. Rows are stations, dependencies are lines, and a station lights when proven. Interchanges show rows that unblock two others, and the train position is the next row. Hill chart and fog-of-war ideas exist, but the map shows the shape of the dependencies.
  Done when: the goal page renders stations and lines from the goal file, with a lit station for each proven row and a pulse on the next one.

- **Wild: pack a contact sheet of the web UI at each milestone** — FEATURE — value 3 — effort M — risk low — category: finish card
  Why: wild. The web UI is the only surface. A screenshot at each must-row close, stitched into one image at finish, gives the user something to show people.
  Done when: finishing a goal that touched the web UI writes one PNG with a captioned frame per milestone.

- **Wild: let the goal sing its status in one line of ASCII** — FEATURE — value 2 — effort S — risk low — category: status line
  Why: wild. A 20-character skyline on the status line, with a taller bar per proven row and a gap per open one, so progress reads in a glance with no number.
  Done when: the status line shows a skyline whose bar count matches the goal's rows, and an empty goal shows a flat line.

- **Wild: say a good-night line when the last session of the day ends** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: wild. A short sign-off ("3 rows closed, 1 half-done, I know where to start") that doubles as the day-end ref and is shown once, like a note left on the desk.
  Done when: the session end writes the line and the next session shows it exactly once, then never again.

Next question: Which finish-card elements does the user actually read, and can a counter on the card show which parts were scrolled past or acted on?
Next question: Which of the 58 cells would a first-time user notice only when a goal ended in "merely stopped," and does any cell cover that first experience?
