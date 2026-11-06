# Brainstorm — lens: the second opinion (invented): a cold rival that sees only the request designs it differently; every place the plans differ is a reading or approach the first one missed

- **Diff option sets against a blind rival** — FEATURE — value 4 — effort M — risk low — category: plan gate
  Why: T-2269 checks that an M/L Approach names 3+ options, but nothing checks whether they're the right ones. A tool-less Haiku sees only title and goal, lists its options, and the gate records any it names that the plan lacks. assumption: a missed option is the commonest way a plan goes wrong.
  Done when: a task whose Approach omits an option the rival named gets a one-line "rival also considered: X" note in its plan, and a test with a stubbed rival covers it.

- **Reject readings that are paraphrases** — FIX — value 3 — effort S — risk low — category: plan gate
  Why: the plan gate counts options and readings, and an earlier gap (T-2285) showed it can be fooled by text shape. The standing rule on templated coverage cells shows the same trap. Each reading must name a different deliverable or check.
  Done when: an L plan with two readings sharing most of their content words is refused, naming the pair.

- **Race at plan time when the top two options are close** — FEATURE — value 4 — effort M — risk med — category: auto race
  Why: T-2271 races the runner-up only after 3 failed runs, which is already late. When the Approach marks two options as near-equal and a cheap probe exists, race them before building.
  Done when: an S/M task with a "close call" marker starts two lanes, and the one that goes green first is recorded with its reason.

- **Keep a confidence ledger scored by outcome** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: Mission 8 #8/#3 predicts minutes, but the "calibrated judgment" ask is about stated confidence. Record a percentage per assumption and decision, then score "said 80%, held x%" at close.
  Done when: `fm calibration` prints a per-bucket hit rate from closed tasks, and a bucket off by more than 20 points is flagged.

- **Downgrade confidence when evidence contradicts it** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: stated confidence is written once at plan time. Two red runs on a step claimed at 90% should lower it and fire the research trigger, so "unsure → research" reacts to what happens, not only to the first guess.
  Done when: a second failure on a high-confidence step rewrites its confidence below the research threshold and opens a research note.

- **Classify steps as reversible or irreversible, and stop only on irreversible plus ambiguous** — FEATURE — value 5 — effort M — risk med — category: judgment
  Why: the request says to stop for the user only when something is irreversible and ambiguous. A command table (push, publish, migrate, rm, mandate) combined with confidence makes that a rule instead of a mood.
  Done when: a reversible low-confidence step proceeds with a recorded decision, and an irreversible one at under 60% confidence goes to `fm ask` once. Both are tested.

- **Log every decision made without the user, each with a one-line undo** — FEATURE — value 4 — effort S — risk low — category: judgment
  Why: "Everything else it decides and records" needs a record the user can read in 20 seconds. The log holds the decision, the confidence, the rejected option and the revert command, and it is shown in the close receipt.
  Done when: `fm task finish` prints "decided for you: N" with each item's undo command.

- **Bound the research trigger with a budget and a citation rule** — FEATURE — value 3 — effort M — risk med — category: research
  Why: the seed row has "unsure → research trigger (3)" but no limits. Without a cap it could loop. Set a query count and a minutes cap, require at least one source file or URL, and end with a confidence update.
  Done when: a research run stops at its cap, writes a note with at least one source, and the plan's assumption row shows the new confidence.

- **Set depth by blast radius times irreversibility, not by tier label** — PERFORMANCE — value 4 — effort M — risk med — category: scaling
  Why: "an S task doesn't pay an L task's cost" assumes the tier label is right. T-2277's blast data can show an S task touching ten co-changing files and escalate its gate.
  Done when: an S task whose blast radius exceeds a threshold is gated like M, with the reason printed.

- **Report how often the runner-up would have won** — FEATURE — value 3 — effort M — risk low — category: evidence
  Why: the plan gate and the race only get scored against signals Foreman didn't author if outcomes feed back. When a chosen option is later reverted or re-fixed, count the rejected option against it. Then check whether the 3-options rule predicts fewer reverts.
  Done when: `fm triggers`-style output lists gate precision by tier, using revert and re-fix counts.

- **Wild: Run a devil's advocate lane that must kill the chosen approach in writing** — FEATURE — value 3 — effort M — risk med — category: adversarial
  Why: assumption: a bounded attempt to refute the plan, with failure to refute raising confidence, catches blind spots better than agreement does. Wild.
  Done when: an L task's plan carries an "attack failed because…" paragraph, or its approach changes.

- **Wild: Pre-register the expected race winner and track the surprise rate** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: write "I expect option B because…" before the race. Surprises show where Foreman's intuition is worst and feed lessons. Wild.
  Done when: each race record has a predicted winner, and the report shows the surprise rate.

- **Wild: Treat disagreement across samples as the ambiguity detector** — FEATURE — value 4 — effort M — risk med — category: judgment
  Why: ask a cold child the same unclear question three times, with the user's steers in context. Ask the user only if the answers differ. This gives "ambiguous" a measurable meaning without a user-twin. Wild.
  Done when: an ambiguous fork with three differing samples reaches `fm ask`, and one with three matching samples is decided and logged.

Next question: Which stated confidence values has Foreman ever written, and have any been compared with how the task actually ended?
Next question: When the gate refuses a plan, how often does the retry add real options rather than reworded ones?
