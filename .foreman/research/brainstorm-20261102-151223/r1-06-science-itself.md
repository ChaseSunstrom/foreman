# Brainstorm — lens: science itself

- **Preregister every brief's proof before the first edit** — FEATURE — value 4 — effort M — risk low — category: proof
  Tier: high. Domain: science (registered reports). Becomes: the proof command and pass criterion are hash-locked at task open. A later edit to either is logged as HARKing and graded below "strong".
  Why: the pack says `fm task prove` shows a test failing without the change, and the stored grade (verified: strong) feeds digests. Nothing shows the proof being locked before the work. Prior art: registered reports; none found in agent harnesses (assumption).
  Done when: editing a brief's proof command after the first diff makes the close grade "post-hoc" and `fm doctor` lists it.

- **Run a null-distribution check on every proof** — FEATURE — value 4 — effort M — risk med — category: proof
  Tier: high. Domain: statistics (negative controls). Becomes: `fm prove --null` runs the proof against several random mutants of the touched code. A proof that passes on all of them is flagged as weak.
  Why: T-2583-style grading counts proofs but never asks whether a proof can fail at all. The `--perf` proof ask (c18) shares the gap. Prior art: mutation testing. Cheapest experiment: run it on 20 closed tasks and see how many proofs survive every mutant.
  Done when: a planted vacuous proof (`true`) is graded "uninformative" and a real test is not.

- **Replicate closed tasks with an independent agent** — FEATURE — value 5 — effort L — risk med — category: verification
  Tier: xhigh. Domain: science (replication crisis). Becomes: a sampled share of closed tasks is re-run from the brief alone in a fresh worktree by a different model. Divergence from the original diff or proof result lands in a replication rate on `fm doctor`.
  Why: the closing agent is the only witness to its own work. Builder lanes in worktrees and `fm drill --restore` already provide the machinery. Prior art: Many Labs. Cheapest experiment: replicate 10 closed tasks by hand and measure agreement.
  Done when: `fm doctor` shows "replicated N/M, agree X%", and a planted flawed close fails replication.

- **Randomize Foreman's own rule changes into trials** — FEATURE — value 5 — effort L — risk med — category: self-measurement
  Tier: xhigh. Domain: clinical trials. Becomes: `fm trial` assigns guard, prompt or skill variants to lanes at random, with a pre-stated outcome (close rate, cost per close, rework). It reports an effect size with an interval, not an anecdote.
  Why: calibration of its own bets exists, but the pack's backlog is all "add X" with no controlled comparison, and the unanswered question about guard false-positive cost needs a control arm. Prior art: feature flags and A/B testing, but not on the agent's own rules.
  Done when: a two-arm trial of a toggled rule completes and prints an interval, and a no-effect rule is reported as "no detectable difference".

- **Keep a negative-results journal the planner reads first** — FEATURE — value 4 — effort M — risk low — category: memory
  Tier: medium. Domain: the file-drawer problem. Becomes: each dropped or failed approach is stored with its reason, and `fm task new` surfaces near-matches before work starts.
  Why: the user's dropped list (guard --dry-run, tidy --verbs) already shows ideas being re-proposed and re-grounded, and T-2659 added grounding checks by hand. Prior art: `fm replay` and the lessons store partly cover it.
  Done when: re-proposing a dropped idea prints the earlier drop reason at intake.

- **Blind the reviewer to the author's claims** — FEATURE — value 3 — effort S — risk low — category: review
  Tier: low. Domain: blinded review. Becomes: the review agent gets the diff and the brief but not the closing agent's summary, then the two verdicts are compared.
  Why: assumption: reviewers anchor on the author's narrative. Cheapest experiment: blind 10 reviews and count the new findings.
  Done when: the review record shows a blind verdict next to the unblinded one.

