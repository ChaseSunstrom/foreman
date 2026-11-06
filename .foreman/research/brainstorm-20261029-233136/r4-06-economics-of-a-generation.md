# Brainstorm — lens: economics of a generation

- **Count dollars per closed scenario at the arm level, not the step level** — FEATURE — value 5 — effort M — risk low — category: unit economics
  Why: the pack lists per-step meters, a cost ledger and a "cost per scenario closed" idea, but the exam already has Foreman and plain-session arms with cost. Nothing says the number is the join of exam.jsonl and the session cost per arm, so the unit is still undefined. Assumption: exam.jsonl rows carry or can be joined to a cost field.
  Done when: `fm genesis status` prints, per generation, `$ / scenario closed` for the Foreman arm and the plain arm computed from exam.jsonl, and a test with a fixture of 3 rows asserts the exact figures.

- **Price the held-out look as a spend that depletes** — FEATURE — value 4 — effort S — risk low — category: exam budget
  Why: held-out exam runs are the most expensive and the most overfit-prone calls. Existing ideas count looks and rotate; none treat a look as a priced, finite resource that competes with the generation budget. Assumption: a held-out run costs a roughly constant multiple of a normal scenario.
  Done when: the budget file holds a `holdout_looks` allowance with a dollar price. A selection that needs a look beyond it stops with "holdout allowance spent" and the test shows no exam call was made.

- **Early-stop a rewrite by sequential test on the first scenarios** — PERFORMANCE — value 5 — effort M — risk med — category: selection cost
  Why: selection is "closes more than the parent", and each rewrite pays the full exam. Idea lists mention screening cheaply and the knee of the curve, but not a statistical stop. If a rewrite is behind the parent after k of N scenarios by a margin it can't recover, abort it. Assumption: scenario order is shuffled so early results are unbiased.
  Done when: on a recorded 12-scenario fixture a clearly losing rewrite stops after at most 5 scenarios, a winning one runs all 12, and the log shows the stop rule's reason.

- **Fix a tie-break by a dollar rule, written down** — FIX — value 3 — effort S — risk low — category: selection
  Why: the request says a rewrite stays only if it closes more scenarios than its parent. A tie at 3× cost is the open case in the lens definition and no idea fixes the number. Assumption: ties are common on small exams (9 scenarios, 3 held-out).
  Done when: lineage.md records for a tied pair "kept parent: tie, child costs 2.9×", and a unit test shows an equal-closure cheaper child wins while an equal-closure dearer child loses.

- **Meter the user's attention in the same ledger as dollars** — FEATURE — value 4 — effort M — risk low — category: user cost
  Why: auto-start, the ratify card and the question card all spend the user's time. An existing idea reports user time, but as a report line. Here it is a ledger column that counts against the stop rule, so a generation that costs 4 approvals for 1 scenario shows as expensive. Assumption: a prompt count is a usable proxy for minutes.
  Done when: each generation row has `asks` and `approvals`, and a test shows a run that asked 5 times ranks below an otherwise identical run that asked once.

- **Pay for the cheap generations out of what the expensive one saved** — FEATURE — value 3 — effort S — risk med — category: budget flow
  Why: budgets are all fixed caps in the ideas so far. A cached stage reused from an unchanged input saves a known cost; that saving could fund the next retry of a not-yet entry instead of disappearing. Assumption: reuse savings are computable as the last run's stage cost.
  Done when: after a reused stage, the ledger shows `credit +$X` and the next not-yet retry draws from it. A test asserts the credit equals the cached stage's recorded cost.

- **Show a break-even date for the whole tower** — FEATURE — value 4 — effort M — risk low — category: ROI
  Why: the user steers hard toward polish and real outputs. Nothing tells them when Genesis has paid back. Assumption: `fm outcomes` 30-day survival plus the closed gaps give a rough value-per-closure in minutes saved.
  Done when: `fm genesis status` prints "spent $A, closed N gaps, estimated payback in D days (assumption: X min per gap)", and the assumption is editable in one place.

- **Rank the not-yet ledger by closure probability per retry dollar, learned from past retries** — FEATURE — value 4 — effort M — risk low — category: retry economics
  Why: the ledger retries every generation, and the earlier list has attempts and a retire rule. Retrying each entry equally burns money on the blocker that never moves. Past attempt outcomes give a per-blocker-class hit rate. Assumption: blockers fall into a few classes (missing tool, flaky exam, hard design).
  Done when: with a fixture ledger of 5 entries and a history of retries, `fm genesis next` retries the entry with the highest rate-per-dollar first, and the order is printed with the numbers.

- **Wild: Let a generation rent the cheaper model for every step the exam can't distinguish** — FEATURE — value 4 — effort L — risk med — category: model mix
  Why: wild. After one generation, replay the exam with a smaller model on one stage at a time; keep the downgrade where closure is unchanged. Saves cost on every later generation. Assumption: closure is a stable enough signal at 9 scenarios.
  Done when: a `model-map.json` records the cheapest model per stage with the ablation run id that justified it, and the next generation's ledger shows the lower spend with the same closure.

- **Wild: Run a prediction market between the Seed variants, settled by the exam** — FEATURE — value 3 — effort L — risk med — category: allocation
  Why: wild. Cheap tool-less children bet a pretend budget on which Seed will close the most scenarios. Only the top-staked Seeds get a full run. This turns the forecast into an allocation rule and scores the forecasters over time. Assumption: tool-less children are cheap relative to a full tower run.
  Done when: with 4 Seeds, only the top 2 by stake are run, and the ledger records each bet and its later score.

- **Wild: Issue a quote and refund the unspent budget as quota carry** — FEATURE — value 3 — effort M — risk low — category: budget flow
  Why: wild. A tower is priced before it starts; when it finishes under quote, the difference is added to the project's next budget, and an overrun shrinks it. Over time the quote becomes accurate, because the user feels the miss. Assumption: a stage-level forecast from history is good enough to quote within 2×.
  Done when: the quote and the actual are logged per tower, and a test shows the next tower's cap moves by the signed difference, bounded at ±25%.

- **Stop the tower when the marginal scenario costs more than plain Claude would** — PERFORMANCE — value 5 — effort S — risk low — category: stop rule
  Why: the plain session arm exists with cost. If the Foreman arm's marginal dollar per extra scenario exceeds the plain arm's dollar per scenario on the same held-out set, more generations are no longer buying anything the user can't get free. Assumption: the plain arm is run at least once per tower.
  Done when: the orchestrator halts with the reason "marginal cost above plain Claude" in a fixture where that holds, and continues in one where it doesn't.

- **Cap a generation's fan-out by price per child, with a cheap-first queue** — PERFORMANCE — value 3 — effort S — risk low — category: fan-out
  Why: Missions, critiques and lenses run as children, and the user's usage is the shared pool with loop and scouts. Assumption: children vary 10× in cost, so ordering by expected cost-per-idea lets the cheap ones finish before the cap.
  Done when: with a cap smaller than the total, the cheapest children are run first, and the ledger lists the ones skipped with their price.

Next question: What does the user's real usage reset look like in practice, and does Genesis share a quota pool with the loop, scouts and lanes, so that one stage's economics are really the whole fleet's?
Next question: Is a "closed scenario" worth the same to the user whether it is a planted gap or a project-specific MUST, and if not, what weights would they actually choose?
