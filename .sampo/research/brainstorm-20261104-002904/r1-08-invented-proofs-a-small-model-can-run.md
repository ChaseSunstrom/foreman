# Brainstorm — lens: invented: proofs a small model can run

- **Turn spec examples into runnable criteria at plan time** — FEATURE — value 5 — effort M — risk med — category: meaning proofs
  Why: the meaning class is the largest unproven one (599), and spec example assertions are the stated fix. A small model should only fill a fixed slot template (command, args, expected output). Anything it can't slot is labelled "meaning: unproven" and gets no criterion.
  Done when: a spec with 5 "given X, expect Y" examples makes `sampo plan` emit 5 executable checks. A 6th, deliberately vague example is listed as unproven rather than dropped.

- **Extract and resolve doc claims with a local model** — FEATURE — value 5 — effort M — risk med — category: docs verification
  Why: 421 docs make claims no run has checked. A small model lists each claim as a sentence plus a candidate probe (a `--json` path, a grep count, a `--help` line). A mechanical runner executes the probe, and a claim with no probe is tagged "unchecked" in the doc's report.
  Done when: running it on MASTER.md prints N claims split into checked-pass, checked-fail and unchecked, and planting a false claim moves it to checked-fail.

- **Lint public surfaces for role names** — FIX — value 4 — effort S — risk low — category: public surfaces
  Why: the steer says surfaces must name models by role and the orchestrator as any agent, never a user's endpoint or vendor. A regex list (jarvis, hostnames, Claude as orchestrator) runs for free over site/, README and scene text. A small model then judges the ambiguous hits, such as "Claude" as a role versus as a product claim.
  Done when: a planted "jarvis" in site/index.html fails the ship gate with file:line, and the current tree passes.

- **Calibrate every small-model verifier before it counts** — FEATURE — value 5 — effort M — risk low — category: verifier trust
  Why: standing rules say only signals Foreman didn't author count, and Haiku scores never decide "done". Each local verifier (Jev classifier, qwen3.8-27b) gets planted true/false claim pairs per class, and its verdict is trusted only above a recorded held-out accuracy. Below that, its output is shown as "advisory".
  Done when: `sampo louhi models` prints per-class accuracy for each verifier, and a verifier below the bar is labelled advisory in the proof receipt.

- **Check entailment of claim against real command output** — FEATURE — value 4 — effort M — risk med — category: meaning proofs
  Why: tests prove behaviour, not that the output means what the task asked. The classifier is given the Done-when sentence plus the captured stdout and returns entails, contradicts or neutral. Neutral stays "unproven".
  Done when: on a fixture set of 20 task/output pairs, a contradicting output is never reported as entailed, and neutral cases show as unproven.

- **Kill rate against model-written wrong implementations** — FEATURE — value 4 — effort M — risk med — category: proof strength
  Why: a proof that passes anything proves nothing. A local model writes 5 plausible wrong patches from the spec alone, and the proof must fail on at least 4. Otherwise the proof is labelled "weak".
  Done when: a proof command of `true` is flagged weak, and a real proof reports its kill count, e.g. 5/5.

- **Offer a constrained proof-template menu** — CLEAN — value 4 — effort S — risk low — category: small-model proofs
  Why: small models fail at free-form scripting but do well at choosing. Six templates (exit code, JSON path equals, grep count, golden diff, file exists, timing under N) are filled via grammar-constrained decoding.
  Done when: qwen3.8-27b produces a valid template-filled proof for 9 of 10 held-out Done-when lines, and the rest fall back to unproven.

- **Detect stale doc sentences by embedding distance to code** — PERFORMANCE — value 3 — effort S — risk low — category: docs drift
  Why: embedders are already planned (T-2893 and the local runtime). Each doc sentence is paired with its nearest `--help` or docstring chunk, and a large distance flags drift at zero generation cost.
  Done when: a doc sentence deliberately contradicting a verb's help text lands in the top 5% drift list.

- **Require two-family agreement for "verified"** — SECURITY — value 4 — effort M — risk low — category: verifier trust
  Why: the rule is to use signals Foreman didn't author. A claim reads "verified" only if two different-family verifiers agree, and a single vote reads "unproven (one reader)".
  Done when: a receipt shows both votes, and disagreement downgrades to unproven.

- **(wild) Round-trip docs through tests** — FEATURE — value 4 — effort L — risk med — category: docs verification
  Why: assumption: a model that sees only the test suite and rewrites the doc will omit what the tests don't cover. The diff against the real doc lists claims nothing backs, which a proof-by-absence can't do.
  Done when: for one doc, the diff names at least 3 sentences with no backing test, and a human confirms 2 of them.

- **(wild) Dispatch a literal-minded newcomer child** — FEATURE — value 4 — effort M — risk low — category: meaning proofs
  Why: a tool-less small model follows the README quickstart step by step in a scratch home and reports where a step is ambiguous or fails. Each failure becomes an "unproven for a stranger" label.
  Done when: planting a missing step in the README makes the child fail at exactly that step.

- **(wild) Run an overnight claim census on idle local hardware** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the 421 figure is a snapshot. A nightly sweep on the local models writes a tally of checked vs unchecked claims per doc, shown as a gauge on the site's Models section, with a falling unchecked line as the goal.
  Done when: two consecutive nights produce a diffable census file, and the site shows the trend.

- **(wild) Let a prosecutor model attack each "verified" label** — FEATURE — value 3 — effort L — risk high — category: adversarial proof
  Why: assumption: a small adversary given only the claim and the proof script tries to name an input the proof would wrongly pass, and any counterexample that actually runs flips the label to unproven.
  Done when: on a seeded vacuous proof, the prosecutor produces a running counterexample and the label flips.

Next question: which of the 599 meaning-unproven claims are about wording or presentation (which no command can check) rather than behaviour, and should they get a separate "judged, not proven" label?
Next question: what accuracy does qwen3.8-27b reach on slot-filling spec examples versus the cheaper classifier, and at what accuracy is a template-filled proof better than none?
