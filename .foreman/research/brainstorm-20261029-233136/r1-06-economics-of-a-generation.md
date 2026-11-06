# Brainstorm — lens: economics of a generation

- **Meter every generation in a cost ledger** — FEATURE — value 5 — effort M — risk low — category: cost ledger
  Why: exam.jsonl records scores and the Foreman vs plain arms record cost, but no tower-level record ties tokens, dollars and wall-clock to a generation. Without that, "is this rewrite worth it" has no denominator.
  Done when: `fm genesis status` prints, per generation, tokens, USD, wall-clock and scenarios closed, and the figures match the sum of the per-child cost records in a test run.

- **Report cost per scenario closed and rank rewrites by it** — FEATURE — value 5 — effort M — risk low — category: selection
  Why: selection today is "closes more exam scenarios than its parent". A rewrite that ties at 3× the cost counts the same as a cheap one. Assumption: cost per child is already captured by fm exam's session arms.
  Done when: lineage.md records for each parent/child pair the scenarios closed, the cost and the cost per closed scenario. A test fixture with a tie and a 3× cost difference picks the cheaper one.

- **Cap each Genesis run with a budget envelope** — SECURITY — value 5 — effort M — risk low — category: budget guard
  Why: the inversion risk "burns a week of usage on one project" has no stated limit. The harness already reports a USD budget. Assumption: the budget value can be read by fm.
  Done when: `fm genesis run --budget 20` stops at a generation boundary once spend reaches 20. The tower file records "stopped: budget", and a resume continues from that point without redoing finished work.

- **Stop a generation early once the marginal gain falls off** — PERFORMANCE — value 4 — effort M — risk med — category: early stop
  Why: the fixed 8 missions per generation spend the same amount whether mission 2 or mission 8 produced the gains. Assumption: per-mission exam deltas are measurable.
  Done when: a generation ends after two consecutive missions that close no new scenarios and lower no cost. The status line says why, and a replay of a recorded run on fixtures stops at the expected mission.

- **Screen cheaply, then run the full exam only on survivors** — PERFORMANCE — value 4 — effort M — risk med — category: staged exam
  Why: every rewrite is graded against the full exam, including session arms that cost real money. Assumption: finders and oracle arms are much cheaper than session arms.
  Done when: candidates first run only the finders arm. Only those that beat their parent there proceed to session arms, and the cost log shows session-arm calls cut by a stated fraction on a fixture tower.

- **Pause on a usage limit and resume at the reset** — FEATURE — value 4 — effort M — risk low — category: scheduling
  Why: a long tower will hit rate limits. Failing the generation wastes the spend so far. Assumption: a limit error and its reset time can be parsed.
  Done when: a simulated limit error makes the tower write "waiting until <time>" and exit cleanly. A later `fm genesis resume` continues at the same step with no repeated child calls.

- **Pick the model per step by price and difficulty** — PERFORMANCE — value 4 — effort M — risk med — category: model routing
  Why: tool-less brainstorm children, exam authors and graders do not need the top model. Briefs and rewrites might. Assumption: the model can be chosen per child.
  Done when: a config maps each tower step to a model tier. A fixture run shows lower cost with the same exam closure, and the ledger records the model used for each step.

- **Reuse unchanged results across generations** — PERFORMANCE — value 3 — effort M — risk med — category: caching
  Why: a rewrite that touches one section re-runs the whole exam. Assumption: scenarios can be keyed to the files and spec sections they depend on.
  Done when: a second run on an unchanged spec reports zero new child calls for cached scenarios. Changing one section invalidates only the scenarios that depend on it.

- **Price a held-out exam before approving it** — FEATURE — value 3 — effort S — risk low — category: forecasting
  Why: the exam asks for at least 9 scenarios with at least 3 held out, across 6 languages, and the user has no preview of the bill. Assumption: past cost per scenario kind can be averaged.
  Done when: `fm genesis plan` prints an estimated cost range before any child starts. After the run, the actual cost is compared to it in the ledger.

- **Show the cost-per-closed-scenario curve on the Genesis page** — FEATURE — value 3 — effort S — risk low — category: site page
  Why: the live tower page already exports generations. The user wants more per-generation detail on it.
  Done when: the exported page shows a chart of cost, time and scenarios closed for each generation. The reduced-motion and palette checks still pass.

- **Wild: Let generations bid for budget** — FEATURE — value 3 — effort L — risk high — category: market (wild)
  Why: assumption: candidate rewrites could each estimate their expected gain per dollar, and the orchestrator funds the best bids first. This is a play on the "no idea killed for ambition" rule, which needs a priced way to keep weak ideas alive cheaply.
  Done when: a fixture with three candidates funds them in expected-gain-per-dollar order. The estimate-versus-actual error is logged and bids shrink for candidates whose estimates were wrong earlier.

- **Wild: Run the cheap ideas overnight on idle quota** — FEATURE — value 3 — effort M — risk med — category: idle compute (wild)
  Why: assumption: the not-yet ledger retries could run in off-peak windows or on local models, so retries cost little while the user is away.
  Done when: not-yet retries marked "low priority" run only inside a configured window or against a local engine. A day-long dry run shows none starting outside it.

- **Wild: Give each project a break-even receipt** — FEATURE — value 2 — effort M — risk med — category: ROI (wild)
  Why: assumption: `fm outcomes` 30-day survival could be compared to spend, so Genesis states plainly "this tower cost $X and its changes survived at Y%". That tells the user when to stop running Genesis on a project.
  Done when: after 30 days a receipt links each generation's cost to the survival of the tasks it produced, and the loop does not auto-start Genesis on projects whose receipts show poor return.

- **Stop auto-start from burning money on quiet projects** — SECURITY — value 4 — effort S — risk low — category: auto-start guard
  Why: starting by itself when the queue runs dry is the highest-spend path and the least supervised. Assumption: it will be added to the loop.
  Done when: auto-start needs a per-project spend cap and a minimum gap since the last tower. Without those it only proposes a run, and a test shows a dry queue twice in a day starts one tower, not two.

Next question: What does the user consider a fair price for one closed scenario, and is that a dollar cap, a share of the weekly usage, or wall-clock time?

Next question: Do the session-arm costs in `fm exam` already include the Genesis children's own spend, or is tower overhead (briefs, critiques, drift check) currently unmeasured?
