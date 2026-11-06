# Brainstorm — lens: delight

- **Ghost-text the predicted next ask, with a one-word go** — FEATURE — value 4 — effort M — risk med — category: prompt UX
  Why: the pack's Anticipation capability is about predicting and drafting the next request, yet every output is announced after the fact. Showing the single best guess faintly in the foreman-ui prompt, accepted with one key and ignored with none, is the moment people show others. Assumption: the foreman-ui mod can paint prompt ghost text.
  Done when: with a fixture history whose next ask is known, the prompt shows that text as ghost text and Tab files it as a task whose title matches.

- **Print "already built" while the user is still typing** — FEATURE — value 5 — effort M — risk low — category: capture
  Why: T-2546 and the dropped-as-built entries show the user repeatedly asked for things that already existed, and the answer arrives only after capture. A one-line "this is MASTER.md's X, T-nnnn" at the moment of the ask is the delight, and it saves a round trip.
  Done when: typing a request that restates a MASTER.md clause names that clause and its task id before submit, and a novel request prints nothing.

- **Close each task with a doorway line** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: the user's asks come in arcs (T-2540/2541, T-2532 through T-2536). One line at close, "you usually follow this with X", turns the end of a task into a handoff. It reads from the asked stream, not a new model. Assumption: sequence co-occurrence in the stream is strong enough to rank.
  Done when: closing a task whose kind has a recorded follow-up shows exactly one doorway line, and the line is absent below the evidence floor.

- **Make dismissal teach, and say so** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the pack's earlier ideas repeat "mute after two dismissals" but nothing makes it feel good. A dismissed nudge replies "noted, not today" and a "not today" shelf shows what Foreman is holding back and why. Restraint becomes visible, so silence is read as respect, not absence.
  Done when: dismissing the same signature twice mutes it, and the shelf lists it with its date and the one-key restore.

- **Add a "told you so" receipt** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: foresight that flags a problem early earns trust only if the user later sees it paid off. Assumption: a flagged signature can be matched to a later failure or a clean ship. When a flagged problem happens, or a flag turns out wrong, the next session prints one line with lead time in minutes.
  Done when: a flag followed by the matching failure produces one receipt with the lead time, and a flag with no matching event is logged as a miss, not shown as a win.

- **Expand "the usual"** — FEATURE — value 3 — effort M — risk med — category: prompt UX
  Why: the user's recurring phrasings ("feel free to push", "FEATURE!:" briefs, one-word replies) are a personal shorthand the pack's ideas already hint at. Typing a short token such as `again` or `the usual` expands to the last matching full ask, shown before it runs.
  Done when: a token bound by three prior identical asks expands in the preview to the full text and can be edited before submit.

- **Forgive the typo from personal history** — FEATURE — value 3 — effort S — risk low — category: CLI
  Why: T-2540 and the `--by harness` steer show the user mistyping flags and verbs in the same ways repeatedly, and Foreman refused. Suggesting the verb they meant from their own history, not a generic edit distance, feels like being known.
  Done when: a flag the user has mistyped before resolves to the corrected one in the suggestion line, using only that user's history.

- **Wild: "Guess my next ask" mini-game in the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI — wild
  Why: assumption: a playful card gives labelled data. The page shows three candidate next asks, the user taps the real one or "none", and a streak counter shows hit rate over time. It calibrates the forecaster without a survey and is the thing people screenshot.
  Done when: each tap writes a labelled row to the prediction ledger and the page shows the running hit@3 against the baseline.

- **Wild: Tip the hard hat when trouble is coming** — FEATURE — value 2 — effort S — risk low — category: status line — wild
  Why: the logo is a hard hat with a check mark. A tiny status-line glyph that tilts, once, when a problem flag is raised, and stays still otherwise, turns a warning into a character instead of text. Assumption: the status line allows a changing glyph.
  Done when: raising a flag changes the glyph for that flag's lifetime and clearing it restores the glyph, covered by a render test.

- **Wild: Publish "Foreman Wrapped" for the user's own month** — FEATURE — value 3 — effort M — risk low — category: web UI — wild
  Why: assumption: the ledger holds enough to summarize locally. A shareable-style page shows asks avoided, problems flagged early and the one guess it got most wrong, kept on the owner's machine and never sent anywhere. The honest "got wrong" line is the delight.
  Done when: the page renders from the local ledgers alone with no network call and includes at least one named miss.

- **Show restraint as a pride line** — FEATURE — value 3 — effort S — risk low — category: status line
  Why: the pack stresses an evidence floor and lean substance, but silence leaves no trace. A quiet line such as "held back 4 guesses, none cost you" at session end shows the forecaster declining to talk.
  Done when: a session where the evidence floor suppressed N forecasts ends with a line naming N, and a session with none prints nothing.

- **Give each forecast a one-line "because"** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: a guess with a visible reason ("you asked this after T-2541 twice before") is far more charming than a bare guess, and lets the user correct the reason. It also exposes weak evidence quickly. Assumption: each predictor can emit its supporting rows.
  Done when: every forecast displayed carries a because-line citing at least one ledger row, and a forecast without one is not displayed.

- **Wild: Open the session with the one thing the user is most likely to type first** — FEATURE — value 3 — effort M — risk med — category: session start — wild
  Why: the pack's recurring wild idea is "what I would have told you if you'd asked". Done as a single warm line at session start, with the hat tipping if the guess is a problem rather than a request, it is the first impression every day.
  Done when: session start prints exactly one such line from a fixture history, or none when below the evidence floor, and the hit or miss is scored by the first real prompt.

- **Draw the 58 cells as a flipbook of moments** — FEATURE — value 2 — effort M — risk low — category: web UI
  Why: the cells are the mission's own request, and a grid of prose is the opposite of delight. Rendering each filled cell as a one-sentence moment ("you type X, Foreman already knows Y") with its reach path makes the coverage readable and exposes templated cells at a glance. Assumption: cells carry a grounded file and a session path.
  Done when: the page shows one card per filled cell with its cited file and session path, and a cell lacking either is drawn as an empty card, not hidden.

Next question: Which of these moments does the user ever see without opening a page, and what is the quietest place each could land?
Next question: Which delights depend on the forecaster being right more often than a dumb baseline, and has that been measured before anything is shown?
