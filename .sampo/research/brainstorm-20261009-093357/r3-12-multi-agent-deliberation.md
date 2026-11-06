# Brainstorm — lens: multi-agent deliberation

- **Elect a facilitator who may not vote** — FEATURE — value 4 — effort M — risk low — category: deliberation
  Why: the pack has panels, debates, judges and dissent registers, but the judge is the main thread, which also planned the work and so grades its own plan. Assumption: the main thread's self-agreement is a real bias source.
  Done when: `fm second --facilitated` runs a panel where a separate fm-facilitator agent only frames the question, enforces the speaking order and writes the synthesis. The ledger shows it cast no verdict, and a test asserts a facilitator verdict is rejected.

- **Run a charter-first panel: agree the question before answering it** — FEATURE — value 4 — effort M — risk low — category: deliberation
  Why: "Sort every disagreement by its cause" and "Require a check that tells interpretations apart" imply panels often argue past each other. Assumption: many disagreements are about different questions, not different answers.
  Done when: before round one, each panelist restates the question in one line. When the restatements diverge by a measurable threshold, the panel stops and reconciles the framing first, with a test fixture of a deliberately ambiguous prompt.

- **Rotate roles between rounds** — FEATURE — value 3 — effort S — risk low — category: deliberation
  Why: fixed roles ("assign each panelist a distinct failure to hunt", "standing devil's advocate") let agents settle into a posture. Assumption: swapping sides surfaces which objections survive.
  Done when: a two-round panel run has each agent argue the opposing position in round two, and the output lists which objections persisted after the swap.

- **Make the panel's output a decision record with a stop-loss** — FEATURE — value 4 — effort M — risk low — category: decisions
  Why: "Give decisions revisit triggers" and "Give every approach kill-criteria" exist separately. Joining them means every panel verdict carries the observable that would void it. Assumption: today these are written by hand.
  Done when: `fm second` refuses to finish unless the verdict includes at least one kill-criterion that is a runnable check. `fm decide` stores it, and the check is re-run at sentinel or night time.

- **Price a panel by the cost of being wrong, and skip it when cheap** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: panels are costly, and the pack already caps deliberation by stakes, but nothing says which decisions are one-way. Assumption: the door classification exists in plan notes.
  Done when: a two-way-door S decision produces zero panel agents, a one-way L decision produces at least three, and a test asserts both from the ledger.

- **Debate with evidence budgets: no claim without a probe result** — FEATURE — value 4 — effort M — risk med — category: deliberation
  Why: debates run from the model's prior; "Settle reviewer disagreements with an experiment agent" is only a later step. Assumption: most panel disputes are empirically settleable in minutes.
  Done when: each panelist gets N read-only probes per round, and the transcript marks every claim as probed or unprobed. The judge may not weigh an unprobed claim above a probed one, and a test checks that.

- **Detect a panel that agrees too fast** — FEATURE — value 3 — effort S — risk low — category: deliberation
  Why: "Detect groupthink" is listed, but only as a post-hoc check. Assumption: early unanimity on L tasks is more often a shared blind spot than a correct answer.
  Done when: unanimous round-one verdicts on a one-way decision automatically trigger a forced-dissent round, and the ledger records `forced_dissent` with its outcome.

- **Wild: Hold a séance with the superseded plan** — FEATURE — value 3 — effort M — risk low — category: deliberation — wild
  Why: assumption: replans bury the original plan's reasoning, and abandoned plans often contained a correct insight. Convene an agent that argues, in the voice of the old plan, for what the new plan lost.
  Done when: on every replan, a "ghost" agent returns a list of claims the new plan dropped, and each claim is either answered in the brief or accepted as a recorded loss.

- **Wild: Run a two-model panel where each is blind to who the other is** — FEATURE — value 3 — effort M — risk low — category: deliberation — wild
  Why: assumption: a model grades output from its own family more kindly. Strip the model identity and the format tells, then let a different-vendor harness judge. The pack already has adapters for codex, gemini and opencode.
  Done when: `fm second --blind` routes each position through a normalizer that removes style markers. The report shows the blind verdict against the unblinded one on a bench case, with the disagreement rate recorded.

- **Wild: Let the lane that will do the work vote last, and cast a veto on infeasibility** — FEATURE — value 3 — effort M — risk med — category: deliberation — wild
  Why: assumption: plans are judged by reviewers who will not implement them, so unbuildable steps pass. Give the builder a structured "this cannot be done as written, because X" right that sends the plan back with a proof.
  Done when: a fm-builder can return `infeasible` with a failing probe attached, the plan reopens automatically, and a test shows a seeded impossible step caught before any edit.

- **Score panelists by what happened after, and re-weight votes** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: the pack proposes calibrating panelists and an outcome ledger separately. Assumption: they are not yet joined, so a vote has equal weight regardless of track record.
  Done when: each panel verdict stores per-role votes and, when the task closes or reworks, the ledger back-fills right or wrong. `fm second` then shows weighted votes, and a replay test shows a changed outcome with the weights.

- **Escalate by dissent shape, not count** — FEATURE — value 3 — effort S — risk low — category: deliberation
  Why: "Score disagreement as the escalation signal" treats disagreement as one number. Assumption: a 2–1 split on a risk is worse than a 2–1 split on style.
  Done when: dissent is tagged by axis (safety, scope, taste, correctness), safety dissent always escalates to the user, and taste dissent resolves from the stored vetoes. A fixture covers each axis.

- **Give each panel a written "what we did not discuss" section** — FEATURE — value 3 — effort S — risk low — category: deliberation
  Why: panels are bounded by their lenses, so omissions are invisible. Assumption: unspoken options are where late surprises come from.
  Done when: every panel verdict ends with a non-empty list of considered-and-skipped topics produced by a separate agent that sees only the question and the verdict, and an empty list is rejected.
