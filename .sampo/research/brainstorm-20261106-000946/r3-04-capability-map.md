# Brainstorm — lens: capability map

Read the pack. The request: Sampo’s own trained model, generic across every project, “a better Kev-style decider and more”: what it does, training data, training/serving, measurement, and how it improves every Rune generation. Lens: capability map — breadth over depth; name what a complete, best-in-class decider does, then propose what the pack doesn’t show. Thin: ui, devices. Ideas so far already cover: kNN oracle, per-project adapters, regret/undo labels, leave-one-project-out, redaction, serving/pinning/failover, shadow mode, grammar, one-verb collapse, museum model, federate-weights, capability-map/spec publication, Rune retrain loop, cost/size estimator, Ward attacker. I’ll go past them into breadth: the missing first-class surfaces — a decision-OS/registry, the “Kev-style” *advice* channel, a cross-project *transfer* store, a **model-health** dashboard, a **training-data** governance plane, a **device/surface** decider (thin), and a **provenance/audit** plane.

Best-first:

- **Stand up the Decision Registry as a first-class, versioned store** (FEATURE) — value 5 — effort M — risk low — category: architecture
  Why: “what it does, how it is measured” implies a stable address for every slot/verdict. The pack shows slots and a champion/challenger registry in passing, but no single registry that is the source of truth for: slot, model, schema, abstain policy, bench baseline, last-retrain hash, and per-project opt-out. Without it, “improves every Rune” has no place to record.
  Done when: `sampo decide registry list` prints every slot with model, schema version, baseline bench, and abstain threshold; a new slot cannot be adopted without a registry row.

- **Add the “Kev-style” advice channel: the decider answers the *user*, not just the task** (FEATURE) — value 5 — effort M — risk med — category: interface
  Why: the user asked for “a better Kev-style decider and more.” Kev is a *person* the user talks to, not a classifier. The pack’s ideas treat the decider as a per-slot judge. A full decider also answers routine asks (“should I split this task?”), pre-drafts the user’s next steer, and says “I’d re-ask this in 6 days.” That’s the breadth nobody in the pack mapped.
  Done when: `sampo ask` (or the existing `fm ask` path) routes to the decider for the three most common ask classes, with a measured “user did not have to re-ask” rate per class.

- **Build the Transfer Store: lessons and priors flow *between* projects on this box** (FEATURE) — value 5 — effort L — risk med — category: genericity
  Why: “generic across every project built or managed with Sampo” is the core ask. The pack has per-project adapters and federate-weights, but no *cold-start* mechanism: when a new project lands, what does the decider already know? A transfer store of redacted, outcome-labeled priors (from sibling projects’ closed briefs) is the missing breadth.
  Done when: a canary project with <20 briefs gets a decider that answers with a measured confidence (not abstain) on 3 of the 5 most common ask classes, sourced from the transfer store.

- **Model-Health Dashboard: one screen per slot — bench, abstain rate, drift, cost, last retrain** (FEATURE) — value 4 — effort M — risk low — category: ui
  Why: thin: ui. The pack has per-slot bench and abstain, but no single surface the user or a cold reader can open and see “is this slot healthy?” A full decider is a *fleet*, and a fleet needs a health view. This is the “what a complete version does” item the pack’s UI ideas (forge runes, chimes) don’t cover.
  Done when: `sampo decide health` (and a web UI page) prints, per slot: bench score, abstain rate, drift delta vs. baseline, cost per call, last retrain hash, and a pass/fail against the slot’s statistical floor.

- **Training-Data Governance Plane: provenance, redaction, exclusion, and a “silent-cut” audit on every row** (FEATURE) — value 5 — effort M — risk low — category: data
  Why: “what it is trained on” is a first-class ask. The pack has quarantine-by-provenance and redaction, but no *plane*: a single store where every training row carries its provenance tag, its redaction state, its exclusion flag, and a “silent-cut” count (how much was cut, what remains). The user’s own words flag “silent-cut scan fails” as a real failure.
  Done when: `sampo decide data audit` lists every row’s provenance, redaction status, and silent-cut count; any row from a tool result or repo file is excluded by default.

- **Provenance & Audit Plane: every verdict is a git-traceable, replayable line with a proof chain** (FEATURE) — value 5 — effort M — risk low — category: audit
  Why: “how it is measured” and “how it improves every Rune” both require an audit trail. The pack has “replayable ledger line” and “model verdict as git object,” but no *plane* that ties a verdict to the exact model hash, the exact training-lake hash, the exact bench, and the exact slot policy that produced it. Without it, a Rune generation’s improvement claim is not reproducible.
  Done when: `sampo decide audit <verdict-id>` prints the model hash, lake hash, bench, slot policy, and a replay command that reproduces the verdict on a scratch machine.

- **Serve the decider as a pinned, content-hashed, fail-over-capable local stack with a 100 ms budget per call** (FEATURE) — value 4 — effort L — risk med — category: serving
  Why: “how it is trained and served on this box” is explicit. The pack has pin-by-digest and fail-over in passing, but no serving contract: a 100 ms per-call budget, a cold-start time, a GPU-sharing policy with the moons funnel and exams, and a “model gone” rehearsal. This is the breadth item the pack’s serving ideas (pin, shadow, museum) don’t fully cover.
  Done when: `sampo decide serve status` prints p99 latency, cold-start time, GPU allocation, and fail-over target; a “model gone” rehearsal passes with the rules fallback within 1 s.

