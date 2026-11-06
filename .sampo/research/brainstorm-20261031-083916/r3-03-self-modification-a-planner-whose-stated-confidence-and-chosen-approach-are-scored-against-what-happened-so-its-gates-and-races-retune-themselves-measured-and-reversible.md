# Brainstorm — lens: self-modification: a planner whose stated confidence and chosen approach are scored against what happened, so its gates and races retune themselves, measured and reversible

- **Hold out a tuning test set** — FEATURE — value 5 — effort M — risk low — category: tuning integrity
  Why: assumption: tuning is scored on the same finished tasks it learned from, so improvements can be memorized noise. Earlier ideas cover backtesting and Foreman-unauthored signals, not a split.
  Done when: `fm tune propose` fits on a fixed older partition of closed tasks, applies a change only if a sealed newer partition also improves, and prints both scores. A test with a noise-only fixture shows no change applied.

- **Pair every knob with a counter-metric** — FEATURE — value 5 — effort M — risk med — category: Goodhart guard
  Why: assumption: a knob tuned to lower refusals will drift toward leniency. Re-opens, reverts and red-after-merge are already recorded (T-0826 and the router in T-2291).
  Done when: each knob declares a primary and a guard metric, and a fixture where the primary improves while the guard worsens auto-reverts the knob and logs both numbers.

- **Snapshot gate inputs at decision time** — FIX — value 4 — effort M — risk low — category: replayability
  Why: assumption: the plan text keeps being edited after the gate runs, so replaying the gate on finished tasks tests the final plan, not what the gate saw. Backtest ideas depend on this.
  Done when: every plan-gate and race-trigger decision stores a hashed input snapshot, and `fm tune replay T-NNNN --knob X=Y` reproduces the original verdict byte-for-byte on current defaults.

- **Sign a user-owned tuning envelope** — SECURITY — value 5 — effort S — risk low — category: self-mod bounds
  Why: fm mandate set/off is already user-only (T-2252), and "quarantine the tuner with a change budget" is listed. Missing: a file the user signs that the tuner cannot widen.
  Done when: knobs live in a signed `envelope` file giving each knob's min, max and max step per week. The tuner writing outside it, or editing the envelope, is refused by the guard and shown in `fm doctor`.

- **Detect knob drift from the ledger** — FIX — value 4 — effort S — risk low — category: integrity
  Why: assumption: knobs can be edited by hand, by a model, or by a merge, so live values may not match the last recorded change.
  Done when: `fm doctor` fails when any live knob value differs from the latest entry in the knob changelog, naming the knob and the commit that changed it.

- **Keep a tabu list of reverted tunings** — FEATURE — value 4 — effort S — risk low — category: learning
  Why: assumption: an auto-reverted change will be proposed again by the next tuning pass. "Auto-revert a knob" is listed, but not remembering why it failed.
  Done when: a reverted change stores its knob, direction and the evidence that sank it. The proposer will not re-suggest the same change until a new outcome class appears, shown by a test proposing it twice.

- **Map binding knobs from near-misses** — FEATURE — value 4 — effort M — risk low — category: attribution
  Why: assumption: most gate thresholds never decide anything. Today only refusals are logged, so passes by a margin of one are invisible.
  Done when: each gate decision records its margin, and `fm tune binding` lists which knobs flipped at least one verdict in the last 50 tasks and which never did.

- **Prune knobs that never bind** — CLEAN — value 3 — effort S — risk med — category: simplicity
  Why: assumption: dozens of knobs add ceremony and attack surface. Follows from the binding map. The lean ratchet (Mission 8/#12) only measures growth, not removal.
  Done when: a knob with no verdict flipped in N tasks is proposed for removal with its replay evidence. Removing it leaves the full suite green.

- **Give tuned gates a sunset clause** — FEATURE — value 3 — effort S — risk low — category: reversibility
  Why: assumption: tightening ratchets only upward. A tuned-stricter gate with no fresh evidence should lapse back to default.
  Done when: every tuned value carries an expiry. After it passes with fewer than K supporting outcomes, the value reverts to default and logs "lapsed".

- **Wild: Synthesize a gate from a failure class** — FEATURE — value 4 — effort L — risk high — category: gate synthesis
  Why: wild; assumption: when a failure signature recurs (Mission 8 #7 files a FIX task), a new check could be written automatically. The check would be a candidate gate that replays the failing tasks, must flag them, and must stay quiet on a held-out passing set.
  Done when: a candidate gate flags at least 2 of the originating tasks and 0 of 20 clean ones in shadow mode, and enters enforcement only after the user approves its one-line description.

- **Wild: Publish a pinned self-model card the tuner can't override** — FEATURE — value 4 — effort M — risk low — category: user control
  Why: wild; assumption: Foreman holds learned beliefs ("my L estimates run 1.8× long", "this user rejects plans over one screen"). The user can see, edit or pin each belief, and a pinned one stops being tuned.
  Done when: `fm self` prints each belief with its evidence and confidence. Pinning one makes the tuner skip it, shown by a test that pins a belief and runs a tuning pass that doesn't change it.

- **Wild: Hold a tuning tribunal with a cold prosecutor** — FEATURE — value 3 — effort M — risk med — category: adversarial review
  Why: wild; assumption: tuner and judge are both Foreman-authored. A different-model cold child gets only the proposed change and its numbers and must argue one plausible way the metric was gamed.
  Done when: a proposal cannot apply until the prosecutor's argument is stored. A fixture with a planted gaming change is caught and a legitimate change is not blocked.

- **Wild: Map hedging words to scored numbers** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild; assumption: the planner says "probably" and "likely" in plans and finish notes, and the user reads those words, not the numbers. Each word gets a hit rate from outcomes and is retuned.
  Done when: `fm calibrate words` lists each hedge with its measured hit rate. A word whose rate is far from its band gets flagged, and a plan using it shows the measured percentage beside it.

Next question: Which knobs does the user ever change by hand, and does the tuner's output match what they chose?
Next question: What outcome signal exists that a model can't forge, and for which gates is there none at all?
