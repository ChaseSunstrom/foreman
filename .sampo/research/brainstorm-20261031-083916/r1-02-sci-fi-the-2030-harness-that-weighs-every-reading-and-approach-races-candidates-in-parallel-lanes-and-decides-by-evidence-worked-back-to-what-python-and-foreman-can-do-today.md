# Brainstorm — lens: sci-fi: the 2030 harness that weighs every reading and approach, races candidates in parallel lanes and decides by evidence, worked back to what Python and Foreman can do today

- **Score confidence like a forecaster** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: Seed #8 wants Foreman to state confidence, but T-2290 predicts only minutes and attempts. Nothing checks whether "80% sure" was right 80% of the time.
  Done when: every plan assumption stores a stated confidence, and `fm calibration` prints a per-tier Brier score and a bucket table from closed tasks (red-first test on a fixture ledger).

- **Stop only for the irreversible and ambiguous** — FEATURE — value 5 — effort M — risk med — category: judgment
  Why: Seed #8 says "stops for me only when something is irreversible and ambiguous". The pack shows this as prose, not a rule. A deterministic table (push, publish, migrate, delete, spend) crossed with the confidence ledger would make it testable.
  Done when: a test shows a reversible, ambiguous choice is decided and recorded with no `fm ask`, and an irreversible, ambiguous one calls `fm ask` exactly once.

- **Race designs at plan time, not only when stuck** — FEATURE — value 5 — effort L — risk med — category: parallel lanes
  Why: T-2271 races the runner-up only after 3 failed runs. For an L task whose Approach lists 3+ options, the cheaper moment to race is before the first edit. Seed row (4) says "auto race by evidence".
  Done when: `fm lane race --plan ID` starts one lane per named option and prints a table with columns tests, diff size, blast neighbours and bench, then picks a winner by script.

- **Pick the winner with a user-owned rubric file** — FEATURE — value 4 — effort S — risk low — category: evidence
  Why: the question "which verbs have a model on both sides with no user-owned check?" applies directly. If a model chooses the winner, the race is judged by the same kind of thing that wrote the candidates.
  Done when: `rubric.toml` holds the weights, the pick is pure Python over recorded numbers, and a test shows that changing a weight flips the winner on a fixture.

- **Scale race depth to risk** — PERFORMANCE — value 4 — effort S — risk low — category: cost
  Why: the request says "scale the depth to the risk, so an S task doesn't pay an L task's cost". Tier already gates the plan content, but lane count and cost cap are unspecified.
  Done when: a table test shows S gets 0 lanes, M gets at most 2, and L gets at most 3. A race is refused if its estimated tokens exceed the cap derived from the blast radius.

- **Write a falsifier with every chosen approach** — FEATURE — value 4 — effort M — risk low — category: decisions
  Why: "decides and records" has no way to reopen a choice. A "what would change my mind" line, such as a bench threshold or a test name, lets later evidence reopen the race instead of being rationalised away.
  Done when: the plan gate requires a Falsifier line on M/L tasks. A failing named check reopens the race, and the event is logged.

- **Audit regret on the road not taken** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: T-2291 routes models from re-fixed and reverted history. The same signal can test the race rule: when a merged task is re-fixed, run the kept runner-up lane's verify and see whether it would have survived.
  Done when: `fm regret` lists reopened tasks with a pass or fail for each saved runner-up, and shows a rate by option-count and tier.

- **Make an adversary lane break the winner before merge** — SECURITY — value 4 — effort M — risk med — category: verification
  Why: the steer on signals Foreman didn't author argues for a writer that hasn't seen the winning code. It gets only the criteria and writes one hostile test.
  Done when: for L tasks the merge waits for that test. A fixture task with a planted edge-case bug is caught by it, and one with no bug passes.

- **Reuse research notes by scope path** — PERFORMANCE — value 3 — effort S — risk low — category: research
  Why: the research trigger fires when confidence is low. Without a lookup keyed to paths or topic, the same question is researched again in each task.
  Done when: focusing a task whose scope matches an existing note surfaces its citation line, and a test shows the research child is not spawned a second time.

- **Log every stop to see which were avoidable** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: nothing measures whether the new "only when irreversible" rule holds. Each `fm ask` or stop is tagged irreversible, ambiguous or neither by a cold reader, and the avoidable rate is reported.
  Done when: `fm triggers` gains a stops row with its avoidable share, and a seeded avoidable stop is flagged.

- **Wild: Run a nightly dojo on the repo's own history** — FEATURE — value 4 — effort L — risk med — category: learning
  Why: wild. The long-horizon tier already replays rolled-back commits. Replaying them again with each alternative approach class on a free arm, offline, would show which approach wins per task type, with no live task paying for it.
  Done when: a nightly job writes a per-type win table from at least 10 replayed commits, and the plan gate quotes it in the Approach hint.

- **Wild: Make lanes bet before they run** — FEATURE — value 3 — effort M — risk med — category: calibration
  Why: wild. Each lane states a pass probability before running, and the result is scored. A lane's past bets weight how much its claim counts in the next race, so overconfident routes lose influence.
  Done when: race output shows each bet and its score, and a fixture shows a habitually overconfident route's weight dropping.

- **Wild: Scrub the decision tape in the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild. The web UI could show readings considered, options raced, evidence and the falsifier as a timeline the user can scrub, so "why did it pick that?" is a view and not a log search.
  Done when: opening a closed M/L task shows its readings, race table and chosen falsifier in order, and an empty state is shown for S tasks.

Next question: When the rubric and the user's gut disagree about a race winner, which does the user actually overrule, and can that become the next rubric weight?
Next question: How many of the user's mid-goal interruptions would the irreversibility table have prevented, if replayed over past sessions?
