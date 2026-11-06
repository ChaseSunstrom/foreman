# Brainstorm — lens: bold bets

- **Make the model the default decider, not the fallback** — FEATURE — value 5 — effort L — risk high — category: architecture
  Why: The request frames "a better Kev-style decider" as the product's heart; every prior idea treats the model as opt-in behind rules. The user’s standing intent is that Sampo earns its place; a system that only ever defers to rules can never *improve every Rune generation* measurably.
  Done when: `sampo decide` returns the model’s verdict on 80%+ of live decisions in a full Rune, and `samo doctor` prints "model: primary" as the default state.

- **Retrain the whole decider from regret alone, zero human labels** — FEATURE — value 5 — effort M — risk med — category: training
  Why: The user’s undo is the only ground truth (stated in words: "Let the user's undo be the only label"). No annotation pipeline exists; the outcome lake has ~2,900 closed briefs. Wild assumption: regret signal is dense enough without any manual labelling.
  Done when: `sampo decide train --from-regret` completes on this box in under 4 hours and the new head beats the kNN oracle on a leave-one-project-out bench with no human-labelled rows.

- **Federate regret, not weights, across all Sampo projects on this box** — FEATURE — value 5 — effort L — risk high — category: training
  Why: The request says "generic across every project built or managed with Sampo." The user explicitly wants cross-project generalisation. Sharing raw text violates the local-only rule; sharing aggregated regret statistics (per-slot flip rates, per-brief-type error shapes) keeps data local while making the model truly generic.
  Done when: `sampo decide train --federate` pulls regret aggregates from 3+ project state dirs, trains a shared base, and leave-one-project-out shows improvement over a single-project model.

- **The model writes the next Moonshot before you ask** — FEATURE — value 4 — effort M — risk med — category: generation
  Why: The funnel generates 10,000 candidate moons; the kill and tier stages are the bottleneck (75 tier batches at ~3 min each). A trained model that *proposes* high-wildness moons directly from the grid’s empty cells and the user’s recent pushback history could cut generation time 10× and raise the wildness floor. The user’s words: "Moons: more and better ideas per hour."
  Done when: The model proposes 50 moons in under 5 minutes, and the cold reviewer scores at least 10 above wild-4, without the 10k funnel.

- **Run the decider as an adversary in its own exam — the Ward’s attacker is the model** — FEATURE — value 5 — effort L — risk high — category: security
  Why: The Ward is rule-based; the standing rule says "a capability whose free arm beats the session arm is a top gap." A trained model that actively tries to *bypass* the Ward using the user’s own phrasing patterns and the repo’s real file paths finds rules that are too permissive. This is the only way to test the Ward against adaptive, context-aware attacks rather than static fuzzing.
  Done when: `sampo exam ward --attacker model` runs for 1 hour, finds at least 2 previously unblocked dangerous command shapes, and files a fix task for each.

- **Distil the 27B only on its verified, green-test runs; keep every loop as a negative** — FEATURE — value 4 — effort M — risk low — category: training
  Why: T-2966 shows small models break loops on repeated actions. The 27B has verified runs from real S tasks and Louhi scenarios. Keeping loops as negatives is direct evidence: T-2966’s fix was "third identical action goes once to the planner." Training on this pattern makes the distilled 4B predict loops before the third repeat.
  Done when: The distilled model, given a Smith journal prefix, flags "loop imminent" before the third identical action in 80%+ of held-out loop scenarios from T-2966 and similar.

- **Make the decider a readable rulebook you can edit, not a black box** — FEATURE — value 5 — effort M — risk med — category: transparency
  Why: The user’s words: "we will want it to be a generic model… and maybe brainstorm on features the model should have." A rulebook the user can read and edit is the only way to make a generic decider *trustworthy* across projects they don’t own. The standing rule "every capability must be called by a real session path" implies the user wants to *see* what the model decided and why.
  Done when: `sampo decide rules` prints a versioned, human-readable rules file; the user edits one rule and the next `sampo decide` call reflects the change with a provenance stamp.

- **Wild — Ship Sampo as one signed file: the model is the product’s core, not a feature** — FEATURE — value 5 — effort L — risk high — category: architecture
  Why: The user’s words: "generic model… what it is trained on, how it is trained and served on this box." The current Sampo is a Python plugin with a 2.4 GB state directory and 2,381 files. If the decider is the core, the *product* is a single signed artifact: model weights + rules + embedding index, one file, one hash, one install. Everything else (hooks, drive, Ward) is a thin adapter around it.
  Done when: `sampo install` downloads one signed file, `sampo decide` works with no Python plugin loaded, and the Ward can verify the file’s hash at session start.

