# Brainstorm — lens: approaches

**Approaches to Sampo's generic model: the five distinct roads**

The pack names a *better Kev-style decider* plus training/serving/measurement on this box, generic across every Sampo project. The ideas wall already covers *what* (slots, heads, distillation, kNN baseline, holdout, abstain). What's under-explored is *how to get there* as distinct bets, each with a trade-off I can stand on. Ranking by value-per-effort and what the pack proves out.

- **Ship the zero-model oracle first; defer all weights** — FEATURE — value 5 — effort S — risk low — category: baseline
  Why: the wall's own consensus is "retrieval-only kNN first." The ~2,900 closed briefs are the whole training signal; bge-m3 + nearest-closed-brief gets you a *working* generic decider in days with no GPU, no VRAM fencing, no leakage risk. It's the cheapest falsification of whether a model helps at all. Done when: `sampo decide` answers a held-out brief from retrieval alone, scored leave-one-project-out, beating majority on ≥1 slot.

- **Distil the 27B on green-only runs, loops as negatives** — FEATURE — value 4 — effort M — risk med — category: training
  Why: the user explicitly asked for "a LoRA on a 0.6–4B through the Jeff stack" and "distil a Smith actor from verified runs." This reuses an installed, local stack and a teacher already resident. Trade-off: highest fidelity, but VRAM contention with the moons funnel (the pack's T-2953 shows the funnel judging one batch at ~3 min); needs a checkpoint-fence. Done when: a 2B student passes a leave-one-project-out brief set that the frozen-embedding kNN misses.

- **Train frozen-embedding heads per decision type, one shared embedder** — FEATURE — value 4 — effort M — risk med — category: training
  Why: "bge-m3 embeddings + a trained head" is verbatim the user's ask. Avoids a model zoo; the head is tiny and retrainable by content hash. Best middle road between the oracle (no head) and LoRA (heavy). Done when: one shared 1024-d embedding serves ≥3 slots, each head scored independently, retrain is one idempotent command.

- **Few-shot retrieval on the resident 27B, no new training** — PERFORMANCE — value 3 — effort S — risk low — category: reuse
  Why: the 27B is already served; wrapping it in the Kev decider prompt + retrieved sibling briefs is a capability you get *today* with zero training infra. Trade-off: latency and endpoint availability (a question the wall left open: "what does the model path do when the GPU is busy?"). This is the "doing less" approach with real lift. Done when: a decide() call returns a typed verdict via the 27B with a rules fallback if the endpoint is cold.

- **Constrained-decoding grammar over a small instruct model, no fine-tune** — FEATURE — value 3 — effort S — risk low — category: reuse
  Why: every decider slot is *typed* (abstain-or-answer, one sentence). You don't need to *train* a model to emit one of N legal verdicts — you need a grammar (the wall: "constrain every typed decision to a grammar, with bounded repair"). A stock small model + menu beats a trained head on the *reliability* axis at near-zero cost. Trade-off: ceiling is the base model's judgment, not learned taste. Done when: every slot emits only grammar-legal output, with a repair pass and a logged abstain rate.

- **Do less: ship the export, the bench, and the abstain contract only** — CLEAN — value 3 — effort S — risk low — category: defer
  Why: the standing rules (T-0866 "needs cases," T-1231 deferred) say the *measurement* and *data export* are the real deliverable; the model is the part most likely to be over-built. Proven harm or duplication removes an idea — this is the anti-bloat approach. Done when: `sampo decide train` produces a flat, name-stripped table + a leave-one-project-out scorecard, and *no weight is shipped*.

- **Use the user's own undo as the only label, self-supervised** — FEATURE — value 4 — effort M — risk med — category: training
  Why: the pack shows the user *constantly* undoing and correcting (the 2967 "undo doesn't stick," the rename, the dropped items). Undo is a free, honest, generic label that works across every project without hand-annotation. Trade-off: noisy, sparse, and biased toward visible reverts. Done when: a labeler turns each undo into a (brief, wrong-decision, right-decision) row, and a head beats the kNN oracle on those.

- **One shared Sampo Head, scored leave-one-project-out** — FEATURE — value 3 — effort M — risk low — category: training
  Why: "generic across every project" is the whole point; a single generic head with a per-project adapter (the wall's "per-project LoRA over a shared base") is the cleanest architecture for genericity. Trade-off: the adapter needs per-project data, which is exactly what "fewer than 20 briefs" breaks (an open wall question). Done when: base head + 3 adapters pass a leave-one-project-out bench each.

- **Pairwise approach-chooser as the first *useful* slot** — FEATURE — value 4 — effort S — risk low — category: slot
  Why: of all decider slots, ranking two candidate plans (which did the user accept?) is the most *learned* from existing data and the least risky — a wrong pick just costs one turn, not a false-done. It's the smallest wedge that proves the model earns its tokens. Done when: the chooser, on held-out plan pairs, matches the user's pick above the free-arm baseline.

- **Wild — make the decider a readable rulebook, and train *rules* not weights** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: the user's steers demand cold reads, legibility, and "no metric-gaming." A model that *emits its own one-line rule* ("when a brief repeats an action 3×, escalate") is auditable, diff-reviewable, and satisfies the "wild: a rulebook you can read" instinct the wall keeps returning to. Trade-off: coverage is limited to patterns you can state; it won't generalize to novel shapes. Done when: `sampo decide explain` prints a rule for any verdict, and a cold Haiku read passes it against gen-0.

- **Wild — mine "regret" from *later* fixes, not from undo** — FEATURE — value 4 — effort M — risk med — category: wild
  Why: the pack is full of "close held, then a later task fixed it" (T-2967 undo, T-2964 ship review). Undo is *immediate* regret; a close that a fix has to walk back 3 days later is *durable* regret — a better, rarer, more honest label than any hand label. This is the label the wall names ("mine regret labels from later fixes") but never wires to a *training* loop. Done when: a (close, later-fix) joiner labels N rows, and a close-holds head beats majority on them.

- **Wild — train a *Ward attacker* with the decider, and let the Ward learn only from safe hits** — SECURITY — value 3 — effort L — risk high — category: wild
  Why: the rename audit (T-2742) and the T-2967 guard-miss show the Ward's path-comparison is brittle; a model that *probes* the Ward generates an endless regression corpus the Ward can train on, without the user hand-writing refusal tests. Trade-off: high risk of the attacker finding a *real* bypass that the Ward then "learns" by memorizing rather than fixing. Done when: the attacker's hit rate on a frozen Ward drops after retraining, and no hit reaches a live session (advisory only).

- **Wild — replay the user's full accept/reject history as the *only* training signal, no labels** — PERFORMANCE — value 3 — effort S — risk low — category: wild
  Why: the wall's "use the user's own undo as the only label" plus their "I want it done quick without burning money" steer: the user *has* labeled every decision by living it. A preference dataset built purely from their own closes/rejects/undos is zero marginal cost and fully generic. Trade-off: it's a closed loop — the model can only be as good as the user's past taste, and it overfits to one person. Done when: a preference pair set is built from ≥500 real decisions and a small model ranks them better than a recency baseline.

- **Wild — commit the project's own weights as `.sampo/model.bin`, git-tracked and content-hashed** — FEATURE — value 3 — effort S — risk low — category: wild
  Why: the rename migration (T-2967) and the "move with backup, manifest and undo" rule mean the model is *part of the repo state* that gets synced across machines. Treating weights as a first-class, hashed, versioned artifact (not a cache) makes `sampo migrate`, `sampo ship`, and the fleet-claims protocol (T-3321) all work on the model for free. Done when: a retrain lands as a hash-pinned commit, `sampo ship` verifies the digest, and a rollback reverts it.

- **Do even less: prove the model is *not* needed before building it** — CLEAN — value 4 — effort S — risk low — category: defer
  Why: the standing rule "a capability whose free arm beats the session arm is a top gap" cuts both ways — if retrieval + rules + a grammar already beat a trained head on the held-out set, training is dead weight and the honest answer is *no model*. This is the strongest "do less" move and the one the wall's "kill a slot that has no ledger incident behind it" steers toward. Done when: the kNN + grammar arm is measured against a trained head on the same leave-one-project-out set, and whichever wins is the shipped default.

Next question: which single decider slot, if it abstains or silently falls back, has *never* left a ledger trace — because that's the one the "measure the fallback" bench can't see yet.
Next question: what is the *smallest* project (fewest briefs) on this box where the generic head must not abstain, so we can set the real floor for "the model should say nothing" before training?
