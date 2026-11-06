# Brainstorm — lens: blind spots

**Answers to earlier questions (my lens):**
- Cells counted under several stages: the pack suggests most collapse into a few predictor families (next-ask, problem-flag, machine-break). One planted-history probe per family, tagged to its cells, is the smallest covering set. This is an assumption.
- Does the sweep check cited behaviour: the pack only shows that the file exists. That is a gap, covered by the first idea below.

**Missed-ask classes I found:** T-2532 and T-2542 are silent degradation. T-2533 and T-2535 are gauges that omit something. T-2534 and T-2536 are missing control arms. T-2546 is duplicate-at-birth. T-2547 is a count mismatch between paired lists.

**Questions I asked of the whole project:** What can stop with no one noticing? What does each gauge leave out? What is each claim's control arm? Is this already built? Do paired artifacts agree in count?

- **Re-run each cell's cited behaviour in the sweep** — FIX — value 5 — effort M — risk low — category: coverage
  Why: the sweep appears to check that a cited file exists. Nothing shows it checks that the file still does what the cell claims after later generations edit it. T-2547 shows the "refuse on mismatch" pattern works.
  Done when: a test that edits a cited function to a no-op turns the sweep red on that cell.

- **Require a planted-history probe per predictor family** — FEATURE — value 5 — effort M — risk med — category: anticipation
  Why: assumption: the 58 cells collapse to a few families. A fixture history with a known next ask and a known breaking machine state is the smallest probe.
  Done when: `fm foresight` run on the fixture names the planted ask in its top 3, and a shuffled-history control run does not.

- **Fail the sweep on forecaster outputs no session path reads** — FIX — value 4 — effort S — risk low — category: reach
  Why: the standing reach rule exists for verbs, and the pack asks "who reads this output?" for deliberation and plan fields without an answer. A forecast written but never surfaced is invisible failure.
  Done when: a forecast field with no reader in `fm next`, the session-start note or the drive makes `fm genesis check` list it.

- **Make the forecaster report abstained, failed or empty distinctly** — FIX — value 4 — effort S — risk low — category: silent failure
  Why: T-2532 and T-2542 both came from silent off-states. An empty forecast list currently looks the same as a crash.
  Done when: killing the forecaster's data source yields "failed: <reason>" in `fm doctor` and the next session's Watch line.

- **Strip mistaken and test-fed captures from the user model** — FIX — value 4 — effort S — risk low — category: data hygiene
  Why: "The first brief" and "The second brief" were fed to `fm intake` while debugging T-2547's test, and were later dropped as "captured by mistake". They sat in the "asked" stream the model learns from.
  Done when: a capture dropped with a mistake reason, or made under a test env flag, is absent from the predictor's input in a test.

- **Meter the forecaster's cost in the lean ratchet from day one** — FEATURE — value 3 — effort S — risk low — category: lean
  Why: T-2533 found hook notes omitted from the ratchet. A new forecaster adds notes and tokens that would be omitted the same way.
  Done when: the ratchet row includes forecaster-injected chars per session and fails when it is absent.

- **Check pairs of generated lists for count parity** — CLEAN — value 3 — effort S — risk low — category: consistency
  Why: T-2547 is the exact case: briefs outnumbering grounding lines. Cells vs probes, steers vs checks and verbs vs index are the same shape.
  Done when: `fm genesis check` names any pair of declared parallel lists with unequal counts.

- **Answer "already built" at the moment of capture, for forecasts too** — FEATURE — value 4 — effort S — risk low — category: duplication
  Why: T-2546 and the dropped-as-built rows (guard arm, 8+ items) show asks arriving for things that exist. Predicted drafts need the same check before a lane is spent.
  Done when: a predicted draft that `fmrecall.covered` matches is shown as "exists: <clause>" and spawns no lane.

- **Score each predictor against a dumb baseline and mute the loser** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: T-2546's word-overlap matcher met no bar. Control arms were missed twice (T-2534, T-2536). Assumption: "same as last request" is the baseline.
  Done when: a predictor trailing the baseline on the asked-stream backtest is muted, with the reason in `fm doctor`.

- **Wild: run a shuffled-history control arm beside every forecast** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: wild. A real forecast that beats a shuffled one proves the model learned the user's patterns and not the format.
  Done when: the exam prints real vs shuffled hit@3 and flags when the gap is under noise.

- **Wild: weekly canary where a stub user sends a scripted ask through the whole chain** — FEATURE — value 3 — effort M — risk med — category: liveness
  Why: wild. This extends T-2542's timers-alive check to an end-to-end proof, from capture through draft to the heads-up line.
  Done when: the night tick logs canary latency, and a broken stage turns `fm doctor` red.

- **Wild: open each session with "what I'd have told you if you'd asked"** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: wild. The dropped-as-built ledger already shows the user finding out late, after asking for something that existed.
  Done when: the session-start note shows at most one line drawn from that ledger, muted after two dismissals.

Next question: Which of Foreman's own outputs would the user only notice missing when it already cost them a task?

Next question: Do the 58 cells' probes run on a harness other than Claude Code, and if not, which cells quietly depend on it?
