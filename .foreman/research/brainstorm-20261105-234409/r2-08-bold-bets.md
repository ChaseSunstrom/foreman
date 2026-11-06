# Brainstorm — lens: bold bets

Lens: bold bets. Round 2 = gaps, second-order, combinations. The pack's real ask is a generic trained decider that improves *every* Rune generation, local, on this box. Most prior ideas are slots, ablations, holdouts. Bets are bigger: what Sampo *becomes* if the model is load-bearing.

- **Make Sampo's weights a first-class build artifact, regenerated each Rune generation** — FEATURE — value 5 — effort M — risk med — category: training/CI
  Why: the request is "how it is trained and served on this box, how it improves every Rune generation" — T-1231 "Foreman beats Claude Code" and the end-of-run exam need a *product* whose capability is measurable across generations, not one-off slots. No idea makes the model a versioned, shipped, diffable thing like a binary.
  Done when: `sampo model build` emits `weights.bin` + `modelcard.json` (bench per slot, abstain rate, holdout) pinned by content hash; a second generation's card diffs against the first and `sampo doctor` shows the delta.

- **Run the whole drive under the decider, not just decide()** — FEATURE — value 5 — effort L — risk high — category: capability
  Why: current model slots are single-verdict. The bold bet: the trained model *drives* — picks the next task, orders the queue, allocates the GPU between moons funnel and Smith — and is measured by "minutes returned per hour," the metric T-3340 asks for. This is the "more" beyond a Kev-style decider.
  Done when: with the model's planner on vs. off over 7 held-out days, the model-driven run beats rule-driven on close-survival at ≤1.2× token cost, and `sampo status` shows the model's pick and why.

- **A "decider regression" gate that fails a Rune when any adopted slot drops below its baseline** — FEATURE — value 5 — effort M — risk low — category: testing/CI
  Why: T-1231/T-3340 need a *measured* claim, not prose (a standing steer). A single bench number that the ship gate checks, so "improves every Rune generation" is falsifiable per generation, exactly the lean/ratchet pattern already in the steers.
  Done when: `sampo model bench` prints per-slot scores with a floor; the ship gate is red when a champion slot falls below its last-recorded holdout score.

- **Federate the user's *own* machines: one model, N installs, weights flow, text never does** — FEATURE — value 4 — effort L — risk high — category: privacy/fleet
  Why: steers say "manage all of that across sessions… even without direct access… not only one machine" and T-3321 builds git-ref claims for a fleet. Prior ideas stop at "weights, not text, across projects." The bold version: the fleet *trains together* — each machine's closed briefs contribute labels to a shared generic base while staying on-device. This is the genericity the user asked for, at scale.
  Done when: two machines each hold <20 briefs; after federated merge, the shared model beats either machine's local model on leave-one-install-out, and a leak scan proves no raw text crossed the wire.

- **Turn the user's undo into the training loop, fully self-supervised** — FEATURE — value 4 — effort M — risk med — category: training
  Why: the user's standing rule that the user's undo/accept is the strongest existing label (T-0217 lessons confidence, the "learn the user's undo" bet) — but no idea closes the *loop*: model proposes, user undoes, that undo is the next training row, retrained nightly on idle GPU. Bold because it makes the model improve *from being wrong in the user's hands*, unattended.
  Done when: a `samo regret` retrain job consumes only undo events since last build, runs on idle GPU (yields to the funnel), and the new build beats the old on those exact replayed regrets.

