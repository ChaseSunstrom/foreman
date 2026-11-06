# Brainstorm — lens: reliability

- **Make the decider fail loud with a named cause** — FIX — value 5 — effort M — risk low — category: reliability
  Why: the whole request is a model in the path of every Rune generation; a silent crash or a malformed JSON from the 0.6B head would quietly revert to rules with no trace. The pack shows this exact class of failure: T-2912's "silent-cut scan" and the `build.py` crash on `wild null` (unrated moon) — null fields already break consumers of the tower. Every model slot must emit a typed verdict or an explicit `abstain|error:<code>`, and `sampo doctor` names the last model failure.
  Done when: kill the endpoint mid-`sampo next` and the next command prints `decider: unavailable (endpoint down), used rules` plus a ledger line; no stack trace, no silent rule-use.

- **Rebuild the decider from its on-disk ledger alone** — FEATURE — value 5 — effort M — risk med — category: recovery
  Why: "how it is trained and served on this box" implies state; the standing rules (kill-safe writers, T-2967 undo, `sampo prune`) show the user lives on rebuildable state. If a corrupt `model.bin` or a botched retrain lands, the user needs one command, not a re-run of the whole stack.
  Done when: on a scratch home, delete the model artifact and run `sampo model rebuild`; the decider serves, and its next ten verdicts match the last run's recorded verdicts on the same inputs.

- **Pin weights, embeddings and serving by content hash** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: the request asks how it is "served on this box" and "improves every Rune generation" — a silently swapped 4B weight or a changed bge-m3 index would shift every decision with no diff to blame. The pack already pins model ids and the rename guard shows the user cares about identity. `sampo model pin` records digests; a serve with a mismatched hash refuses.
  Done when: replace the 0.6B weights with another build of the same id; `sampo next` refuses the slot and names the digest mismatch in the ledger.

- **Hold the model out of the guard's path** — SECURITY — value 5 — effort S — risk med — category: safety
  Why: earlier ideas float a "Ward classifier" and a "user twin." A small model deciding what a command is allowed to do is the single worst reliability and safety move: it is the one slot where being silently wrong is catastrophic, and the standing rules never grant a model authority over the Ward. Keep the Ward rule-based; the model may only *tighten* and only after an adversarial test, never relax.
  Done when: `sampo doctor` asserts the Ward's decision function contains no model call; a planted prompt trying to loosen a rule changes nothing.

- **Shadow the decider until it beats the rules on holdout** — FEATURE — value 4 — effort M — risk low — category: adoption
  Why: the user's own words: "we will want it to be a generic model… maybe brainstorm on features the model should have." Adoption must be earned, and the steers already demand free-arm vs session-arm comparison and a "free arm beats the session arm = top gap" rule. Run the new model in shadow on every real decision for a generation, logging model-vs-rules-vs-outcome, and promote a slot only on a leave-one-project-out margin.
  Done when: `sampo model shadow` shows, per slot, a 14-day table where the model's shadow verdict is compared to the rule's verdict and to the 14-day close-survival outcome; no slot auto-activates.

