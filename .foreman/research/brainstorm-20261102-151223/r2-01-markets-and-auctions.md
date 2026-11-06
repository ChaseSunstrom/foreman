# Brainstorm — lens: markets and auctions

- **Keep double-entry books for every dollar** — FEATURE — value 4 — effort M — risk low — category: spend accounting
  Why: tier high; domain accounting. Today `fm run --stall-usd`, spend receipts and `fm burden` each measure spend separately, and nothing proves they add up. Each dollar becomes a debit on a task, lane, tick or child process and a credit to a transcript-usage source. A trial balance row in `fm doctor` flags orphan spend. Prior art: none found in coding harnesses, though cloud FinOps tools tag costs. Assumption: transcripts expose enough usage to credit against.
  Done when: a fixture run with one untagged child process makes `fm doctor` print a nonzero trial-balance gap naming that child, and a clean run prints zero.

- **Publish a task-price index** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: tier xhigh; domain macroeconomics (CPI). A fixed basket of 10 canonical tasks is replayed weekly and reports dollars, minutes and verified-close rate per task. This catches silent model drift or price changes that affect every verb at once. The earlier ideas swap models once or run single ablations. This one is a time series. Prior art: model benchmarks exist, but none are priced on the user's own repo. Assumption: the `plugin/tests/fixtures` repos can serve as the basket.
  Done when: two runs against a stub backend with a doubled price produce an index of about 2.0x and a named regression line.

- **Learn the user's price from revealed preference** — FEATURE — value 5 — effort L — risk med — category: user model
  Why: tier xhigh; domain econometrics. The user's overrides, `--stall-usd` choices, drops and "re-grounded to S" steers are trade-offs between dollars, time and risk. Foreman fits a simple utility curve to them and uses it as the default for budgets and stall limits. This is learned rather than set, unlike the earlier "charge the user's attention a price" idea. Prior art: conjoint analysis and inverse reinforcement learning; none found in harnesses. Cheapest experiment: fit on the last 100 decisions and check whether it predicts the next 20 better than a constant default.
  Done when: a held-out replay shows the fitted defaults match the user's actual choice more often than the fixed default, with the numbers printed.

- **Set audit rates by probation bond** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: tier high; domain the market for lemons and inspection games. A new backend, model or lane starts at 100% independent replay of its closes. The rate falls as verified closes accumulate, and one caught false close resets it. T-2656 to T-2671 show closes the user had to re-ground. Prior art: sampling audits in finance and manufacturing. Assumption: replay cost is small next to a false close.
  Done when: a stub backend with a planted false close is audited every time until it earns a lower rate, and the audit log shows the rate changing.

- **Charge queue rent and evict the unwanted** — CLEAN — value 3 — effort S — risk low — category: queue hygiene
  Why: tier medium; domain real estate and holding costs. Each queued or deferred task accrues rent, and the rent is waived when new evidence matches the brief (T-2656). Tasks past a threshold get a one-line obituary and move to a graveyard file. The dropped items above show stale asks pile up. Prior art: stale-bot on GitHub, though it uses a fixed timer. Cheapest experiment: apply it to the current queue and count how many evictions the user reverses.
  Done when: `fm queue` shows rent per task, and a test with a 90-day-old task evicts it with a reason.

- **Net lane file intents through a clearinghouse** — FEATURE — value 4 — effort L — risk med — category: coordination
  Why: tier xhigh; domain securities clearing. Builder lanes declare the files they intend to touch before editing. A clearinghouse matches disjoint sets, queues overlaps and settles the merge order. This avoids conflicts rather than resolving them. Prior art: file locks and merge queues; netting is new. Assumption: lanes can predict their files from the brief.
  Done when: two lanes with overlapping intents are serialised, and a conflict-free pair runs in parallel in a fixture.

- **Price each retry, hedge and fallback on the receipt** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: answers the left question about agent behaviours changing spend unseen. The receipt gains a line per retry, hedge, fallback and skip, with the dollars it cost and whether it changed the outcome. This extends the yield-per-dollar receipt (c22) down to the behaviour level. Prior art: itemised invoices. Assumption: the events are already logged.
  Done when: a run with one forced fallback shows a receipt line with its cost and outcome.

- **Hold big tasks for model price drops** — PERFORMANCE — value 3 — effort M — risk med — category: cost
  Why: tier high; domain real options. Deferred, non-urgent, expensive tasks wait on a watch for cheaper or stronger models, using the vendor-release watcher already proposed. The option value of waiting is shown next to the cost of delay. Prior art: spot-instance schedulers wait on price; none do this for model releases. Assumption: the user has tasks where a week's delay is harmless.
  Done when: a stub price feed dropping 40% wakes a held task, and the receipt cites the saving.

- **Give each hook a latency allowance** — PERFORMANCE — value 3 — effort S — risk low — category: footprint
  Why: tier medium; domain Pigouvian taxes. `bench_hooks.py` and `fm burden --by-source` already measure the cost. Each source gets an allowance, and one that exceeds it for a week is flagged for disabling with the user's name on the decision. It targets the footprint the user feels, per the left question.
  Done when: a planted slow hook is named in `fm doctor` within one bench run.

- **Wild: run a bankruptcy court for exhausted budgets** — FEATURE — value 4 — effort M — risk med — category: budgets
  Why: tier xhigh; domain bankruptcy law. When a run hits its budget mid-task, Foreman files a restructuring plan. It salvages partial work on a branch, ranks dependent tasks as creditors, and lists what a smaller second budget could finish. Prior art: Chapter 11; none found in harnesses. Evidence: `--stall-usd` stops runs, but the half-finished state isn't handled.
  Done when: a run killed by the budget leaves a branch of salvaged work and a plan file with a ranked order.

- **Wild: crowdfund missions all-or-nothing** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: tier xhigh; domain Kickstarter. A Genesis Mission or large brief starts only when pledged budget, from the user's own allowance or a team's, covers a quote at the 80th percentile. Otherwise nothing is spent, and Foreman reports what was missing. Prior art: none found for agents. Assumption: there is a quote model, perhaps from "quote before building".
  Done when: an underfunded mission stays unstarted and prints the shortfall, and a funded one starts.

- **Wild: route work through a privacy dark pool** — SECURITY — value 4 — effort L — risk med — category: privacy
  Why: tier high; domain dark pools and venue selection. Each task gets a sensitivity grade and a leakage price per backend. Sensitive tasks go to the local model, and the receipt names the venue and what each choice cost in dollars. This extends the reverse auction across backends with a privacy term. Prior art: smart order routers; none for privacy.
  Done when: a task tagged secret never reaches a remote backend in a stub run, and the routing line appears in the receipt.

Next question: which of these prices (dollars, minutes, risk) does the user actually accept being traded off against each other, and in what exchange rate?
Next question: when two of the auction or market mechanisms disagree on the same task, which one does the user trust, and who settles it?