- **Make “does the decider beat plain” a permanent, nightly, falsifiable claim with a confidence interval** (FEATURE) — value 5 — effort M — risk low — category: measurement
  Why: “how it is measured” is the ask. The pack has leave-one-project-out and shadow mode, but no *permanent, nightly* claim with a CI. A full decider must answer “is it earning its tokens?” every night, not just at Rune generation. This is the breadth item the pack’s measurement ideas (bench, scorecard) don’t fully cover.
  Done when: `sampo decide claim` prints, per slot: decider vs. plain, with a 95% CI, last 30-day trend, and a pass/fail against the slot’s floor; the claim is re-run nightly.

- **The “Next-User” surface: the decider drafts the user’s next steer and answers routine asks, with a measured “user did not have to type” rate** (FEATURE) — value 4 — effort M — risk med — category: interface
  Why: “and more” in the request, plus the user’s own words (“we will want it to be a generic model… maybe brainstorm on features the model should have”). The pack has “user twin” and “draft the user’s next steer” as wild ideas, but no *surface*: a single `sampo ask` or `sampo next` that the user sees, with a measured rate of “the user did not have to re-ask.” This is the breadth item the pack’s interface ideas (veto, propagate) don’t fully cover.
  Done when: `sampo next` prints, per session, the top 3 predicted asks with confidence; the measured “user did not have to type” rate is printed in `samo doctor`.

- **The “Rune Improvement” loop as a closed, causal, re-benched pipeline with a per-generation delta** (FEATURE) — value 5 — effort L — risk med — category: training
  Why: “how it improves every Rune generation” is the final ask. The pack has “Rune retrain” and “champion/challenger,” but no *closed loop* that ties a Rune generation’s training to its measured delta vs. the previous generation. This is the breadth item the pack’s training ideas (regret, adapters, distil) don’t fully cover.
  Done when: `sampo decide rune <gen>` prints the training delta, the bench delta, and the abstain-rate delta vs. the previous generation; a negative delta files a regression task.

- **wild — The decider as a “living rulebook”: compile its decisions into a versioned, user-editable rules file** (FEATURE) — value 5 — effort L — risk high — category: interpretability
  Why: wild, and a genuine gap. The pack has “readable rulebook” as a wild idea, but no *capability*: the decider’s decisions are compiled into a versioned rules file that the user can read and edit, and the model is re-trained to match the edited rules. This is the breadth item nobody in the pack mapped.
  Done when: `sampo decide rules` prints the current rules file; the user edits it; the next retrain produces a model that matches the edited rules on a held-out set with a measured delta.

- **wild — A “decision distillation” pipeline from the user’s own `fm decide` logs, with a “user did not override” rate** (FEATURE) — value 4 — effort M — risk med — category: data
  Why: wild, and a genuine gap. The pack has regret/undo labels, but no *pipeline* that mines the user’s own `fm decide` history into a training set, with a measured “user did not override” rate. This is the breadth item the pack’s data ideas (regret, provenance) don’t fully cover.
  Done when: `sampo decide distill` runs on the last 90 days of `fm decide` logs, produces a training set with a measured “user did not override” rate per class, and files a retrain task if the rate drops below a floor.

- **wild — The decider as an “adversary” in the moons funnel: it kills moons the generator can’t defend** (FEATURE) — value 4 — effort M — risk med — category: measurement
  Why: wild, and a genuine gap. The pack has “Ward attacker” and “adversary,” but no *capability*: the decider runs as a kill-judge in the moons funnel, killing moons that the generator can’t defend, with a measured “false-kill” rate. This is the breadth item the pack’s measurement ideas (bench, claim) don’t fully cover.
  Done when: the moons funnel’s kill stage calls the decider as a judge; `sampo decide funnel` prints the decider’s kill rate and false-kill rate vs. the current kill stage.

- **wild — A “decision museum”: a frozen copy of the first decider, re-run on every close forever, as a tripwire for drift** (FEATURE) — value 4 — effort M — risk low — category: audit
  Why: wild, and a genuine gap. The pack has “museum model” in passing, but no *capability*: a frozen copy of the first decider, re-run on every close, with a measured “drift” vs. the live model. This is the breadth item the pack’s audit ideas (provenance, replay) don’t fully cover.
  Done when: `sampo decide museum` prints the frozen model’s verdict on the last 30 closes, with a measured drift delta vs. the live model; a drift delta above a floor files a retrain task.

- **The “device” surface: a thin, read-only decider for phone, car, and watch — “what’s my top predicted ask?” and “veto this class”** (FEATURE) — value 3 — effort M — risk low — category: devices
  Why: thin: devices. The pack has “phone” and “car” in passing, but no *surface*: a thin, read-only decider that answers “what’s my top predicted ask?” and lets the user veto a class of decisions, with a measured “user acted on it” rate. This is the breadth item the pack’s device ideas (phone push, watch) don’t fully cover.
  Done when: a phone surface prints the top 3 predicted asks with confidence; a “veto this class” action is logged and the decider’s abstain rate for that class drops by a measured delta.

Next question: What is the *smallest* set of ask classes (3–5) where the decider’s advice channel would measurably reduce the user’s re-asks in the first 30 days, so we can set the floor for “the model should say nothing” before training?
Next question: Which single device surface (phone, car, watch) would the user actually *touch* for a decider veto in the first week, so we can set the device-surface floor before building it?
