# Brainstorm — lens: approaches

Through the **approaches** lens, I see a fundamental fork: the user asked for "Sampo's own trained model(s) ... a better Kev-style decider." The pack shows a 2.4 GB state, a 27B local endpoint, and a 0.6-4B training stack. The "ideas so far" are drowning in *what* to build (slots, registries, wild dreams) but missing *how* to actually train, serve, and measure it on this specific box without burning the GPU or leaking data. Here are the approaches to solve the *mechanics* of the request.

- **Build a "decision distillation" pipeline from existing `fm decide` logs** — FEATURE — value 5 — effort M — risk med — category: training
  Why: The pack shows `fm decide --check` and ~2,900 closed briefs. Instead of training from scratch, extract the user’s actual accept/reject/undo patterns from the ledger. This is the "Kev-style" data. The 27B is already resident; use it to label ambiguous cases, then distill into the 0.6-4B. This is the "yes-and" on T-0035 (eval capture).
  Done when: `sampo decide train --source ledger` produces a 0.6B model that beats the kNN oracle on a holdout of 500 past decisions.

- **Serve the decider as a local "sidecar" with a 100ms budget** — PERFORMANCE — value 5 — effort M — risk low — category: serving
  Why: The user’s steer is "quick." The 27B is too slow for per-tool-call decisions. The 0.6-4B model must run in <100ms to be usable in the Smith act loop (T-2966). The pack shows `plugin/bin/sampo` and `plugin/lib/sampo/cli.py`. Use the installed Jeff training stack to quantize to INT4 and serve via Ollama or llama.cpp with a hard timeout. If it misses 100ms, fall back to rules.
  Done when: `sampo decide --bench` shows p99 latency <100ms on the local GPU with 4B INT4, and the fallback path is triggered in a simulated slow-GPU test.

- **Make "genericity" a testable property with a "canary project"** — SECURITY — value 4 — effort S — risk low — category: genericity
  Why: The user explicitly said "generic across every project... not just the Sampo repo." The pack shows T-3312 (Kalevala) and T-3316 (Headroom census). The danger is the model overfitting to Sampo’s repo structure. Create a tiny, synthetic "canary" project (e.g., a 5-file Python web app) with no Sampo code. Train/evaluate on it. If the model’s accuracy drops >20%, it’s not generic.
  Done when: `samo decide eval --project canary` runs on a fresh git repo with 50 synthetic tasks, and the model’s score is within 20% of its score on the Sampo ledger.

- **Use a "two-tier" serving strategy: 0.6B for speed, 27B for audit** — FEATURE — value 4 — effort M — risk med — category: architecture
  Why: The pack shows a 27B local endpoint (Jarvis) and a 0.6-4B training stack. The 0.6B makes fast decisions; the 27B is used *only* when the 0.6B is uncertain (low confidence) or for weekly "dream" runs (T-0831). This keeps the 27B idle 95% of the time, respecting the user’s "no burning money" steer. The 0.6B is the "Kev" fast path; the 27B is the "judge."
  Done when: `sampo decide --audit` shows the 27B was called <5% of the time in a 100-task run, and the 0.6B’s decisions match the 27B’s in >90% of cases.

- **Implement "abstain" as a first-class, measurable output** — FEATURE — value 5 — effort S — risk low — category: decision
  Why: The user’s own words (T-2966) show small models breaking loops. A "better Kev" must know when it *doesn’t* know. The pack has T-0826 (round ledger) and T-0217 (confidence). The model must output `abstain` with a confidence score. If confidence <0.8, it falls back to rules. This is the "Kev" trait: it doesn’t guess, it delegates.
  Done when: `samo decide --verbose` prints `abstain` for 10% of test cases, and the fallback rules are triggered correctly in a replay test.

- **Train on "regret" labels from `samo undo` and reverts** — FEATURE — value 5 — effort M — risk med — category: training
  Why: The user’s steer is "I don’t want to just cap the cost... I want it to still get done." The best signal for "good" decisions is "the user didn’t have to undo it." The pack shows T-2967 (undo doesn’t stick) and T-0831 (salvage partial results). Mine the ledger for `samo undo` commands and git reverts. These are the "bad" examples. The "good" examples are decisions that stayed. This is self-supervised, no human labeling.
  Done when: `samo decide train --label-source regret` uses 500 undo/revert events as negative examples, and the model’s false-positive rate drops by 30% compared to label-less training.

- **Wild: Make the decider a "living rulebook" that users can edit** — FEATURE — value 3 — effort L — risk high — category: delight
  Why: The user’s steer is "the decider is a readable rulebook, not a black box" (from ideas so far, but unaddressed). Instead of a pure ML model, compile the trained weights into a set of human-readable rules (e.g., "If diff touches `guard.py`, abstain"). The user can edit these rules. The model is the *learner*; the rulebook is the *interface*. This is wild because it mixes ML with a traditional rule engine.
  Done when: `samo decide export-rules` generates a YAML file with 20-50 rules, and editing one rule changes the model’s behavior in a live test.

