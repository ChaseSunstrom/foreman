# Brainstorm — lens: delight

- **Ghost-text the next request** — FEATURE — value 4 — effort M — risk med — category: prompt UX
  Why: Anticipation's point is predicting the next ask; the pack lists no surface where a prediction is simply *seen*. assumption: foreman-ui's prompt area can show dim completion text.
  Done when: with a fixture history containing a repeated ask pair, the prompt shows the predicted second ask as dim text, Tab accepts it, and any keystroke dismisses it with no model call.

- **Show "already built" before the ask is finished** — FEATURE — value 5 — effort S — risk low — category: capture
  Why: T-2546 shipped the at-birth check, and dropped items like the guard-only exam arm were "already built". The delight is hearing it *while typing*, not after filing.
  Done when: `fm capture --preview "text"` prints the matching MASTER.md clause and task id in under 300 ms, and fm next shows it for a draft.

- **Add a "told you so" receipt** — FEATURE — value 3 — effort S — risk low — category: foresight
  Why: assumption: flagged-early problems vanish once avoided, so the user never sees the save. The close receipt could say "flagged Tue, hit Thu, avoided".
  Done when: a flag followed by a matching avoided failure produces one line in the task-finish receipt, and none when no flag fired.

- **Make dismissal teach, with a "not today" shelf** — FEATURE — value 4 — effort S — risk low — category: foresight
  Why: the steers show the user dislikes repeats (they asked for a re-offer fix, T-2507). A dismissed guess should sleep rather than return.
  Done when: dismissing a forecast twice mutes its signature, and `fm next` lists the muted ones on one line with a restore key.

- **Print one annoyance forecast at session start** — FEATURE — value 3 — effort M — risk med — category: session start
  Why: the pack shows recurring pain (ETXTBSY flake, tmpfs children dir, brief-guard false positives). assumption: the event log can rank by recurrence per machine.
  Done when: a session on a fixture machine with a recorded flaky-test history prints one line naming it and the rerun command, capped at one line.

- **Give each forecast a one-line "because"** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user's steers insist on traceable, grounded claims; a forecast without a reason feels like a guess.
  Done when: every forecast output includes a reason citing an event id or steer date, and a forecast without one is dropped by a test.

- **Close each task with a doorway line** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: assumption: the next ask often follows the closed task's co-changed files. A single "next you may want: X" line costs nothing.
  Done when: finishing a task whose files have a co-change history prints at most one doorway line, and none when history is thin.

- **Add a web UI Anticipation card on Today** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: a surface for anticipation is among the 58 empty cells; the pack records a Today view already exists. Show forecasts with accept, dismiss and the "because".
  Done when: the page renders a forecast with an empty, a loading and an error state, and it passes a keyboard-only walkthrough.

- **Show restraint as a pride line** — FEATURE — value 2 — effort S — risk low — category: status line
  Why: the user pushed back on noise (lean ratchet, silence ratio). "Stayed quiet 14 turns" turns restraint into a visible feature.
  Done when: the status line shows a silence count that matches the injected-bytes ledger for the session.

- **Wild: Hold a "guess my next ask" mini-game** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild. The user types their guess of what Foreman will predict, and the game scores the predictor's hit@3 against it, playfully producing labelled backtest data.
  Done when: the page records 10 rounds and shows a hit rate that matches `fm outcomes` for the same set.

- **Wild: Publish a "Foreman Wrapped" page** — FEATURE — value 3 — effort M — risk low — category: site
  Why: wild. Genesis already publishes site data; a yearly local-only recap (asks predicted, problems caught, steers kept) would be something people show others.
  Done when: `fm wrapped` generates a static HTML file from local ledgers only, with nothing sent anywhere.

- **Wild: Tip the hard hat when trouble is coming** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The logo is a hard hat with a check mark. A tilted hat on the status line, with no text, signals a flagged risk, and a glance replaces a paragraph.
  Done when: the status line glyph changes only when an unmuted forecast exists and returns when it is dismissed.

- **Wild: Write the "sorry, already built" note before it's typed** — FEATURE — value 4 — effort M — risk med — category: capture
  Why: wild, and supported by the dropped ledger where several items were already built. A tool-less child drafts the likely ask, the check runs against MASTER.md, and the user gets the answer in advance.
  Done when: for 5 historical dropped-as-built asks, the backtest flags at least 3 before their capture date, with no false flags on 20 kept asks.

Next question: Which forecast surfaces does the user actually look at (status line, `fm next`, web UI), measured by read receipts, so delight work goes where attention is?
Next question: What would make a correct forecast feel creepy rather than helpful, and does any steer or past dismissal show where that line is?
