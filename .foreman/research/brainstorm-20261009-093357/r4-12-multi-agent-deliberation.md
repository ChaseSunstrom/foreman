# Brainstorm — lens: multi-agent deliberation

- **Seat jurors by voir dire** — FEATURE — value 4 — effort M — risk low — category: panel staffing
  Why: the pack has panel ideas on roles, weights and decorrelation, but none checks that a panelist understands the area before it votes. Assumption: a model with the right role card can still be blind to a subsystem like the guard.
  Done when: before seating, each candidate answers 2–3 cheap seeded questions about the touched files (answers known from `fm map` and the ledger), and a candidate who fails is replaced. A test with a deliberately uninformed stub shows it is never seated.

- **Anonymize and shuffle every proposal** — FIX — value 4 — effort S — risk low — category: bias control
  Why: the pack lists "probe reviewers for authority bias" as a wild idea, and nothing removes the bias. Assumption: panel inputs currently carry author, model and order.
  Done when: panel inputs use neutral labels in randomized order, and a bench A/B with the same proposals in swapped order gives the same verdict at least as often as before, with the rate recorded.

- **Negotiate the plan as tracked changes** — FEATURE — value 5 — effort M — risk med — category: plan negotiation
  Why: the pack's panels are vote-and-tally (votes, dissent, a judge). Assumption: when panelists co-edit one plan file instead, objections get resolved rather than tallied.
  Done when: `fm plan negotiate` yields one plan file where each change carries `resolves: <objection id>`, and the command refuses to finish while an objection is neither resolved nor waived by the judge.

- **Test verdict fragility by flip and paraphrase** — FEATURE — value 4 — effort M — risk low — category: verdict robustness
  Why: "rotate roles" exists, but no idea measures how brittle a verdict is. Assumption: a verdict that reverses when sides swap or the question is reworded is guesswork.
  Done when: a verdict record carries a fragility score from N paraphrase and side-swap re-runs, and a fragile verdict (below a threshold) is escalated instead of accepted. A fixture with a coin-flip question scores fragile.

- **Assign credit to the argument that carried the verdict** — FEATURE — value 4 — effort M — risk low — category: panel learning
  Why: "score panelists by what happened after" and "marginal contribution" credit people, not claims. Assumption: the argument graph records which cited claim moved the judge.
  Done when: after a task's outcome is known (rework, clean pass), `fm friction` lists the decisive arguments of the worst verdicts with their evidence type, and recall surfaces them in later plans.

- **Define deliberation protocols as data** — FEATURE — value 4 — effort L — risk med — category: orchestration
  Why: roles as data is already an idea, but the protocol (rounds, who sees what, stop rule, tiebreak) is still prose in skills. Assumption: `fm second` and `fm ideas` each hard-code their own rounds.
  Done when: one protocol file format drives plan, debate and brainstorm. `fm bench` can run two protocol files on the same finished tasks and report which gets the higher first-pass rate.

- **Stop seating panelists once the verdict is stable** — PERFORMANCE — value 3 — effort S — risk low — category: deliberation cost
  Why: "cap by stakes" fixes the budget up front. This is an anytime rule: add independent opinions one at a time and stop when k consecutive ones leave the verdict unchanged. Assumption: most panels over-seat.
  Done when: the panel runner halts early on stability, and a replay over past panels shows the same verdicts at fewer calls, with the savings printed.

- **Close every objection to a diff hunk** — FEATURE — value 4 — effort M — risk low — category: done gate
  Why: the dissent register survives to done, but nothing says where an objection was addressed. Assumption: reviewers' objections can be tied to files and lines.
  Done when: at done, each accepted objection maps to a hunk or an explicit waiver with a reason. An unmapped objection blocks the gate, and a test with one dropped objection fails.

- **Duel interpretations with failing tests** — FEATURE — value 5 — effort M — risk med — category: intake
  Why: the user's terse requests ("fix the login timeout") are ambiguous, and the pack has misreading and shared-prefix ideas but no way to settle which reading is meant. Assumption: a failing test written per reading is cheaper for the user to judge than prose.
  Done when: on a flagged-ambiguous intake, up to 3 panelists each write one failing acceptance test for their reading. The user is shown the test names and one-line behaviours, picks one, and the others are archived as non-goals in the brief.

- **Adjourn unresolved disputes to an overnight experiment (wild)** — FEATURE — value 3 — effort M — risk med — category: dream mode
  Why: dream mode and experiment agents exist separately, but a stalled panel currently just escalates to the user. Assumption: many disputes can be settled with a measurement.
  Done when: a deadlocked panel files a read-only experiment task with its hypothesis and decision rule. The morning digest shows the result and the verdict it implies, and no unattended step writes to the repo.

- **Relay briefs through a telephone chain (wild)** — FEATURE — value 3 — effort S — risk low — category: handoff ambiguity
  Why: handoff fidelity is drilled by swapping models, but nothing stresses the brief itself. Assumption: each retelling by a cheap agent drifts exactly where the brief is ambiguous.
  Done when: for an L task, 3 successive Haiku retellings of the brief are diffed against the original. The drifted clauses are shown as "ambiguous here", and the brief is revised until the third retelling keeps the acceptance criteria intact.

- **Run speed-dating pair rounds before the full panel (wild)** — FEATURE — value 3 — effort M — risk low — category: cheap pre-panel
  Why: full panels are costly and the pack wants cost caps. Assumption: two-turn exchanges between every role pair (builder↔reviewer, recon↔debugger) surface most objections.
  Done when: pair rounds produce a deduplicated objection list, and the full panel runs only if the list contains a blocker. On replayed tasks it catches the same blockers at lower cost.

- **Keep standing boards with minutes** — FEATURE — value 3 — effort M — risk med — category: persistent committees
  Why: spokesperson agents and case law exist, but not a persistent per-area body whose minutes keep growing. Assumption: areas like the guard or the UI recur in tasks.
  Done when: a task touching a board's area gets that board's last 5 rulings as capped context, and a board that has not ruled in 90 days is flagged for sunset.

- **Test the judge with sealed ground truth (wild)** — FEATURE — value 4 — effort M — risk low — category: judge calibration
  Why: the main thread both judges panels and merges. Assumption: the judge's own bias is the least-measured component.
  Done when: bench replays past panels whose outcomes are sealed, and the judge's verdict is compared with the outcome. A judge accuracy figure appears in `fm friction`.
