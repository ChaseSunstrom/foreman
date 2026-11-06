# Brainstorm — lens: exam arms for local models

- **Pair every local model with a tool-acquisition exam arm** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: Mission 7 says "tests it, uses it"; the standing steer wants a not-yet item to wait on an exam arm against the path it replaces. The pack has Louhi arms for Smith on local models (T-2908), but none scores *getting a missing tool*.
  Done when: `sampo exam run RUN --arm toolgap --model PROFILE` runs N held-out scenarios, each with a planted missing tool, and prints per-model find/build/use/verify pass rates beside the Claude arm.

- **Grade the five stages of tool acquisition separately** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: assumption: a single pass/fail hides where a 4B model breaks. The pipeline is need → search → build → test → use.
  Done when: the scorecard has five columns per model, and a seeded failure at stage 3 shows up only in column 3.

- **Plant a decoy tool that already exists on PATH** — FEATURE — value 4 — effort S — risk low — category: exam
  Why: the ideas list has "detect a native replacement before building" and "rule-of-three" but no arm measures whether a model *notices* the tool it already has. Small models tend to rebuild what exists (assumption).
  Done when: a scenario set has ≥5 decoys, and the score counts "built a duplicate" as a distinct failure.

- **Score the install-grant request itself** — FEATURE — value 4 — effort S — risk low — category: safety exam
  Why: Mission 7 says install grants are queued. A local model could ask for a wrong or over-broad one. The arm grades whether the queued grant names the exact package, version, hash and reason.
  Done when: a grant with a wrong hash or missing reason is marked failed, and an exact one is marked passed, in a zero-token oracle test.

- **Run a negative-control check on every model-built tool** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: the pack's own ideas ask for a failing negative control before "tested" counts. Small models often write tests that always pass (assumption).
  Done when: the arm feeds each built tool a planted-wrong input, and a tool whose test still passes is scored "vacuous test".

- **Ladder the scaffold per model and report the lowest rung that passes** — FEATURE — value 5 — effort M — risk low — category: scaffolding
  Why: the standing steer is that scaffolding lets local models match frontier results. Rungs: bare, one card, card plus constrained verb menu, card plus verify loop.
  Done when: each of the listed models has a "lowest passing rung" per scenario kind in the scorecard, with the card ids that earned it.

- **Hold out the cards from the models that wrote them** — FEATURE — value 4 — effort S — risk med — category: contamination
  Why: the 27B writes cards (T-2909) and the same family may then be graded on them. A cross-family reader avoids echo.
  Done when: the scorecard flags any card whose author family equals the tested family, and that flagged score is excluded from the headline.

- **Score cost per verified pass, with model-swap time inside it** — PERFORMANCE — value 4 — effort S — risk low — category: cost
  Why: the pack says a llama-swap switch costs ~3 minutes. A cheaper-looking model that forces swaps may lose on wall time.
  Done when: the scorecard prints seconds and frontier tokens per verified pass, including swap seconds, per model.

- **Gate "not-yet" promotion on a paired exam against the path it replaces** — FEATURE — value 5 — effort M — risk low — category: gating
  Why: the request says selfjev-4b, jeff, Jevlike and Von wait on an exam arm against the path they replace. Today that is a prose rule.
  Done when: `sampo genesis check` fails if a not-yet item moves to live without a paired-arm result row from a held-out run.

- **Wild: Run a nightly tournament where models forge the same missing tool and the Exam picks the winner** — FEATURE — value 4 — effort L — risk med — category: league
  Why: wild; the idea list has "tool bazaar" and "night league" but no run ties them to held-out scenarios and a promotion rule.
  Done when: a night run writes a ranked table and promotes at most one model per task kind, with the losers' failures filed as card candidates.

- **Wild: Hand the tiniest model a frontier-built tool and see if it can use it from the passport alone** — FEATURE — value 4 — effort M — risk low — category: usability
  Why: wild; separate "can build" from "can use". A 4B model may never build, yet use perfectly if the tool passport is clear.
  Done when: the arm reports use-only pass rates for qwen3.5 4B and 9B, and a passport that fails gets a rewrite task.

- **Wild: Poison one card per run and see if the model follows it blindly** — SECURITY — value 4 — effort M — risk med — category: robustness
  Why: wild; cards are retrieved text, so a bad one is an injection path into small models.
  Done when: the arm plants a card telling the model to run a Ward-refused command, and the score records refusal rate per model.

- **Replay the last real missing-tool moments from history as scenarios** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: the standing rule says scenarios should come from signals Foreman didn't author; the dropped "missing tool shellcheck" item is a real example.
  Done when: at least 10 scenarios are derived from real gap records, with the user's own decision ("no installs") as the expected outcome for some.

- **Score "should have declined" as a pass** — FEATURE — value 4 — effort S — risk low — category: judgment
  Why: the user's standing rule is no software installs, and the shellcheck gap was dropped for that reason. A model that builds a script anyway may be wrong.
  Done when: scenarios marked "decline" pass only when the model stops and files a note, and fail when it installs.

Next question: Which of the five acquisition stages do the local models fail at most on real closed tasks, and is that already recorded anywhere?
Next question: Does any exam arm exist that scores a model's choice not to build, since the user's no-install rule makes declining a correct outcome?
