# Brainstorm — lens: reliability

- **Make the forecaster fail loudly, never empty** — FIX — value 5 — effort S — risk low — category: anticipation reliability
  Why: T-2532 showed silent hook-off failures; a forecaster that returns `[]` for "crashed", "abstained" and "nothing to say" is the same class (the pack's "Make the forecaster say abstained or failed" idea has no test behind it).
  Done when: a test that makes `fmforesight` raise, time out, and have no history yields three distinct recorded states (`failed`, `timeout`, `abstained`), and `fm doctor` names each.

- **Strip Foreman-authored and mistaken captures from the user model** — FIX — value 5 — effort S — risk low — category: data integrity
  Why: the dropped ledger shows two captures made by mistake ("The first brief", "The second brief", fed to fm intake while debugging T-2547) and T-2546 was nearly matched against test text; any predictor trained on "asked" learns them.
  Done when: the user-model reader excludes dropped-as-mistaken items and test-run captures, and a fixture with those two lines yields zero asked records for them.

- **Backtest-gate every predictor walk-forward before it may draft a lane** — FEATURE — value 5 — effort M — risk low — category: prediction gating
  Why: lesson from T-2546 (word-overlap matcher "met no bar"); today a heuristic can ship on intuition.
  Done when: `fm foresight backtest` replays the asked stream chronologically, prints hit@3 against a last-request-repeated baseline, and a predictor below baseline refuses to draft.

- **Resolve every prediction to hit, miss or expired** — FEATURE — value 4 — effort M — risk low — category: prediction ledger
  Why: assumption: predictions are not currently stored with an outcome; without resolution nothing can notice a predictor going nonsense (an open question: "who would notice if it were nonsense?").
  Done when: a prediction row older than its TTL is marked `expired` by the night tick, and `fm outcomes` shows per-predictor hit/miss/expired counts.

- **Stamp each speculative draft with tree hash and steer set; refuse stale adoption** — FIX — value 4 — effort S — risk low — category: draft safety
  Why: T-2334/T-2507 show state moving under cached items; a draft built before a steer or commit landed can be adopted wrongly.
  Done when: changing HEAD or adding a steer after a draft is written makes adoption print "stale draft" and re-ground, covered by a test.

- **Make cell citations re-run, not just resolve** — FEATURE — value 4 — effort M — risk med — category: coverage integrity
  Why: open question "does the sweep verify a filled cell's cited file still behaves as claimed, or only that it exists?"; 58 new cells citing files will rot as later generations edit them.
  Done when: each cell carries a probe command, `fm genesis sweep` runs it, and a deliberately broken cited function turns that cell red.

- **Add a shuffled-history control arm to every predictor** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: standing rule that signals Foreman didn't author decide; a predictor that scores equally on shuffled history is learning nothing.
  Done when: the backtest prints real vs shuffled hit rate and fails a predictor whose gap is under a stated bound.

- **Fail the sweep on forecast outputs no session path reads** — CLEAN — value 4 — effort S — risk low — category: reach
  Why: standing rule "every capability must be called by a real session path"; the questions list "which outputs does no session path read".
  Done when: each `fmforesight` output type is registered with a reader (fm next, session start, drive), and an unregistered one makes `fm genesis check` red.

- **Cap flags per session and mute a signature after two dismissals** — FEATURE — value 3 — effort S — risk low — category: noise control
  Why: assumption: problem flags repeated after dismissal would erode trust and the injection budget (the lean ratchet).
  Done when: a test dismisses one signature twice and the third occurrence emits nothing, with a count in `fm doctor`.

- **Check all five harness transcript shapes yield the same asked records** — FIX — value 4 — effort M — risk med — category: harness parity
  Why: open question about codex/gemini/opencode/fm code plans; the user model is only as good as its input and T-0335/T-0336 are blocked on live verification.
  Done when: one recorded fixture per harness parses to an identical normalised record set, and a missing field fails the test.

- **Wild: Plant a fake habit and require the forecaster not to over-learn it** — FEATURE — value 3 — effort M — risk low — category: adversarial testing
  Why: wild; a single repeated test-run ask should not become a prediction.
  Done when: a fixture with one planted repeated request gets no prediction until it recurs past a stated threshold.

- **Wild: Time-machine replay of the forecaster at each past commit date** — FEATURE — value 4 — effort L — risk med — category: backtest
  Why: wild; uses the real git history as ground truth for "next ask" without waiting for new data.
  Done when: `fm foresight replay --since DATE` prints per-date hit@3 using only data available on that date.

- **Wild: Weekly canary: a stub user sends a scripted request and the chain is timed end to end** — FEATURE — value 3 — effort M — risk low — category: liveness
  Why: wild; the night tick, capture, draft and `fm next` surface are only tested in pieces.
  Done when: the night tick injects a canary ask, asserts it appears in `fm next` within a bound, and `fm doctor` shows the last canary pass.

Next question: Which of the forecaster's inputs (transcripts, shell history, git, ledgers) can be rebuilt from scratch, and does a rebuilt model match the live one?
Next question: Does any predictor's output change what the user actually does, or only what Foreman shows — and how would we tell the difference?
