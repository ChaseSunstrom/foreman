# Brainstorm — lens: deepen: delight

- **Fold the "things I'd have told you" cards into one forecast object** — FEATURE — value 5 — effort M — risk med — category: anticipation
  Why: the delight list repeats one idea at session start, resume, close and pre-answer. Assumption: `fmforesight` can emit a single forecast record (id, claim, evidence task id, surface) that every surface renders. This covers many of the 58 cells with one probe.
  Done when: one forecast record renders on session start, resume and task close, and a test fails if any surface prints a warning with no record id.

- **Score every forecast as hit, miss or ignored** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: `fm outcomes` already stores bets with Brier scores per harness. Assumption: forecasts can be settled the same way, by checking whether the predicted thing happened within N days.
  Done when: `fm outcomes --judgment` lists forecast hit-rate beside bet Brier, and a seeded forecast that came true shows as a hit.

- **Ground each warning in its one past incident** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the Mission 3-5 lesson says to ground ideas in a ledger or decision entry. The same rule makes a warning believable: "last time (T-2532) this silently turned hooks off."
  Done when: a forecast line cites a real task id from the ledger, and one that can't cite one is not printed.

- **Learn the annoyance threshold from behavior, not a swipe deck** — FEATURE — value 4 — effort M — risk med — category: personalization
  Why: assumption: the user's acts and dismissals (acting on a warning, `fm task drop`, ignoring it) already signal what they value, so a swipe deck is unnecessary. The cap is one forecast per session, and the bar rises after ignores.
  Done when: replaying 20 recorded sessions with dismissals raises the print threshold, and the same replay with acts lowers it.

- **Offer a ghost next task in `fm next`** — FEATURE — value 5 — effort L — risk med — category: drafting
  Why: the capability text says "predicts the next request and drafts it on spec in a lane." The ghost sits dimmed in the queue, one key adopts it and it is discarded silently otherwise. The backtest rule applies: ship only if predictions beat a base rate on real history.
  Done when: a backtest on the last 100 captured requests reports precision, and the ghost only appears when it clears a stated bar.

- **Show a Foresight page in the web UI with predicted versus actual** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: web UI is the only surface in the mission. The page is a timeline of forecasts with hit and miss marks. Its empty state says what it is still learning, and it shows the same data as the terminal line, so a user who never opens it loses nothing.
  Done when: a screenshot shows the empty, loading and populated states, and the page reads the same forecast records the session hook prints.

- **Fix flag typos from the user's own history** — FIX — value 3 — effort S — risk low — category: CLI
  Why: steers show `--by harness` versus `--by-harness`, and `fm next --last` was wrongly called an unknown flag. An unknown flag could suggest the nearest accepted one, or the one the user typed last time.
  Done when: `fm outcomes --judgment --by-harness` prints "did you mean `--by harness`" and exits nonzero.

- **Draft commit and PR text in the user's recorded style** — FEATURE — value 3 — effort M — risk med — category: drafting
  Why: recent commits share a "T-NNNN: verb phrase naming the observable result" shape. Backtest first: a draft must match the real message on shape for most of 50 past commits.
  Done when: the backtest reports a match rate over a stated bar, and `fm ship` pre-fills only above it.

- **Wild: Tip the hard hat when trouble is coming** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: wild. The logo is a hard hat with a check mark. On the web UI header and the foreman-ui pane it tips slightly when a forecast is pending, with a text equivalent for accessibility and a reduced-motion rule.
  Done when: the header shows a tipped state when a forecast is open, and a static label appears under reduced motion.

- **Wild: Write a monthly letter from last month's me** — FEATURE — value 3 — effort M — risk med — category: reflection
  Why: wild. It is compiled locally from dated steers, dropped items and settled forecasts: what the user kept asking for, what they dropped, what was predicted. Assumption: the content stays local and is never published to `site/genesis`.
  Done when: `fm letter` writes a local file citing at least 5 dated steers, and nothing under `site/` changes.

- **Wild: Read the machine's weather report** — FEATURE — value 3 — effort M — risk low — category: machines
  Why: wild. It combines usage-burn pace, the last trigger and result of the night timers (T-2542), and a hook p95 trend into one line, such as "usage limit likely Thursday; night timer healthy." The capability says to model "my machines."
  Done when: the session-start line names one of pace, timer health or disk, each from a real source, and says nothing when all are normal.

- **Pre-answer the user's usual follow-up questions in the close receipt** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: assumption: the user's follow-ups after a close repeat ("did it push?", "what did it cost?", "what's left?"). Mine them from recorded sessions and put the top three answers in the receipt.
  Done when: a close receipt answers the top three mined questions, and a question that never recurs is not added.

- **Wild: Reveal sealed predictions at each generation end** — FEATURE — value 4 — effort M — risk low — category: Genesis
  Why: wild. The standing rule seals a prediction of the user's next three steers before each Seed. The reveal shows predicted against actual steers with hit marks, in the genesis page and the report.
  Done when: the generation report prints the sealed prediction beside the steers that followed and marks each hit or miss.

Next question: which forecast surface does the user act on rather than merely read, and is the hit rate on acted-on forecasts better than on ignored ones?
Next question: can the sweep check that a cell's cited forecast path still fires after later generations change it, rather than only that the file exists?
