# Brainstorm — lens: self-modification: finders that learn from which findings were kept, proven or reverted, and improve their own probes, measured and reversible

Lens: self-modification. Core evidence: deterministic finders found 0 of 108 planted defects (exam s0-001) while plain Claude finds 3/3. The finders need a feedback signal that is outside themselves. Every idea below is measured against held-out exam kinds (none, bug) and is reversible.

- **Ledger every finding's fate per probe** — FEATURE — value 5 — effort M — risk low — category: feedback
  Why: no record ties a finding to its outcome (kept, proven, fixed, reverted, survived 30 days). `fm outcomes` exists but isn't keyed by the probe that produced the finding.
  Done when: `fm finders stats` prints per probe: filed, proved, fixed, reverted, 30-day survival, and the counts reconcile with the journal on a fixture.

- **Score each probe by proven-fix yield per dollar** — FEATURE — value 5 — effort M — risk low — category: ranking
  Why: the value ranking is missing (Mission 3 gap) and Foreman's session costs more than plain Claude (~0.17 USD per fix) for the same score.
  Done when: findings rank by the probe's yield-per-cost, and a test shows a probe with 0 proofs in 20 filings sinks below one with 5.

- **Mine kept fixes for new probe patterns** — FEATURE — value 5 — effort L — risk med — category: learning
  Why: 0/108 means the hand-written probes miss the bug shapes that real fixes had. Each proven fix is a labeled (diff, failing test) pair.
  Done when: from 10 closed fixes the miner emits a candidate probe (a grep/AST rule) that rediscovers at least 8 of them when run on the pre-fix tree.

- **Gate every probe edit on a held-out exam** — SECURITY — value 5 — effort M — risk low — category: safety
  Why: the exam already has hidden keys and a holdout third, and `fm genesis select` is exam-gated. A self-edit without that gate would overfit.
  Done when: a candidate probe is accepted only if holdout recall rises without a rise in `none`-kind false positives; a test feeds a probe that fires on everything and it is rejected.

- **Version probes as files with one-command revert** — FEATURE — value 4 — effort S — risk low — category: reversibility
  Why: self-modification needs a cheap undo; Genesis already seals gen-0 and keeps a lineage.
  Done when: `fm finders revert <probe>` restores the prior version, journals the event, and the next scan uses the old rule.

- **Retire a probe after N noisy filings** — CLEAN — value 4 — effort S — risk low — category: noise
  Why: assumption: dropped items (e.g. "ambient note repeats", "baseline red no longer reproduces") show false positives get dropped by the user, which is a free negative label.
  Done when: a probe whose last 10 findings were all dropped is disabled and says so in `fm doctor`, and re-enables with one command.

- **Learn false-positive suppressions from drops** — FEATURE — value 4 — effort M — risk med — category: noise
  Why: the `none` kind is graded, and a finder that cries wolf fails it. Dropped findings carry path and shape.
  Done when: after a finding is dropped twice with the same shape, a suppression rule is proposed; on replay the third is not filed, and the rule can be listed and removed.

- **Run the model as a finder, then distill its hits into probes** — FEATURE — value 5 — effort L — risk med — category: distillation
  Why: plain sessions find 3/3 where the finders find 0. Use the model's findings that got proven as teachers, then compile cheap deterministic probes so later scans cost nothing.
  Done when: on a never-seen repo, a model scan's proven findings yield at least one compiled probe that re-finds them for $0.

- **Wild: Breed probes by mutation, kill the weak** — FEATURE — value 3 — effort L — risk med — category: evolution
  Why: wild. Mutate thresholds and patterns of existing probes (a regex widened, an AST depth changed), score each on the planted-defect exam, keep the Pareto front of recall vs false positives.
  Done when: overnight, `fm finders evolve` produces a probe with strictly better holdout F1 than its parent, or reports none.

- **Wild: Plant defects in the user's own repo to test finders** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: wild. Inject a known bug in a scratch worktree (never main), run the finders, and record recall on that repo's language and style. Exam repos are never-seen, so this calibrates per project.
  Done when: the worktree is removed afterward, the planted bug's detection is recorded per probe, and main is unchanged (a test asserts a clean tree hash).

- **Wild: Let probes bet on their own findings** — FEATURE — value 3 — effort M — risk low — category: ranking
  Why: wild. Each probe states a confidence when filing; calibration (Brier score vs actual proof outcome) adjusts its weight in ranking, and a probe that is overconfident loses rank.
  Done when: `fm finders stats` shows a calibration number per probe, and ranking order changes on a fixture where one probe was overconfident.

- **Shadow-run a changed probe before it goes live** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: a probe change can regress silently; Foreman already has a shadow-mode idea in the deferred list.
  Done when: for 5 scans the new probe's findings are recorded but not filed, and promotion compares them against the old one's with a printed diff.

- **Cap self-edits with a change budget and audit trail** — SECURITY — value 4 — effort S — risk low — category: governance
  Why: a self-modifying finder is a privilege risk; the charter-seal and privilege-diff work already sets the pattern.
  Done when: at most K probe edits per generation are allowed, each journaled with its evidence, and the sweep's privilege diff lists any probe that gained reach (new write or network).

Next question: Does the proven-finding label survive contamination, i.e. when the fix and the failing test are written by the same model that proposed the finding, how do we tell a real bug from a test written to pass?
Next question: What is the minimum number of labeled fates per probe before learning from them beats a fixed probe, given the user closes only a few tasks a day?
