# Brainstorm — lens: deepen: ranking

- **Ship one `fm rank` ledger that every finding is priced through** — FEATURE — value 5 — effort M — risk low — category: ranking core
  Why: the list repeats "rank by value per dollar with a shown formula" in six phrasings. Merge them into one verb with one record per finding: `{kind, blast, churn, proof_cost, est_fix_cost, score, formula}`. Each score prints its formula beside it.
  Done when: `fm rank` on a fixture repo with 5 planted findings prints 5 rows in descending score, each with a formula string that reproduces the score when recomputed by hand.

- **Rank only findings that carry a proof** — FEATURE — value 5 — effort S — risk low — category: ranking gate
  Why: the exam shows the finders found 0 of 108 planted defects, and the mission requires a failing test before any fix. An unproven finding can't outrank a proven one. Unproven findings sit in a separate "suspected" tier with their precision shown.
  Done when: a finding with no failing test or repro never appears above a proven one in `fm rank`, and a test asserts this ordering.

- **Learn weights from outcomes, with a prior that holds until data arrives** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: the pack proposes learning weights from 30-day survival, `fm outcomes` exists, and reverts are already tracked. Start from fixed kind weights. Blend toward the measured survival and acted-on rate per probe only after N≥10 closed findings, so early noise can't flip the order.
  Done when: replaying a synthetic outcomes file where probe A's fixes are always reverted lowers A's weight below its prior, and with N<10 the weights equal the prior.

- **Score the ranking itself against the exam's held-out kinds** — FEATURE — value 4 — effort M — risk low — category: ranking eval
  Why: Mission 3 is graded on the none and bug kinds in never-seen repos. A ranker that surfaces 10 false bugs on a `none` repo fails. Measure precision@k and the abstain rate per run, and write them to `exam.jsonl`.
  Done when: `fm exam` output includes precision@3 and false-positive count for the ranker, and the `none` kind counts any surfaced finding as an error.

- **Abstain below a learned threshold, and say so** — FEATURE — value 4 — effort M — risk med — category: abstention
  Why: the exam has a `none` kind (repos with nothing to find). Combine the ROC-threshold idea with the "queue dry" question: when the top score is under the threshold, print "nothing worth your attention: N suspects dropped" rather than padding the list.
  Done when: on a clean fixture repo, `fm rank` exits 0 with the abstain message and zero findings, and on a planted-bug repo the bug clears the threshold.

- **Price findings in the user's own closing times** — FEATURE — value 3 — effort S — risk low — category: cost model
  Why: the pack asks to "price in the user's own closing times", and task history already holds durations per kind and size. Show "≈ 9 min, ≈ $0.17" beside each finding, using the median for that kind in this project, falling back to the Foreman-wide median.
  Done when: each ranked row shows an estimated time and cost taken from past tasks of the same kind, and the fallback is labelled.

- **Re-rank after each lane lands, because fixes change blast radius** — FEATURE — value 3 — effort M — risk med — category: dynamic ranking
  Why: the find→prove→fix pipeline runs several lanes (PARALLEL_MAX 3). A fix that touches a hot file can make two other findings stale or duplicate. Re-score the queue after each merge and drop findings whose proof test now passes.
  Done when: a fixture with two findings sharing a root cause shows both resolved by one fix, and the second is closed as "resolved by T-x", not fixed twice.

- **Give each probe a running record that decides whether it runs again** — FEATURE — value 4 — effort M — risk low — category: probe budgeting
  Why: this combines "score each probe by proven-fix yield per dollar" and "order the hunt by churn × complexity × past-fix density". A probe that spent $2 and produced 0 proven fixes across 3 repos is skipped on the next night run until a human re-enables it. The hunt starts with the hottest files.
  Done when: after three empty runs a probe is listed as "paused (0 proven / $2.10)" in `fm scout`, and `fm scout --probe NAME` still runs it manually.

- **Wild: Let probes stake budget on their own findings** — FEATURE — value 3 — effort L — risk med — category: market ranking
  Why: wild. Each probe holds a balance. It stakes credit on each finding, wins when the fix survives 30 days, and loses when it's reverted or never acted on. Rank is stake times its record, so a probe that is usually right gets more room in the morning list.
  Done when: a simulated history shows a probe with 80% survival ranking its findings above an equally confident probe with 20%, and balances persist across runs.

- **Wild: Have a second probe try to refute each finding before it ranks** — FEATURE — value 4 — effort M — risk med — category: adversarial check
  Why: wild. Cold-read review already exists (`fm second`). A tool-less refuter reads the finding and its failing test and tries to argue the test is wrong, or that the behavior is intended. Survivors get a "refuted-failed" badge and a score bonus. This targets the biggest risk on `none` repos, which is confident false positives.
  Done when: on a fixture where the "bug" is documented intended behaviour, the refuter marks it refuted and it drops out of the ranked list.

- **Wild: Print a morning digest that reads like a newsroom front page** — FEATURE — value 3 — effort S — risk low — category: presentation
  Why: wild. The user's habits (night queue, site, demos) suggest they like showing results. Lead with the one best finding in plain words and its receipt (test name, red→green), followed by a short list. Each line shows its formula on request, so the ranking explains itself.
  Done when: `fm rank --digest` prints a headline finding with its failing test path and ends with a count of dropped suspects.

- **Rank by proximity to what the user cares about** — FEATURE — value 3 — effort S — risk low — category: relevance
  Why: the pack lists "closeness to what the user already cares about". The steers show strong repeated interest (genesis, site, fm code). Boost findings in files that recent asks, open tasks or recent commits touched. Show the boost as a separate term.
  Done when: two findings with equal base score order by overlap with files in recently touched tasks, and the boost shows in the formula.

- **Wild: Backtest the ranker on git history** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: wild. Combines "forecast hotspots from git" with "check the ranking against what survives". Check out a repo as of 6 months ago, run the finders, and see whether the top-ranked files later received bug-fix commits. This gives weights and thresholds before any outcome data exists, on any repo with history.
  Done when: `fm rank --backtest <repo> --since 6mo` prints precision@10 against later fix commits and writes it to a calibration file the weights read.

- **Exclude Foreman's own setup failures from the ranked list** — FIX — value 3 — effort S — risk low — category: ranking hygiene
  Why: the pack notes that probe_doctor may queue Foreman setup failures as tasks in user projects. These would outrank real findings on a fresh repo. Tag them as "tooling" and list them in a separate line that never mixes with project findings.
  Done when: a project with a broken `fm` setup shows its findings with no probe_doctor task in the top-k, and tooling issues appear under a separate heading.

Next question: Do the rank weights learned on Foreman's own repo transfer to unseen repos, or do they need a per-language and per-size prior, as the exam's six languages suggest?

Next question: What does a finding cost when its proof fails, and should an abandoned proof attempt count against its probe's record or only the finding's?
