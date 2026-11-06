# Brainstorm — lens: cognitive architectures (research frontier)

- **Plan by recognition before enumeration** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: intake always builds 3+ options for M/L, but a task with a close solved look-alike (fm recall) is usually the known play. Recognition-primed decision-making means retrieve the prototype, mentally simulate that one option, and only fall back to enumeration if the simulation hits a snag. Assumption: recall can score "prototype strength" well enough to gate this.
  Done when: a task whose brief matches a past finished task above a set similarity gets a one-option plan with a written simulation. A seeded snag in that simulation forces the full option table.

- **Warn on false-friend analogies** — FEATURE — value 4 — effort S — risk low — category: recall
  Why: the pile has "plan from solved look-alikes" and "map problems by relational structure", but nothing guards against a similar-looking case that differs in the one way that matters. Hippocampal pattern separation does this: next to each analogue, list its structural differences (different file layer, different failure class, different harness).
  Done when: recall output for a planned task shows, per analogue, "same:" and "differs:" lines. A fixture pair of near-duplicate briefs with a differing key detail surfaces that detail.

- **Reconsolidate lessons when they're recalled** — FEATURE — value 4 — effort M — risk med — category: memory
  Why: T-0217 gives lessons confidence, but lessons are only written at finish and never revised. In memory reconsolidation, recalling a trace makes it editable. At finish, each lesson recalled during the task is reopened: narrow its scope, split it, or reword it with the new evidence, and the diff is logged.
  Done when: finishing a task that recalled a lesson leaves a revision entry on that lesson (kept, narrowed, split, or contradicted). `fm recall` shows its revision count.

- **Monitor conflict at action time** — FEATURE — value 4 — effort M — risk med — category: executive control
  Why: the pile covers static contradictions and precedence, but not the moment a veto, a lesson and the brief pull toward different next actions. An anterior-cingulate-style conflict monitor, run before each step, checks the active constraints against the intended action. Conflict raises deliberation, such as a second read or a precedence-resolution note, instead of silent compliance with one side.
  Done when: a fixture where a veto and a brief criterion disagree on the next edit produces a recorded conflict event naming both, plus the winner and why.

- **Add a reflex layer below the model** — FEATURE — value 4 — effort M — risk med — category: architecture
  Why: friction fixes today become prose rules the model must remember. Brooks-style subsumption puts fast stimulus→response reflexes in the hooks, with the model layer above them. Each reflex is a tiny recorded rule (for example "after editing X, run the linked test"), promoted from repeated friction and logged when it fires. Assumption: the existing hooks can run these cheaply.
  Done when: a promoted reflex fires on its trigger with no model turn and appears in the ledger. Removing it restores the prior behaviour.

- **Keep an inhibition ledger of suppressed urges** — FEATURE — value 3 — effort S — risk low — category: executive control
  Why: Foreman "captures new requests instead of chasing them", but captures only what the user asked for. Record what the agent itself was tempted to do (adjacent refactor, extra test, scope creep) and declined, with a one-line reason. Review these at done, and they feed the over-build and gold-plating checks.
  Done when: `fm task done` lists inhibited impulses. A seeded "while here I could…" note shows up there and not in the diff.

- **Segment episodes at surprise boundaries for recall** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: recall is BM25 over whole briefs. People store experience as events cut where prediction fails. Cut each ledger into episodes at surprises (a failed prediction, a block, a steer), and index and retrieve episodes with their before and after context. Assumption: "log surprises from stated predictions" supplies the boundary signal.
  Done when: `fm recall` can return a single episode (for example "the guard-block loop") rather than a whole task. The episode includes its trigger and resolution.

- **Keep a transactive-memory directory** — FEATURE — value 3 — effort M — risk low — category: knowledge routing
  Why: the pile has asking by information gain and interrogating the memory, but no registry of who knows what. For each fact class, record where the answer lives (the user's head, repo, docs, ledger, web, a past task) and the cost of getting it. Foreman then routes a question to the cheapest source, and asks the user only for facts classed "user-only".
  Done when: a question tagged "naming preference" resolves to the taste model or user. One tagged "test command" resolves to `fm map` with no user ask.

- **Extract explicit rules from implicit outcome statistics** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: the ledger holds thousands of outcomes with features such as tier, files touched, and plan shape. CLARION-style bottom-up learning fits simple stumps and rule lists, such as "tasks touching fmguard without a red-first proof escape 3× more". Each rule is shown as a candidate with held-out accuracy and never auto-applied.
  Done when: `fm friction` or `fm bench` lists at least one candidate rule with its support count and held-out hit rate, reproducibly on the same ledger.

- **Test new lessons for interference** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: complementary-learning-systems theory says fast new learning can overwrite old behaviour unless old cases are interleaved. Before a lesson or instruction edit is promoted, replay a sample of previously passing bench cases and block promotion if any regress. This differs from the embargo on born-from lessons, which is about leakage.
  Done when: adding a lesson that deliberately contradicts a past pass makes the interference gate fail, naming the regressed case.

- **Wild: Arbitrate habit against deliberation, with devaluation probes** — FEATURE — value 3 — effort M — risk med — category: dual-process
  Why: model-free versus model-based control. Per task type, track how often the cached playbook gave a clean pass; when it is strong, run it directly. Periodically force a cold re-derivation of the plan and diff it against the habit. A mismatch means the world changed (new Claude Code version, new repo layout) and the habit is demoted. Wild.
  Done when: a seeded environment change (a renamed gate) makes a periodic probe flag the stale playbook and drop its habit strength.

- **Wild: Keep a common-ground ledger per delegation** — FEATURE — value 3 — effort M — risk low — category: multi-agent
  Why: grounding in dialogue says communication is cheap once both sides know what's mutual. For each child agent, keep the set of facts both main thread and child provably share, and brief only the delta. On return, check which assumed common-ground items the child contradicted. Wild.
  Done when: a second brief to the same lane omits facts already grounded. A child that contradicts one gets that item flagged as a grounding failure.

- **Wild: Lesion one faculty at a time to find double dissociations** — FEATURE — value 2 — effort L — risk low — category: evaluation
  Why: neuropsychology infers separable faculties by selectively damaging them. Run bench with recall off, then with second opinions off, then with the conflict monitor off, and so on. Compare the failure signatures: if two lesions fail on different task classes, the faculties are doing distinct work, and if they fail the same way, one is redundant. This goes past a plain ablation into a map of what each thinking organ is for. Wild.
  Done when: a report pairs each faculty with the task classes that degrade without it. Any pair with identical signatures is flagged as a candidate for merging.
