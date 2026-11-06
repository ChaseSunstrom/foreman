# Brainstorm — lens: deepen: delight

- **Open every Mission page on the cell the user opens first** — FEATURE — value 4 — effort S — risk low — category: grid
  Why: the pack asks "which cell do they open first, and does the grid order match it?"; assumption: open-history can be read from the web UI's page views.
  Done when: a Mission page opens scrolled to its most-opened cell, and a test shows that order changes after three opens of another cell.

- **Turn the left-out list into a keepable slip** — FEATURE — value 4 — effort M — risk low — category: receipts
  Why: the request is "says what it left out"; the delight list has the tear-off slip, the postcard and the torn-edge idea scattered. Merge them into one object: each Mission close prints a slip with left-out items, a reason and the date each expires. `fm slip keep` saves it to a drawer, and `fm slip tear` marks it dismissed, recorded so it counts toward dissent scoring.
  Done when: closing a Mission writes a slip file listing every left-out item with its reason, and `fm slip tear ID` changes its state in `fm outcomes`.

- **Score a torn slip against what happened next** — FEATURE — value 5 — effort M — risk med — category: dissent
  Why: carried gap "dissents scored against outcomes". A torn slip is a dissent. If the dismissed item resurfaces as a failure or a typed ask within 14 days, the slip is marked "should have kept". If it never does, it is marked "rightly torn".
  Done when: `fm outcomes --slips` prints counts of rightly torn and should-have-kept slips for a fixture ledger.

- **Show a one-glyph Exam state in the status line** — FEATURE — value 3 — effort S — risk low — category: status
  Why: merges the "Exam forecast" and "hard-hat lamp" ideas into one state: lit (measure and live reading both fresh), dim (reading stale), flicker (reading unavailable or gameable), dark (no measure). Assumption: the status line can show one glyph.
  Done when: a fixture brief with no live-state reading renders the dark glyph, and one with a stale reading renders the dim glyph.

- **Say "unmeasured" in plain words when a snapshot can't be taken** — FIX — value 4 — effort S — risk low — category: honesty
  Why: the open question "service down, offline: say unmeasured or block?". Pick carry-forward with a loud label, and decide it with `fm decide --kind costly`, per the standing rule. The lamp glyph flickers, and the slip lists the unmeasured reading as a left-out item.
  Done when: with the snapshot service stubbed off, the Exam prints "unmeasured, carried from <date>" and the Mission still closes.

- **Make a Mission's grid fingerprint comparable between generations** — FEATURE — value 3 — effort M — risk low — category: grid
  Why: the "fingerprint" wild idea turned practical. Render each Mission's 13×surface grid as a small fixed-size glyph block (filled, empty, n/a), and show gen N beside gen N-1 so empty cells shrinking is visible at a glance.
  Done when: `fm genesis grid --compare 3 4` prints two aligned blocks, and a test confirms a newly filled cell flips one glyph.

- **Call the coverage "visited" or "unvisited" separately from "passes"** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the open question "exam passes but no typed ask landed in the cell all generation: covered or just unvisited?". The night-sky map idea fits here: dark means never asked, dim means asked but not exam-checked, lit means both.
  Done when: the coverage report prints three states per cell, with a fixture cell passing but never asked showing as "unvisited".

- **Open each generation with the user's own sentence** — FEATURE — value 3 — effort S — risk low — category: seed
  Why: merges "letter from the last user message" with "title each generation by the most repeated phrase". The seed starts with the user's most repeated recent phrase quoted verbatim, which keeps the intent the standing rules protect. Assumption: repeated phrases can be counted from the intake text.
  Done when: a seed draft starts with a quoted phrase that appears at least 3 times in a fixture steer log.

- **Mark a Mission's first-ever cell with a chime and a one-line note** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: the "chime and badge" idea, narrowed: only the first time a cell is filled with a measured outcome, never on repeats, so it stays rare.
  Done when: the first filled cell in a fixture grid emits a bell and writes a "first" note, and a second fill in the same cell does not.

- **Wild: Mail a dated postcard from the Mission that was left out** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: wild. On the expiry date of a left-out item, a one-paragraph postcard shows up in `fm next`: "You tore me off on Nov 2; here is what happened since." It is built from real ledger events, and it combines the regret postcard with the dated letter.
  Done when: a fixture slip past its expiry date produces a postcard in `fm next` that cites at least one ledger event.

- **Wild: Run a one-minute stranger's-morning test on every Mission page** — FEATURE — value 3 — effort M — risk med — category: wild
  Why: wild. A tool-less child reads only the Mission page and says in three sentences what was built, what was left out, and what to do first. If it names a wrong left-out item, the page fails a check.
  Done when: `fm genesis check` fails a fixture page whose summary omits a listed left-out item.

- **Wild: Play a Mission back as a seven-second changelog frame** — FEATURE — value 2 — effort M — risk low — category: wild
  Why: wild. The site's `demo/live.svg` approach already animates real sessions. Replay the Mission's grid filling cell by cell, with the slip printed last, on the Genesis site page.
  Done when: `site/genesis` serves an animated frame whose cell fill order matches the Mission's close-times in a fixture.

- **Wild: Show the tower's weather at session start** — FEATURE — value 2 — effort S — risk low — category: wild
  Why: wild. One line such as "clear: 0 empty cells, 2 stale readings" uses the lamp states and the unvisited count, and sets the tone before the first prompt.
  Done when: the session-start output includes the weather line, and it changes when a fixture reading goes stale.

Next question: Which delight touches get seen more than once, and does the ledger record that anyone looked, or do we only assume it?
Next question: When a user tears a slip, is the cause "I disagree" or "I'm done for the day", and can one extra word capture it without adding friction?