- **Cold-start a brand-new project by *project fingerprint*, zero-shot, in minutes** — FEATURE — value 4 — effort M — risk med — category: genericity
  Why: "generic across every project built or managed with Sampo" (user's words) + the question "what does a project with fewer than 20 briefs get from a shared model." Bold: on `sampo init` the model classifies the new repo against sibling fingerprints (stack, change-graph shape, failure shapes) and activates the right heads, with an honest abstain when nothing matches — no per-project training.
  Done when: a never-before-seen repo with 5 briefs gets a working slot set on `init` in <10 min, scored by a held-out sibling; when similarity < threshold, every slot abstains and says why.

- **Make the decider *explain in the user's own compression*** — FEATURE — value 4 — effort S — risk low — category: UX
  Why: standing steer "make the tower speak in the user's compression" and "show a one-line model-saved-you X receipt." A model whose verdict the user can't veto in one breath is a liability; the bold bet is a *verdict grammar* the user can strike through, so every model decision is one editable line.
  Done when: every adopted-model verdict renders as one plain sentence with a strike-through veto in the web UI; a vetoed verdict is logged as a negative training row automatically.

- **Wild: Let the decider draft the *next Moonshot* before the user asks** — FEATURE — value 4 — effort M — risk med — category: moonshot/wild
  Why: "Moonshots must be wild" steer + "the model drafts the user's next steer." Bold: the trained model, fed on the whole ledger + grid + not-yet.md, proposes the next wild Moonshot *from the shape of the user's own unasked-for asks* (the "blind-spot predictor" class) — and is scored by whether the user says "yes, that."
  Done when: the nightly Moonshot draft's accept-rate over a month exceeds the human-filed Moonshot accept-rate, measured from ledger accept/reject.

- **Wild: Run the model as an *adversary* in its own exam — the Ward's attacker is the decider** — SECURITY — value 4 — effort M — risk high — category: safety/wild
  Why: prior ideas train "a Ward classifier plus an attacker." The bold inversion: the *same generic decider* that decides tasks also generates the hardest bypass attempts against the Ward on idle GPU, and the Ward learns from them. One model, two roles, an arms race the pack's "Red Queen" class only hinted at.
  Done when: weekly, the decider-generated bypass suite finds at least one new Ward hole or confirms zero, logged; a planted canary proves the Ward detects the decider's own best attack.

- **Wild: Ship Sampo as *one signed file* — the model is the product's core, not a feature** — FEATURE — value 5 — effort L — risk high — category: packaging/wild
  Why: the whole prior list treats the model as a slot among capabilities. The genuinely bold bet: a `sampo-model` binary+weights is *the* installable, with a "no-model" mode as a fallback tier (a standing idea) — i.e., Sampo's identity becomes the decider, generic across projects, shipped and updated like the rest.
  Done when: a fresh machine runs `sampo install` and gets a working, signed, hash-pinned decider with a documented `--no-model` fallback; `sampo doctor` names the model build and its bench.

- **Wild: A "decider obituary" — the model writes its own retirement when a slot stops earning** — CLEAN — value 4 — effort S — risk low — category: lean/wild
  Why: standing "lean" steer + "retire verbs when the host does them natively." Bold: each model slot carries a *retire-when* predicate; when its marginal value over the free arm hits zero for N generations, the model *files its own retirement brief* and the slot auto-demotes to retrieval-only, with the receipt on the morning card.
  Done when: a slot whose model no longer beats majority over 3 generations is auto-demoted with a self-filed brief and a one-line "the model retired X" receipt; re-earning a slot requires a re-bench.

- **Make serving *self-healing*: the model can't be the single point of failure** — PERFORMANCE — value 4 — effort M — risk med — category: serving
  Why: "how it is served on this box" + "what does the model path do when the GPU is busy with the moons funnel, and is the fallback measured?" Prior ideas schedule GPU but none make the decider *degrade gracefully and provably*. Bold: a warm local daemon, content-addressed weights, and a measured fallback so a dead endpoint never blocks a task.
  Done when: killing the model endpoint mid-run leaves every task completing via the rules path, with a logged "degraded: reason" line and a measured latency delta.

- **A "what-if" decider: replay any closed task against the current model, no work** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: T-3340 "Measure what the user feels" + "retrain on the previous generation's mistakes." Bold: `sampo model whatif T-id` re-runs *only the decision* (not the work) of a closed task through the current model, so the user sees "the new model would have picked differently here" before trusting it — cheap, local, zero-risk.
  Done when: `sampo model whatif` returns the model's decision vs. what actually happened for a closed brief in <5s, with the diff; over a sample, its "would-change" rate is reported per slot.

- **Wild: Bet on *predicting the user's next bad week* and pre-stage the fix** — FEATURE — value 4 — effort M — risk med — category: prediction/wild
  Why: "Dream the user's next bad week" + "anticipate." Bold: the trained model, over the full ledger, forecasts a *failure cluster* (which tasks/stages will false-done or loop in the next 7 days) and pre-drafts the guard clause or regression test, held for one yes. This is the decider *forward-looking*, not just deciding now.
  Done when: over a month, the forecasted bad-week items hit at a rate above the base rate, and each pre-staged fix, when applied, would have prevented a logged false-done or loop.

Next question: does the user want the decider to be *replaceable mid-run* (hot-swap a model build without restarting the drive), and if so, is a mid-swap decision allowed to change an in-flight task's plan, or only the next one?
Next question: what is the *floor* the user will accept for the generic model on a <20-brief project — full abstention (say nothing) is safer, but is there a middle tier (retrieval-only, no head) they'd consider "the model is present"?