- **Stage adversarial collaborations for disputed decisions** — FEATURE — value 4 — effort M — risk med — category: coordination
  Tier: xhigh. Domain: science (Kahneman and Klein). Becomes: when two agents or tiers disagree, each states a prediction. They design the cheapest discriminating test together, run it, and the result settles the dispute.
  Why: the pack's "approaches" disputes (re-grounded to S, dropped as "mostly built") are settled by assertion. Crossbreed parents: this idea plus the trials idea above.
  Done when: a seeded disagreement ends in a run test and a recorded winner.

- **Put error bars and a calibration phantom on every gauge** — FIX — value 3 — effort M — risk low — category: measurement
  Tier: medium. Domain: metrology. Becomes: each gauge reports a value with its known error. A fixture repo with known truth (`tests/fixtures/instruments` already exists) is measured on a schedule to catch drift.
  Why: fm burden missed hook_success stdout (T-2667), so the gauge was wrong and no one knew. Prior art: the c17 cross-check, which was dropped as low value.
  Done when: a planted undercount in `fm burden` is caught by the phantom run.

- **Wild: Detect paradigm shifts from accumulated anomalies** — FEATURE — value 4 — effort L — risk med — category: self-repair
  Tier: xhigh. Domain: Kuhn. Becomes: unexplained events (guard overrides, flaky tests, rework, abstains) are tallied against the model of how Foreman works. When anomalies cross a threshold, it proposes replacing a mechanism, not patching it again.
  Why: the missed-asks list shows the same class repeating. Cheapest experiment: tag 3 months of history by hand and see whether clusters appear.
  Done when: a seeded cluster of 10 anomalies produces a "redesign X" proposal.

- **Wild: Estimate causal effects of past features by synthetic control** — FEATURE — value 4 — effort L — risk high — category: simulation
  Tier: extreme. Domain: econometrics. Becomes: the ledger is treated as a natural experiment. For each shipped feature, Foreman builds a counterfactual from unaffected periods and projects what the metrics would have been. It answers "did the guard pack earn its cost?".
  Why: assumption: ledger history is long enough, and confounds are modelable. Cheapest experiment: apply it to one feature with a known before/after jump.
  Done when: it recovers a planted effect of known size within a stated interval.

- **Wild: Publish Genesis generations as peer-reviewed papers with a citation graph** — FEATURE — value 3 — effort M — risk low — category: tower
  Tier: high. Domain: scholarly publishing. Becomes: each moonshot is a short paper (claim, method, cheapest experiment, result). Cold-read reviewers write rebuttable reviews. Accepted ideas get IDs, and citations show which ideas built on which.
  Why: the tower's cold reads and the site's `genesis/` page already exist. Rebuttal rounds force falsification, not enthusiasm.
  Done when: the Genesis page lists each idea with its review verdicts and its parents.

- **Wild: Pool effect sizes across consenting users' projects as a meta-analysis** — FEATURE — value 4 — effort L — risk high — category: privacy, learning
  Tier: massive. Domain: meta-analysis. Becomes: opt-in, anonymized effect sizes (not code) on practices such as plan-first and proof grades, merged into shared priors for new installs.
  Why: assumption: users will share numbers if nothing else leaves their machine. It must default to off and stay local-first. Cheapest experiment: two volunteer homes exchange one metric file.
  Done when: nothing is sent without an explicit setting, and the shipped file contains only aggregate numbers.

- **Require a cheapest falsifying experiment for every tower idea, and run it unattended** — FEATURE — value 5 — effort M — risk med — category: tower
  Tier: high. Domain: Popper. Becomes: Genesis refuses an idea without a runnable kill test, then runs the test in a lane and records "survived" or "refuted" in the calibration store.
  Why: MOONSHOT asks for this experiment per idea, yet the pack shows ideas still being dropped only after grounding by hand.
  Done when: a seeded false idea is refuted by its own experiment with no human step.

Next question: Which of Foreman's own claims (close rate, "strong" grades, calibration) has never been checked by anyone other than Foreman?
Next question: How many tasks does a trial need before an effect is distinguishable from noise at this user's volume?
