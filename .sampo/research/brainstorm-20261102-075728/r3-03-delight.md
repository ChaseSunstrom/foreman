# Brainstorm — lens: delight

- **Open with a first-light row** — FEATURE — value 4 — effort S — risk low — category: momentum
  Why: assumption: a vague goal feels abstract until something visible runs. The pack shows plans carried over days but no early payoff rule.
  Done when: a fresh plan's first row is capped at about 10 minutes of work and closes with a runnable or viewable artifact. A plan whose first row has no such artifact fails the plan lint.

- **Run a show-and-tell every third row** — FEATURE — value 4 — effort M — risk med — category: demo
  Why: assumption: users trust progress they have watched run more than a ticked row. Existing ideas (trailer, cast on a closed row) cover only the finish or single rows.
  Done when: after every third closed row Foreman executes the product's real entry point and prints a ≤5-line live transcript with its exit code. A row with no runnable entry is named as such instead of skipped.

- **Replay the last green demo on resume** — FEATURE — value 4 — effort S — risk low — category: resume
  Why: the goal "carries the plan over days, across crashes and compactions", and resume currently reconciles state files. The user's first question on return is "does it still work?"
  Done when: the first resume of each day re-runs the newest show-and-tell and prints "still standing" or the failing step before any new row starts.

- **Add one gift row, declinable** — FEATURE — value 3 — effort M — risk med — category: surprise
  Why: assumption: a best-in-class version has one touch the user didn't ask for (a good error message, a README GIF). The user's "surprise me" idea exists only as a per-row choice.
  Done when: each plan holds at most one row tagged `gift`, shown with a one-key decline. A declined gift never returns in a replan, and no gift row is counted toward "done".

- **Quote the user's own words at the moment they matter** — FEATURE — value 4 — effort M — risk low — category: callbacks
  Why: "The user's own words" are stored verbatim, and the user keeps restating intent (T-2554 and the steers). A callback shows that Foreman was listening.
  Done when: when a row closes whose evidence relates to a stored user phrase, the close line quotes the phrase with its date, for example `you said "must feel instant" (Tue): p95 41 ms`. Matches are exact substring or id matches, never paraphrase.

- **Scale the celebration to the row's size** — FEATURE — value 2 — effort S — risk low — category: ceremony
  Why: assumption: uniform "closed" lines become noise over a multi-day goal. Topping-out and first-light moments are already proposed, but nothing sets the ceremony by effort.
  Done when: S rows close with one quiet line, L rows with a 3-line summary, and the last must-row with a distinct marker. A test pins the three tiers.

- **Give stuck goals a hint ladder** — FEATURE — value 3 — effort M — risk low — category: stuck
  Why: the pack proposes "declare a stuck goal" and "name the stage behind a stalled goal", but only as a verdict. A puzzle-style ladder keeps the user in control.
  Done when: a stalled goal offers three tiers on request. Tier 1 is the evidence, tier 2 is a suggested next probe, tier 3 is a proposed approach switch. Each tier prints only on a one-word ask.

- **Show finish-date weather on the status line** — FEATURE — value 3 — effort S — risk low — category: status
  Why: an honest finish-date band is already proposed, but as a chart. A single glyph (clear, cloudy, storm) is the glanceable form.
  Done when: the status line shows one of three glyphs derived from the band's width and the scope-growth rate. `fm goal status` prints the numbers behind the glyph.

- **Keep a personal-bests card** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: multi-day goals give the user a reason to compare themselves with their own history. Row estimates versus actuals are already recorded, so the data exists.
  Done when: finish prints at most two true records, such as fewest user words per row or fastest resume. It prints nothing if no record was set.

- **Wild: print the finish on a receipt printer** — FEATURE — value 2 — effort M — risk low — category: tactile
  Why: wild; assumption: some users have a thermal printer or a pipeable `lp`. It would turn "You said / We built / Not proven" into a physical receipt.
  Done when: `fm goal receipt --print` pipes the finish card as ESC/POS or plain text to a configured command. Nothing is sent unless that setting is set.

- **Wild: keep a sealed reveal for the finish** — FEATURE — value 3 — effort M — risk med — category: surprise
  Why: wild; assumption: the finished version can include one polish item built last and shown only at finish, such as an `--about` easter egg or an animated splash. It must be listed in the final report so nothing is hidden.
  Done when: the finish card shows a "reveal" line pointing at the item, and a test checks that the item appears in the diff and the report.

- **Wild: hatch a hard-hat creature that can't be fed fake progress** — FEATURE — value 2 — effort M — risk low — category: mascot
  Why: wild; assumption: a small ASCII creature in `fm status` whose mood is computed only from verified rows, reopens and stalls. It lives in the same family as the existing hard-hat logo.
  Done when: closing a row without a passing probe leaves the mood unchanged, and the mood shows in `fm status` and on the Goal page.

Next question: Which of these moments does the user actually look at, and does reading the status line or the finish card ever change what they do next?
Next question: What does the user do when a goal goes quiet for a week: ignore it, shelve it, or forget it, and which delight would have brought them back?
