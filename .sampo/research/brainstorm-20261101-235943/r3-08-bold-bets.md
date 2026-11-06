# Brainstorm — lens: bold bets

- **Run a shadow-user twin that pre-answers every yes-card** — FEATURE — value 5 — effort L — risk med — category: anticipation
  Why: assumption: ~30 standing steers plus the "asked" stream are enough to model the user's tie-breaks; T-0864 and the blocked-on-user backlog show unanswered cards stall lanes. The twin drafts a proposed answer per card, marked as a guess, never acting.
  Done when: on a replay of the last 50 real user answers, the twin's proposed answer matches in at least the share a "always approve" baseline does, and `fm next` shows the guess beside each card.

- **Backtest every cell by retrodiction on history** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the lessons say T-2546's word-overlap matcher met no bar; the open question is which of the 58 cells are really one capability. A cell counts only if a walk-forward replay on the asked stream shows a hit or a catch.
  Done when: `fm genesis check` prints per-cell hit@3 and lead time from a replay, and a cell with no replayed hit stays "unread".

- **Collapse the 58 cells into predictor families with one probe each** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: the earlier questions ask which cells are one capability counted under several stages; the standing rule forbids templated cells.
  Done when: a family table lists at most 12 families, every cell cites a family and a session path, and a lint rejects a cell sharing 20 lines with a neighbour.

- **Strip Foreman-authored input from the user model** — FIX — value 4 — effort S — risk low — category: reliability
  Why: T-2547 notes "The first brief" and "The second brief" were captured by mistake from test feeds and sit in the asked stream, so they would poison any model of the user.
  Done when: a test feeds fm intake a sample line and the model-of-me input excludes it, and the two dropped captures are filtered.

- **Make forecasts a single ranked heads-up row in fm next** — FEATURE — value 4 — effort S — risk low — category: reach
  Why: the standing rule says every capability must be called by a real session path; a page no one opens is silent. Capped at one line, muted after two dismissals.
  Done when: with a seeded history, `fm next` prints one "heads-up" line with a because-clause, and two dismissals mute that signature.

- **Run a purge-resistant prediction ledger that resolves hit, miss or expired** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the bets pipeline exists (Brier, harness split), but nothing scores request or breakage predictions; abstention must be recorded as "abstained", not an empty list.
  Done when: `fm outcomes --judgment` lists forecast rows with a hit rate against a "repeat the last ask" baseline.

- **Predict the user's drop before filing a self-filed task** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: the "dropped" list is long (stack cards for single-use deps, the guard-only arm already built, mistaken captures); Foreman keeps filing work the user drops.
  Done when: replaying the dropped ledger, the filter would have held back at least half of dropped self-filed items while holding back under 10% of kept ones.

- **Forecast machine exhaustion with an ETA** — FEATURE — value 3 — effort M — risk low — category: machines
  Why: the environment shows lanes writing to tmpfs under /run/user/1000, and T-2543 shows ETXTBSY flakes. Disk and tmpfs runway are cheap to compute before spawning lanes.
  Done when: before a lane spawn, `fm lane` refuses with an ETA message when projected tmpfs use exceeds the free space in a seeded fixture.

- **Verify each cell's cited behaviour, not its file, every sweep** — CLEAN — value 4 — effort M — risk low — category: rot
  Why: an earlier question asks whether the sweep checks that a filled cell still behaves as claimed; today it checks existence.
  Done when: a cell's probe command runs in the sweep and a seeded behaviour change turns that cell red.

- **Wild: add a shuffled-history control arm to every predictor** — FEATURE — value 4 — effort M — risk low — category: honesty
  Why: wild; assumption: predictors can look good by recency alone. Run each on the real history and on a shuffled one; only the gap counts.
  Done when: `fm exam` prints real-vs-shuffled hit@3 per predictor and flags any within noise of the control.

- **Wild: open the session with "what I would have told you if you had asked"** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: wild; the dropped-as-built entries (T-2529, the guard-only arm) are exactly asks the user made that were already done. Surfacing them before the ask saves the round trip.
  Done when: session start prints at most one already-built line when the open queue's newest item matches a built clause, and nothing otherwise.

- **Wild: a time-machine replay that runs the forecaster at each past commit date** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: wild; the long-horizon tier already replays real repos at past commits, so the same harness can replay the forecaster with only the history available then.
  Done when: a run on this repo reports the predicted next-ask hit rate per month, using no data newer than each replay point.

- **Wild: plant a fake habit and check the forecaster does not over-learn it** — FEATURE — value 3 — effort S — risk low — category: robustness
  Why: wild; a canary habit injected into a fixture history shows whether predictors chase noise.
  Done when: a fixture with a planted three-time pattern produces no draft below the evidence floor, and a real five-time pattern does.

- **Park a predicted ask as a title-only deferred task** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: speculative lanes spend tokens; the lean steer says growth must be measured. A stub costs nothing and is scored at wake time.
  Done when: a predicted ask appears as a deferred stub with no lane started, and a yes spawns the draft.

Next question: Which anticipation outputs would the user actually read in a week of normal use, and what does `fm next` look like if only one survives?
Next question: What do the host CLIs' transcripts for codex, gemini and opencode lack that the user model needs, so a forecast built on Claude's data would silently mislead on them?
