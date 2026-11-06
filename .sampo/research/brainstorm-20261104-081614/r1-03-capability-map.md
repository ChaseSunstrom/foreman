# Brainstorm — lens: capability map

- **Add a champion/challenger model registry with per-slot adoption** — FEATURE — value 5 — effort M — risk low — category: model ops
  Why: the pack says a model is adopted only where the bench shows it leads, and nothing beats majority on tier (0.58). Today that rule is manual. Each slot (intake, tier, playbook, loop breaker, close verifier) would get a champion, a challenger, the majority and free-arm baselines, and a rollback.
  Done when: `sampo model status` lists every slot with its champion, bench score, baseline and date, and a challenger that doesn't beat the baseline is refused.

- **Bench with whole projects held out** — FEATURE — value 5 — effort M — risk low — category: eval
  Why: the request is "generic, not just the Sampo repo". The data is 13 projects, and Sampo alone is 1,767 of 4,078 briefs, so a random split would leak project style.
  Done when: the bench reports leave-one-project-out scores per slot, with repo names stripped, and the generic score is the headline number.

- **Build a provenance-tagged training lake with exclusion flags** — SECURITY — value 5 — effort M — risk med — category: data
  Why: constraints say a sensitive project's data stays on the machine and may be excluded, and Claude's outputs can't be trained on. Briefs, ledgers and Smith journals would each carry source, project, model-of-origin and sensitivity tags, with a redactor.
  Done when: a build with project X excluded contains no row from X, and no row is tagged Claude-authored text.

- **Train a close verifier on "did the close hold"** — FEATURE — value 5 — effort M — risk med — category: verifier
  Why: gemma4:12b closed 4→5 tasks with many false-done. Briefs have done/blocked/reverted outcomes plus later fixes. A classifier on criteria, evidence runs and diff summary would predict whether the close survives, and Smith's close slot would consult it.
  Done when: on held-out projects it beats an exit-code-only baseline at catching false-done, and Smith refuses to close below its threshold in an exam run.

- **Give every head a calibrated abstain** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: the best intake type score is 0.73 vs 0.595 majority, and tier doesn't beat majority. A head that abstains and defers to the 27B or to `decide()` is useful where a forced guess isn't.
  Done when: each head reports a coverage-vs-accuracy curve, and at a stated coverage its accuracy beats majority on held-out projects.

- **Rejection-sample and preference-train Smith, with loops as negatives** — FEATURE — value 4 — effort L — risk med — category: actor
  Why: T-2971 only keeps green runs. Pairs from the same scenario (green vs looped or false-done) allow a DPO-style step, and loops are 4/10 of exam deaths. The loop-breaker events in the journals are ready-made negatives.
  Done when: a LoRA trained on pairs lowers the loop-death rate versus the base on Louhi's held-out split.

- **Fine-tune the embedder on brief-to-lesson and brief-to-later-fix pairs** — PERFORMANCE — value 4 — effort M — risk low — category: retrieval
  Why: bge-m3 title→brief recall@1 is 0.85. Pairs come free from lessons, recall-before-pass events and "later fixes" links.
  Done when: recall@1 on held-out projects rises over the stock bge-m3 on the same queries.

- **Synthesize verified scenarios by mutation across languages** — FEATURE — value 4 — effort L — risk med — category: data synth
  Why: Louhi has 18 runs in six languages, a thin set for training. SWE-smith-style bug injection into the repos of other Sampo projects, kept only when a test flips red→green, would yield thousands of verified tasks.
  Done when: a generator emits N scenarios from a project it never saw, each with a failing test that its reference fix turns green.

- **Stack per-project LoRA adapters on a generic base** — FEATURE — value 4 — effort M — risk med — category: local-first
  Why: it reconciles "generic" with "sensitive data never leaves". The base trains on shareable projects, and a private project gets an adapter built locally that no one else loads.
  Done when: an adapter trained on project X lifts X's bench without touching the base weights or any file outside X's directory.

- **Retrain and re-bench every Rune generation with a published scorecard** — FEATURE — value 4 — effort M — risk low — category: loop
  Why: the request says it improves every generation. Each generation would pin the dataset hash, retrain, re-bench and record regressions in the tower, and a regression blocks adoption.
  Done when: `sampo genesis` output includes per-slot model deltas against the prior generation, and a seeded regression stops adoption.

- **Train a cost/size estimator on the repo's change graph** — FEATURE — value 3 — effort M — risk low — category: estimation
  Why: tier sits at majority (0.58) from text alone. Adding files-touched, test counts and past tasks' step counts as features may lift it. Assumption: those features are in the briefs.
  Done when: tier accuracy on held-out projects beats 0.58 by a stated margin, or the slot is retired.

- **Ward text-channel red team for any trained risk model (advisory only)** — SECURITY — value 4 — effort M — risk med — category: ward
  Why: an earlier question asks whether the Ward and the funnel's local models share an attack channel. A trained risk head may only tighten, never loosen, a verdict, and should be tested against injected text in briefs and tool output.
  Done when: an injection suite shows the head never turns a Ward refusal into an allow.

- **Dream overnight: idle-GPU self-play on old commits (wild)** — FEATURE — value 4 — effort L — risk med — category: self-play
  Why: wild. The 5070 Ti sits idle. Smith could attempt rolled-back real commits across the 13 projects, with the recorded follow-on change as the goal, and keep only test-verified traces in the lake.
  Done when: a morning report shows N new verified traces, with held-out scores unchanged or better.

- **Project fingerprint for zero-shot onboarding (wild)** — FEATURE — value 3 — effort M — risk med — category: transfer
  Why: wild. A small embedding of stack, gates and conventions (from `fm map`) would let a new project borrow the lessons and cards of its nearest neighbours on day one.
  Done when: on a project with under 20 briefs, retrieval seeded by the fingerprint beats unseeded retrieval on held-out tasks.

- **Learn the user's accept/reject taste to pre-rank moons and pre-answer asks (wild)** — FEATURE — value 4 — effort M — risk med — category: preference
  Why: wild. The ledgers hold asks, answers and steers, and a prior question wants the funnel's stages checked against the user's own history. A preference head could rank moons and drop likely rejects before any judge call.
  Done when: its ranking predicts the user's past accept/reject on held-out moons better than the Foreman-authored judges do.

Next question: which ledger events (steers, reverts, "dropped" items) carry the user's real corrections, and do they have enough labels to train on without leaking one project's habits into another?
Next question: what is the smallest model that beats majority on each slot, so the 5070 Ti can serve all heads at once while Smith's 12B or 27B runs?
