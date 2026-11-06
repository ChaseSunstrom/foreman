# Brainstorm — lens: user value

- **Show "already built" at capture time, with the clause and task id** — FEATURE — value 5 — effort S — risk low — category: capture
  Why: T-2546 (fmrecall.covered matching MASTER.md clauses) exists but the dropped ledger shows several asks later dropped as already built (guard-only exam arm, T-0963). The user pays a round trip each time.
  Done when: `fm capture "a guard-only exam arm"` prints the MASTER.md clause and T-0963 before filing, tested red-first on that sentence.

- **Strip test and debug captures from the user model's input** — FIX — value 5 — effort S — risk low — category: user model
  Why: "The first brief" and "The second brief" were captured by mistake from T-2547's test and both sit in the asked stream. An Anticipation model trained on them learns noise.
  Done when: running the T-2547 test fixture leaves `fm intake` and the asked stream with zero new rows, and a fixture history containing such rows yields identical forecasts with and without them.

- **Put one ranked heads-up line in `fm next`** — FEATURE — value 5 — effort S — risk low — category: reach
  Why: the open question "which outputs does no session path read" applies to fmforesight; gen-0 #3 requires session-path reach. A line in the verb every session already calls gives the user value without opening the UI.
  Done when: with a planted history, `fm next` prints exactly one line naming the predicted problem or request, and prints nothing when evidence is below the floor.

- **Backtest every predictor walk-forward before it may draft** — FEATURE — value 5 — effort M — risk low — category: predictor gating
  Why: lessons from Missions 3-5: T-2546's word-overlap matcher met no bar. The asked stream has enough history for hit@3 versus a last-request baseline.
  Done when: `fm foresight backtest` prints hit@3 and the baseline per predictor, and a predictor under the baseline is refused lane drafting by a test.

- **Predict which self-filed task the user will drop, before filing** — FEATURE — value 4 — effort M — risk low — category: noise reduction
  Why: the dropped ledger shows Foreman-filed items (guard arm, cleanup candidates, stack cards) repeatedly dropped with measured reasons; the user spends attention to say no.
  Done when: replaying the last 30 dropped self-filed items, at least half are flagged "likely dropped" from their class, and a flagged item is held in a digest, not filed.

- **Mute a flag signature after two dismissals** — FEATURE — value 4 — effort S — risk low — category: restraint
  Why: assumption: proactive problem flags will annoy as fast as the brief-guard false positives did; no dismissal memory exists.
  Done when: dismissing the same signature twice stops it appearing, and `fm doctor` lists the muted signatures with a one-command unmute.

- **Forecast machine exhaustion with an ETA before spawning lanes** — FEATURE — value 4 — effort M — risk low — category: machine model
  Why: the children directory lives on a tmpfs under /run/user/1000, and the environment shows parallel lanes; the pack mentions ETXTBSY and lane failures but no runway check.
  Done when: with a planted disk or tmpfs fill rate, lane spawn prints runway and refuses when it falls short of the lane's estimated need.

- **Resolve every prediction to hit, miss or expired, and show abstained** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the open question that a forecaster returning an empty list looks identical to a dead one; the bets machinery (fm outcomes --judgment) already scores Brier for plans, not asks.
  Done when: `fm foresight` shows counts per outcome including abstained, and a killed predictor shows "failed", not zero.

- **Draft the third ask of a series from the user's steer chain** — FEATURE — value 4 — effort L — risk med — category: drafting
  Why: the asked stream shows chained series (T-2532 to 2536, 2540-2542); the user repeats the same shape "FEATURE: X, DONE-WHEN: Y". A spec-only lane with an expiry could draft the next one.
  Done when: on a fixture history ending at the second of a known series, the draft matches the third in at least a tested keyword overlap, carries a grounding line, and expires unmerged.

- **Warn when a new feature collides with a standing steer** — FEATURE — value 4 — effort M — risk med — category: pre-flight
  Why: 40+ steers are in force (round-first, pace off, lean substance); a new ask can violate one silently and cost a correction round.
  Done when: capturing a request that contradicts a stored steer (fixture: "drop work for budget") prints the steer id and date before filing.

- **Wild: Open each session with "what I would have told you if you'd asked"** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: wild; built from the dropped-as-built ledger and recent decisions, answering questions the user has historically had to ask.
  Done when: session start prints at most three items, each citing a ledger row, and none the user already dismissed.

- **Wild: Shuffled-history control arm for every predictor** — FEATURE — value 3 — effort M — risk low — category: validity
  Why: wild; a predictor that scores the same on shuffled history is learning priors, not the user. No such control exists in the exam.
  Done when: the exam reports real versus shuffled hit@3 and flags any predictor whose gap is under a threshold.

- **Wild: Time-machine replay of the forecaster across past commit dates** — FEATURE — value 3 — effort L — risk low — category: evaluation
  Why: wild; the git history and asked stream give ground truth for free, with no new model calls needed.
  Done when: `fm foresight replay --since 60d` prints weekly hit rate from only the data available on each date.

- **Wild: Pre-write tomorrow's first task as a title-only stub, scored at wake** — FEATURE — value 3 — effort S — risk low — category: speculative drafts
  Why: wild; costs no tokens, only a title, and gives an honest daily hit measurement.
  Done when: each night the tick writes one stub tagged speculative, and next session start reports whether the user's first ask matched it, then deletes it.

Next question: Which of the user's recurring corrections is not yet in the asked stream at all because it was spoken in a harness whose transcripts Foreman doesn't read?
Next question: What does the user do in the first minute of a session before typing a request, and could that signal drive the first heads-up?