- **Wild: Run the decider as an "adversary" in its own exam** — SECURITY — value 4 — effort M — risk med — category: evaluation
  Why: The pack shows T-0034 (headless read-only lens reviewers) and T-0867 (held-rate scorecard). The best test for a decider is to *attack* it. Use the 27B to generate "tricky" decisions that the 0.6B might get wrong (e.g., a diff that looks like a guard bypass but isn’t). This is a "red team" for the model. If the 0.6B fails, the 27B’s attack is added to the training set.
  Done when: `samo decide red-team` generates 50 adversarial cases, and the 0.6B’s accuracy on them is <80%, proving the 27B found its weaknesses.

- **Wild: Let the decider "dream" its own mistakes overnight** — FEATURE — value 3 — effort L — risk high — category: delight
  Why: The pack shows T-0793 (overnight work) and T-0831 (salvage partial results). The 27B is idle at night. Use it to replay the day’s 0.6B decisions and find the ones that "looked wrong." File them as "regrets" in the ledger. This is a self-improving loop. It’s wild because it’s unsupervised, self-correcting, and uses the GPU when the user is asleep.
  Done when: `samo decide dream --run` is triggered at 02:00, and the next morning’s `samo decide --bench` shows a 5% improvement in accuracy on the "regret" cases.

- **Do less: Ship a "kNN oracle" with no training** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: The user’s steer is "do less." The pack shows T-0035 (eval capture) and T-0826 (round ledger). Before training any model, ship a kNN over the 2,900 closed briefs. If the kNN oracle already achieves >80% accuracy on the holdout, the 0.6B model might not be needed. This is the "zero-model" baseline. It’s the cheapest, most reliable, and most transparent approach.
  Done when: `samo decide --oracle knn` answers 100 test cases, and the accuracy is >80% without any GPU use.

- **Serve the model as a "git object" in the repo** — SECURITY — value 4 — effort S — risk low — category: portability
  Why: The pack shows T-3342 (mirror folder rename) and T-3321 (fleet claims on git refs). The model weights should be part of the repo, not a separate artifact. Commit the 0.6B INT4 weights as a `.gitignore`-ed but versioned file. This ensures the model is reproducible, reviewable, and tied to the code. It’s a "Sampo model as a build artifact" (from ideas so far).
  Done when: `git log --oneline -- model.bin` shows 10 commits, and `samo decide --verify` checks the hash of the weights against the commit.

- **Make "genericity" a "leave-one-project-out" test** — FEATURE — value 4 — effort M — risk med — category: evaluation
  Why: The user explicitly said "generic across every project." The pack shows T-3312 (Kalevala) and T-3316 (Headroom). The standard test for genericity is to train on all projects *except* one, and test on the held-out project. If the model can’t generalize to a project it never saw, it’s not generic. This is the "hold out whole projects" capability.
  Done when: `samo decide eval --holdout project-X` shows the model’s accuracy on project-X is within 15% of its accuracy on the training projects.

- **Wild: Let the user "veto" a model decision and teach it** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: The user’s steer is "I want it to still get done." The best way to make a model better is to let the user correct it. When the user overrides a `samo decide` output, log the input, the model’s decision, and the user’s correction. This is a "user-in-the-loop" training signal. It’s wild because it’s interactive, immediate, and requires no retraining.
  Done when: `samo decide --veto` is triggered by the user, and the next 10 similar decisions are influenced by the correction in a replay test.

- **Make the model’s "confidence" a "cost" metric** — PERFORMANCE — value 4 — effort S — risk low — category: efficiency
  Why: The user’s steer is "no burning a fuck ton of money." The model’s confidence can be mapped to a "cost" of running the 27B audit. If confidence >0.95, no audit. If <0.7, full audit. This is a "cost-aware" router. It’s a "cost/size estimator on the repo’s change graph" (from ideas so far).
  Done when: `samo decide --cost` shows the 27B was called only when confidence <0.7, and the total GPU time is reduced by 50% compared to always-auditing.

- **Wild: Make the model a "fossil" that never changes** — CLEAN — value 3 — effort S — risk low — category: reliability
  Why: The pack shows T-0829 (brainstorm lens scaling) and T-0831 (salvage partial results). The most reliable model is the one that doesn’t change. Ship a "fossil" 0.6B model that is frozen after the first training run. All improvements go into a "challenger" model. Only if the challenger beats the fossil on the holdout does it replace it. This is a "champion/challenger registry" (from ideas so far).
  Done when: `samo decide --fossil` shows the model version is pinned to a commit, and the challenger model is in shadow mode, not serving traffic.
