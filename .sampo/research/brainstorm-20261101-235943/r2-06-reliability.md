# Brainstorm — lens: reliability

- **Re-run every filled cell's probe each sweep and go red on drift** — FIX — value 5 — effort M — risk low — category: coverage rot
  Why: the pack's open question asks whether the sweep verifies a cited file still behaves as claimed, or only that it exists. T-2547 checks grounding lines exist, not that they stay true across generations.
  Done when: editing a cited function in a scratch copy turns its cell red in `fm genesis sweep`, with the cell id named.

- **Make the forecaster say "abstained" or "failed", never an empty list** — FIX — value 5 — effort S — risk low — category: silent failure
  Why: assumption: `fmforesight` returns nothing both when it has no signal and when it crashed or its source was unreadable, so the user cannot tell quiet from dead. The pack records the same class of bug in T-2532 (hook events silently off) and T-2542 (timers assumed alive).
  Done when: a test that corrupts the forecaster's input ledger yields an output whose status is `failed` with a reason, distinct from the `abstained` output on an empty history.

- **Backtest every predictor walk-forward before it may draft a lane** — FEATURE — value 5 — effort M — risk med — category: prediction gate
  Why: the Missions 3-5 lesson says T-2546's word-overlap matcher "met no bar". The "asked" stream gives labelled history. Without a gate, a predictor that loses to "repeat the last request" would draft lanes anyway.
  Done when: `fm foresight backtest` prints hit rate per predictor against the last-request baseline, and a predictor under the baseline cannot start a draft lane (tested).

- **Strip mistaken and test-fed captures out of the user model** — FIX — value 4 — effort S — risk low — category: data hygiene
  Why: "The first brief" and "The second brief" were captured by mistake from a sample line fed to `fm intake` while debugging T-2547's test, and both appear in the asked stream. The model of me would learn from them.
  Done when: a test feeds `fm intake` under a test marker and the item is absent from the model's input, and the two dropped items are excluded retroactively.

- **Stamp each speculative draft with tree hash and steer set; refuse stale adoption** — FIX — value 4 — effort M — risk low — category: stale drafts
  Why: a draft written overnight may rest on a tree or a standing rule that has since changed. The steers list moved several times on 2026-11-01 alone.
  Done when: adopting a draft after a commit or a new steer prints "stale: <which>" and redrafts instead of merging.

- **Cap problem flags per session and mute a signature after two dismissals** — FEATURE — value 4 — effort S — risk low — category: alert fatigue
  Why: assumption: foresight flags are announcements. The user already dropped self-filed items "measured" as not worth it; a flag that repeats teaches them to ignore the real one.
  Done when: a third identical flag in a session, or any flag after two dismissals of its signature, is suppressed, and `fm doctor` lists the muted signatures.

- **Rebuild the user model from its append-only sources and prove it matches** — CLEAN — value 4 — effort M — risk low — category: model integrity
  Why: if the model is cached state, a partial write or a kill leaves a quietly wrong profile. The pack shows repeated baton/ledger/repo disagreement after kills.
  Done when: deleting the cache and rebuilding yields a byte-identical model on a fixture history, checked in `fm doctor`.

- **Check that all four non-Claude harness transcripts yield the same asked records** — FIX — value 4 — effort M — risk med — category: harness parity
  Why: the pack's open question on codex, gemini, opencode and `fm code` stage data. T-0336 (live-verify on real codex, gemini, opencode) is still blocked, so parity is unproven.
  Done when: one fixture conversation rendered in each harness's format produces identical request/correction records, and a mismatch fails the test.

- **Give each of the 58 cells a planted-history probe with a known next request** — FEATURE — value 4 — effort L — risk med — category: cell probes
  Why: the standing rule says a cell counts only if grounded in a file or a real gap. A synthetic history with a known answer shows whether the cell's capability fires at all.
  Done when: each filled cell names a fixture and an expected output, and `fm genesis sweep` runs all of them hermetically in under a set budget.

- **Wild: run a shuffled-history control arm beside the real forecaster** — FEATURE — value 3 — effort M — risk low — category: control arm
  Why: wild; assumption: if the shuffled history predicts as well as the real one, the "model of me" is learning nothing. It is a free arm, consistent with the standing rule to use zero-token measures between exams.
  Done when: the backtest report shows real versus shuffled hit rates, and a forecaster within noise of shuffled is flagged "no signal".

- **Wild: plant a fake habit and check the forecaster does not over-learn it** — FEATURE — value 3 — effort S — risk low — category: overfitting
  Why: wild; assumption: a single repeated request, such as the two mistaken captures, could be promoted to a "habit". A planted one-off should stay below the evidence floor.
  Done when: injecting three identical asks in one minute does not produce a prediction, and four across separate days does.

- **Wild: time-machine mode that replays the forecaster at each past commit date** — FEATURE — value 3 — effort L — risk med — category: retrodiction
  Why: wild; the repo has 2547+ task commits with dated asks, so every past date has a known next request. This gives the walk-forward backtest real ground truth and finds regressions between generations.
  Done when: `fm foresight replay --since DATE` outputs a per-week hit-rate curve that is reproducible across two runs.

- **Fail the sweep on predictor outputs that no session path reads** — CLEAN — value 4 — effort S — risk low — category: reach
  Why: the standing reach rule says a capability must be called by a real session path, and the pack's open question asks which deliberation outputs nobody reads. Foresight is the likeliest to be write-only.
  Done when: `fm genesis check` lists each foresight output with its reading call site, and a test with an unread output makes it fail.

Next question: Which of fmforesight's existing outputs has a recorded hit or miss, so that a baseline for each exists before any new predictor is added?
Next question: If the user is away for a week, which forecasts and drafts are still valid when they return, and what ages them out?
