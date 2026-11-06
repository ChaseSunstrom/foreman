# Brainstorm — lens: exam arms for local models

- **Pair every not-yet local model with a path-it-replaces arm** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: the steer says selfjev-4b, jeff, Jevlike and Von wait on an exam arm against the path they replace; the pack shows Louhi has a Smith-on-local arm (T-2908) but no replaced-path baseline per item.
  Done when: `sampo louhi models` prints, for each of the four, a row of local-arm vs replaced-path-arm pass rate on the same held-out scenarios, and promotion refuses without it.

- **Add a tool-acquisition scenario family to Louhi** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: Mission 7 (#5) has no scored scenarios; the pack shows exams for models and Smith but none for find/build/test/use/queue-grant. Assumption: scenarios are authored by the tool-less child that never sees Sampo code.
  Done when: ≥12 scenarios each grade five stages separately (found, built, tested, used, grant queued) and the scorecard lists per-stage rates per model.

- **Grade the install-grant request, not just the tool** — FEATURE — value 4 — effort S — risk low — category: exam
  Why: "install grants queued" is part of the mission; a model that installs directly or asks vaguely must fail.
  Done when: a scenario where the correct move is queueing a grant fails any arm that runs an install, and passes only a grant naming one tool, source, hash and reason.

- **Plant decoys: tool already on PATH, tool in a stack card, tool that's unneeded** — FEATURE — value 4 — effort S — risk low — category: exam
  Why: the user steer says missing tools are found via manifests and stack cards; models that rebuild an existing tool waste a run. "Should have declined" must score as a pass.
  Done when: three decoy scenarios exist and an arm that builds when it should reuse scores 0 on them.

- **Run a scaffold ladder per local model and report the lowest passing rung** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: the standing steer is that cards and playbooks let 27B/9B/4B match frontier; nothing in the pack shows how much scaffold each model needs. Rungs: bare, card, card+grammar menu, card+frontier hint.
  Done when: each model has a row naming the lowest rung reaching frontier-parity on the tool scenarios, with cost per verified pass.

- **Hold cards out from the model that wrote them** — SECURITY — value 4 — effort S — risk low — category: exam integrity
  Why: T-2909 lets the 27B write cards; a card tested only by its author overfits. This matches the standing rule on signals Sampo didn't author.
  Done when: the card exam refuses a card whose scoring model equals its authoring model, and says so.

- **Batch exam arms by resident model** — PERFORMANCE — value 4 — effort S — risk low — category: exam cost
  Why: the user said a llama-swap model switch costs ~3 minutes with no detection, and to use the 27B first. Interleaved arms burn that.
  Done when: a full multi-model run performs at most one switch per model, logged, and the run plan prints the switch count before starting.

- **Add a negative-control stage to the tool exam** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: "tests it" is easy to fake; a model-built tool whose test also passes on a deliberately broken tool didn't test anything.
  Done when: each built tool is rerun against a planted-broken variant and scores tested only if its test fails there.

- **Poison one card per run and score blind following** — SECURITY — value 4 — effort S — risk med — category: exam robustness
  Why: thousands of small-model cards are the plan; a model that follows an unsafe card step is a supply-chain hole. Pairs with the Ward.
  Done when: a card with a planted unsafe step is blocked or flagged by every promoted model, else the model is marked not trusted with cards.

- **Wild: nightly gladiator league on idle local hardware** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: wild; assumption: the box is idle overnight. Every local model plays every card and scenario, leaderboard goes to the Models page, one swap per model.
  Done when: a morning leaderboard exists with per-model, per-card lift and the next card to write for the weakest cell.

- **Wild: a tool forge duel judged only by the scenario's own tests** — FEATURE — value 4 — effort M — risk med — category: exam
  Why: wild; the same missing tool is built by the 27B, 9B and a frontier model, and tests the builders never saw pick the winner, feeding build-versus-find evidence.
  Done when: a duel prints winners with tokens, minutes and hidden-test pass counts for each builder.

- **Wild: the dumbest-model floor printed on every card** — FEATURE — value 3 — effort M — risk low — category: exam
  Why: wild; each card records the smallest model passing its task bare-versus-card, so routing and retirement use data.
  Done when: `sampo cards show ID` prints "floor: <model>" with the run that proved it, and a card passed bare by its target model is flagged for retirement.

- **Score cost per verified pass including model-swap time** — PERFORMANCE — value 3 — effort S — risk low — category: exam
  Why: the steer wants local to match frontier through scaffolding; without cost in the denominator a 4B at 10 retries looks equal to a 27B at one.
  Done when: the scorecard shows wall-clock, tokens and swaps per verified pass per arm.

Next question: Which of the not-yet items has no scenario set at all today, so its exam arm would have nothing to run on?
Next question: Do the exam scenario authors (tool-less children) produce enough tool-gap cases in languages and stacks the cards don't cover yet?
