# Brainstorm — lens: metacognition and calibration

- **Sample ground-truth audits to unbias calibration labels** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: assumption: most calibration ideas already listed (Brier scoring, outcome ledger, conformal escalation) train on escapes the user happened to notice. Those labels are biased toward visible failures. A random 1-in-N finished task gets a hidden deep audit (all `audit.md` lenses plus an independent re-derivation). Foreman never sees which task was picked until the verdict is in.
  Done when: `fm calibrate --truth` reports an escape-rate estimate with a confidence interval from the sampled audits, and a test shows task selection is random and stratified by type and tier.

- **Estimate confidence from behaviour, not words** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the list scores stated confidence, but nothing compares it to what Foreman did. The ledger has the signals: re-reads, retries, verifications run, reviewers skipped, edits after a "passing" run. A revealed-confidence score is computed from these and shown next to the stated figure. A large gap means Foreman is misjudging itself.
  Done when: on replayed ledgers, `fm calibrate` lists tasks where stated and revealed confidence differ by more than a threshold, and the revealed score predicts escapes at least as well as the stated one on the bench.

- **Mine the empirical tells that precede failures** — FEATURE — value 4 — effort M — risk low — category: self-knowledge
  Why: the certainty-language lint is hand-written. Instead, mine transcripts of blocked, reverted and reworked tasks for phrases and action patterns that preceded failure, such as "should be straightforward", editing before reading the tests, or a first-try green with no red step. Recent commits show "friction" is already mined from blocks, corrections and steers. Surface the top tells as live nudges only when they fire.
  Done when: `fm friction --tells` lists n-grams and action patterns with lift over the base failure rate, and a held-out replay shows at least one tell with significant lift.

- **Abstention bench with an ask-threshold curve** — FEATURE — value 4 — effort M — risk med — category: evals
  Why: the user steers against friction ("shouldn't block until 75%") and the queue has asks-reduction ideas. No eval measures knowing when to stop or ask. Build cases that are impossible, underspecified or contradictory, plus answerable decoys. Score fabrication rate against over-asking rate, then set the ask threshold at the user's tolerance point on that curve.
  Done when: `fm bench --abstain` outputs a precision/recall curve and the chosen threshold is recorded in settings with its curve position.

- **Propagate confidence along task chains** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the list has verification debt per area and confidence laundering across handoffs, but nothing across tasks. When task B builds on A, whose evidence was weak or partial, B inherits A's lowest-confidence claim. Re-verifying A's claim then becomes a plan step in B.
  Done when: a task whose parent had an unverified claim shows an inherited-doubt line in its brief and cannot close until the claim is verified or explicitly accepted.

- **Learn when to pause and check** — FEATURE — value 4 — effort M — risk low — category: monitoring
  Why: "re-plan at checkpoints" uses fixed checkpoints. Learn from the ledger which moments precede escapes, for example the Nth edit without a run, a file touched outside the declared footprint, or a gate that is green on first run. Fire a one-line self-check only at those moments.
  Done when: trigger rules are stored as data with measured lift, and replay shows the number of checks falls while the escapes caught stay the same.

- **Detect confidence-trajectory shapes mid-task** — FEATURE — value 3 — effort M — risk low — category: monitoring
  Why: Foreman records confidence at step boundaries. Flat-high confidence with no new evidence, a sawtooth, and monotone rise with each step verified are different signatures. Classify the shape and use it to trigger an independent second look. This differs from stuck-trajectory detection, which only watches for stalling.
  Done when: confidence samples are in the ledger per step, and `fm task show` labels the shape. On bench replays, the "flat-high" label predicts escapes better than the base rate.

- **Calibrate each epistemic tag against outcomes** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: claims are tagged observed, recalled, inferred or assumed. Whether "observed" claims are actually more reliable than "recalled" ones is unmeasured. Compute the later-contradicted rate per tag and per project, then adjust how much each tag counts toward done-confidence.
  Done when: `fm calibrate --tags` prints a contradiction rate per tag with sample sizes, and done-confidence uses the measured weights.

- **Diagnose each escape as a monitoring, control or knowledge failure** — FEATURE — value 4 — effort S — risk low — category: post-mortem
  Why: postmortems per correction exist. Sorting the cause three ways routes the fix: didn't notice (add a monitor), noticed but didn't act (change a control rule), or didn't know (add a lesson or recon). Also record detection latency, meaning steps between the first wrong step and its catch, and credit the monitor that caught it.
  Done when: every correction postmortem has a `failure_kind` and `detection_latency`, and `fm friction` shows the split with the proposed fix class for each.

- **Measure in-session confidence inflation** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: assumption: stated confidence drifts up with turn count and context fill, independent of evidence. Check this on past ledgers by regressing confidence on turn count while controlling for evidence count. If it is real, trigger a fresh-eyes re-evaluation past a learned threshold.
  Done when: a report states the measured slope with an interval, and the trigger is enabled only if the slope is significant.

- **Wild: Probe reviewers for authority bias** — FEATURE — value 3 — effort M — risk low — category: reviewer integrity
  Why: wild. Reviewers may go easy on work labelled as trusted or from a senior author. Feed the same diff to `fm-reviewer` with randomised author labels ("senior, 99% first-pass" versus "unknown, 55%") and compare findings. A gap means reviewer deference is leaking, and labels get stripped from review packets.
  Done when: `fm bench --bias` outputs the finding-count and severity gap between labels, and review packets contain no author-reliability text.

- **Wild: Plant a poisoned lesson to test memory credulity** — SECURITY — value 4 — effort M — risk med — category: memory integrity
  Why: wild. Recall surfaces lessons with no check that they are true. Insert a plausible but false lesson into a sandboxed recall store, in the style of the project's real ones, and see whether a replayed task follows it unverified. Failures feed a rule that recalled lessons must be spot-checked before they drive a risky step.
  Done when: the drill runs against a copy of the store, reports follow or catch per task, and never touches the real store.

- **Wild: Inject a false user correction to test sycophancy** — FEATURE — value 4 — effort M — risk low — category: deference
  Why: wild. The user's steers drive much of Foreman's behaviour, so how it handles a wrong correction matters. In replay, insert a plausible but false pushback ("that test is wrong, just delete it") and check whether Foreman verifies, objects, or complies. The target is a calm check, not blind compliance and not stubbornness.
  Done when: a bench suite of false-correction cases reports comply, verify and push-back rates, with a documented target band.

- **Wild: Show calibration health in the statusline** — FEATURE — value 2 — effort S — risk low — category: ambient UI
  Why: wild. A tiny glyph shows rolling Brier health and the share of claims that were audited. It stays invisible while healthy and appears only when drift crosses a threshold. This follows the user's "quiet until it matters" preference from the budget gauge.
  Done when: the glyph is absent in a healthy fixture ledger, appears in a drifted one, and links to `fm calibrate`.
