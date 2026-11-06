# Brainstorm — lens: ecology and evolution

- **Run lane tournaments with heritable strategy genomes** — FEATURE — value 5 — effort L — risk med — category: coordination
  Why: tier xhigh, domain evolution. Builder lanes in worktrees and `fm prove` already give a selection signal. A brief runs in N lanes whose genomes (prompt, model, plan style, test-first or not) differ. Proof strength and cost pick the winner, and the winner's genome seeds the next brief of that type. Prior art: AlphaEvolve and DGM-style self-improving agents, but none gated by evidence-closed tasks. Cheapest experiment: replay 20 closed tasks with 2 genomes each, and drop the idea if the winner can't be told apart from a coin flip.
  Done when: `fm run --tournament 2` closes a task with two lane receipts, names the winner by proof grade per dollar, and logs the genome.

- **Give every guard rule and lesson a fitness and let it senesce** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: tier medium, domain population ecology. This also answers the false-positive-cost question. A rule's fitness is the true catches it made minus the overrides and reruns it caused. Rules with zero firings across N sessions go to a "dormant" state and are revived only by a replay hit. Prior art: anergy in gen 2 promotes rules, but nothing demotes them. Cheapest experiment: score the existing rules against `fm replay` over 60 days and see whether many are dead weight.
  Done when: `fm doctor` lists rules by fitness, and one dormant rule is skipped at hook time, with the skip logged.

- **Run a Red Queen arms race between a bypass adversary and the guard** — FEATURE — value 5 — effort L — risk high — category: security
  Why: tier xhigh, domain coevolution. Unattended, an adversary agent mutates destructive commands (quoting, encoding, heredocs) until one slips through. Each escape becomes a guard test and a rule patch proposal, never auto-applied. `fm drill` and the red-team items (c13) are the seeds, and the pathological-timing test (T-2668) is a sibling. Prior art: fuzzing and grammar-based mutation, with no coevolving defender in the harness space. Cheapest experiment: one overnight run of 500 mutations against the current guard; zero escapes would mean the idea has little room.
  Done when: a run reports N mutants tried and M escapes, and each escape lands as a failing test.

- **Knock out a capability in a sandbox and measure the cascade (keystone test)** — FEATURE — value 4 — effort M — risk low — category: slimming
  Why: tier high, domain keystone species. It answers "when a capability is retired, who notices first". `fm usage --prune` lists unused verbs but can't say what depends on them. `fm drill --knockout VERB` disables the verb in a temp home, runs the e2e round trip, and prints which gates and readers break. Prior art: chaos engineering, though aimed at services rather than a tool's own verbs. Cheapest experiment: knock out 3 verbs by hand and see whether the round trip reports anything.
  Done when: knocking out a named verb yields a list of broken readers or an explicit "none broken" verdict.

- **Govern spend with a logistic carrying capacity** — FEATURE — value 4 — effort M — risk med — category: spend
  Why: tier high, domain population ecology. T-2669 (`--stall-usd`) is a fixed cap. Instead, estimate the yield curve (closes per dollar) from the receipts and scale lane count up while the marginal yield rises, then back off at the plateau. Prior art: autoscalers and bandit budgeting. Assumption: the receipts hold enough runs to fit a curve.
  Done when: a drive run adds or drops lanes based on marginal yield and the receipt states the reason.

- **Quarantine invasive processes: spawned children inherit no authority by default** — SECURITY — value 4 — effort M — risk med — category: authority
  Why: tier high, domain invasive species. This is the open question about lanes, ticks, `fm code` tools and prover children inheriting the push grant, credentials and the ledger key. Each spawn carries an explicit authority manifest (an allowlist), and the rest is stripped from its environment. Prior art: capability-based security. Cheapest experiment: list the environment and file handles of each child type and count the authorities it inherits.
  Done when: a test spawns each child type and asserts the push grant and signing key are absent unless the manifest lists them.

- **Report a diversity index across deciders and reviewers (monoculture risk)** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: tier medium, domain biodiversity. If the same model writes the code, the tests and the review, their errors are correlated. `fm doctor` reports a Shannon index over who proposed, proved and reviewed each close, and flags a stretch with a single source. Assumption: close records identify the model per role.
  Done when: `fm doctor` prints the index, and a synthetic single-model ledger scores 0 and is flagged.

- **Read the ledger as stratigraphy to date regressions** — FEATURE — value 3 — effort M — risk low — category: forensics
  Why: tier medium, domain paleontology. Hash-chained ledger layers hold metrics at each close, so `fm strata METRIC` shows the layer where hook latency or burden first shifted and names the closing task. Prior art: git bisect, which is blind to Foreman's own gauges. Cheapest experiment: chart `bench_hooks` history against the ledger by hand.
  Done when: given a planted latency step, the verb names the task that introduced it.

- **Cross-breed failed plans** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: tier medium, domain recombination. When two lanes each prove half of a brief, a merge lane takes the passing parts of both. Today the loser is discarded. Assumption: partial proof results are recorded per criterion.
  Done when: a brief whose criteria are split across two lanes closes from a combined lane.

- **Wild: run a digital terrarium that forecasts which verbs and rules go extinct** — FEATURE — value 3 — effort L — risk med — category: prediction — wild
  Why: tier extreme, domain ecosystem modelling. It fits a birth and death model to the usage and ledger history, simulates a year ahead, and predicts which capabilities decline, feeding `fm tidy` and the calibration of Foreman's own bets. Prior art: none found for a harness.
  Done when: a backtest on the first half of history predicts the verbs that were unused in the second half better than a "last-used" baseline.

- **Wild: share lessons between installs by signed horizontal gene transfer** — FEATURE — value 4 — effort L — risk high — category: federation — wild
  Why: tier massive, domain horizontal gene transfer. Installs optionally exchange fitness-scored lessons and guard rules as signed packets. Nothing leaves without an explicit setting and a user-visible diff, and each import enters dormant until it proves itself in a replay. Prior art: shared rule packs and `cc-skills`, without fitness evidence. Assumption: the privacy default is off.
  Done when: an exported packet imports on a second home, stays dormant, and activates only after a passing replay.

- **Wild: send predator agents after weak tests** — FEATURE — value 4 — effort M — risk low — category: proof — wild
  Why: tier high, domain predation. A predator lane mutates the code under a closed task and counts the mutants the task's tests fail to catch. Surviving mutants downgrade the stored proof grade (strong to weak), which the digests count. This gives the re-grounded grade question a real signal. Prior art: mutmut and Stryker, not wired into close grades.
  Done when: a task with a vacuous test gets a lowered grade, and the digest line shows it.

- **Choose work by succession stage** — FEATURE — value 2 — effort M — risk low — category: triage
  Why: tier medium, domain ecological succession. Classify the repo area by stage (new and churning, stabilising, climax) and favour exploration tasks early and hardening tasks late. Wakes for deferred tasks (T-2656) can use the stage as a signal. Assumption: churn per directory is a usable proxy.
  Done when: `fm next` shows the stage for each candidate and ordering changes with it.

Next question: which of Foreman's selection signals (proof grade, overrides, spend per close) can an agent game, and what is the Goodhart check for each?
Next question: when two lineages of lanes, rules or lessons diverge across the user's projects, what should transfer, and what must stay local?
