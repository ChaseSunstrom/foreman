# Brainstorm — lens: science itself

- **Debug by hypothesis tree** — FEATURE — value 5 — effort L — risk med — category: debugging
  Why: assumption: failed or slow-to-close tasks come from agents guessing at causes. Tier guess: xhigh. Domain: scientific method. Prior art: scattered "scientific debugging" prompts and git bisect, but no harness keeps a ranked, evidence-weighted list of causes. Cheapest experiment: replay 20 past bug tasks and see whether the tree's top-ranked cause beats first-guess fixes on edits to close.
  Done when: `fm debug T-x` writes causes with priors, a falsifying command for each and posteriors updated from the results, and a fixture bug closes with a proof that names the cause that survived.

- **Retract lessons by cascade** — FEATURE — value 4 — effort M — risk low — category: provenance
  Why: assumption: lessons and guard rules derive from tasks that can later be shown wrong (reverted, flaky proof). Tier guess: high. Domain: scientific retraction and citation. Prior art: none found for agent lessons. Cheapest experiment: link 30 existing lessons to their source tasks and count how many sources were later reverted.
  Done when: marking a task retracted flags every lesson or rule citing it as "suspect" in `fm doctor` and the planner stops using them until re-verified.

- **Correct for multiple comparisons** — FIX — value 4 — effort M — risk low — category: measurement
  Why: the pack lists many deciders, doctor rows and proposed A/B trials, and each is a separate test; with no false-discovery control some "effective" lessons are noise. Tier guess: medium. Domain: statistics. Prior art: Benjamini-Hochberg; none found in harnesses. Cheapest experiment: apply it to the last 100 promoted lessons and count how many fall out.
  Done when: promotion of a lesson or rule from a trial needs a q-value under a set bar, and a planted-noise fixture with 50 null trials promotes at most the expected fraction.

- **Reproduce any landed task from a manifest** — FEATURE — value 4 — effort M — risk low — category: reproducibility
  Why: assumption: proofs pass at close but nobody re-runs them later, so bit rot goes unseen. Tier guess: high. Domain: reproducible research. Prior art: CI reruns, Nix and Docker, but not tied to a task's evidence. Cheapest experiment: rerun 20 old proofs in clean worktrees and count failures.
  Done when: `fm reproduce T-x` rebuilds the tree, reruns the recorded proof command in a clean worktree and reports match or drift with the diverging output.

- **Detect forking paths in proofs** — SECURITY — value 4 — effort M — risk med — category: proof integrity
  Why: assumption: an agent that sees its proof go red can edit the proof until it goes green. Tier guess: medium. Domain: p-hacking and researcher degrees of freedom. Prior art: no tool found that counts proof edits after the first red. Cheapest experiment: scan the ledger for tasks whose proof command or test changed after a failed run.
  Done when: closes record the count of proof edits after the first failure, and a fixture that weakens its assertion mid-task is graded weak.

- **Run a standing assay on a seeded-bug repo** — FEATURE — value 4 — effort M — risk low — category: evaluation
  Why: the pack has fixtures and a calibration-phantom idea, but nothing says Foreman's own detection and fix rate is tracked per version. Tier guess: high. Domain: positive controls and model organisms. Prior art: SWE-bench style suites; none a user runs on their own harness change. Cheapest experiment: seed 15 bugs, run once, record the rate.
  Done when: each release adds a row of catch and fix rate on the assay, and a deliberately broken gate drops it visibly.

- **Flag Simpson's paradox in digests** — FIX — value 3 — effort M — risk low — category: observability
  Why: assumption: digests compare outcomes across model, task type and repo, and mixes shift over time. Tier guess: low. Domain: confounding. Prior art: none found in harness dashboards. Cheapest experiment: split a month of closes by type and check whether any aggregate trend reverses.
  Done when: a digest line warns when an aggregate trend reverses in the stratified view, tested on a constructed reversal.

- **Stamp the instrument version on every series** — FIX — value 3 — effort S — risk low — category: measurement
  Why: the user asked for a single clock and boundary tests for readers, so metric definitions do change. Tier guess: low. Domain: measurement invariance. Prior art: changepoint detection; none tied to code versions. Cheapest experiment: grep metrics whose formula changed in the last 30 commits.
  Done when: `fm doctor` marks a break in any series where the producing code changed, instead of drawing one line through it.

- **Chart dose-response curves for the knobs** — FEATURE — value 3 — effort M — risk low — category: tuning
  Why: assumption: budgets, context size and retries are set by feel. Tier guess: medium. Domain: pharmacology. Prior art: hyperparameter sweeps; none for harness settings. Cheapest experiment: sweep one budget over four levels on assay tasks.
  Done when: `fm tune` outputs close rate and cost per level and names the knee.

- **Add a limitations line to every receipt** (wild) — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: assumption: receipts report what was proven, not what wasn't looked at. Tier guess: medium. Domain: papers' limitations sections. Prior art: none found. Cheapest experiment: hand-write limitations for five receipts and ask whether the user would have acted differently.
  Done when: each receipt lists unmeasured areas (untested paths, unrun gates, skipped backends) in one line.

- **Measure brief ambiguity by many analysts** (wild) — FEATURE — value 4 — effort L — risk med — category: planning
  Why: assumption: vague briefs waste the most spend. Tier guess: xhigh. Domain: many-analysts studies. Prior art: self-consistency sampling; none used to price a brief. Cheapest experiment: run three cheap plans per brief and check whether disagreement predicts later rework.
  Done when: `fm plan --spread` reports plan disagreement and the queue defers briefs above a threshold for the user to clarify.

- **Run ring tests across harnesses** (wild) — FEATURE — value 3 — effort L — risk low — category: benchmarking
  Why: Foreman fronts Claude Code, Codex, Gemini CLI and opencode, so it can send identical tasks to each. Tier guess: high. Domain: interlaboratory round robins. Prior art: public leaderboards, not private per-repo ones. Cheapest experiment: send five tasks to two backends and compare proof outcomes.
  Done when: a table shows each backend's verified close rate and cost on the user's own repo.

- **Infer unseen work from ledger residuals** (wild) — FEATURE — value 3 — effort M — risk med — category: observability
  Why: assumption: edits made by hand, in IDEs or cron never reach the ledger. Tier guess: high. Domain: dark-matter inference. Prior art: none found. Cheapest experiment: diff git history against ledger-landed lines and count untracked changes.
  Done when: `fm doctor` reports the share of commits with no ledger record and the paths they touch.

Next question: which of Foreman's claims about itself (lessons, rules, gauges) has never been re-tested since it was first accepted?
Next question: where does the user's own judgment act as an uncontrolled variable in Foreman's measured outcomes?
