# Brainstorm — lens: inversion: how exhaustive thinking and judgment fail: acts on the first reading, takes the first approach, never tests alternatives, states false confidence, asks the user what it could decide, doesn't stop when a step is irreversible and ambiguous

- **Fail the plan when the Approach's "options" are one idea in three costumes** — FIX — value 4 — effort M — risk med — category: plan gate
  Why: T-2285 shows the gate counts text after a marker, so "1) --bench … 2) --bench … 3) …" passes. Evidence the gate measures form, not distinctness. Assumption: a cheap check (distinct first verbs/paths, or a cold Haiku "are these different?") is enough.
  Done when: a fixture plan listing three options that differ only in a flag fails the gate naming the duplicates, and a fixture with three genuinely different options passes.

- **Record the confidence number with the evidence that moved it** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: Mission 5 #8 asks for stated confidence; a bare "80%" is false confidence by default. Assumption: no field today ties a stated confidence to a source.
  Done when: every confidence line in a plan or close note carries "because: <file/run/note id>", and `fm doctor` flags one with none.

- **Score stated confidence against outcomes and show the calibration curve** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: T-2290 predicts minutes and attempts but the pack shows nothing scoring "I was sure" claims. Without it, confidence can't be trusted or tuned.
  Done when: `fm calibration` lists confidence buckets (50/70/90) with the fraction that held after close, and a bucket that is overconfident by 20 points or more is flagged.

- **Classify each stop-and-ask as decidable, irreversible-ambiguous, or user-only before it is sent** — FEATURE — value 5 — effort M — risk med — category: judgment
  Why: Mission 5 #8 says stop only when irreversible and ambiguous; the pack has `fm ask` but no gate that tests a question against that rule. Assumption: many asks today are decidable from steers or repo evidence.
  Done when: `fm ask` refuses a question that has no irreversibility marker and is answerable from steers, printing the steer or evidence it would have used; the decision is recorded.

- **Mark each plan step reversible, costly-to-undo or irreversible, and hold the irreversible ones to a stricter path** — FEATURE — value 5 — effort M — risk med — category: safety
  Why: the whole "when to stop" rule depends on knowing irreversibility, and nothing in the pack labels steps with it (publish, push, migration, delete, external send). Assumption: the guard knows commands but the plan doesn't carry the label.
  Done when: a plan with a push or migration row shows the label, and focusing that row with a low-confidence assumption unresolved is refused.

- **Run the race for real when the first approach's verify is cheap, and record who won and why** — FEATURE — value 4 — effort M — risk med — category: approaches
  Why: T-2271 races only after 3 failures. The brief wants candidates tested in parallel lanes by evidence, but the pack shows no up-front race for cheap-to-verify S/M tasks. Assumption: lane cost is small for those.
  Done when: an M task whose Approach lists two options with a runnable check gets two lanes at focus, and the choice record names the check output that decided it.

- **Detect a first-reading lock-in by diffing the plan's readings against the user's actual words** — FEATURE — value 4 — effort S — risk low — category: readings
  Why: the intake ideas list notes steers later contradicting first answers. Assumption: the plan's chosen reading can be compared to the verbatim ask by a cold read.
  Done when: a plan whose chosen reading omits a clause of the ask is flagged, with the omitted clause quoted.

- **Record every decision Foreman made instead of asking, with a one-line undo** — FEATURE — value 4 — effort S — risk low — category: decisions
  Why: the request says "everything else it decides and records". Assumption: records exist as scattered notes, not one reviewable list.
  Done when: `fm decisions` lists autonomous decisions since a date, each with its evidence and an undo command, and a decision lacking either is marked.

- **Treat a research note as required when two sources disagree, and cite both** — FIX — value 3 — effort S — risk low — category: research
  Why: T-2269 requires a research note for a low-confidence assumption but not that the note face conflicting evidence. Assumption: notes can end up confirming the first guess only.
  Done when: a research note with no "against" line is rejected by the plan gate for low-confidence rows.

- **Wild: Hire a devil's-advocate lane that must find the plan's most expensive wrong assumption** — FEATURE — value 4 — effort M — risk med — category: red team
  Why: wild; no check today challenges the chosen approach from outside it. Assumption: a cold child on a different model gives an independent signal, matching the standing "signals Foreman didn't author" rule.
  Done when: an L plan gets a one-paragraph objection quoting a specific plan line, and the user can see whether it changed the plan.

- **Wild: Make confidence expire, so a claim made before a file changed must be re-earned** — FEATURE — value 3 — effort M — risk med — category: calibration
  Why: wild; a "sure" stated at plan time goes stale after commits touch the scope. Assumption: scope paths are known.
  Done when: editing a scope file after a stated confidence marks that confidence stale in the next status and the close gate asks for a re-check.

- **Wild: Replay past tasks through the plan gate to measure how often first-instinct plans lost to the runner-up** — FEATURE — value 4 — effort L — risk low — category: evidence
  Why: wild; the request says choose by evidence, and history of races (T-2271) can show where the first approach fails. Assumption: enough closed tasks hold options and outcomes.
  Done when: a report lists task kinds where the runner-up won more than 30% of races, and the plan gate raises its depth for those kinds.

- **Surface "I assumed" lines in the finish receipt, grouped by whether they held** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: assumptions recorded at plan time are invisible at close, so false confidence never gets challenged. Assumption: assumptions are stored as plan rows.
  Done when: a closed task's receipt prints each assumption as held, broke or untested.

Next question: Which decisions did Foreman make autonomously in the last month that the user later reversed, and what did they have in common?
Next question: Is there any step type besides push, publish and migration that is irreversible but not yet recognised by the guard?
