# Brainstorm — lens: invented: proofs a small model can run

- **Sieve doc claims into mechanical, structural and semantic before any model sees them** — FEATURE — value 5 — effort M — risk low — category: claims
  Why: 421 docs flag claims no run has checked; most are likely checkable by grep, `--help` or file existence. A small model should only get the residue (assumption: a majority are mechanical).
  Done when: `sampo claims classify` prints a three-way count over the 421 and a held-out hand-labelled sample of 30 matches at ≥90%.

- **Compile spec examples to criteria through a fixed template menu** — FEATURE — value 5 — effort M — risk med — category: plan-time criteria
  Why: meaning is the largest unproven class (599); free-form generation by a small model invents wrong assertions. A menu (exit code, stdout contains, file exists, JSON path equals) limits it to filling slots.
  Done when: 20 spec examples from closed tasks compile into criteria with slots filled, and a schema check rejects any output outside the menu.

- **Require every compiled criterion to fail against a stub first** — FEATURE — value 5 — effort S — risk low — category: vacuous proofs
  Why: a small model writes tautologies; a criterion that passes on an empty stub proves nothing (assumption: stub runner is cheap).
  Done when: a planted tautological criterion is rejected at plan time, and a real one is accepted only after a recorded failing run.

- **Calibrate the small verifier on planted claims before its verdicts count** — SECURITY — value 4 — effort M — risk low — category: calibration
  Why: the local models (qwen3.8-27b, qwen3.6-35b) are unmeasured as judges; the model bench exists to measure them (T-2886).
  Done when: `sampo louhi models` reports precision/recall on 40 planted true/false claims per model, and a model below 0.9 precision on false claims is barred from labelling anything "verified".

- **Quote-or-unproven: a claim-to-output check by exact quotation** — FEATURE — value 4 — effort S — risk low — category: entailment
  Why: small models judge poorly but quote well. The model must return a substring of the real command output; a script confirms the substring exists (assumption: most claims reduce to "output says X").
  Done when: a verdict without a verbatim, script-confirmed quote is stored as unproven, covered by a test with a fabricated quote.

- **Three-sample vote, disagreement means unproven** — FEATURE — value 4 — effort S — risk low — category: verifier reliability
  Why: small-model verdicts are noisy; local inference is free at volume (user steer on going wild with local models).
  Done when: a claim with split votes is labelled unproven with reason "verifier disagreed", and the vote tally is in the ledger row.

- **Score each criterion by how many wrong implementations it kills** — FEATURE — value 4 — effort M — risk med — category: mutation
  Why: a small model can write cheap wrong variants (off-by-one, swapped branch); a criterion that kills none is weak.
  Done when: each closed task shows a kill rate, and a criterion killing 0 of 5 variants is flagged weak in `sampo task finish`.

- **Scan the rendered site and SVG text for orchestrator and machine names with a small reader** — SECURITY — value 4 — effort M — risk low — category: public surfaces
  Why: the request says public surfaces name roles, not the user's machine or a vendor model; regex catches known strings, a reader catches paraphrases like "the box in the closet" (assumption: paraphrase leaks exist).
  Done when: a planted "jarvis endpoint" caption in a test scene is flagged, and the clean site scans with zero findings.

- **Cap small-model proofs to claim classes that passed calibration** — SECURITY — value 4 — effort S — risk low — category: scope control
  Why: a model good at "output contains" may be bad at "reach" claims; trust should be per class.
  Done when: a verdict from a model on an uncalibrated class is recorded as unproven regardless of its answer.

- **Expire a model-made proof when its judge changes** — FIX — value 3 — effort S — risk low — category: provenance
  Why: model swaps happen (the 3-minute llama-swap switch); stale verdicts would silently outlive their judge.
  Done when: changing the profile's model id flips dependent "verified" rows to "re-check", shown by a test.

- **Wild: Literal-minded newcomer runs the quickstart and logs every guess** — FEATURE — value 4 — effort M — risk low — category: docs (wild)
  Why: a small model with only the README and a scratch home acts like a cold user; each guess it makes marks a doc gap that no checker sees.
  Done when: a run produces a list of guesses, each tied to a README line, and one fixed line removes its guess on re-run.

- **Wild: Predict the output before running it, and score the surprise** — FEATURE — value 3 — effort M — risk low — category: meaning (wild)
  Why: a model that predicts a command's output from the docs alone, then is compared with the real run, turns mismatches into a measured list of wrong doc claims.
  Done when: for 20 documented commands, predictions are stored, diffed against real runs, and mismatches are listed with doc line numbers.

- **Wild: Overnight claim census on idle local hardware** — PERFORMANCE — value 3 — effort M — risk low — category: batch (wild)
  Why: local models cost no tokens, so the full 421-claim shelf can be swept nightly with 3-sample votes and reported as a morning card.
  Done when: a scheduled run finishes in a set window and the morning card shows counts changed since last night.

- **Wild: A prosecutor model attacks every "verified" label** — SECURITY — value 3 — effort M — risk med — category: adversarial (wild)
  Why: a second small model tasked only with finding the cheapest way the proof could pass without the claim being true catches gamed evidence.
  Done when: a planted gameable proof is flagged by the prosecutor and a sound proof is not, in a test of 10 cases.

Next question: Which of the 599 meaning-unproven items can be settled by a run with no model at all, and what share is left for a small model?
Next question: Does the small model's error rate on Sampo's claims track its error on general benchmarks, or must calibration always be local?
