# Brainstorm — lens: approaches

- **Build a leave-one-out backtest for any predictor** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the pack's anticipation ideas (n-grams, follow-up tables, recency) all lack a shared scorer. Without one, Mission 7 can't choose between them (assumption: no such harness exists yet).
  Done when: `fm anticipate backtest --predictor recency` replays the ask ledger, hides each ask, and prints hit@1/3/5 plus the count of asks with no prior history.

- **Do less: print one "you usually ask X next" line at finish** — FEATURE — value 4 — effort S — risk low — category: finish card
  Why: the asks include recurring ones ("Ship this session's landed work (fm ship)"). A plain count of what followed the same task kind needs no model and no drafting.
  Done when: closing a task whose kind has at least 3 past follow-ups shows one line naming the most common one, with its count (e.g. 4 of 6).

- **Detect periodic asks and schedule them** — FEATURE — value 4 — effort M — risk low — category: cadence
  Why: ship-at-session-end and "Genesis gen-N Mission K" asks recur at regular intervals in the user's words. A timestamp-gap detector over the ask ledger would find them.
  Done when: given a fixture ledger with an ask every ~7 days, `fm anticipate cadence` lists it with the next expected date and tolerance.

- **Predict from coverage-grid neighbours** — FEATURE — value 4 — effort M — risk low — category: grid
  Why: the user already works through `coverage.md` cells (surface × stage), and gen-3 missions walk capabilities in order (#12, #2, #3). The adjacent unfilled cell is a grounded guess with no history needed.
  Done when: finishing a task tagged with cell (surface, stage) prints the nearest empty cells, and a backtest on past missions shows hit@3 above the recency baseline.

- **Extract a promise ledger from the user's deferral words** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: the dropped items carry "noted remainder" and "later" phrasing that later becomes a new ask. Capturing it verbatim turns it into a due-for-resurfacing list.
  Done when: a user message containing "later" or "also next" files a promise row quoting the sentence, and `fm next` shows it once the related task closes.

- **Prefetch read-only verb output from verb-transition counts** — PERFORMANCE — value 3 — effort M — risk low — category: performance
  Why: the thin area is performance, and `fm usage` already has per-verb history. After `fm next`, the user usually runs one of a few verbs. Their output can be cached for the current ledger epoch.
  Done when: the predicted verb returns from cache in under 50 ms on a fixture, and the cache is dropped on any ledger append.

- **Keep the predictor local-only and show what it read** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the thin area is privacy. The user's asks contain their own words, so a predictor that sends nothing off the machine, plus a listing of the files it read, means no setting to explain.
  Done when: `fm anticipate --explain` lists every file read and a test with the network blocked passes.

- **Pool follow-up tables across the user's registered repos** — FEATURE — value 3 — effort M — risk med — category: transfer
  Why: assumption: the user has several repos registered. A new repo has no history, so a cross-repo prior removes the cold start. The risk is leaking one project's phrases into another.
  Done when: in a repo with fewer than 5 closed tasks, the predictor uses the pooled table, labels its source, and never prints text from another repo.

- **Retire the predictor when it loses to the baseline** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: standing rule "Lean substance": growth without measured gain waits or is subtracted. A predictor that scores at or below recency after N asks should switch itself off.
  Done when: a fixture where recency wins 20 times to 5 turns the predictor off and writes a decision record with the counts.

- **Wild: Let the user bet against the prediction** — FEATURE — value 3 — effort M — risk low — category: calibration (wild)
  Why: a one-keypress "I'll ask something else" at the finish card yields a labelled miss and a stated alternative, which is far richer data than silent non-use.
  Done when: pressing the key stores the user's actual next ask against the prediction, and the next backtest includes it.

- **Wild: Predict only the gaps in a replayed week** — FEATURE — value 3 — effort L — risk med — category: evaluation (wild)
  Why: replay the user's last 30 days of asks and mask every ask that a simple rule already predicts. The residual is the true blind-spot set, and it is the signal that earlier brainstorms missed.
  Done when: the report lists the masked asks and the share of the month no predictor reached.

- **Wild: Draft the follow-up as a task title with a one-word veto** — FEATURE — value 2 — effort M — risk med — category: finish card (wild)
  Why: the cheapest useful anticipation is a pre-filed deferred task the user kills with one word. A veto rate under some threshold promotes it, over it silences it.
  Done when: a predicted follow-up appears as a deferred task tagged "predicted", vetoes are counted, and more than 70% vetoes in 10 trials stop that task kind being drafted.

Next question: what share of the user's asks in the last 60 days had any prior ask within the same task kind that a table could have used, versus first-of-kind asks?
Next question: does the user read the finish card at all, so that a line added there has any chance of being used?
