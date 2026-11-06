# Brainstorm — lens: blind spots

**Blind-spot classes the pack shows**
- Silent failure: T-2532 (hook events switching off), T-2542 (dead timers).
- Unattributed or unmeasured cost: T-2533, T-2535, T-2536.
- Asked for something already built: T-2534, T-2546.
- Claims with no check behind them: T-2547.
- Foreman's own noise read as the user's voice: the "first brief" and "second brief" captures made while debugging T-2547.

I put the question that would have caught each class to the Anticipation capability (gen-0 #3) and its 58 empty cells. Everything below is new relative to the earlier lists.

- **Make the forecaster report its own liveness** — FIX — value 5 — effort S — risk low — category: observability
  Why: T-2532 and T-2542 both found silent-off components. Nothing shows that `fmforesight` ran, abstained or crashed. Assumption: it has no beat of its own.
  Done when: a session that runs `fmforesight` with a forced import failure shows "foresight: failed (reason)" in `fm doctor` and the SessionStart Watch line, distinct from "abstained: no evidence".

- **Tag every user-model input with its origin and drop Foreman-authored ones** — FIX — value 5 — effort M — risk med — category: data hygiene
  Why: the "first brief" and "second brief" fixture captures became real asked/dropped rows. A model of the user trained on them learns Foreman's debugging, not the user.
  Done when: a test pushing a captured-by-mistake line through `fm intake` leaves the predictor's training set unchanged. The origin tag shows in `fm foresight --explain`.

- **Run an already-built check before any predicted draft is lane-ed** — FEATURE — value 5 — effort S — risk low — category: anticipation
  Why: the user had to ask for T-2534 (already built) and T-2546 (the cure). A predicted draft with no `fmrecall.covered` pass would repeat that waste at lane cost.
  Done when: a draft whose request restates a MASTER.md clause is parked with a "covered by T-NNNN" line and spawns no lane.

- **Read dropped-as-built asks at session start** — FEATURE — value 4 — effort S — risk low — category: user model
  Why: two of the "dropped" rows say "already built", so the ledger records what the user could not know. Assumption: no session path reads that class today.
  Done when: SessionStart prints at most one line naming a dropped-as-built item that matches the open queue's newest item.

- **Make the cell probe a per-cell planted-history replay** — FEATURE — value 5 — effort M — risk med — category: coverage
  Why: the earlier left question asks whether a filled cell's cited file still behaves as claimed. Each cell would seed a tiny fake history with a known next request and assert `fmforesight` returns it.
  Done when: `fm genesis sweep` reds a cell whose probe fails on the current tree, and it names the cell and the commit that broke it.

- **Add a shuffled-history control arm to every predictor** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the T-2546 word-overlap matcher "met no bar". A prediction beating its own shuffled control proves it learned something.
  Done when: `fm outcomes --judgment` prints each predictor's hit rate beside its shuffled-control rate, and a predictor within noise of control is muted.

- **Flag silent changes in what a gauge omits, per predictor** — FIX — value 3 — effort S — risk low — category: observability
  Why: T-2533 existed because a gauge missed per-call notes. Foresight output (flags, drafts) injected into context is probably uncounted in the lean ratchet. Assumption: it is not charged today.
  Done when: the lean ratchet's static row includes the chars foresight injected per session, and a test fails if a new foresight surface isn't counted.

- **Rank the anticipation outputs nothing reads for deletion** — CLEAN — value 3 — effort M — risk low — category: simplicity
  Why: the left question "which deliberation outputs does no session path read" applies here. A prediction written to a file nobody opens never gets scored.
  Done when: `fm genesis check` lists each foresight output file with its reader path or "no reader", and every "no reader" becomes a task or a recorded n/a.

- **Predict which self-filed task the user will drop, before filing it** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: the dropped ledger holds measured examples (T-2529-style "1 of 22" and "5 of 1219 cards used"). A drop-likelihood score from the dropped ledger's reasons could gate filing. Backtest on the existing dropped rows first, per the Lessons.
  Done when: the backtest on the dropped ledger shows precision above the always-file baseline, or the idea is recorded as failed with the numbers.

- **Test the same predictor on all five harnesses' transcript shapes** — FIX — value 3 — effort M — risk med — category: harness parity
  Why: the earlier left question about non-Claude plans. Assumption: asked records come only from Claude Code transcripts.
  Done when: fixtures from codex, gemini, opencode and `fm code` each yield the same asked-record fields, or `fm doctor` names the harness with none.

- **Wild: Hold a "silent day" drill for anticipation** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: wild. Once a week the night tick breaks one foresight source (empty history, stale tree hash, dead timer) and records which surface noticed and how fast.
  Done when: the drill's report lists each break with the first surface that named it, and a break nobody named becomes a task.

- **Wild: A stub-user twin written only from the steers list** — FEATURE — value 4 — effort L — risk med — category: evaluation
  Why: wild. The standing steers are the one input Foreman didn't author about the user. A tool-less child given only those predicts "the next three asks", scored against what the user actually asked.
  Done when: a sealed prediction file exists before each Seed, and `fm outcomes` scores it against the next three asked lines.

- **Wild: Print "things I'd have told you if you'd asked" at resume** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: wild. Both T-2534 and T-2546 were asks for what already existed. One line at resume names the feature the open queue's newest item overlaps.
  Done when: resuming a session with an overlapping open item prints exactly one such line with the existing task id, and prints nothing otherwise.

- **Add expiry to cell n/a rulings, with a counterexample search** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: the left question about the standing n/a-needs-a-counterexample rule. An n/a without a recorded search never gets re-examined.
  Done when: `fm genesis sweep` reds any n/a cell lacking a dated search note, and re-opens it after the set expiry.

Next question: Which of the 58 cells' probes would still pass if `fmforesight` were deleted, and are those cells real?
Next question: What does the user do in the first minute after a wrong prediction (dismiss, ignore, retype), and does any path record it?
