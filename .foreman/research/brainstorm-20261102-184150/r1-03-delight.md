# Brainstorm — lens: delight

- **Underline the request, cell by cell** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: assumption: the grid and the request live on separate screens, so the user can't see which of their words produced which cell. The idea is to show the request text with each phrase underlined, and hovering or pressing a key on a phrase lights its cells, including the empty ones.
  Done when: a rendered Mission page for gen-4 Mission 1 has every grid cell linked to at least one request span or marked "implied", and a test checks this.

- **Say "Left out: nothing" only with a receipt** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the pack's carried gap is that Foreman must say what it left out. An empty list is indistinguishable from a skipped check. Print "Left out: nothing (N cells, M probes, K n/a with falsifiers)" so an empty answer carries its own evidence.
  Done when: a Mission with zero left-out cells prints that line, and a unit test fails if the counts are missing.

- **Open the Mission page on the sting cell** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: an earlier question asks which cell the user opens first, and the pack doesn't answer it. Anchor the page on the empty cell with the highest sting, then let j/k step through the other empty cells. Log which cell the user actually moves to, so the order can be learned.
  Done when: the page loads scrolled to the top-ranked empty cell, and j/k moves focus in rank order, checked by a DOM test.

- **Give every Exam a "run it yourself" line** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: briefs must name an outcome measure and a live-state reading, but the user has to hunt for the command. Print one copyable line, `Check: <cmd> → expect <value>`, beside each reading, with a one-key copy in the web UI.
  Done when: every filed brief renders a Check line whose command parses, and `fm brief show` prints it.

- **Crown or retire the dissenter in one line** — FEATURE — value 4 — effort S — risk low — category: feed
  Why: dissents scored against outcomes is a carried gap, but a score is cold. When one settles, the feed shows "Dissent from the approaches lens: right, the outcome moved 14 → 9" or "overruled, and the outcome agreed". That makes the dissenters worth reading.
  Done when: settling a scored dissent appends a one-line feed entry with the lens name and the measured change.

- **Ask "which width?" with a timer and a default** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: scope width is already recorded, but nothing lets the user choose it cheaply. Offer three readings (narrow, medium, wide) as one-key choices with a 15-second default, so a user who walks away still gets a sane run.
  Done when: an ambiguous request shows the three-way choice, and a timeout records the default in the ledger as "unanswered-default".

- **Show a coverage bar that admits uncertainty** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: "exhaustive" is a claim. A bar with segments for covered, left out, n/a and unverified, plus a "can't tell" hatch where a canary wasn't run, tells the user how much to trust it.
  Done when: the bar's four counts sum to the grid's cell count and a test fails otherwise.

- **Add a "stop and show me" key to an unattended Mission** — FEATURE — value 3 — effort M — risk low — category: control
  Why: assumption: long unattended Missions feel opaque. One key shows the partial grid and the left-out list so far, then lets the run continue. It reads state only and never pauses the drive.
  Done when: the key prints a grid snapshot whose filled-cell count matches the ledger at that moment.

- **Wild: Argue for doing nothing** — FEATURE — value 4 — effort M — risk low — category: thinking — wild
  Why: every Mission adds things, and the user keeps asking for less. A lens that may only write the brief for "don't build this" gives the user a real alternative, with its own Exam and live-state reading.
  Done when: each Mission page carries a do-nothing brief, and cold-read tests reject one that merely restates a built feature.

- **Wild: Blind-spot bingo** — FEATURE — value 2 — effort M — risk low — category: delight — wild
  Why: assumption: a weekly bingo card of the grid's empty cells would make the user glance at gaps. Squares fill when the user's real work touches that cell, and a line or full card gets one celebratory line.
  Done when: `fm bingo` prints a 5×5 card drawn from the empty cells and marks squares from session activity, checked on a fixture ledger.

- **Wild: Pop quiz, guess the hole** — FEATURE — value 2 — effort S — risk low — category: delight — wild
  Why: before showing the left-out list, ask the user to name one thing they think was missed. Their guess either matches (a nice moment) or reveals a real gap, which is then filed as a cell.
  Done when: the guess is stored with a match or miss flag, and a miss files a candidate cell.

- **Settle a Mission's "what I left out" against the user's later asks** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: this is the outcome measure for the whole request. It's a hit rate: the share of the user's typed asks over the next 14 days that were already on a left-out list. Show it as a small, honest number on the next Mission.
  Done when: the next Mission's pack carries "left-out hit rate: X of Y typed asks", computed from the ledger.

- **Keep a kind tone for empty and failed cells** — FIX — value 2 — effort S — risk low — category: copy
  Why: assumption: "empty", "missing" and "FAIL" repeated across a grid read as scolding. A one-time copy pass gives each state a plain, neutral word ("not yet looked at", "looked, found nothing") and keeps the exact meaning.
  Done when: a lint fails on the old state words in rendered Mission pages, and the glossary lists the new ones.

Next question: which single sentence in a finished Mission do users re-read, and does the page lead with it?
Next question: does a user ever act on a left-out list, and what would make them?
