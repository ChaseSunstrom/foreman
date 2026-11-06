# Brainstorm — lens: delight

- **Ghost-text the next request** — FEATURE — value 4 — effort M — risk low — category: prediction UX
  Why: assumption: the pack has drafting and scoring of predicted requests, but no way to show a guess where the user types. A dim suggestion in the web UI prompt box and the `fm code` prompt, Tab to accept, `?` to show the three user phrases behind it.
  Done when: with a fixture history, the box shows the predicted line in dim text, Tab fills it, and `?` prints the source phrases.

- **Make dismissal a lesson** — FEATURE — value 4 — effort S — risk low — category: feedback loop
  Why: the pack tracks hit rates, but nothing in it says how a no is captured. Each "Heads up before you ask" line has one shape, and `fm nope "reason"` stores a labeled negative example the predictor must beat next time.
  Done when: a dismissed warning writes a negative row, and the same warning on a replayed history is suppressed.

- **Expand "the usual"** — FEATURE — value 4 — effort M — risk med — category: habit
  Why: assumption: the "asked" stream shows repeated request shapes (ship, tidy, status). `fm usual` learns the user's habitual sequence on a given weekday or after a given task kind, shows it as a plan, and runs it on one yes.
  Done when: after 3 recorded repeats of the same sequence, `fm usual` proposes it and a yes runs each step.

- **Forgive the typo from personal history** — FIX — value 3 — effort S — risk low — category: DX polish
  Why: T-2540 (bare `del` meaning rm) and the "no unknown flag" steer show the user types verbs and flags from habit. A mistyped verb gets "you meant `ship` (you've run it 14 times)", ranked by the user's own counts rather than edit distance alone.
  Done when: `fm shpi` suggests `ship` first because of its use count, and no suggestion appears with fewer than 3 uses.

- **Keep missed guesses on a "not today" shelf** — FEATURE — value 3 — effort S — risk low — category: waste to value
  Why: the pack lists 30+ deferred "Later from" items, and an unused speculative draft is currently expired and deleted. Instead it parks as a deferred item with a revisit date and one line saying why the guess missed.
  Done when: an expired draft appears in `fm next --deferred` with its miss reason and a revisit date.

- **Show restraint as a status-line pride line** — FEATURE — value 3 — effort S — risk low — category: status line
  Why: the standing rules favor precision floors and silence. A line like "held back 2 guesses today, precision floor 0.6" tells the user the quiet is deliberate and not a dead predictor. It shows only when guesses were withheld.
  Done when: withholding a guess below the floor increments the line, and with no withheld guesses the line is absent.

- **Close each task with a doorway line** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: assumption: the end of a task is the moment the user decides what's next. The receipt ends with "Next I'd guess: <draft title> — say `go`" and the one-word reply starts the lane, using the existing one-word-reply binding idea.
  Done when: `fm task finish` prints a guess line, and `go` as the next prompt starts a lane with that draft.

- **Add a "told you so" receipt for problems flagged early** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: assumption: a flagged problem that later happens is the best proof anticipation works, and nothing shows it. When a flagged risk (red ship, slow hook, steer collision) materializes, the next summary quotes the earlier flag with its date.
  Done when: a seeded flag followed by the matching failure produces a "flagged <date>" line in the next fm status.

- **Wild: Hold a "guess my next ask" mini-game in the web UI** — FEATURE — value 2 — effort M — risk low — category: web UI
  Why: wild. The user types what they will ask next while Foreman's hidden guess is revealed afterwards. It scores both sides and quietly calibrates the predictor from user-labeled outcomes, as a ten-second idle toy.
  Done when: submitting a guess reveals Foreman's guess and a match score, and the pair lands in the prediction ledger.

- **Wild: Publish a shareable "Foreman Wrapped" page** — FEATURE — value 3 — effort M — risk med — category: shareable recap
  Why: wild. A local page with the user's best call, funniest miss, longest hit streak and most-saved hour, built only from local ledgers (no upload) as one exportable HTML file people can show others.
  Done when: `fm wrapped` writes a self-contained HTML file from a fixture ledger and makes no network call.

- **Wild: Tip the hard hat when trouble is coming** — FEATURE — value 2 — effort S — risk low — category: status line
  Why: wild. The logo glyph on the status line tilts in 3 states (level, tipped for a pending forecast, off for dead tick) so the user can read anticipation state at a glance without any text. The brand mark is already a hard hat.
  Done when: the status line glyph differs across the three states in a render test, and the states map to forecast, heartbeat and idle.

- **Offer a one-line "because" for any nudge** — FEATURE — value 3 — effort S — risk low — category: explainability
  Why: assumption: unexplained nudges get ignored. Every anticipation line carries a short `fm why` id. The answer names the history rows behind it, such as "you reverted this 2 times in October".
  Done when: every nudge prints an id, and `fm why <id>` lists at least one cited history row.

- **Fill the 58 cells as a flipbook of "moments"** — CLEAN — value 3 — effort M — risk low — category: coverage grid
  Why: assumption: cells that read as grid entries get templated. Writing each as a one-sentence before/after moment of one real request from the asked stream (with its task id) resists the templating the standing rule forbids, and makes the page readable by a visitor.
  Done when: every new cell cites a task id from the asked stream, and the templating lint finds no shared 20-line shingles.

Next question: Which anticipation moments does the user actually look at (status line, close-out receipt, web UI), so delight lands where their eyes already are?
Next question: When a guess is wrong, what does the user want done with it: silence, a shelf, or a correction they can type in one word?
