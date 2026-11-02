# Moonshot catalogue

### M-01 · Deliver a product from one paragraph at a fixed, warrantied price
- Tier: massive
- Domain: freelance contracting and insurance
- Lens: crossbreed: markets and auctions (Quote before building) × bold bets (Take a product request to shipped, under a warranty)
- What: `fm deliver "<paragraph>"` returns a price, a date and a p90 overrun from the user's own calibrated record, plus the acceptance proofs it will hand over. On a yes it specs, builds, deploys and watches the app for 30 days under a hard cap; an overrun is booked as Foreman's visible loss, and a warranty claim inside the window reopens the work at no charge and refunds that share of the budget.
- Prior art: Devin, Replit Agent, Lovable and Bolt build apps from prompts with no price or guarantee; agencies quote fixed bids by hand; Foreman's `fm queue --cost` (T-1878) quotes tokens as a median, with no band and no commitment.
- Better by: the price rests on a backtested band from this user's history and the guarantee is enforced by proofs and a claims ledger, so the scoping, delivery and support work of a small agency is done and priced by one harness.
- Novelty: 4
- Needs: M-13, M-16, M-17, M-20
- Unblocks: none
- Kill: Quote, then build, one CRUD app (a todo API with auth, about ten endpoints) from a one-paragraph request; pass if it lands under its quoted p90 cost with every acceptance proof green in a clean container, fail if either misses.
- Stage: idea

### M-02 · Keep code as a regenerable cache of intent clauses and proofs
- Tier: massive
- Domain: manufacturing (the CAD file is the source, the printed part is a cache)
- Lens: crossbreed: 2030 worked back (Make source the intent and the code a regenerable cache) × science itself (Prove a quote against a reference implementation)
- What: A module's source of truth becomes its intent clauses (the standing intent and the steer checkers of T-1063) plus its stored proofs: tests, hunk-mutation proofs and differential twins. `fm regen PATH` deletes the module, rebuilds it on any model or language from those alone, and lands it only when every proof passes and the twin agrees on recorded inputs; run as a standing check, the round trip shows where the proofs are too weak to pin behaviour.
- Prior art: spec-driven development (GitHub Spec Kit, Kiro specs), model-driven code generation from UML, literate programming; all use the spec as a one-time input to generation.
- Better by: regeneration is a gate, not a generator: a round trip that must pass every proof measures whether intent and proofs really pin the code, which no spec-first tool checks, and it makes model and language changes routine.
- Novelty: 5
- Needs: M-18
- Unblocks: none
- Kill: In the T-1232 spec-suite toy repo, delete three modules and have a headless `claude -p` rebuild each from its briefs and tests alone, two attempts each; pass if at least two of the three pass every original test, fail otherwise.
- Stage: idea

