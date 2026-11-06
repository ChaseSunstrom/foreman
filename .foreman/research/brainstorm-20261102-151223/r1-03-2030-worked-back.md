# Brainstorm — lens: 2030 worked back

- **Run a task auction between lanes and models** — FEATURE — value 5 — effort L — risk med — category: markets
  Why: tier xhigh; domain markets/auctions. Each lane or model bids price and confidence on a brief, and Foreman awards it by calibrated cost per verified close. By 2030 models are interchangeable and priced per token, so routing is the lever. Prior art: Contract Net Protocol, FrugalGPT routers. Cheapest kill: replay 50 closed tasks and compare cheapest-bid awards with actual assignments on close rate and dollars.
  Done when: `fm bid --replay 50` prints awarded vs actual cost and close rate, and the award wins on at least one.

- **Replay the ledger under a changed policy (a harness digital twin)** — FEATURE — value 5 — effort L — risk med — category: simulation
  Why: tier extreme; domain science (off-policy evaluation). Replaying past tasks with a different guard, model or budget predicts what would have changed. Evidence: Foreman keeps calibration of its own bets and `fm replay` already runs logged commands through the guard. Cheapest kill: predict 20 held-out tasks under one policy change and score the prediction against what actually happened.
  Done when: `fm twin --policy X` reports predicted close rate and spend, and the Brier score on held-out tasks is shown.

- **Swap the model under the tower and prove nothing regressed** — FEATURE — value 5 — effort M — risk low — category: continuity
  Why: tier high; domain manufacturing (requalifying a part). By 2030 the underlying model changes every quarter. Foreman has exams and drills but no model-swap rehearsal. Prior art: none found for harnesses. Cheapest kill: run the existing exam on two models and diff.
  Done when: `fm drill --model-swap A B` outputs a per-exam score diff and fails on a drop beyond a threshold.

- **Pay an adversarial auditor lane per defect found in other lanes' closes** — FEATURE — value 4 — effort M — risk med — category: markets
  Why: tier xhigh; domain markets (bug bounty). A lane earns budget for each planted or real defect it proves in a landed close. Evidence: closes are evidence-gated but checked by the same lane that wrote them. Cheapest kill: seed 20 known bugs into closed tasks and measure the auditor's catch rate against its cost.
  Done when: the seeded run reports catch rate and cost per catch, and a real catch reopens its task.

- **Put a warranty on every landed change and bill regressions to the producer** — FEATURE — value 4 — effort M — risk med — category: accountability
  Why: tier xhigh; domain law/insurance. A change carries an N-day warranty. A revert or user hand-edit (c14) inside the window debits the producing agent's reputation and budget. Prior art: none found for agent commits. Cheapest kill: join past reverts to their task closes and see whether the signal is non-empty.
  Done when: `fm warranty` lists open warranties and the claims against them from the last 30 days.

- **Keep a per-model, per-task-type reputation (Elo) from verified closes** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: tier high; domain games (Elo). It feeds the auction and the model-swap drill. Assumption: enough closes exist per task type to rank. Cheapest kill: compute it from the existing ledger and check the spread between models.
  Done when: `fm doctor` shows the ranking with sample sizes and marks types with too few samples as abstain.

- **Hold out a random verb-off sample to measure what each verb is worth** — FEATURE — value 4 — effort M — risk med — category: inversion
  Why: tier xhigh; domain science (ablation, randomized trial). Inversion: native harnesses will absorb planning and proving, so Foreman must show marginal value. It also answers the earlier question of who notices a retired capability, and complements `fm usage --prune`, which only counts use. Cheapest kill: turn one cheap verb off for 10% of tasks for a week and compare close quality.
  Done when: `fm ablate VERB` reports the effect size with a confidence interval, or states there is not enough data.

- **Issue portable signed proof receipts that other CI or harnesses verify** — FEATURE — value 4 — effort M — risk low — category: attestation
  Why: tier high; domain law/supply chain. Evidence: the ledger already has a signing key and `fm verify-ledger`. In 2030 reviewers will want to verify an agent's claims without trusting its harness. Prior art: in-toto, SLSA. Cheapest kill: emit one receipt and verify it from a clean checkout with no Foreman installed.
  Done when: a standalone script verifies a receipt's commands, tree hash and signature and exits nonzero on tampering.

- **Run low-priority work on idle quota like spot instances** — FEATURE — value 4 — effort M — risk med — category: spend
  Why: tier xhigh; domain markets (spot vs reserved capacity). Idle-yield and the spend receipt (c22) exist. Add a reserved lane for the user's active session and a preemptible lane for background tasks that yields when the user returns. Cheapest kill: measure idle quota over two weeks.
  Done when: a background task is preempted within N seconds of user activity and resumes with no lost work.

- **Ship a whole small app from a goal sentence, end to end (wild)** — FEATURE — value 5 — effort L — risk high — category: massive
  Why: tier massive; wild. The Genesis tower, exams and the site already chain plan, build, prove and publish, so `fm ship "goal"` would run them as one run with a stall budget (T-2669). Prior art: app-builder agents, which skip the proof discipline. Cheapest kill: give it one CRUD app spec and have a cold reader grade the result.
  Done when: one goal sentence yields a deployed app plus a receipt, and a cold read finds no unproven claim.

- **Federate Foremen to trade proven lessons with priced provenance (wild)** — FEATURE — value 3 — effort L — risk high — category: federation
  Why: tier extreme; wild; domain markets and the scientific literature. A lesson ships with its evidence and a replication count, and consumers re-verify it locally before use. Assumption: nothing leaves the machine without an explicit setting. Prior art: none found. Cheapest kill: export one lesson as a file and replicate it in a second repo by hand.
  Done when: an imported lesson is rejected unless its proof reruns green locally.

- **Let tasks bet their own odds, and fund runs from the calibrated ones (wild)** — FEATURE — value 4 — effort M — risk med — category: markets
  Why: tier xhigh; wild; domain prediction markets. Agents stake budget on "this proof passes" and a Brier score sets their next allowance, building on Foreman's calibration of its own bets. Cheapest kill: log stakes on 30 tasks without acting on them and check calibration.
  Done when: `fm doctor` shows per-agent Brier scores and the budget share that follows from them.

- **Name sub-agent deadlocks instead of failing silently** — FIX — value 3 — effort S — risk low — category: transparency
  Why: from the left-over question about a tool allowlist blocking the only way to finish. By 2030 most work is delegated, so silent skips are costly. Cheapest kill: block one tool in a drill and see whether the receipt says so.
  Done when: a drill with a blocked tool produces a receipt line that names the tool and the task.

Next question: when Foreman's bids and reputations steer real spend, which of its own measures could an agent game, and how would a drill show it?
Next question: what does the user still do by hand in 2030 that Foreman could take over without being asked?
