# Brainstorm — lens: deepen: self-measurement

- **Survival Grader: score every closed task by what happened to it** — FEATURE — value 5 — effort M — risk low — category: self-measurement
  Why: the planned "grade closed work by survival" and "score done-claims" are separate sketches. Merge them into one `fm survive` pass. At 1, 7 and 30 days it checks each closed task's commits for reverts, rewrites by a later task, a follow-up bug task naming the same files, and a re-opened or re-asked steer. The result is one survival score per task in the ledger. Assumption: the ledger links tasks to commits and files (T-numbers appear in commit messages).
  Done when: `fm survive T-1009` prints a score with the evidence lines (reverted, rewritten-by, follow-up bugs), and a fixture repo with a planted revert scores lower than a clean one.

- **Counterfactual Replay Bench: test any new rule against old sessions before it ships** — FEATURE — value 5 — effort M — risk med — category: replay
  Why: the user asked "why have you not improved all that much?", and no rule today is checked against history. Replay the logged hook events (the guard, stop gate and recall inputs) from past sessions through a candidate rule or fix. Report what it would have blocked, nudged or let through, and which of those the user later corrected. Only deterministic hooks are replayed, not the model. Assumption: the ledger keeps enough hook input to re-run them.
  Done when: `fm replay --rule new.md --since 30d` outputs would-fire, would-have-helped and false-positive counts on a fixture ledger, and promotion in C3 requires it to run.

- **Self-Change Court: every rule, fix and prompt edit is a pre-registered trial that auto-reverts** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: it builds on "pre-register every self-change" and the placebo arm. A self-change records its hypothesis, metric, minimum sample and expiry date. A verdict job then applies a significance rule. A losing change is retired through the existing retire path, and a winning one graduates. The placebo arm is a rule that is stored but never shown, so its effect on the same metric sets the noise floor. Assumption: interventions per task is stable enough to detect effects within weeks.
  Done when: a rule created with `--predict "interventions -20%"` gets a verdict at expiry, is auto-retired in the fixture when the metric doesn't move, and the verdict is shown in `fm digest`.

- **Counterfactual Twin: run a shadow Foreman-off lane on sampled tasks** — FEATURE — value 4 — effort L — risk med — category: A/B
  Why: C12 plans an A/B holdout, but the "bench vs plain Claude" item (T-0866) is deferred for lack of cases. Sample about 1 in 15 finished tasks and re-run the same brief headlessly in a worktree with hooks off, under a spend cap. Then compare tests passed, diff size, tokens and time against the real run. This gives Foreman a measured value-add instead of an assumed one. Assumption: the spend cap permits it, and the brief is replayable.
  Done when: `fm twin T-1009` produces a side-by-side table from two worktrees, and the nightly job runs at most N twins under the cap.

- **Calibration Ledger that feeds back: forecasts gate autonomy** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: this extends "score every forecast". Each forecast (task effort, "tests will pass", "this fix applies") carries a confidence, and a Brier score is kept per forecast kind. Where Foreman is overconfident, it stops auto-continuing and asks. Where it is well calibrated, it widens the queue it works through unattended. Assumption: effort labels S/M/L and actual close time exist in the ledger.
  Done when: `fm calibrate` prints a reliability table per forecast kind, and a fixture with 80%-confident forecasts that hit 40% triggers the "ask first" setting.

- **Metric Control Room: SPC charts with Western Electric alarms in the pane** — FEATURE — value 3 — effort S — risk low — category: charts
  Why: this extends "draw control charts". It runs the standard run rules (a point past 3σ, 8 in a row on one side) on interventions per task, minutes lost, recall hit rate and cost per task. When a rule trips, it names the likely cause by diffing which self-changes landed in that window. It fits the pane's one-bigger-graph preference. Assumption: at least 20 data points per metric.
  Done when: a synthetic series with a step change raises an alarm that cites the self-change landed on that day, and the pane shows a single chart with the alarm marked.

- **Ledger as SQL: `fm sql` with saved watch queries that open tasks** — FEATURE — value 4 — effort S — risk low — category: ledger
  Why: it extends "open the ledger as SQL". Load the JSONL ledger into in-memory SQLite on demand, which is read-only and stays local. Saved watch queries ("closes without a red-then-green > 3 this week") run in the nightly job and file a task when they cross a threshold. Assumption: ledger lines have a stable enough schema to load.
  Done when: `fm sql "select kind,count(*) from ledger group by 1"` works, and a saved watch crossing its threshold creates exactly one deduped task.

