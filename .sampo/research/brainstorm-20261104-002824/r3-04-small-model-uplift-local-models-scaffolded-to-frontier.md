# Brainstorm — lens: small-model uplift: local models scaffolded to frontier

- **Shadow the frontier turn by turn** — FEATURE — value 5 — effort M — risk low — category: local models (wild)
  Why: wild. While a frontier session works, the 27B silently predicts each next tool call. The match rate per task kind and per model decides when that kind can be handed to local, which is promotion on live evidence, not a league on closed tasks. It costs only idle GPU time and writes no files.
  Done when: `sampo louhi shadow` prints a per-task-kind agreement rate from at least 50 real turns, and one kind is flagged "safe to hand over" or "not yet".

- **Drive weak models by numbered menus** — FEATURE — value 5 — effort M — risk low — category: scaffolding
  Why: assumption: small models fail at free-form tool calls and succeed at picking one of N. Each step shows the model at most 7 numbered legal next moves from the stage rail and `fm next`, and it answers with a digit. This matches how decision models like d3 already work.
  Done when: on 20 closed tasks, the 27B run through the menu loop produces zero malformed tool calls, and its close rate is reported next to free-form.

- **Escalate on logprobs, not on a second opinion** — PERFORMANCE — value 4 — effort S — risk low — category: routing
  Why: assumption: the llama-swap endpoint can return token logprobs. A low-margin key token (the verdict, the chosen option) sends only that step to the frontier at zero extra local tokens. This is cheaper than the disagreement-based escalation already listed.
  Done when: a held-out run shows that the lowest-confidence 20% of steps hold at least 50% of the wrong answers.

- **Pick the draft by running N samples against the Exam** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: the user is asleep and local tokens are free. Sample 8 drafts at temperature, run each through its brief's dry-runnable Exam, and cluster by observed result. The largest passing cluster wins. This goes beyond verifying a single draft.
  Done when: for one task kind, best-of-8 beats best-of-1 pass rate on at least 15 held-out briefs, with both rates printed.

- **Pre-read the repo for the frontier model** — PERFORMANCE — value 5 — effort M — risk low — category: cost
  Why: the budget is $200 and the standing steer is local models scaffolded to frontier results. The local model writes cached per-file digests and invariants, keyed by tree hash. Frontier sessions then read the digest and open a file only when the digest says it matters.
  Done when: the same task, run with and without digests, shows frontier input tokens falling by at least 30% with an equal Exam result.

- **Keep a hint bank triggered by local failures** — FEATURE — value 4 — effort M — risk low — category: scaffolding
  Why: assumption: failures repeat in shape. When a local attempt fails and the frontier fixes it, a 3-line "what went wrong, what to do" hint is stored with an embedding. The next similar task retrieves the top hint. This differs from compiling whole traces into scaffolds.
  Done when: a re-run of a previously failed local task with the hint injected passes, and the hint's retrieval hit is logged.

- **Measure each model's effective context** — PERFORMANCE — value 4 — effort S — risk low — category: local models
  Why: T-2893 shows a reply cut by length, and long packs are likely to degrade small models. A needle-and-instruction bench per model gives an accuracy-versus-length curve. Pack builders cap context at the knee instead of the nominal window.
  Done when: `sampo louhi models` prints a knee length per model, and a pack builder refuses to exceed it for local callers.

- **Optimise scaffold prompts overnight against the Exam** — FEATURE — value 4 — effort L — risk med — category: scaffolding
  Why: instead of hand-ablating steps, a search mutates the scaffold wording per model and task kind. It is scored on train briefs and kept only if it also beats on a sealed holdout.
  Done when: one task kind gains at least 10 points of Exam pass rate on holdout, with the winning prompt and its score history saved.

- **Pair a small draft model with the 27B for speculative decoding** — PERFORMANCE — value 3 — effort M — risk med — category: speed
  Why: assumption: the server runs llama.cpp, which supports a draft model. This could cut latency on the long 27B generations that currently dominate the overnight wait.
  Done when: tokens per second on a fixed 2k-token generation improves by at least 1.5× with byte-identical greedy output.

- **Repair broken structured output without a model** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: truncated JSON and fenced or half-closed replies are the commonest small-model failures. A tolerant zero-token repair pass runs before any retry, and it counts every repair by failure class.
  Done when: replaying recorded bad replies, at least 60% parse after repair without a retry, and the counts appear in the bench.

- **Calibrate the local judge against frontier verdicts** — FEATURE — value 4 — effort M — risk low — category: judging
  Why: a small model judging pass or fail is only usable if its score means something. Fit a calibration map from its confidence to agreement with frontier verdicts, with an abstain band that routes to the frontier.
  Done when: in the confident band, local and frontier verdicts agree at least 90% on 40 held-out items, and the abstain share is printed.

- **Run a three-model jury where the frontier only breaks ties** — FEATURE — value 3 — effort M — risk med — category: ensembles (wild)
  Why: wild. Qwen 27B, the MoE and a decision model vote on cold reads and slate triage. The frontier is called only on a 1–1–1 split, and the tie rate is tracked per question kind.
  Done when: on 30 cold reads, the jury plus frontier tie-breaks matches frontier-alone verdicts at least 90% of the time and costs under 30% as much.

- **Give local models a frontier-token allowance they must justify** — FEATURE — value 4 — effort M — risk med — category: budget (wild)
  Why: wild. Each task starts with a small frontier allowance. The local model can spend it only by writing a one-line reason, such as "stuck on X after 2 tries". Reasons are logged and later graded, so over-asking becomes visible.
  Done when: a night's run prints frontier spend per task, the reasons given, and the share judged necessary by a cold read.

- **Train a per-repo LoRA overnight from accepted work** — FEATURE — value 3 — effort L — risk high — category: fine-tuning (wild)
  Why: wild, and local-first. The user's accepted briefs and closed diffs form the training data, and the resulting adapter hot-swaps in only if it beats the base model on a sealed holdout.
  Done when: one repo's adapter beats base on holdout briefs, or the run records that it did not, with the data size.

Next question: which task kinds do the local models already match the frontier on, and has anyone measured that on the user's closed tasks instead of assuming it?
Next question: when the 27B is the only model in play, what does the 3-minute switch to the MoE actually save per night, and is that ever worth the swap?
