# Brainstorm — lens: economics of a generation

Round 2 under the economics lens. These skip what's already listed (budget envelope, cost ledger, cost per scenario, early stop, screen then full exam, usage-limit pause, model per step, reuse of unchanged results, bid for budget, break-even receipt, idle-quota overnight runs).

- **Price a rewrite by its marginal scenarios per dollar against its parent** — FEATURE — value 5 — effort M — risk low — category: selection
  Why: the pack's selection rule is "closes more exam scenarios than its parent", with nothing about price. Assumption: a rewrite tied at 3× cost currently looks like a tie, but it's a regression.
  Done when: `fm genesis status` shows, for each rewrite, Δscenarios, Δdollars and Δseconds against the parent, and a fixture rewrite that closes +1 scenario at 4× cost is marked "won, but expensive" and not promoted by default.

- **Add a cost-regression check to the carry-over defaults** — FEATURE — value 4 — effort S — risk low — category: carry-over
  Why: the Mission 2 focus says winning Seed and mission templates carry over as defaults, and nothing records what they cost to run. Assumption: a template that wins can still triple token use in a later project.
  Done when: each default in `defaults.json` stores its median cost per closed scenario, and a default whose cost on a new project exceeds 2× its stored median is flagged for review.

- **Rank not-yet entries by expected value per retry dollar** — FEATURE — value 4 — effort M — risk low — category: not-yet ledger
  Why: the not-yet ledger is retried every generation, and "no idea killed for ambition" is a standing steer. Retrying everything every generation will eventually dominate the bill. Assumption: attempts and blocker age are enough to estimate a retry's odds.
  Done when: with a budget for 3 retries and 10 ledger entries, the generation retries the 3 with the highest (value × odds ÷ cost), and `status` lists the other 7 with a reason for skipping them. None is dropped.

- **Calibrate cost forecasts against actuals and show the error** — OBSERVABILITY (FEATURE) — value 4 — effort M — risk low — category: forecasting
  Why: the ideas so far include "price a held-out exam before approving it", but a price with no track record is only a guess. Assumption: `exam.jsonl` already holds per-run cost for the finders, foreman and plain-session arms.
  Done when: every forecast is stored beside its actual cost, and `fm genesis status` shows the median error. A forecast that has been off by more than 50% over the last 5 runs is labeled "unreliable" and cannot approve a run on its own.

- **Gate the plain-Claude arm on whether it could change the decision** — PERFORMANCE — value 4 — effort S — risk low — category: exam spend
  Why: the foreman and plain session arms are the costliest part of `fm exam run`. Assumption: for a scenario where the empty arm and the oracle already separate the two outcomes widely, a session arm adds cost and no information.
  Done when: a session arm is skipped on scenarios where the finders arm already decides the parent-vs-rewrite comparison with a stated margin, and the skip is recorded with its reason. A replay of a past tower produces the same selection outcome with fewer paid calls.

- **Stop at the first generation whose spend can't be justified by the last gain** — FEATURE — value 4 — effort S — risk med — category: stop rules
  Why: the pack has "stop early once the marginal gain falls off" for within a generation, but nothing at tower level. Gen-1 to gen-2 can keep spending after the tower has plateaued. Assumption: the plateau is visible in closed-scenario counts across 2 generations.
  Done when: after two consecutive generations that close fewer than N new scenarios each, the tower halts and writes "plateau: spent $X for +k scenarios" into `status`, plus a one-line question to the user about continuing.

- **Charge auto-start for what the last auto-start produced** — FEATURE — value 3 — effort S — risk low — category: auto-start
  Why: the pack covers "cap what auto-start spends per project" as a flat cap. Assumption: a project whose previous auto-start closed nothing deserves a smaller allowance than one that closed many.
  Done when: the allowance for each auto-start is derived from the prior auto-start's closed-scenarios per dollar, and a project with two empty runs in a row gets a proposal only, with no spend.

- **Report the user's own time as a cost: count the questions and approvals a generation asked for** — FEATURE — value 3 — effort S — risk low — category: attention cost
  Why: the user's recent asks show them correcting and steering often, and each "user's yes" in the Mission 2 design is a human interruption. Assumption: attention is the scarcest resource and nothing meters it.
  Done when: `status` shows interruptions per generation, and a tower that asked more than a set number of questions per closed scenario gets a note recommending that it batch its asks into a single card.

- **Wild: Run a "cheap twin" tower on a small model, and spend big only when the twin and the real tower diverge** — FEATURE — value 4 — effort L — risk med — category: model economics
  Why: wild. The tower mostly writes and ranks text. Assumption: Haiku-class output ties the larger model on most steps, so disagreement is the signal worth paying to resolve.
  Done when: on a fixture project, the twin runs end to end for under 25% of the real tower's cost, and the report lists the steps where the two differ. Only those steps are rerun on the stronger model.

- **Wild: Quote the whole tower like a contractor before it starts, then hold itself to the quote** — FEATURE — value 4 — effort M — risk low — category: budget UX
  Why: wild. Assumption: users approve more readily, and burn less, with a fixed range up front ("gen-0 write, 3 generations, about $9 to $14, 40 to 70 minutes") than with an open-ended run. Overruns past the high end pause and ask.
  Done when: `fm genesis plan` prints low/expected/high cost and time from the calibrated forecasts, and a run that crosses the high figure halts with an itemised bill and an offer to extend.

- **Wild: Let a failed generation sell its salvage** — FEATURE — value 3 — effort M — risk low — category: waste recovery
  Why: wild. A rewrite that loses selection still paid for exam scenarios, critiques and briefs. Assumption: parts of it, such as a sharper brief or a well-formed scenario, are reusable even though the whole lost.
  Done when: each lost rewrite is split by section, with each section tagged "won / tied / lost" against the parent on the scenarios it touched, and a winning section can be offered as a candidate patch to the parent without rerunning the exam.

- **Show the cost curve against plain Claude on the same held-out scenarios** — FEATURE — value 4 — effort M — risk low — category: value proof
  Why: "Foreman beats Claude Code on the duel: more tasks passed, lower cost, less time" is an open deferred item (T-1231). Assumption: a tower is only worth its spend if its output beats the plain arm for the money.
  Done when: the Genesis page and `status` show, per generation, scenarios closed and dollars for the foreman arm and the plain arm side by side, with a visible "not worth it yet" state when the plain arm is cheaper at equal closure.

Next question: What does the user consider a fair price for one closed scenario, and does that price change by scenario kind (a planted bug versus a missing capability)?
Next question: Which spend is invisible today: child processes that `fm ideas`, `fm second` and the exam authors launch outside the tower's own meter?
