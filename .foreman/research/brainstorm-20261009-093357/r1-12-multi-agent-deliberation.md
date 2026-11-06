# Brainstorm — lens: multi-agent deliberation

- **Run a structured plan deliberation with fixed roles** — FEATURE — value 5 — effort M — risk low — category: deliberation
  Why: Intake produces one plan and `fm second` gives a single opinion. The pack lists "planner/critic/executor tournament" but not a protocol with roles that must produce different artifacts. A fixed round (proposer, skeptic who must name a falsifying probe, simplifier who must cut a step, and a judge who must cite which objection changed the plan) makes disagreement structured rather than a vibe.
  Done when: `fm deliberate T-xxxx` on an M/L task writes a record with each role's artifact and a "plan changed because" line; a test with a seeded flawed plan shows the skeptic's probe altering the final steps.

- **Hold a pre-registered vote before any tiebreak** — FEATURE — value 4 — effort S — risk low — category: deliberation
  Why: Reviewers and seconds are consulted after the main thread has already leaned. Assumption: anchoring on the main thread's plan is the weak point. Each panelist commits an answer and confidence blind (hashed into the ledger) before seeing others' answers, then they are revealed together.
  Done when: the deliberation record stores every panelist's commitment with a timestamp earlier than any reveal, and a test fails if a panelist's prompt contains another's answer.

- **Score disagreement as the escalation signal** — FEATURE — value 5 — effort M — risk med — category: deliberation
  Why: "Ask the user only when sampled plans disagree" is listed, but nothing defines how to measure disagreement for plans, which are prose. Compare the sets of touched files, ordered steps and verify commands across panelists, and treat low overlap as "ambiguous request" (ask) and high overlap as "proceed", with the thresholds calibrated on `fm bench` cases.
  Done when: `fm deliberate --score` prints a disagreement number from 0 to 1, and on a bench set of known-ambiguous and known-clear briefs it separates the two groups with a stated threshold.

- **Assign each panelist a distinct failure to hunt** — FEATURE — value 4 — effort M — risk low — category: deliberation
  Why: Existing audit lenses (self, intent, adversary, edge, operator, maintainer) are used on finished work. "Staff reviewer panels for decorrelated errors" is listed generally. A plan-time version assigns each panelist a different cause of death (wrong requirement, wrong abstraction, wrong order, hidden coupling, unverifiable criterion) so errors are not shared.
  Done when: running the panel on an L plan yields findings tagged by assigned failure class, and each class has at least one prompt that differs materially from the others (checked by a test on the rendered prompts).

- **Make a dissent register that survives to done** — FEATURE — value 4 — effort S — risk low — category: deliberation memory
  Why: When a plan is chosen over a rival, the losing argument is lost. Assumption: this is why some failures repeat. Record each overruled objection with its reopen trigger, and at done require a line stating whether the objection materialised.
  Done when: `fm task done` on a deliberated task lists unresolved dissents and refuses to close until each is marked materialised, did not, or unknown.

- **Run a steelman-then-attack debate on risky decisions** — FEATURE — value 4 — effort M — risk med — category: debate
  Why: `fm second debate` exists, but two sides arguing their own cases tend to talk past each other. Require each side to restate the opponent's best argument to the opponent's satisfaction (a third agent confirms the restatement) before rebuttal.
  Done when: a debate transcript contains a restatement accepted by the opposing side before any rebuttal, and the run fails if the acceptance step is skipped.

- **Calibrate panelists by how often they were right** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: "Weight reviewers by measured precision" exists for review. Extend it to deliberation: record each role's position against the eventual outcome (rework, reverts, escapes) and weight votes accordingly. Assumption: the ledger has enough outcomes to estimate this per role.
  Done when: `fm deliberate --weights` shows per-role hit rates computed from finished tasks, and the vote tally uses those weights, with a unit test on a synthetic history.

- **Cap deliberation cost by stakes** — FEATURE — value 3 — effort S — risk low — category: cost control
  Why: Panels are expensive, and the first brainstorm covers budgets generally. Tie panel size to tier and reversibility: S tasks get none, M get a single skeptic, L or irreversible get the full panel.
  Done when: a table-driven test shows panel composition per tier and reversibility, and `fm deliberate` on an S task exits with "no panel needed" and the reason.

- **Wild: Seat a standing devil's advocate who is paid only for being right** — FEATURE — value 3 — effort M — risk med — category: deliberation (wild)
  Why: wild. An agent whose only job is to oppose gets discounted over time. Reward it only when its objection materialises, so its prompt and persistent memory are tuned on hits, and it learns to stay silent when it has nothing.
  Done when: the advocate's objection rate falls on tasks where no dissent materialised, measured on bench replay, while its hit rate holds or rises.

- **Wild: Convene the past-failure jury** — FEATURE — value 3 — effort M — risk med — category: deliberation (wild)
  Why: wild. Instead of a generic panel, summon three agents each primed with one past failure from `fm recall` that most resembles the current plan, and let each argue "this is how it happens again." Distinct from the "post-mortem court" idea in that jurors are drawn per plan from the closest failures.
  Done when: for a plan resembling a recorded failure, the jury cites that failure's task id and the plan is amended or the objection is explicitly rejected with a reason.

- **Wild: Let panelists trade a limited budget of probes** — FEATURE — value 3 — effort L — risk high — category: deliberation (wild)
  Why: wild. Disagreements are usually settled by argument. Give each side a few cheap, read-only experiments (run this test, grep that call site) and let the evidence, not the rhetoric, decide. Related to "settle disagreements with an experiment agent", but here the debaters spend the probes themselves under a shared cap.
  Done when: a seeded disagreement over whether a function is called anywhere is resolved by a probe, and the record shows the probe command and its output as the deciding evidence.

- **Require the judge to write a minority report** — FEATURE — value 3 — effort S — risk low — category: deliberation
  Why: Judges tend to merge views into a bland compromise. Force the verdict to include the strongest rejected position in its own words, which feeds the dissent register and gives the user a fair view if they open the record.
  Done when: every verdict record has a non-empty minority section, and a lint rejects a verdict whose minority text is a substring-paraphrase of the winning text.

- **Detect groupthink between panelists** — FEATURE — value 3 — effort M — risk med — category: deliberation
  Why: Panelists from the same model share blind spots, so unanimous agreement can be false confidence. Mix model families or temperatures where available and flag runs where the panel agrees too perfectly on a task type that history shows is error-prone.
  Done when: a unanimous panel on a task type with a past escape rate above a threshold is flagged "agreement unverified", and the flag appears in the done summary.
