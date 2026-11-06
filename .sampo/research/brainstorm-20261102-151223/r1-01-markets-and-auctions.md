# Brainstorm — lens: markets and auctions

- **Run a yield auction for the queue** — FEATURE — value 5 — effort L — risk med — category: scheduling
  Why: tier xhigh, domain markets. Each task bids its expected value over expected cost, using calibration data and the spend receipt (c22, T-2669). Prior art: Borg priority quotas and spot schedulers, none that price by proof-strength yield. Assumption: closed tasks carry enough cost data to estimate cost.
  Done when: a replay of the last 50 closed tasks shows the auction order closes more tasks per dollar than FIFO, or the brief is dropped.

- **Open a forecast market on task outcomes** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: tier xhigh, domain prediction markets. Before work, the planner, the cold reader and a base-rate model each post a probability that the task closes with strong proof. Prices are scored with Brier, and track record sets weight. Prior art: Hanson's idea futures and Metaculus. Foreman already calibrates its own bets, so this adds many forecasters rather than one.
  Done when: the Brier score of the pooled forecast beats the best single forecaster on 30 closed tasks.

- **Hold a Vickrey auction for model and backend choice** — FEATURE — value 4 — effort M — risk med — category: routing
  Why: tier xhigh, domain auctions. Claude Code, Codex, Gemini and `fm code` models each quote cost and success odds. The best value wins but pays the runner-up's price, so the quotes stay honest. Prior art: RouteLLM and OpenRouter pick models by heuristic, not by auction. Assumption: exams give per-backend success data.
  Done when: a backtest on exam tasks beats a fixed-model default on success per dollar.

- **Issue warranties on landed commits** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: tier high, domain insurance. A landed commit gets a warranty window. A user edit or revert inside it is a claim that reopens the task at top priority and raises the premium for that task type. This builds on c14, mining user edits of landed lines. Prior art: SZZ-style bug-introducing-change studies, with no pricing.
  Done when: a seeded user edit to a landed line reopens its task with a claim recorded, and the type's premium changes.

- **Auction injected context slots** — PERFORMANCE — value 4 — effort M — risk low — category: footprint
  Why: tier high, domain ad auctions. The T-2667 work shows SessionStart notes and other sources compete for a limited injection budget. Each source bids its measured past use, meaning the share of its characters the agent acted on, and losers are dropped. Prior art: ad slot auctions, with no equivalent in agent harnesses. Assumption: `fm burden --by-source` can attribute use.
  Done when: with a capped budget, the winning sources show a higher use rate than the unmanaged baseline, and dropped notes are listed.

- **Price authority as expiring capability options** — SECURITY — value 4 — effort L — risk high — category: guard
  Why: tier xhigh, domain options. Lanes, ticks and prover children get no ambient push grant or ledger key. They buy a capability from a small budget, with expiry and a logged price. This addresses the unanswered question about inherited authority. Prior art: object-capability systems and short-lived cloud credentials, but not budgeted per task.
  Done when: a lane that tries to push without a purchased capability is refused and the refusal is recorded.

- **Halt runs with market circuit breakers** — FEATURE — value 3 — effort S — risk low — category: spend
  Why: tier low, domain exchanges. This generalises T-2669's `--stall-usd`: halt when spend velocity or retry rate jumps well above the run's own trailing norm, then resume after a cool-off. Prior art: exchange limit-up/limit-down halts.
  Done when: a fault-injected retry storm halts the run and the receipt names the breaker.

- **Size budgets with Kelly sizing** — FEATURE — value 3 — effort M — risk med — category: spend
  Why: tier medium, domain portfolio theory. Each task's budget cap scales with calibrated win probability and payoff, so uncertain tasks get smaller stakes. Prior art: the Kelly criterion, not used in agent harnesses. Assumption: calibration is good enough to size from.
  Done when: in a replay, the Kelly caps give lower total spend on failed tasks than flat caps at equal closes.

- **Sell proofs by forgery cost** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: tier medium, domain signalling theory. A proof that is costly to fake, such as a real command the tree must change, earns a higher grade than a cheap one. This refines the stored grade the digests count. Prior art: Spence's job-market signalling.
  Done when: each proof kind carries a forgery cost, and a trivially passing proof is graded below a test that fails without the change.

- **Charge the user's attention a price (wild)** — FEATURE — value 4 — effort M — risk low — category: interruption
  Why: wild, tier xhigh, domain attention markets. Foreman asks the user a question only if its expected value exceeds a price set by the user's observed response latency and past dismissals; otherwise it defers or decides and logs. Assumption: question and answer timing are logged. Prior art: interruption cost models in research, none shipped in coding agents.
  Done when: a question below the price is held for the digest instead of interrupting, and the user's later override rate is measured.

- **Quote before building (wild)** — FEATURE — value 5 — effort L — risk med — category: planning
  Why: wild, tier massive, domain freelance contracting. `fm quote "request"` returns price, time and a p90 overrun with the proof it will deliver. On acceptance it works under a hard cap, and an overrun is eaten as a visible loss in the receipt. Prior art: fixed-bid contracts and estimation tools, none that back the quote with a calibrated record.
  Done when: quotes on 20 past requests land within their p90 band at least 90% of the time.

- **Make an idea market for Genesis (wild)** — FEATURE — value 4 — effort M — risk low — category: Genesis
  Why: wild, tier xhigh, domain prediction markets crossed with the tower. Cold readers hold points they can bet for or against each idea in the 525-idea catalogue. Prices rank briefs, and later outcomes pay out. Parents: forecast market and warranties. Prior art: Hanson's idea futures.
  Done when: price rank from one generation correlates better with realised value than the brainstormers' own value scores.

- **Run a spot market on idle quota (wild)** — FEATURE — value 4 — effort M — risk med — category: spend
  Why: wild, tier high, domain spot compute. Quota that would expire unused is cheap, so deferred and low-value tasks (c23) run then, while urgent work pays full price. Prior art: cloud spot instances. Assumption: quota expiry is readable.
  Done when: a run near quota expiry drains deferred tasks and the receipt shows their yield per dollar.

- **Escrow tools for blocked sub-agents** — FIX — value 3 — effort M — risk med — category: agents
  Why: tier medium, domain escrow. This answers the question about sub-agents blocked by their allowlist. The sub-agent posts a priced request for the missing tool, the orchestrator or user releases it, and the grant is logged instead of the task failing silently.
  Done when: a sub-agent with a blocking allowlist produces a request record and the task does not fail silently.

Next question: which of these prices can be computed from ledger data that exists today, and which need a new ledger record class first?
Next question: when a market-style mechanism is gamed, such as agents inflating bids, who audits it and how would the user notice?
