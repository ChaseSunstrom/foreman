# Brainstorm — lens: reasoning and thought process

- **Keep a falsifiable-belief board per task** — FEATURE — value 5 — effort M — risk low — category: reasoning
  Why: the debugger has ranked hypotheses and `fm task hypo` exists, but only for FIX. Assumptions (`fm task assume`) and hypotheses are separate stores, and the pack's "assumptions with confidence" in briefs are never re-tested during execution. Assumption: beliefs about the code (where a bug is, what a function does, why a test fails) are stated in prose and silently go stale.
  Done when: every belief a step relies on is a row with a confidence, a cheap probe, and a status (untested/confirmed/refuted); `fm task done` refuses while a load-bearing belief is untested; a refuted belief prints the steps that depended on it.

- **Decompose by risk-first spike ordering** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: planning.md sequences steps, but the pack shows no ordering by uncertainty. Assumption: plans put easy steps first, so a wrong core assumption is found after most of the work is done.
  Done when: for M/L plans, `fm plan` tags each step with an uncertainty score and orders the riskiest first with a one-command probe; a test shows a plan with an unknown API call placing it before UI wiring.

- **Run a premise check before planning** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the pack lists "detect the XY problem" and "capture contradictions", but both are about the request. This is about the brief's facts: file X exists, function Y is called from Z, the failing test fails as described. Assumption: briefs are written from the request and recall, not from a quick look at the code.
  Done when: before a brief is accepted, `fm-scout` verifies each factual claim in it (path, symbol, command output) and the brief shows confirmed/not-found beside each; a mismatch is shown at the top.

- **Pick the approach with a decision matrix that records the rejected options' kill reasons** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: M/L briefs require 3+ options, but nothing says why the losers lost, so later steers or failures can't reopen them. Assumption: the options section is currently prose.
  Done when: each option has criteria scores and a one-line "would be chosen if…" condition; when a step fails twice, `fm` surfaces the options whose condition now holds.

- **Replace the third failed attempt with a structured "what do I now know" reset** — FEATURE — value 5 — effort M — risk low — category: debugging
  Why: today 3 failed attempts → block with diagnosis. Assumption: the diagnosis is written after giving up, not used to change strategy. Before blocking, a forced step would list what each attempt ruled out, switch the method (bisect, minimal repro, instrument, ask recon), and only then block.
  Done when: the third failure triggers a reset record (ruled out / still possible / new method) and the fourth attempt must name a different method than attempts 1–3; a test asserts a repeated method is rejected.

- **Calibrate stated confidence against outcomes** — FEATURE — value 4 — effort M — risk low — category: judgement
  Why: briefs carry assumption confidences and `fm bench` has outcomes, but nothing compares them. Assumption: "high" confidence is applied loosely.
  Done when: `fm calibrate` prints, per confidence band, the share of assumptions that held, and intake shows the project's own hit rate next to each new confidence label.

- **Add a devil's-advocate pass that must argue for the rejected option** — FEATURE — value 3 — effort S — risk low — category: reasoning
  Why: `fm second` debates a plan, but as a free critique. Assumption: critiques tend to agree with the plan. Forcing the second reader to build the strongest case for the runner-up, then the main thread to answer it point by point, produces a recorded rebuttal.
  Done when: for L plans, the brief stores the runner-up's best case and a written answer to each point; missing answers block plan approval.

- **Reason in a scratch ledger that survives compaction** — FEATURE — value 5 — effort M — risk med — category: thought process
  Why: Foreman resumes at the exact step after `/compact`, but the reasoning behind the step (what was tried, what surprised, the half-formed theory) is lost; only state survives. Assumption: the reasoning is the thing most lost.
  Done when: `fm think "<note>"` appends typed notes (theory, surprise, ruled-out, next) to the task, and the resume packet includes the last N; a test compacts mid-task and the resumed session sees the theory note.

- **Wild: Hold an inner monologue review where a cheap model reads the transcript for reasoning errors** — FEATURE — value 3 — effort M — risk med — category: meta-reasoning
  Why: wild. Assumption: logic slips (confirmation bias, anchoring on the first hypothesis, claiming a cause with no probe) have recognisable shapes. A Haiku-class reader tags them live and the main thread gets a one-line nudge.
  Done when: on a fixture transcript with a planted "declared cause with no probe", the reader flags it within one turn, and a clean transcript yields no flag.

- **Wild: Play out the plan in a "tabletop" before touching files** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild. A read-only agent walks the plan step by step against the real tree, predicting each diff and gate result; where its prediction can't be formed (missing symbol, ambiguous owner), the plan is wrong. Cheaper than finding out in a worktree.
  Done when: `fm tabletop T-xxxx` outputs per-step predicted files and expected outcomes, flags unresolvable steps, and a later comparison shows the prediction hit rate.

- **Wild: Keep a "what would change my mind" line on every decision** — FEATURE — value 3 — effort S — risk low — category: reasoning
  Why: wild; related to decision tripwires, but this is stated at decision time as an observable, not a file pattern. Assumption: tripwires are file-based and miss evidence-type triggers like "if the p95 exceeds 200ms".
  Done when: `fm decide` requires a refutation condition with a check command; the sentinel runs it, and a failing check reopens the decision.

- **Classify the kind of difficulty and pick the agent mix from it** — FEATURE — value 4 — effort M — risk med — category: agent selection
  Why: today agent types are fixed roles chosen by the main thread. Assumption: tasks differ in difficulty kind (unknown location, unknown cause, unknown API, ambiguous intent, large mechanical change) and each wants a different mix. Intake would tag the kind and propose a mix, learned from bench outcomes.
  Done when: intake emits a difficulty kind with a suggested staffing (e.g. unknown cause → debugger×2 with different seeds + scout), and bench compares it with the default staffing on replayed tasks.

- **Separate "understood" from "done" with a comprehension check before editing** — FEATURE — value 4 — effort S — risk low — category: understanding
  Why: the pack shows read-before-edit coverage as an idea, but not a statement of understanding. Assumption: edits begin right after reading. Requiring a three-line "how this code works, what I'll change, what could break" that a scout can falsify against the code catches misreadings early.
  Done when: the first edit on an M/L task is blocked until the comprehension note exists, and a scout check marks each claim as supported or contradicted.

- **Learn which reasoning moves worked per task type** — FEATURE — value 4 — effort L — risk med — category: learning
  Why: lessons are facts about the project; none record method (bisecting first, reading the test before the code, asking recon). Assumption: ledger events already show the order of moves. Mining first-time-pass tasks for move sequences by type gives a ranked "start here" for the next one.
  Done when: for FIX tasks, intake shows the top two opening moves from past clean passes with their pass rates, and a replay shows tasks that followed them passing more often than ones that did not.

- **Wild: Let a second Foreman argue the user's side of every steer** — FEATURE — value 2 — effort M — risk med — category: reasoning
  Why: wild. Assumption: steers like "build it in Tauri" encode reasons never stated. A pass infers the reason, writes it as a testable principle, and shows the user "I think you meant X" for confirmation.
  Done when: after a steer, a one-line inferred principle is stored as unconfirmed; the user's accept or reject updates it, and rejected principles are never applied.
