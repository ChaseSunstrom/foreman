# Brainstorm — lens: reliability

Lens: reliability. Prior ideas covered abstain, registry/rollback, shadow mode, LOPO bench, provenance and loop prediction. These go past them: how a model-bearing system stays correct when the model, GPU, endpoint or data misbehave.

- **Pin a deterministic fallback contract per slot** — FEATURE — value 5 — effort M — risk low — category: fallback
  Why: models plug into decide(), intake, playbook routing, the guard, the funnel judges and Smith slots, and the Ollama and remote endpoints can be down or mid model switch (~3 min). Assumption: today a dead endpoint degrades each slot differently.
  Done when: with the endpoint killed, every slot in a table returns its documented rule-based answer within a timeout, and a test asserts each one.

- **Validate model output against a typed schema with bounded repair** — FIX — value 4 — effort S — risk low — category: output validity
  Why: reasoning-off runs exhausted budgets (gemma4:12b ran out on 7 of 10 scenarios) and the think:false setting didn't reach Ollama. Small models emit malformed JSON and labels outside the enum.
  Done when: a fuzz test of truncated, empty and off-enum replies yields a valid decision or an explicit abstain, never an exception or a silently accepted value.

- **Canary-probe the serving stack at session start** — FEATURE — value 4 — effort S — risk low — category: serving health
  Why: the settings-not-reaching-endpoint bug (reasoning_effort) went unseen for whole runs. A 3-prompt probe with known answers (reasoning actually off, context size honoured, latency in range) would catch a silent drift after an Ollama or model upgrade.
  Done when: changing the Ollama context default makes `sampo doctor` flag the model as unfit before any run uses it.

- **Make adoption cards expire** — FEATURE — value 4 — effort S — risk low — category: staleness
  Why: a bench win is true for one model hash, one corpus and one prompt. Assumption: nothing now invalidates it when a prompt, scaffold or corpus changes.
  Done when: editing a slot's prompt or retraining flips its card to "unverified", and the slot falls back to the rule path until re-benched.

- **Add a statistical floor to every adopt decision** — FIX — value 4 — effort S — risk low — category: measurement
  Why: the bench is 200 tasks and intake 0.73 vs 0.595 majority is fine, but the uplift exam's 3/8 vs 1/8 on 10 scenarios is noise-level. Assumption: adoption currently compares point estimates.
  Done when: adopt requires a confidence interval excluding the baseline (bootstrap, project-clustered), and the card prints the interval.

- **Checkpoint-and-fence training against GPU sharing** — FIX — value 4 — effort M — risk med — category: training safety
  Why: one 16 GB card is shared by Ollama, the funnel and training. An OOM mid-LoRA must not leave a half-written adapter that a slot then loads.
  Done when: killing training at a random step leaves no loadable artifact, resume continues from the last checkpoint, and registry loads refuse files without a completion marker and hash.

- **Detect concept drift per slot from live agreement** — FEATURE — value 4 — effort M — risk low — category: monitoring
  Why: Rune generations change the product, so the briefs' distribution moves. Compare the model's shadow prediction with the eventual outcome and alert when rolling accuracy falls below the adoption-time interval.
  Done when: a synthetic shifted stream trips the alert within N decisions and demotes the slot to its fallback.

- **Record every model call in a replayable ledger line** — FEATURE — value 4 — effort M — risk low — category: reproducibility
  Why: 149k ledger lines exist, but a wrong decision can't be reproduced if the model, prompt, seed and inputs aren't pinned. Assumption: calls are partly logged.
  Done when: `sampo replay <decision-id>` re-runs the call from the ledger and reports same or different output.

- **Bound the blast radius of a wrong model decision** — SECURITY — value 5 — effort M — risk low — category: safety
  Why: a model verdict can reach actions like closing tasks, merging or loosening the Ward. Models should only be allowed to tighten, to ask or to rank, never to authorise.
  Done when: a test enumerates every call site with a model input and proves none can turn a refusal into a permit or mark a task done without the command evidence.

- **Wild: Run a chaos monkey for model slots** — FEATURE — value 3 — effort M — risk low — category: chaos testing
  Why: wild. Randomly inject timeouts, garbage replies, a 3-minute model switch and an OOM during a Louhi exam run to prove the system's end results match the clean run.
  Done when: an exam under 20% injected faults grades within tolerance of the clean run, with no crash.

- **Wild: Keep a frozen "museum" model as a permanent tripwire** — FEATURE — value 3 — effort S — risk low — category: regression
  Why: wild. Retain generation-0's model and rerun it on every new benchmark, so a "gain" caused by a changed exam or grader shows up as the old model's score moving too.
  Done when: the scorecard prints the museum model's score each generation and flags a shift beyond its interval as a harness change.

- **Wild: Vote across independent heads and trust only unanimous agreement for automation** — FEATURE — value 3 — effort M — risk low — category: ensembles
  Why: wild. A kNN, a frozen-embedding head and a LoRA make different errors. Auto-acting only on a three-way agreement turns three mediocre models into a high-precision gate, and disagreement becomes the ask-the-user signal.
  Done when: on held-out projects, unanimous-agreement precision exceeds any single head's, and the coverage is reported.

- **Wild: Self-test the corpus with a poisoned-row tripwire** — SECURITY — value 3 — effort S — risk low — category: data integrity
  Why: wild. Plant known canary rows in the training lake and check that no trained model reproduces them. This catches leakage from sensitive-project data, or a pipeline step that bypasses exclusion.
  Done when: a canary string from an excluded project is never emitted by any model across 1,000 probes, and the check fails loudly if the exclusion step is removed.

Next question: Which model-bearing call site has no timeout today, and what does the session do while it waits?
Next question: When two slots' fallbacks disagree (rules versus kNN), which one does the system believe, and has that ever been measured?
