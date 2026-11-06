# Brainstorm — lens: reasoning ahead

- **Forecast a push's CI minutes before it lands** — FEATURE — value 4 — effort M — risk low — category: CI cost
  Why: The pack shows runs lost to the 20-min job cap and the 35-min macOS limit (T-1809). Nothing predicts the minutes a push will burn before it runs. Assumption: per-job durations from past runs are stored.
  Done when: `fm push --dry` prints a predicted minute range per job, and in a replay of the last 20 pushes the actual time falls inside that range for at least 16.

- **Project the suite's runtime growth to the commit that breaks the cap** — PERFORMANCE — value 4 — effort S — risk low — category: CI headroom
  Why: T-1808 added a 480 s kill, and the 20-min cap has hidden where time goes. The pack gives no trend, so the cap is hit by surprise. Assumption: per-run timings are kept.
  Done when: `fm doctor` names the first commit whose projected runtime passes 80% of the cap, computed from the last 30 commits' timings.

- **Pin each run to a model snapshot id, not an alias** — FEATURE — value 4 — effort S — risk low — category: model drift
  Why: The pack moved every builder to Sonnet and reran the cost math after a model change. An alias can repoint mid-queue, so one queue can mix two models without notice.
  Done when: each run's journal records the snapshot id, and a queue whose alias resolves to a new id halts before its next run and asks for a cost recompute.

- **Pause new lanes on a provider incident feed** — FEATURE — value 4 — effort M — risk med — category: incident safety
  Why: The pack lists API errors and usage limits as stall causes. Lanes start into an outage and fail one by one. Assumption: the provider publishes a machine-readable status feed.
  Done when: with a simulated feed that flags an outage, no new lane starts within one poll interval, and lanes resume within one interval after the flag clears.

- **Project journal and receipt growth and compact before the disk fills** — PERFORMANCE — value 3 — effort S — risk low — category: disk headroom
  Why: The ideas list has compaction, but nothing forecasts when the state volume fills. Assumption: journal size grows roughly linearly with events.
  Done when: `fm doctor` shows days-to-full for the state volume, and compaction is scheduled automatically when that falls under 14 days.

- **Price the expected loss of each gate a run skips** — FEATURE — value 3 — effort M — risk low — category: gate risk
  Why: `fm check --affected` skips gates silently. The cost of a missed failure is never shown. Assumption: the flake and escape ledgers can supply rough failure rates per gate.
  Done when: `fm check --affected` prints the probability-weighted cost of each skipped gate on its summary line, and the figure matches a seeded escape in a test.

- **Expire each plan assumption on a timer and re-check it when it lapses** — FEATURE — value 3 — effort M — risk low — category: plan trust
  Why: Plans rest on facts that go stale, such as the cap, the model, and the reset date. The pack shows a deferral that fired at the wrong time because its assumption had aged. Assumption: plans can record assumptions as data.
  Done when: an assumption with a 7-day TTL is re-checked on the day it lapses, and a failed re-check blocks the next step with the stale fact named.

- **Name each plan's falsifiers and check them at every step** — FEATURE — value 4 — effort M — risk med — category: early stop
  Why: A plan states what success looks like, but not what would prove it wrong. Runs continue long after the premise fails. Assumption: the planner can state conditions that would refute the plan.
  Done when: a plan with a stated falsifier that trips stops before its next edit, and the trip is written to the receipt with the falsifier quoted.

- **Buy a probe only when its expected information beats its cost** — FEATURE — value 3 — effort M — risk low — category: probe economics
  Why: Runs take expensive verification steps even when the answer is already known. Assumption: prior outcomes give a rough probability for each probe's result.
  Done when: `fm task` shows each probe step's expected cost and expected information gain, and a probe with gain below cost is skipped and logged with that reason.

- **Wild: a brake test before every long run** — FEATURE — value 4 — effort S — risk low — category: safety drill
  Why: A stop that has never been tested may not work when it matters. The pack's stop and kill paths are exercised only in failures. Assumption: a run can be halted at a known step on demand.
  Done when: before a run longer than 30 minutes starts, a 60-second drill halts a dummy run mid-step, and the run starts only if the halt lands within 5 seconds.

- **Wild: order the queue by a two-reset look-ahead** — FEATURE — value 4 — effort L — risk med — category: queue order
  Why: A queue that ignores the next usage limit can lose its greens to the wall. Assumption: the reset schedule and per-task cost forecasts are known.
  Done when: for a seeded queue straddling a reset, the chosen order completes at least as many tasks as the naive order, and the receipt states the greens it expects to lose.

- **Wild: a fuse that burns down with each task's forecast cost** — FEATURE — value 3 — effort S — risk low — category: spend visibility
  Why: Spend is seen only after it is paid. A visible fuse makes the remaining budget a shape the user can read. Assumption: the forecast cost is updated as the run progresses.
  Done when: the fuse's length matches the remaining forecast at every step in a replayed run, and it reaches zero exactly when the spend cap would stop the queue.
