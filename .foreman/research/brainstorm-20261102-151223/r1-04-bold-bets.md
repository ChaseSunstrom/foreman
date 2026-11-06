# Brainstorm — lens: bold bets

- **Auction the queue by expected yield per dollar** — FEATURE — value 5 — effort L — risk med — category: markets
  Why: xhigh, markets × calibration. Tasks bid with calibrated P(close) × value ÷ predicted cost, and the run funds the best bids first. Evidence: the c22 spend receipt, `fm run --stall-usd` and the calibration ledger already hold the inputs. Prior art: Kubernetes priority queues, Mesos DRF, with no calibrated bids. Assumption: past runs hold enough closes to replay.
  Done when: replaying the last 100 closed tasks under bid ordering beats the real order on closes per dollar, or the idea is dropped.

- **Run a prediction market among deciders** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: xhigh, markets × science. Guard, prover and reviewer stake budget on "this close survives 14 days", and payouts weight their vote and rank their trust. Evidence: `decide()` doesn't book abstentions, and the user wants a measured false-positive cost. Prior art: Metaculus and Augur, with none for agent harnesses.
  Done when: a backtest shows stake-weighted votes predict later user reverts with lower Brier score than the unweighted vote.

- **Bill each model a spot price per task type** — FEATURE — value 5 — effort L — risk med — category: routing
  Why: xhigh, markets. `fm code` runs on any model, so keep an Elo and a cost per (model, task type) from closes and reverts, then route each task to the cheapest model whose lower bound clears the bar. Prior art: OpenRouter, RouteLLM (they route on prompts, not on proven closes).
  Done when: on 50 replayed tasks, routed spend is at least 25% below single-model spend at an equal close rate.

- **Price guard rules by regret** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: high, markets × law. This answers the open question on false-positive cost. Each block rule gets a tab: overrides and manual reruns count as cost, prevented damage from `fm drill` counts as benefit, and negative-value rules are proposed for demotion to warn. Prior art: Pigouvian pricing, with no guard that reports a profit and loss.
  Done when: `fm guard --pnl` lists every rule with a net score, and one rule is auto-proposed for demotion from replay data.

- **Make every child spend a capability token** — SECURITY — value 4 — effort M — risk med — category: authority
  Why: high, markets × military logistics. This answers the inheritance question: push grant, credentials and ledger key become scoped, expiring tokens a lane must be handed, and nothing is inherited by default. Prior art: Macaroons and object-capability systems. Assumption: today children inherit the environment.
  Done when: a test lane spawned without a token fails a push and the ledger records the denial.

- **Stage a bounty board with human prices** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: xhigh, markets. The user puts a dollar bounty on a task, and Foreman works it only if predicted cost is below the bounty, then prints profit or loss on the receipt. Evidence: the user keeps asking for yield per dollar and stall stops.
  Done when: a task with a $1 bounty and a $3 estimate is declined with the stated reason.

- **Warrant landed work for 14 days** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: extreme, insurance. Each landed commit opens a warranty window, user hand edits and reverts debit the deciding model's account, and trust ratchets from the outcome. It extends c14 into a pricing signal. Prior art: SWE-bench measures only at merge time.
  Done when: a commit with a user edit in its window shows a debit in `fm doctor`.

- **Rehearse tasks in a digital twin** — FEATURE — value 5 — effort L — risk high — category: simulation
  Why: extreme, finance Monte Carlo. Before spending, fit cost, time and close odds from past runs and the repo map, and simulate the task 1,000 times to quote a price and a risk range. No harness quotes before it works. Assumption: past runs are enough signal.
  Done when: quoted P50 cost lands within 30% of actual on 20 held-out tasks.

- **Run Foreman with a feature off to test obsolescence** — FEATURE — value 4 — effort M — risk low — category: inversion
  Why: xhigh, inversion. Each new base model arrives and the harness A/B-runs its own scaffolding (planner, prover, guard rules) off against on, then retires any feature whose absence costs nothing. This feeds the unanswered "who notices a retirement first" question. Prior art: ablation studies, never as a harness habit.
  Done when: `fm ablate plan` reports a measured delta for at least 3 features.

- **Take a product request to shipped, under a warranty (wild)** — FEATURE — value 5 — effort L — risk high — category: end-to-end
  Why: massive, 2030 worked back. A one-paragraph request goes through spec, build, deploy and a 30-day watch with a fixed price quote and an auto-refund if proofs fail. Wild: today it needs a team. Prior art: Devin and Replit agents (none give a priced guarantee).
  Done when: one small CRUD app ships from a paragraph, with a quote, proofs and a warranty log.

- **Bid for expiring quota overnight (wild)** — FEATURE — value 3 — effort M — risk low — category: spend
  Why: high, markets (Dutch auction). When a quota window is about to lapse unused, the deferred backlog's cheapest high-yield tasks run, and the lowest-value items are cut first. Evidence: the idle-yield item c22 and deferred wake-up c23.
  Done when: a simulated idle window runs only tasks whose yield clears a falling threshold.

- **Swap lessons across installs by consent (wild)** — FEATURE — value 3 — effort L — risk high — category: federation
  Why: massive, ecology and markets. Opt-in, anonymized lessons are traded between local Foremans, and each imported lesson earns trust only through the importer's own proofs. Nothing leaves the host unless a setting says so. Prior art: federated learning, shared dotfile repos.
  Done when: two sandbox homes exchange one lesson and the importer logs its trust outcome.

- **Pay a red team to break the proof (wild)** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: high, markets × games. Before a close, a second agent earns budget only by finding a false-positive proof, such as a test that passes with the fix reverted. Extends `fm task prove`. Prior art: mutation testing, bug bounties.
  Done when: a planted vacuous test is caught by the adversary and the close is refused.

Next question: which of Foreman's decisions have any measured outcome label (a revert, a user edit, a rerun) at all, since every market idea depends on that supply?
Next question: what does the user pay in attention, not dollars, per run, and could a market price that?
