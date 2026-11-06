# Brainstorm — lens: invented: proofs a small model can run

- **Run a claim-to-probe table before any model sees a doc sentence** — FEATURE — value 4 — effort M — risk low — category: docs proof
  Why: 421 docs flag claims no run has checked; most are file paths, verbs, flags, counts. A regex/`--help`/grep table resolves those at zero tokens, leaving the small model only the residue.
  Done when: `fm` prints, for the 421 flagged claims, a count per resolver (path, verb, flag, number, residue), and the residue is under half.

- **Constrain the small model to a fixed proof-template menu** — FEATURE — value 5 — effort M — risk med — category: meaning
  Why: free-form proof writing by a 27B local model is the failure mode; the request says meaning is the largest unproven class (599). A menu (exit code equals, stdout contains, file exists, json key equals, diff empty) lets it fill slots, not write scripts.
  Done when: given 20 spec examples, the model emits only menu-valid criteria, and a validator rejects anything off-menu.

- **Run each compiled criterion against a stub first and require it to fail** — FEATURE — value 5 — effort M — risk low — category: criteria quality
  Why: spec example assertions become runnable criteria at plan time; a criterion that passes on an empty stub is vacuous. Ideas so far mention mutation and tautology lint, but not stub-first as the gate small-model output must clear.
  Done when: a criterion that passes against a do-nothing stub is refused at filing, with the reason printed.

- **Calibrate the small verifier on planted claims before its verdicts count** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: local models are not authored-by-Sampo-independent signal until measured. Seed 40 true and 40 planted-false doc claims with known answers; record the model's precision per claim class.
  Done when: each verifier verdict carries its class precision, and a class under 90% is auto-labelled unproven.

- **Vote three samples and treat disagreement as unproven** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: small models are noisy, and qwen3.6-35b and qwen3.8-27b are both on hand. Self-consistency is cheap at local volume.
  Done when: a verdict needs 3 of 3 agreement across two profiles, otherwise it prints "unproven: models disagree".

- **Check a claim against real output by quoting, not judging** — FEATURE — value 4 — effort M — risk low — category: entailment
  Why: small models judge badly but extract well. Make it return the exact output line supporting the claim; a string-match step confirms the quote exists in the captured output.
  Done when: any "verified" doc claim stores a quote that appears verbatim in the saved run output; a missing quote downgrades it.

- **Scan the rendered site for role-word leaks with a small reader** — FEATURE — value 3 — effort S — risk low — category: public surfaces
  Why: public surfaces must name roles, never the user's machine or a vendor model; a lint plus a small-model "what is the orchestrator here?" pass catches paraphrases a word list misses (jarvis already slipped once).
  Done when: a planted "jarvis" or vendor name in a scene SVG caption fails the ship gate.

- **Score each criterion by how many wrong implementations it kills** — FEATURE — value 4 — effort L — risk med — category: criterion strength
  Why: the small model writes cheap wrong implementations of a spec example at volume; a criterion that kills none is weak.
  Done when: each filed criterion shows "killed 7/8 mutants", and 0/8 blocks filing.

- **Wild: Have a literal-minded small model run the quickstart and log every guess** — FEATURE — value 4 — effort M — risk low — category: docs proof
  Why: wild. A weak model is a good proxy for a newcomer; each point where it improvises is a doc gap, found overnight on idle local hardware at no token cost.
  Done when: the run emits a list of steps where it deviated from the text, and fixing them drops the count on rerun.

- **Wild: Let a prosecutor model attack every "verified" label overnight** — SECURITY — value 4 — effort M — risk med — category: adversarial
  Why: wild. A second small model is rewarded only for a counterexample input; a success flips the label to unproven with the input stored. Gaming is bounded because a counterexample must reproduce by command.
  Done when: a planted false "verified" claim is flipped within one overnight pass.

- **Wild: Predict the output before running it, and score the surprise** — FEATURE — value 3 — effort M — risk low — category: meaning
  Why: wild. The small model writes the expected output of a criterion from the spec alone; the real run is diffed. Agreement is evidence the spec means what the criterion says, mismatch is a spec-or-code conflict to show the user.
  Done when: a spec example whose prediction differs from the output is listed as "spec/code conflict", not as a pass or fail.

- **Expire a model-made proof when its judge changes** — CLEAN — value 3 — effort S — risk low — category: provenance
  Why: verdicts from a small model are only as stable as the model and prompt; the ledger lacks the model id and prompt hash on each.
  Done when: swapping the profile marks every verdict from the old one "stale, re-run", visible in the unproven shelf.

- **Cap small-model proofs to the claim classes the calibration passed** — SECURITY — value 4 — effort S — risk low — category: trust
  Why: pairs with calibration; without the cap, a weak class quietly counts as proven.
  Done when: a verdict outside a passed class is rejected at write time with the class named.

Next question: Which of the 599 meaning-class claims are checkable by a menu template at all, and what share needs the user's eyes?
Next question: Does a 27B local model's calibrated precision on doc claims beat a plain regex table, or is the model adding cost without gain?