- **One retrain is idempotent, resumable and VRAM-fenced** — CLEAN — value 4 — effort M — risk low — category: process
  Why: "how it is trained" on a shared box where the moons funnel and Ollama also run. The pack shows the GPU-contention class (funnel judged one-at-a-time while the endpoint serves 2; PERF's CPU cap). A training job must yield, resume after a kill, and never OOM the box.
  Done when: start a retrain, SIGKILL it mid-epoch, restart; it resumes from the last checkpoint and completes with identical weights (within tolerance), and the endpoint's p99 is unchanged during the run.

- **Label by outcome, with the negative label coming from the user's own undo** — FEATURE — value 5 — effort M — risk med — category: data
  Why: the request's real ask is "a better decider," and a decider trained only on green closes learns what *passes*, not what *holds*. The steers already define "done-and-held versus reverted or later-fixed" as the label, and "treat the user's silence as a label." Mine regret from later fixes and from the user's manual undos as the negative class, so the model learns the user's actual bar.
  Done when: the training table contains a row per closed brief with a `held|reverted|later-fixed` label derived from git, and at least one model head is trained on the `later-fixed` negatives and scores them in the bench.

- **Strip names and provenance before any row leaves the machine** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: "generic across every project" means the corpus will contain other repos, users and machines. The pack has a whole privacy lens and the steer "train only on text the user or a tool wrote, never on repo or web content." A provenance manifest per row, plus a redaction pass that fails the build on a planted canary, is the only safe way to make it generic.
  Done when: plant a canary string in a training row; the redaction pass refuses to emit the table and names the canary, and the emitted table carries a per-row provenance tag.

- **Canary-probe the serving stack at session start, silently unless it fails** — PERFORMANCE — value 3 — effort S — risk low — category: liveness
  Why: a dead Ollama or a hung 27B would make every `sampo next` hang or silently fall back. The pack already has the Ward canary concept and "probe each model's quirks at install." A 5 ms golden-prompt probe per resident model at SessionStart, cached, with a stale flag, makes liveness a fact not an assumption.
  Done when: stop Ollama before a session starts; SessionStart shows `4b: stale (last ok 03:12)` and the decider uses rules without prompting.

- **Record every model call as a replayable ledger line** — FEATURE — value 4 — effort S — risk low — category: audit
  Why: "how it is measured" and "how it improves every Rune generation" both require that a decision be re-runnable. The standing rules lean on ledgers as the source of truth, and the exam recall rule wants per-language reporting. Each call stores input hash, weights digest, verdict, latency and the outcome it was graded against.
  Done when: `sampo model replay <row-id>` re-derives the same verdict from the stored inputs and weights, and the output diffs to zero.

- **wild: Give the decider a "I don't know, here's why" and a confidence the user can veto** — FIX — value 4 — effort M — risk low — category: wild
  Why: the user's words keep circling trust and control ("maybe brainstorm on features the model should have"). The most reliable model is the one that says so. A calibrated abstain with a one-line reason, surfaced in the close line, and a per-project "no model" switch that *actually* changes behaviour (not just a flag) is the feature the user will show others.
  Done when: on a brief the model is unsure about, `sampo next` prints `decider: abstain — "no closed brief like this in <project>` and `sampo model off` makes the next run use only rules, verified by the ledger showing zero model calls.

- **wild: Dream the decider's mistakes overnight: replay yesterday's close decisions against the model and file the regrets** — FEATURE — value 3 — effort M — risk med — category: wild
  Why: "how it improves every Rune generation" needs a loop, not a one-shot. An idle-GPU night job that re-runs the day's decisions through the model, flags the ones the user later overrode or that reverted, and files them as new training rows with a "regret" label turns every bad call into data — and the morning card shows "model saved you 3, cost you 1."
  Done when: after a night run, the ledger has new regret rows tagged from the user's own overrides, and the morning card prints the saved/cost count for the slot.

- **wild: A frozen "museum" decider as a permanent tripwire** — FEATURE — value 3 — effort S — risk med — category: wild
  Why: every retrain risks silent drift. Keep one immutable copy of the first good model on disk, always in shadow, and alarm the moment its verdicts and the current model's diverge beyond a threshold — that divergence is the earliest signal that retraining or a weight swap broke something. It is cheap, it is the only thing that catches "the new model is quietly wrong," and it is the single most reliable watchdog a small-model slot can have.
  Done when: `sampo model tripwire` prints, per slot, the agreement rate between the museum model and the live model over the last 7 days, and a drop below the threshold files a task.

- **wild: Let the user's undo be the only label, and the model's job be to predict it** — CLEAN — value 4 — effort M — risk high — category: wild
  Why: the steers already say "treat the user's silence as a label" and "use the user's own undo as the only label." Take it to the end: instead of training on green closes, train the decider *specifically* to predict "will the user undo this?" That is the real, felt reliability question, and it is what the user actually experiences. It reframes the whole decider around the user's taste rather than test-passing.
  Done when: the bench reports "undo-prediction AUC" per project, and the decider's abstain threshold is set from the user's own override rate, not a fixed 0.5.

Next question: What is the user's acceptable latency budget for a model verdict in the `sampo next` path, and is a >500 ms decider acceptable or must it be a background pre-computation?
Next question: Does the user want the decider to *change* what Sampo does (route, retry, skip), or only to *advise* (show a score, pre-rank) — the blast radius of a wrong decision depends entirely on that answer.