### M-03 · Run an owner-less project under a charter until an heir takes over
- Tier: massive
- Domain: law (wills, trusts and dead man's switches)
- Lens: crossbreed: 2030 worked back (Appoint an heir and keep a dead man's switch) × bold bets (Take over an open-source maintainer's inbox; Dependency upgrade autopilot)
- What: When the owner is silent past N days, the project drops to a written charter: Foreman reproduces each new issue as a failing test and lands the clear fixes, bumps dependencies with call sites repaired and proven, publishes an honest status page, and refuses anything outside the charter. After a second deadline it hands the keys, the ledger and the open work to a named heir.
- Prior art: Dependabot and Renovate bump versions without repairing callers; GitHub's Copilot coding agent works issues a person assigns; Google's Inactive Account Manager hands over data, not upkeep; Foreman's watchers (T-2356) start work from CI and issues while the owner is present.
- Better by: the project keeps shipping proven fixes with nobody assigning work, under authority bounded by a charter and expiring tokens rather than the owner's credentials, which today takes a maintainer team or a foundation.
- Novelty: 4
- Needs: M-15, M-16
- Unblocks: none
- Kill: In a local fixture repo with a one-page charter and 20 seeded issues (the T-1232 spec-suite kind), run fm night unattended for seven nights with no owner input; pass if at least 12 issues close with proofs that still hold under fm outcomes a week later and no close breaks a charter line, fail otherwise.
- Stage: idea

### M-04 · Own the pager for insured crash classes, from trace to proven fix
- Tier: massive
- Domain: insurance underwriting and site reliability engineering
- Lens: crossbreed: 2030 worked back (Own the pager: turn production crashes into failing tests and fixes) × markets and auctions (Issue warranties on landed commits)
- What: A crash feed (a log file, a Sentry export, a pasted trace) becomes a brief whose first step is a test, rebuilt from the trace, that fails; the fix is proven against it and against recorded production inputs through a differential twin, then canaried with automatic rollback. Foreman publishes the crash classes it is insured for, those whose warranty claim rate stays under a bar, and runs those with no human, while the rest wait for one.
- Prior art: Sentry Seer autofix and AI on-call agents (Cleric, Resolve AI, Datadog Bits AI); Foreman's `fm capture --incident` (T-2388) runs a signal command but neither reproduces from a trace nor grants autonomy per class.
- Better by: autonomy is granted per crash class by a measured claim rate, and no fix lands without a reproduction that failed first, so on-call becomes an insured service rather than a rota.
- Novelty: 3
- Needs: M-15, M-16, M-18
- Unblocks: none
- Kill: Take Foreman's last 30 FIX tasks whose request holds a traceback and have a headless run turn only the trace into a test at each task's start snapshot (`fm at`); pass if at least 10 fail there and pass at the fix commit, fail below.
- Stage: idea

### M-05 · Merge any agent's pull request on rerun proofs, not prose review
- Tier: massive
- Domain: law (evidence and chain of custody)
- Lens: crossbreed: inversion (Review any agent's PR with plan, proof and guard checks) × science itself (Replicate closed tasks with an independent agent)
- What: A CI app takes a PR from any agent or person, finds or derives its brief, reruns each claimed proof in a clean container, mutation-grades it, scans the diff for guard-class effects and posts one signed check. PRs whose proofs grade strong, from authors whose forecast-weighted record clears a bar, merge with no human reading; the rest list exactly what failed or was never proven.
- Prior art: CodeRabbit, Copilot code review and Graphite's agent comment in prose; merge queues require green CI; SLSA attests builds, not claims; Foreman's `fm audit scan` and `fm pr` work only inside its own sessions.
- Better by: it checks the author's claims by re-execution and grades their strength, for any harness, so review of agent output stops scaling with the number of agents.
- Novelty: 4
- Needs: M-12, M-17
- Unblocks: none
- Kill: For the builder-lane merges of the last 60 days, rerun each one's criteria and `fm task prove --hunks` at its merge commit and compare the grade with `fm outcomes` (reverted or fixed later vs held); pass if the grade separates them with an AUC of at least 0.7, fail below.
- Stage: idea

### M-06 · Predict a policy change's effect from the ledger before running it
- Tier: extreme
- Domain: econometrics (off-policy evaluation and synthetic control)
- Lens: crossbreed: 2030 worked back (Replay the ledger under a changed policy) × science itself (Estimate causal effects of past features by synthetic control)
- What: `fm twin --policy "<change>"` (a guard rule, a model, a budget, a gate) selects the logged tasks the change would have touched, reweights their outcomes with off-policy estimators against a synthetic-control baseline, and prints predicted close rate, spend and claims with an interval. Every self-change, model switch and budget move is quoted by the twin first and scored against what happened; no current harness can predict the outcome of changing its own policy before trying it.
- Prior art: off-policy evaluation in recommender systems and reinforcement learning; Foreman's `fm backtest` (would a rule fire), `fm replay` (guard verdicts) and `fm bench` (reruns cases at full model cost).
- Better by: it predicts outcomes rather than firings, costs no model calls, and carries its own Brier score.
- Novelty: 5
- Needs: M-16
- Unblocks: none
- Kill: For T-2353 (the router picks the cheapest model that holds), give the twin only the 60 days before it and predict close and cost for the 20 tasks after; pass if its Brier beats the pre-change base rate by at least 0.03 and its cost error is within 30%, fail otherwise.
- Stage: idea

### M-07 · Forecast when each gate stops paying, and retire it on evidence
- Tier: extreme
- Domain: ecology (extinction forecasting) and law (sunset clauses)
- Lens: crossbreed: inversion (Run the necessity corpus on every new model ID) × ecology and evolution (Run a digital terrarium that forecasts which verbs and rules go extinct)
- What: Each new model ID replays the gates' past catches (guard blocks, failed proofs, plan rejections) with that gate off; every gate carries a retire-when predicate and a fitted decline curve, and `fm delta --forecast` prints when each gate's measured value, and Foreman's whole delta, reaches zero. A gate that meets its predicate drops to shadow mode with a necropsy record and a one-command revival; no current harness measures, on the user's own history, which of its safeguards a new model no longer needs.
- Prior art: ablation studies; Foreman's hook-feature ablation in `fm bench duel` (T-1375) and `fm evolve`'s instruction ablation, both started by hand and run once.
- Better by: it runs on every model change, per gate, with a forecast that is scored later and a retirement that can be undone.
- Novelty: 4
- Needs: M-19
- Unblocks: none
- Kill: Take 20 plan-gate rejections and 20 failed-proof catches from the last 60 days and replay each as a bench case with the gate off, on the current and on the previous model; pass if the unaided miss rate differs between the two models by more than its 95% interval for at least one gate, fail if it does for none (nothing to forecast).
- Stage: idea

### M-08 · Pool self-trials across installs; import only what replicates
- Tier: extreme
- Domain: medicine (meta-analysis) and microbiology (horizontal gene transfer)
- Lens: crossbreed: science itself (Pool effect sizes across consenting users' projects as a meta-analysis) × ecology and evolution (Share lessons between installs by signed horizontal gene transfer)
- What: Each consenting install randomizes its own practices (plan review, a guard rule, a lesson) across tasks and publishes only effect sizes with intervals; pooled estimates become the priors behind new installs' defaults. An imported lesson or rule arrives as a signed packet, enters dormant and activates only after it replicates on the importer's own replays; no current harness sets its defaults from randomized evidence pooled across users while every user's code stays local.
- Prior art: federated learning (shares gradients, not effects), vendors' A/B telemetry (the vendor decides), Cochrane reviews, shared rule packs and AGENTS.md templates with no evidence behind them; Foreman's `fm home export` moves one user's own state.
- Better by: evidence is randomized at the source, pooled with its heterogeneity shown, and must replicate locally before it acts.
- Novelty: 5
- Needs: M-17, M-19
- Unblocks: none
- Kill: From this install's ledger, estimate the effect of `fm second plan` on the fixed-later rate of M tasks with a 95% interval, then compute how many installs of this volume a pooled estimate needs to resolve a 5-point effect; pass if 200 or fewer, fail above.
- Stage: idea

### M-09 · Settle work between strangers by escrow released on replayed proof
- Tier: extreme
- Domain: law (escrow) and labour markets
- Lens: crossbreed: inversion (Act as escrow between a client and an agent) × markets and auctions (Stage a bounty board with human prices)
- What: A client writes a contract file with acceptance proofs (some held back until settlement), a price and a deadline, and any agent, Foreman-driven or not, attempts it under scoped tokens. `fm contract settle` releases the escrowed budget only when every proof, the held-back ones included, passes in a clean container on the delivered commit, and writes a signed settlement both sides can verify; no current harness acts as a neutral settlement layer that pays on machine-checked acceptance.
- Prior art: smart-contract escrow (not tied to test evidence), bounty platforms (Algora, Gitcoin) settled by a maintainer's approval, Upwork escrow released by a person; Foreman's `fm contract` (T-1158) bounds a run's time and spend, not a payment.
- Better by: acceptance is fixed before work starts and settled by re-execution with held-back proofs, so neither side judges and gaming the visible tests does not pay.
- Novelty: 4
- Needs: M-15, M-17
- Unblocks: none
- Kill: Write one contract (a CSV export with five visible and five held-back tests in the T-1232 spec-suite repo) and run two agents, one honest and one told to special-case the visible inputs; pass if settlement pays the honest one and refuses the gamed one, fail if the gamed one is paid.
- Stage: idea

### M-10 · Detect when a mechanism needs redesign, not another patch
- Tier: extreme
- Domain: ecology (early-warning signals before a regime shift) and history of science (Kuhn's anomalies)
- Lens: crossbreed: science itself (Detect paradigm shifts from accumulated anomalies) × ecology and evolution (Meter the error threshold for self-edits)
- What: Foreman tracks, per mechanism (the guard's shell parser, the hook path, the router), its stream of patches, re-fixes, overrides and flaky failures, and watches for the signals ecologists read before a collapse: shrinking intervals between patches, each fix holding for less time, rising variance. Past a threshold it files a redesign proposal naming the replacement class instead of one more patch; no current harness can tell that its own design, not a bug, is the cause.
- Prior art: Kuhn's anomaly accumulation; critical-slowing-down indicators in ecology and climate science; Foreman's recurring-failure capture (T-2272), which files one root-cause FIX per signature and stays at the patch level, and the deferred incident ledger (T-2404).
- Better by: it reads the trend across many patches to one mechanism, so it can say "replace" before the next failure rather than after the tenth.
- Novelty: 4
- Needs: M-19
- Unblocks: none
- Kill: Run the detector over 12 months of Foreman's own patches per module; pass if it flags the guard's shell parser (T-0170 to T-0190, T-1928, T-1937, T-2629) before T-2668 while flagging at most 2 of the next 10 most-patched modules, fail otherwise.
- Stage: idea

### M-11 · Auction the queue by calibrated yield and Kelly-size each stake
- Tier: xhigh
- Domain: auctions and portfolio theory
- Lens: crossbreed: markets and auctions (Size budgets with Kelly sizing) × bold bets (Auction the queue by expected yield per dollar)
- What: Each queued task bids its calibrated chance of a strong close times its value, divided by its predicted cost; a run funds the best bids first, and each task's budget cap scales with its calibrated edge, so uncertain work gets a small stake and an early stop. Bids, awards and realized yield per dollar print on the run's receipt.
- Prior art: Kubernetes priority classes and Mesos DRF; Foreman's inbox ranking (fixed weights for who asked, waiting time and tier, T-0111), `fm run --fit` and `--stall-usd` (T-2669).
- Better by: order and stake come from the user's own calibrated record instead of fixed weights, and the policy is backtested before it runs.
- Novelty: 3
- Needs: M-20
- Unblocks: none
- Kill: Replay the last 100 closed tasks with a budget of half their real spend, each bid computed only from data before it; pass if bid order funds at least 15% more closes than the real order and no task that closed would have hit its Kelly cap, fail otherwise.
- Stage: idea

### M-12 · Weight deciders by a scored market on whether a close survives
- Tier: xhigh
- Domain: prediction markets
- Lens: crossbreed: markets and auctions (Open a forecast market on task outcomes) × bold bets (Run a prediction market among deciders)
- What: Before a close, the planner, a cold rival read, the guard, the prover and a base-rate model each post a probability that the work survives its warranty window. Log-scored payouts set each decider's weight and trust budget; a pooled forecast below a bar sends the close to independent replication or the user, and above it the close stands alone.
- Prior art: Metaculus, Hanson's idea futures, ensemble stacking; Foreman's calibration ledger (T-2337) scores single stated confidences and confidence routing (T-2338) acts on one.
- Better by: many forecasters weighted by track record replace one self-report, settled on a real outcome rather than the closing agent's own check.
- Novelty: 3
- Needs: M-16
- Unblocks: M-05
- Kill: For 40 closed tasks with `fm outcomes` labels, have three cheap forecasters read only the brief and the diff and post a probability; pass if the log-weighted pool beats the best single forecaster's Brier by at least 0.02, fail otherwise.
- Stage: idea

### M-13 · Price the user's attention and cap unreviewed output to it
- Tier: xhigh
- Domain: attention economics and factory work-in-progress limits (Little's law)
- Lens: crossbreed: markets and auctions (Learn the user's price from revealed preference) × 2030 worked back (Cap what a swarm can do per hour of human review)
- What: Foreman fits the user's price for an interruption and for an hour of reading from their own response times, dismissals, overrides and budget choices. A question is asked only when its expected value beats that price, otherwise Foreman decides and logs it for the digest; new lanes stop when landed-but-unread diff exceeds what the user has historically reviewed in that window.
- Prior art: interruption-cost models in HCI research, conjoint analysis, Kanban WIP limits; Foreman's doors (stop only at an irreversible, ambiguous step, T-2342) and anergy (T-2563) use fixed rules, and its budgets cap dollars, not review load.
- Better by: the threshold is learned from the user's revealed choices and checked on held-out decisions, and output is throttled to review capacity rather than spend.
- Novelty: 4
- Needs: none
- Unblocks: M-01
- Kill: Fit the price on the user's first 100 ask and decide events in the ledger and predict the next 20 (answered and kept vs dismissed or overridden); pass if it matches the user's choice more often than the fixed default does, fail otherwise.
- Stage: idea

### M-14 · Breed lane strategies by tournament, with heritable genomes
- Tier: xhigh
- Domain: evolutionary biology
- Lens: crossbreed: ecology and evolution (Run lane tournaments with heritable strategy genomes) × markets and auctions (Run a task auction between lanes and models)
- What: A brief runs in two to four lanes whose genomes differ (model, prompt variant, plan style, test-first or not, context pack size), and proof grade per dollar picks the winner. The winning genome, mutated, seeds the next brief of that task type, and a lane that builds a shared helper is credited with the downstream closes it enabled.
- Prior art: AlphaEvolve and the Darwin Gödel Machine evolve code or agents on benchmarks; Foreman's lane race (T-1069) and L plan races (T-2340) pick a winner per task and keep nothing.
- Better by: strategies are inherited and selected per task type on verified closes in the user's own repos, not chosen afresh per task.
- Novelty: 3
- Needs: none
- Unblocks: none
- Kill: Run 20 closed S tasks of one type as bench cases under two genomes each; pass if the genome that wins the first 10 cases also wins at least 7 of the next 10, fail otherwise.
- Stage: idea

### M-15 · Spawn every child with expiring capability tokens and no inheritance
- Tier: high
- Domain: finance (expiring options) and ecology (quarantining invasive species)
- Lens: crossbreed: markets and auctions (Price authority as expiring capability options) × ecology and evolution (Quarantine invasive processes: spawned children inherit no authority by default)
- What: Lanes, night ticks, fm code tools, prover children and audit children start with no push grant, credentials or ledger signing key. Each holds only the tokens its brief names, each expiring and charged to a small per-task authority budget; `fm authority` prints what every process class holds, and a use without a token is refused and logged.
- Prior art: Macaroons, object-capability systems, short-lived cloud credentials (AWS STS), Claude Code's per-subagent tool lists; Foreman's builder sandbox and outbound ledger (T-1086) and fm code's Landlock (T-1607) confine writes, not grants.
- Better by: authority is scoped per task, expires and is budgeted and logged, so an unattended run's reach is known before it starts.
- Novelty: 3
- Needs: none
- Unblocks: M-03, M-04, M-09
- Kill: Spawn each child kind in a fixture home and list the environment variables, open files and grant files it inherits; fail (nothing to build) if none holds a push grant, credential or signing key it doesn't need, pass otherwise.
- Stage: idea

### M-16 · Open a warranty window on landed work and count hand edits as claims
- Tier: high
- Domain: insurance (warranties and premiums)
- Lens: crossbreed: markets and auctions (Issue warranties on landed commits) × science itself (Infer unseen work from ledger residuals)
- What: Each landed commit opens an N-day window; a revert, a later fix, or a user's own commit touching its lines (blamed back to the task, using the signal deferred T-2647 mines) files a claim that reopens the task at top priority and is charged to the producing model and task type. Claim rates per type become premiums that routing, quotes and autonomy read.
- Prior art: SZZ studies of bug-introducing changes; Foreman's `fm outcomes` (reverted, fixed later, held) and history router (T-2291), which miss the user's quiet hand edits and set no window or price.
- Better by: it captures the rework the user does by hand, invisible today, and turns every outcome into a per-type price other mechanisms can bid against.
- Novelty: 3
- Needs: none
- Unblocks: M-01, M-03, M-04, M-06, M-12
- Kill: For the last 60 landed tasks, blame the lines changed by the user's own commits within 14 days back to their task; pass if at least 5% of tasks carry a hand-edit claim that `fm outcomes` doesn't already count, fail below.
- Stage: idea

### M-17 · Ship every close as a signed evidence bundle anyone can rerun
- Tier: high
- Domain: law (chain of custody) and software supply-chain attestation
- Lens: crossbreed: inversion (Hand the user a signed audit pack a third party can verify) × 2030 worked back (Let outsiders replay your proofs without your machine)
- What: `fm export --replay T-NNNN` writes the brief, the proof commands, a container recipe, the tree hash and the ledger slice with its hash chain and signature, in an open attestation format (in-toto). A standalone verifier with no Foreman installed rebuilds the container, reruns the proofs and checks they match the stored results.
- Prior art: in-toto and SLSA attest builds; Foreman's `fm verify-ledger` (T-1065) proves the chain locally and its proof worlds (T-2398) record interpreter and lockfile hashes.
- Better by: a third party re-executes the agent's claims instead of trusting a signature or the harness that made them.
- Novelty: 3
- Needs: none
- Unblocks: M-01, M-05, M-08, M-09
- Kill: Bundle 10 closed tasks and rerun each in a clean container with no Foreman home; pass if at least 8 reproduce their stored proof result, fail below.
- Stage: idea

### M-18 · Prove a rewrite against the old build on recorded inputs
- Tier: medium
- Domain: experimental science (control groups) and manufacturing (golden-master testing)
- Lens: crossbreed: 2030 worked back (Prove a quote against a reference implementation) × science itself (Run a standing assay on a seeded-bug repo)
- What: `fm prove --twin OLD` records inputs from the test suite, logs or a fixture, runs the old and new builds side by side and reports the first input whose output diverges. A brief marked behaviour-preserving (a refactor, port or upgrade) can't close without it.
- Prior art: differential and golden-master testing, approval tests, Twitter's Diffy; Foreman's hunk proofs check that tests notice a change, not that behaviour is preserved.
- Better by: it is a close gate on the brief and takes its inputs from what the project already records.
- Novelty: 2
- Needs: none
- Unblocks: M-02, M-04
- Kill: Plant 10 behaviour-changing refactors in fixture modules whose existing tests still pass; pass if the twin catches at least 8, fail below.
- Stage: idea

### M-19 · Hold every self-promotion to a false-discovery bar
- Tier: medium
- Domain: statistics (multiple comparisons, Benjamini–Hochberg)
- Lens: science itself
- What: Foreman promotes lessons, guard rules, trial verdicts, playbook lifts and retire proposals out of many tests run at once. Each promotion gets a q-value under Benjamini–Hochberg across its week's family, and one above the bar stays in shadow instead of acting.
- Prior art: Benjamini–Hochberg in genomics and clinical trials; Foreman's trials (T-1059) call a change "moved" when a rate halves, with no error control across the many trials graded together.
- Better by: the share of promoted lessons and rules that are noise is bounded and stated, which every later retirement and pooling step depends on.
- Novelty: 2
- Needs: none
- Unblocks: M-07, M-08, M-10
- Kill: Grade the last 100 promotions (trial verdicts, promoted lessons, playbook lifts) with Benjamini–Hochberg at q = 0.1; fail if fewer than 5 would be withdrawn (no noise to control), pass otherwise.
- Stage: idea

### M-20 · Put a backtested p90 band on every cost quote
- Tier: low
- Domain: finance (value at risk)
- Lens: markets and auctions
- What: `fm queue --cost` and `fm goal show` gain a p90 cost and finish date per task from the spread of similar past closes, not only the median. Each line shows the band's backtested coverage, the share of past tasks that landed inside it.
- Prior art: Monte Carlo burn-up charts and value-at-risk bands; Foreman's `fm queue --cost` (T-1878, a median per type and tier) and goal estimate (T-2145, a P25–P75 time range with no coverage check).
- Better by: the band's coverage is measured and printed, so a quote can be held to and priced.
- Novelty: 2
- Needs: none
- Unblocks: M-01, M-11
- Kill: Backtest the last 100 closed tasks, each quoted only from tasks closed before it; pass if at least 85% land under their p90, fail below.
- Stage: idea
