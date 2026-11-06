# Brainstorm — lens: reliability

- **Gate adoption on whole-project holdout** — FEATURE — value 5 — effort M — risk low — category: evaluation
  Why: the pack's rule is "hold out whole projects"; the tier head already fails to beat majority (0.58 vs 0.58), and Sampo's 1,767 briefs dominate the 4,078.
  Done when: `sampo exam model` trains on N-1 projects, scores the held-out one (leave-one-project-out over all 13), and refuses to flip a call site on unless it beats majority and the current decider on every held-out project that has at least 30 briefs.

- **Make every model answer abstain-able** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: intake type reaches 0.73 against 0.595, so about a quarter of answers are wrong. The existing rule/Kev path should take those.
  Done when: the decider returns (label, calibrated confidence); below a threshold fixed on held-out data, `decide()` uses the old path; a test shows the covered subset's accuracy exceeds 0.9, with coverage reported.

- **Keep a per-call-site adoption registry with auto-revert** — FEATURE — value 5 — effort M — risk med — category: serving
  Why: models plug into about 14 sites (decide, intake, playbook, foresight, loop breaker, moonscale judges, and others). The rule is "adopted only where the bench shows it leads".
  Done when: a registry file maps site → model hash → bench score → status. Each Rune generation re-benches it, and a site whose live accept rate falls below the old path's reverts automatically and logs a ledger line.

- **Split by time and dedupe before any training** — FIX — value 4 — effort S — risk low — category: data hygiene
  Why: briefs carry outcomes and "later fixes", which leak labels. Near-duplicate briefs (the moons and genesis tasks) inflate scores. Assumption: the bench's current split is random.
  Done when: the dataset builder splits by close time, drops cosine-similar duplicates (bge-m3 at a stated threshold), and a test fails if any test row's later-fix text appears in the features.

- **Keep a provenance manifest on every training row** — SECURITY — value 5 — effort S — risk low — category: provenance
  Why: Anthropic's terms bar training on Claude outputs, and sensitive projects must stay on the machine.
  Done when: every row records project, source (outcome, ledger, local-model trace or Claude transcript) and an allowed-for-training flag. The builder fails closed on a Claude-text source or an excluded project, and a test plants one of each.

- **Filter distillation by durable success, not green tests** — FIX — value 5 — effort M — risk low — category: data quality
  Why: the uplift runs show closes rising 4→5 with many false-done. A close that held for N days with no later fix or revert is a far cleaner label.
  Done when: the distilled-run set contains only runs with green tests, a held close and no revert. A report shows how many runs the extra filter removes, and a model trained on the filtered set beats one trained on the unfiltered set on the same held-out scenarios.

- **Red-team the local models over the shared text channel** — SECURITY — value 4 — effort M — risk med — category: injection
  Why: the open question is whether the Ward and the funnel's local models can be attacked through the same text. Repo text, briefs and moons all flow into model prompts.
  Done when: a corpus of injected strings (built from real guard refusals in the ledgers) is planted in briefs and file contents, and the classifiers' verdicts on a fixed set are identical with and without them. Any flip fails the gate.

- **Pin and record the serving stack** — FIX — value 4 — effort S — risk low — category: determinism
  Why: the remote endpoint has 2 sessions and a ~3 min model switch, and Ollama's OpenAI API ignored the reasoning-off flags until patched. Silent config drift changes results.
  Done when: every model call logs model hash, quantization, context size, reasoning setting and temperature. The decider calls at temperature 0, and an endpoint timeout falls back to the local or rule path inside a stated bound, tested by killing the endpoint.

- **Make training resumable and VRAM-safe** — FIX — value 3 — effort M — risk med — category: training
  Why: a LoRA on 0.6–4B runs on one 16 GB card that also serves Ollama. Assumption: a training run today can evict served models or die without a checkpoint.
  Done when: a preflight checks free VRAM and refuses to start if it would evict a model in use. Checkpoints are written every N steps, and killing a run then re-running it resumes with an identical final loss curve.

- **Train a loop predictor for Smith** — FEATURE — value 4 — effort M — risk low — category: Smith
  Why: loops end 4 of 10 uplift scenarios, and the current breaker only fires on the third identical action.
  Done when: a small head over the last k actions flags a loop before the third repeat. On recorded journals (74 runs) it catches at least 80% of loops with a false-break rate below 5%, and escalation fires earlier.

- **Run a time-travel backtest of the whole decider (wild)** — FEATURE — value 4 — effort L — risk low — category: evaluation
  Why: assumption: ledgers are timestamped, so each historical decision can be replayed using only data from before it. That gives a live-like accuracy curve over months.
  Done when: `sampo exam backtest` replays the decisions of a chosen quarter and prints rolling accuracy against what was actually chosen. Each Rune generation's model is compared on the same replay.

- **Train an error predictor that routes to escalation (wild)** — FEATURE — value 4 — effort L — risk med — category: routing
  Why: nothing beats majority on tier, but knowing when the model is wrong may still be learnable. That would route uncertain cases to the 27B or to the user's queue.
  Done when: a second head predicts the first model's mistakes on held-out projects with an AUC above 0.7, and routing by it raises the accuracy of the answers actually used.

- **Ship a falsifiable claim with each model, retested nightly (wild)** — FEATURE — value 3 — effort M — risk low — category: model card
  Why: the "adopted only where it leads" rule is only checked at adoption time. A claim like "≥0.73 on intake type for unseen projects" can be rechecked cheaply.
  Done when: each registry entry holds a machine-checkable claim, and a nightly zero-token run re-evaluates it. A failed claim pulls the model from its session path and files a task.

- **Generate canary projects with planted faults (wild)** — FEATURE — value 3 — effort L — risk med — category: genericity
  Why: the user wants generic models, but only 13 real projects exist. A tool-less child that never sees Sampo's code can make fresh small projects in unfamiliar stacks (the exam already uses c, js, ts, python, ruby and rust).
  Done when: a fresh canary project is generated each generation, and a model that does well on the 13 real projects but falls more than a stated margin on the canaries is flagged as overfit to Sampo's habits.

Next question: Which of the 14 call sites has no ledger evidence of the current decider ever being wrong, so a model there gains nothing and only adds risk?
Next question: If a retrained model passes the held-out bench but the user's accept/reject history disagrees with it, which signal wins and who records that choice?
