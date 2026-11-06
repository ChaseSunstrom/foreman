# Brainstorm — lens: invented: proofs a small model can run

- **Compile spec examples into stub-first criteria with a small model** — FEATURE — value 5 — effort M — risk med — category: meaning proofs
  Why: gap "meaning is the largest unproven class (599)"; the ask is spec example assertions becoming runnable criteria at plan time. A local qwen3.8-27b can extract "given X, expect Y" lines into a constrained template (command, input, expected substring/exit code); no free-form code is generated. Every compiled criterion is run against a stub that does nothing and must fail, otherwise it is discarded as vacuous.
  Done when: on a fixture spec with 10 examples, `sampo plan` emits ≥8 criteria, all fail on the empty stub, and the 2 rejected are listed with a reason.

- **Calibrate every small-model verifier before it counts** — FEATURE — value 5 — effort M — risk low — category: verifier trust
  Why: the user steers "weakness-finding uses signals Foreman didn't author"; a small model's verdict is evidence only if it has a measured error rate. Keep a bank of closed tasks with known right/wrong outcomes; each verifier role (claim extractor, entailment checker) gets a held-out accuracy and is labelled "advisory" below a threshold.
  Done when: `sampo louhi verifiers` prints per-role precision/recall on the bank, and a verifier below 0.9 precision cannot flip a claim to "verified".

- **Check entailment of doc claims against captured command output** — FEATURE — value 5 — effort M — risk med — category: doc claims
  Why: "421 docs flag claims no run has checked". Mechanical claims ("`fm doctor` prints N checks") get a command run; the small model only answers a narrow question: does this captured output entail the sentence (yes/no/unclear + quoted span)? A quote that isn't in the output voids the verdict.
  Done when: on 30 planted-true and 30 planted-false doc sentences with outputs, the checker's quoted spans always exist verbatim in the output, and false-accepts are ≤2.

- **Classify the 421 flagged claims by checkability with a small classifier** — FEATURE — value 4 — effort S — risk low — category: doc claims
  Why: before spending any runs, the small model sorts claims into command-checkable, file-checkable, host-behaviour, and opinion; opinion ones are labelled unproven with that reason, not queued. Output feeds the "Unproven shelf grouped by reason".
  Done when: all 421 claims carry a class, and a 40-claim hand-labelled sample agrees ≥85%.

- **Lint public surfaces for role words with a model-assisted rewrite suggestion** — FIX — value 4 — effort S — risk low — category: public surfaces
  Why: request says public surfaces must name models by role and the orchestrator as any agent, never the user's machine or a vendor model. A regex list finds names (jarvis, qwen paths, hostnames, vendor models); the small model only proposes the role-word replacement, which a human or test confirms.
  Done when: `sampo lint public` fails on a planted "jarvis" in README, site, and an SVG's text, and prints a role-worded replacement for each.

- **Kill-rate score for each criterion using model-written wrong implementations** — FEATURE — value 4 — effort M — risk med — category: proof strength
  Why: a criterion that passes on a plausible wrong solution proves little. Ask the small model for 3 plausible-but-wrong patches per task; the criterion earns "strong" only if it fails all that apply cleanly. Cheap, local, and the patches are never merged.
  Done when: `sampo task prove --strength` reports kills/total, and a seeded always-true criterion scores 0/3.

- **Require two-family agreement before "verified" on a judgment-class proof** — FEATURE — value 4 — effort M — risk low — category: verifier trust
  Why: the user's rule favours cold reads by a different model; a single local model echoing the author's own bias is not independence. Two different local model families must both say yes; disagreement renders as "unproven: verifiers split".
  Done when: a test with two stub verifiers that disagree yields the split label, not a pass.

- **Constrained proof-template menu instead of free-form proofs** — FEATURE — value 4 — effort S — risk low — category: small-model reliability
  Why: small models fail at open-ended test writing but do well at filling slots. Offer ~12 templates (exit code, substring, file exists, json path equals, count, ordering, idempotent rerun…); the model picks and fills, and a parser rejects anything outside.
  Done when: a model reply outside the template grammar is rejected, and ≥70% of the 599 meaning gaps map to a template on a sample.

- **Detect stale doc sentences by embedding distance to the code they cite** — PERFORMANCE — value 3 — effort M — risk low — category: doc drift
  Why: the local embedder already planned (qwen3-embedding, bge-m3); cheap zero-generation signal. When the cited file changes and the sentence's nearest-neighbour shifts, flag for re-check instead of re-running everything.
  Done when: editing a cited function flags its doc sentence within one sweep, with unchanged docs flagged at ≤5%.

- **Wild: Dispatch a literal-minded newcomer child over the docs** — FEATURE — value 4 — effort M — risk low — category: wild, doc proofs
  Why: wild. A small model with no repo access follows the README quickstart step by step in a scratch home; every step it must guess or can't perform is filed as an unproven doc claim.
  Done when: running it on the README produces a list of steps with pass/guess/stuck status and files at least one claim on a README with a planted missing step.

- **Wild: Let a prosecutor model attack each "verified" label** — FEATURE — value 3 — effort M — risk med — category: wild, adversarial proof
  Why: wild. A second small model is rewarded only for producing a concrete command or input that makes the verified claim false; a successful counterexample revokes the label and is kept as a regression probe.
  Done when: on a planted weak claim, the prosecutor finds a counterexample and the claim reverts to unproven.

- **Wild: Overnight claim census on idle local hardware** — PERFORMANCE — value 3 — effort M — risk low — category: wild, local-first
  Why: wild. When the machine is idle, a local model works through the unproven shelf at zero token cost, one claim per slot, with results sealed as advisory until calibrated; a morning card shows how many moved from unproven to checked.
  Done when: a scheduled run processes a bounded batch with no network egress and the morning card lists counts by outcome.

- **Round-trip docs through tests** — FEATURE — value 3 — effort M — risk med — category: doc proofs
  Why: a small model writes a one-line test from a doc sentence, and a second model, seeing only the test, writes the sentence back; if the meanings diverge, the sentence is ambiguous and labelled so.
  Done when: a planted ambiguous sentence is flagged and a precise one passes.

Next question: Which verifier roles are small models actually reliable at on Sampo's own bank, and does any role beat a plain regex?
Next question: When a small-model verdict and a real command run disagree, which one has been right historically?
