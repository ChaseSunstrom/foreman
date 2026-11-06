# Brainstorm — lens: reliability

- **Stamp every forecast with the tree hash and steer set it was computed on** — FEATURE — value 4 — effort S — risk low — category: forecast integrity
  Why: speculative drafts (fmforesight) outlive the repo state and standing steers that justified them, and 25+ steers changed in two days (round-first, pace off, lean substance). Assumption: drafts currently carry no staleness check.
  Done when: a draft whose tree hash or steer list moved since it was written is refused at adoption, with a test that edits a steer and sees the refusal.

- **Resolve every prediction to hit, miss, expired or abstained** — FEATURE — value 5 — effort M — risk low — category: forecast integrity
  Why: "Questions earlier brainstorms left" asks which outputs no session path reads; a forecaster that returns an empty list is indistinguishable from one that crashed. Bets already settle this way in fm outcomes (T-2527 era), so the pattern exists.
  Done when: fm doctor shows counts of the four resolutions for the last 30 days, and a forecaster forced to raise shows "failed", not "abstained".

- **Strip Foreman-authored and mistaken captures from the user model input** — FIX — value 5 — effort S — risk low — category: data hygiene
  Why: the pack's dropped list shows "The first brief" and "The second brief" were test strings fed to fm intake while debugging T-2547; they sit in "The user's own words" as asks. A model of the user trained on them is poisoned.
  Done when: a test that captures a string marked as debug/test leaves the model-of-me input unchanged, and the two existing dropped items are absent from it.

- **Walk-forward backtest gate for every predictor before it may draft** — FEATURE — value 5 — effort M — risk med — category: backtest
  Why: lessons say "for a heuristic, name the backtest that decides whether it ships (T-2546's word-overlap matcher met no bar)". Standing exam rules also favour signals Foreman didn't author.
  Done when: fm foresight refuses to enable a predictor lacking a recorded hit@3 against a shuffled-history control, printing both numbers.

- **Add a shuffled-history control arm to the foresight probe** — FEATURE — value 4 — effort S — risk low — category: backtest
  Why: without a control, a hit rate from habit-heavy history (the user's recurring FEATURE:/FIX: phrasing) can't be told from chance. Assumption: no control exists today.
  Done when: the probe reports real vs shuffled hit rates and fails when the gap is under a stated margin.

- **Plant a known next-ask in a fixture history and require the forecaster to find it** — FEATURE — value 4 — effort M — risk low — category: cell probes
  Why: answers "does anything verify a filled cell's behaviour, or only that the file exists?". One planted-history probe per predictor family replaces 58 prose cells.
  Done when: removing the cited function from a scratch copy makes the probe fail, and the sweep runs it.

- **Make cell citations re-run, not just resolve** — FEATURE — value 4 — effort M — risk med — category: coverage
  Why: the pack's open question: sweep checks existence, not behaviour, after later generations change a file (T-2547 only checks briefs vs grounding lines).
  Done when: coverage cells carry a probe command; the sweep goes red naming the cell when its command exits non-zero.

- **Fail the sweep on forecast outputs no session path reads** — CLEAN — value 3 — effort S — risk low — category: reach
  Why: standing rule that every capability must be called by a real path; "Which deliberation outputs does no session path read" is unanswered.
  Done when: fm genesis check lists each fmforesight output with its reading path or marks it "unread" and goes red.

- **Mute a flag signature after two dismissals and cap flags at one per session** — FEATURE — value 4 — effort S — risk low — category: noise control
  Why: assumption: problem-flagging that repeats erodes trust the way the brief-guard false positives did (two known).
  Done when: a test dismisses a flag twice and it never reappears; a second flag in one session is queued, not shown.

- **Wild: time-machine replay — run the forecaster at each past commit date and score it on what was asked next** — FEATURE — value 4 — effort L — risk med — category: backtest
  Why: wild; the asked stream and git dates give free ground truth for hundreds of points.
  Done when: fm foresight replay prints a learning curve of hit@3 against history length.

- **Wild: plant a fake habit and check the forecaster does not over-learn it** — FEATURE — value 3 — effort M — risk low — category: robustness
  Why: wild; a synthetic user who always asks for X after Y must produce a prediction only after N repeats, never after one.
  Done when: a probe shows zero predictions after 1 occurrence and a correct one after the threshold.

- **Wild: weekly canary where a stub user asks a scripted request and the whole anticipation chain is timed end to end** — FEATURE — value 3 — effort M — risk low — category: liveness
  Why: wild; the night tick liveness work (T-2542) shows silent dead timers happen.
  Done when: fm doctor shows the canary's last pass time, and a disabled forecaster turns it red.

- **Rebuild the user model from its append-only sources and prove it matches the stored one** — CLEAN — value 3 — effort M — risk low — category: data hygiene
  Why: assumption: a derived store that can't be regenerated can't be audited; five harness transcript shapes feed it.
  Done when: fm doctor reports a diff of zero between rebuilt and stored, or names the diverging records.

Next question: Which predictor inputs come from a harness other than Claude Code, and has any forecast ever been produced from them?
Next question: What does the user see when the forecaster is disabled by a failing backtest gate: silence, or a one-line reason?