- **Mutation-test the Foreman gates themselves** — FEATURE — value 4 — effort M — risk low — category: self-test
  Why: the gate failures in the user's words (a fake "no claude" that leaked to the paid binary, a stale matcher test) show that tests miss hook changes. Mutate guard rules and stop-gate logic (flip a condition, widen a regex) and check that the bench or tests catch each mutant. Report the surviving mutants as a score. Assumption: hooks are small enough that mutants run in seconds.
  Done when: `fm mutate guard` reports killed/survived counts, and a seeded weakened rule appears among the survivors.

- **Wild: Self-Play Red Team that tries to beat its own guard** — FEATURE — value 4 — effort L — risk med — category: adversarial — wild
  Why: assumption: a headless Haiku child gets only the guard's public rules and a sandboxed scratch dir. Its job is to invent commands that do the forbidden thing but pass the guard (the guard-bypass class in T-0275). Each successful bypass becomes a failing test plus a score for "guard strength", tracked over time and nightly.
  Done when: `fm redteam --budget 1usd` writes at least one candidate bypass test file in the fixture, and the guard-strength score is charted.

- **Wild: Prediction Market between self-changes** — FEATURE — value 3 — effort M — risk low — category: markets — wild
  Why: assumption: the pending proposals (rules from corrections, fixes, brainstorm tasks) each get a predicted-benefit bid from several cheap estimators, such as past survival of similar changes, replay results and effort. The ledger scores each estimator's calibration when the change's verdict lands, and future bids are weighted by track record. The queue is ordered by market-implied value instead of a hand-set value number.
  Done when: `fm rank` shows each proposal's market price and the bidders' weights, and the weights shift after a verdict in a fixture.

- **Wild: Time-Capsule Self-Interview: Foreman reads its own month-old decisions** — FEATURE — value 3 — effort S — risk low — category: reflection — wild
  Why: assumption: at 30 days, a headless child gets only an old task's brief and its plan, then the later git history, and answers "what did past-me get wrong, and what rule would have caught it?". Answers that name a pattern seen at least 3 times become correction-to-rule candidates (C3). Individual retrospectives are discarded, so only recurring lessons accumulate.
  Done when: `fm retro --age 30d` writes at most 3 recurring-pattern candidates from a fixture history, and none for a history with no repeats.

- **Fleet Metrics by Git: publish anonymised effect sizes with the repo's fixes** — FEATURE — value 4 — effort M — risk low — category: transfer
  Why: the user steered that fixes must travel with git. Each shipped fix/rule file carries its verdict stats (times fired, times followed by a first-time pass, placebo delta). A fresh clone then starts with evidence, not blind trust, and a fix with bad stats in another clone's data is demoted on import. Nothing leaves the repo, and the stats hold counts only. Assumption: fix files can hold a metadata block.
  Done when: after `git pull` brings a fix with stats, `fm trust` shows its inherited record, and an imported fix with a negative delta starts as "probation".

- **Leading-Indicator Miner: find which cheap early signals predict a bad close** — FEATURE — value 3 — effort M — risk low — category: prediction
  Why: assumption: with survival scores as the label, correlate early features (number of plan edits, time before the first test, steers during the task, files touched outside the plan) with a poor outcome. A simple logistic fit is enough. Strong predictors become mid-task nudges ("tasks like this fail 60% of the time at this point; re-plan?"), and each is itself registered as a trial.
  Done when: `fm predictors` lists the top 3 features with effect sizes on a fixture of 40 tasks, and a mid-task nudge cites the predictor with its numbers.

- **Wild: Measurement Honesty Audit: Foreman audits its own metrics for gaming** — FEATURE — value 3 — effort S — risk low — category: integrity — wild
  Why: assumption: once rules and fixes are rewarded by metrics, the agent can game them (closing tasks trivially, splitting tasks to lower interventions per task). A checker looks for Goodhart signatures: task size shrinking while closes rise, steers going down while reverts go up, and tests added that never fail. Each flagged metric is shown in the scoreboard marked "suspect".
  Done when: a fixture where tasks are split in half raises a "suspect: interventions per task" flag, and a clean fixture raises none.