- **Wild — Bet the whole product on one number: "decider beats plain" on whole held-out projects, or the slot retires** — FEATURE — value 5 — effort M — risk high — category: measurement
  Why: The standing rule: "a capability whose free arm beats the session arm on the same scenarios is a top gap." The user’s words: "how it is measured." Every slot must earn its place or die. A single, falsifiable, publicly visible number — "on N held-out projects, the model’s decider beats the rules-only baseline by X%" — forces honest measurement and makes retirement automatic.
  Done when: `sampo decide benchmark --holdout N` runs on 5+ projects, prints the beat/loss per slot, and any slot below baseline is automatically demoted to shadow mode with a retirement date.

- **Wild — Federate only weights, never text, across the user’s own machines, with a consent gate per project** — FEATURE — value 4 — effort L — risk high — category: privacy
  Why: The user’s words: "generic across every project… and maybe brainstorm on features the model should have." Multiple machines (T-3321 fleet, many machines no duplicates) are explicit. The standing rule: "keep data on the owner’s hardware." Federating *weights* (not text) across the user’s own machines lets the model improve with more data while respecting local-only. A consent gate per project prevents Sampo’s own repo from dominating.
  Done when: `sampo decide federate --machines N` syncs model weights (not training text) between 2+ machines, and `sampo decide provenance` shows which machine contributed which weight update, with a per-project opt-out.

- **Train a "user twin" that drafts steers before they are said, scored by edit distance** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: The user’s words: "the need behind what they keep asking for and pushing back on." The standing rule: "every user steer becomes a standing rule plus an automatic check." If the model can draft the steer the user *will* say, the user can edit it instead of typing it, reducing friction and making the training loop self-supervised (the edit *is* the label).
  Done when: `sampo decide draft-steer` produces a draft steer at session start; the user’s edit distance to the final steer is logged, and after 30 sessions the mean edit distance drops by 30%.

- **Wild — The model writes its own retirement when a slot stops earning** — FEATURE — value 4 — effort S — risk low — category: lifecycle
  Why: The standing rule: "only proven harm or exact duplication removes an idea, with the reason recorded." The user’s words: "how it improves every Rune generation." If the model can *prove* a slot is no longer useful (by its own benchmark dropping below baseline for 3 consecutive Runes), it can file its own retirement with a one-paragraph explanation. This makes the system self-pruning and honest.
  Done when: `sampo decide retire --auto` files a retirement task for any slot below baseline for 3 Runes, with the model’s own explanation, and the user can veto with one key.

- **Run the decider as an *adversary* in the funnel: it kills moons the generator can’t defend** — FEATURE — value 4 — effort M — risk med — category: generation
  Why: The funnel’s kill and tier stages are slow (75 tier batches at ~3 min). A trained model that *attacks* each candidate moon (finds the flaw, the duplicate, the low-wildness) in parallel is 10× faster than sequential LLM judging. The user’s words: "Moons: more and better ideas per hour: parallel generators on every endpoint… a kill judge that knows Sampo exists."
  Done when: `sampo moons kill --parallel N` processes the 10k funnel in under 30 minutes using the decider as the kill judge, and the kill rate matches the current LLM judge within 10%.

- **Wild — Let the decider *refuse the work*, and pay it for saying "no"** — FEATURE — value 4 — effort S — risk low — category: decision
  Why: The user’s words: "we will want it to be a generic model… a better Kev-style decider." A decider that only says "yes" or "maybe" is useless. The user’s standing rule: "never block on the user for a question about rules, gates or process: pick the option most consistent with gen-0." If the model can say "this task is not worth the tokens, here’s why" with a confidence score, the drive can skip it and log the refusal. The user’s "no" is a *valuable signal* for training.
  Done when: `sampo decide refuse --task ID` is a first-class path; the model’s refusal is logged with a reason and confidence, and the drive skips the task; after 50 sessions, the refusal precision (user agrees it should have been refused) is above 70%.

- **Make every model verdict a git object: replayable, diffable, and auditable from the repo alone** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: The user’s words: "how it is measured." The standing rule: "every capability whose free arm beats the session arm is a top gap." If the model’s verdicts are git objects (a small JSON blob in `.sampo/decisions/`), the user can `git log` every decision, `git diff` two Rones’ decisions, and `git blame` a bad decision to the training run that produced it. This makes the model *legible* without a dashboard.
  Done when: `git log --oneline .sampo/decisions/` shows one line per model verdict; `git diff HEAD~1 .sampo/decisions/` shows what changed between Rones; and `samo doctor` verifies the decision log is complete.
