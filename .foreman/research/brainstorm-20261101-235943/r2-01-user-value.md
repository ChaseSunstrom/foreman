# Brainstorm — lens: user value

- **Show "already built" before the user finishes asking** — FEATURE — value 5 — effort M — risk low — category: anticipation
  Why: the "dropped" list is full of asks answered by existing code (guard-only arm, T-2534; docs-unknown test). T-2546 only checks at capture time.
  Done when: typing a request into `fm capture` or the prompt hook prints the matching MASTER.md clause and task id within 1s, and a fixture ask for the guard-only arm names `fmexam.py:2893`.

- **Draft the ask the user is about to make from their own steer chain** — FEATURE — value 5 — effort L — risk med — category: forecasting
  Why: the asked stream is serial (T-2532 → 2533 → 2535 → 2536 each followed the last). Backtest is a stated lesson from T-2546.
  Done when: a walk-forward backtest over the asked stream reports a hit rate against a "repeat last topic" baseline, and drafting is enabled only if it beats it.

- **Bind each of the 58 empty cells to a past incident or mark it unreached** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: the standing rule says a cell counts only if grounded in a file or real gap. Questions left ask which cells are one capability counted repeatedly.
  Done when: every Anticipation cell cites a file/symbol or a decisions.md/ledger entry, and `fm genesis check` rejects any cell sharing 20 lines of shingle overlap with another.

- **Strip captured-by-mistake input from the user model** — FIX — value 4 — effort S — risk low — category: data quality
  Why: "The first brief" and "The second brief" were fed by a debugging test (T-2547) and landed in asked/dropped. A forecaster trained on them learns noise.
  Done when: fixture history with those two lines yields identical predictions with and without them, and test-run captures are tagged and excluded.

- **Warn before the usage wall hits the queue** — FEATURE — value 4 — effort M — risk low — category: foresight
  Why: steers say usage limits are waited out, not skipped; the user can't see ahead of time which work will stall.
  Done when: session start prints "at current burn the 5h window ends before item X" and a replayed burn log produces that line.

- **Put one ranked "heads-up" slot in `fm next`** — FEATURE — value 4 — effort S — risk low — category: reach
  Why: question left: which outputs does no session path read? A forecast nobody sees has no user value; steers also demand a real session path.
  Done when: `fm next` shows at most one foresight line, and an exam scenario fails if fmforesight output isn't read by it.

- **Dismissal teaches: mute a signature after two dismissals** — FEATURE — value 3 — effort S — risk low — category: restraint
  Why: assumption: flags that repeat get ignored; the dropped ledger already records user rejections of Foreman-filed classes.
  Done when: dismissing the same flag signature twice suppresses it for 30 days and `fm doctor` lists muted signatures.

- **Predict the correction before delivery** — FEATURE — value 4 — effort M — risk med — category: pre-flight
  Why: many asks are corrections of just-shipped work (T-2529 "as its docstring promised", T-2540 bare words). Corrections have recurring shapes.
  Done when: at finish, a check lists the top matching past correction shapes against the diff, and it catches a planted example from history.

- **Forecast machine exhaustion with an ETA** — FEATURE — value 3 — effort M — risk low — category: machine model
  Why: the environment has a tmpfs children dir under /run/user and the ETXTBSY flake (T-2543) shows machine state breaking runs.
  Done when: before spawning N lanes, fm reports free tmpfs/disk runway and refuses with an ETA if it won't fit.

- **Wild: ghost-user lane that attempts the predicted ask blind** — FEATURE — value 3 — effort L — risk med — category: speculation
  Why: wild. Spec-only draft with an expiry, never merged; first question it asks reveals the ambiguity before the user types.
  Done when: a draft lane yields a spec file and a list of its questions, and is auto-deleted unmerged after 48h.

- **Wild: a "what I would have told you" card on resume** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: wild. The dropped-as-built list is the user's own evidence that Foreman knew things it didn't say.
  Done when: session resume prints up to three one-line items from dropped-as-built that touch recently edited files.

- **Wild: a cell is a bet with a Brier score** — FEATURE — value 3 — effort M — risk med — category: calibration
  Why: wild. Bets already settle via `fm night`; applying the same to coverage cells makes empties measurable instead of prose.
  Done when: each filled cell records a prediction and `fm outcomes` scores it once the next matching event occurs.

- **Show the lead time of each anticipation hit** — FEATURE — value 3 — effort S — risk low — category: proof of value
  Why: a hit is worth little if it arrives after the user typed the ask; no metric currently shows minutes of lead.
  Done when: `fm doctor` prints median lead time for hits, and a hit with negative lead is counted as a miss.

Next question: Which Anticipation cells would a stub user built only from the steers fail, and are those the cells that matter?
Next question: Does any forecaster output reach the user without them opening a page, and what is the evidence they read it?
