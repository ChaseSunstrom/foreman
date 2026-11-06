---
id: T-2687
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T22:44:24Z
updated: 2026-11-02T22:51:49Z
base_note: Calibration: this plan states Choice 70% where RESEARCH M closes (27) held on the first finish 96% of the time: 26 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-02T22:44:52Z
rival_split: true
base: 33b4ee6f798786eae6c7669eb2cef21022fddec6
base_tree: 9cfdfd32a98872475f4c567f91c6b6505f7fefe4
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-02T22:45:06Z
plan0_scope: []
verified: strong
unproven: [research-uncited]
---
# M-12 kill test (moonshot spike, gen 3): does a log-weighted pool of three blind forecasters beat the best one on whether a close survives 14 days?
## Raw request
> M-12 kill test (moonshot spike, gen 3): does a log-weighted pool of three blind forecasters beat the best one on whether a close survives 14 days?
## Interpretation
Reading 1 (chosen): run M-12's kill test as moonshot.md states it (pool vs best single Brier, margin 0.02), with a sample that can't leak era into the label, and record the verdict. Reading 2 (ruled out): build the decider market into fm task finish now. Ruled out: the campaign stages a big idea kill test first, and run 1 already shows the LLM forecasters at chance. Context: run 1 (scratch, before this task) held closes T-0014..T-0198 only, so its not-yet says nothing about forecasting.
## Assumptions (confidence)
## Acceptance criteria
- [x] the kill test ran on era-matched failed and held closes and printed its verdict — verify with `python3 bench/moonshot/kill_m12.py /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/moon/m12-run2.json 30`
- [x] moonshot.md's M-12 says Stage: kill with the verdict, numbers and this task as Evidence — verify with `grep -A14 '^### M-12' state/projects/foreman-4a056f/research/genesis/moonshot.md | grep -q 'Evidence: T-'`
## Non-goals
## Approach (options → choice → why)
1. Era-matched sample: label = fixed or reverted within 14 days of close, both classes closed 14+ days ago, each failure paired with the nearest-id held close; leave-one-out log-score weights; bootstrap the margin. Likely outcome: not-yet, if the LLM forecasters stay near chance; fails if 30 pairs can't separate 0.02 (the bootstrap says so).
2. Natural-rate sample (4% failures). Fails if: the base rate dominates every Brier and 2-3 failures in 60 can't tell 0.02 apart.
3. Use what exists: fmoutcomes.outcomes for fates, fmideas.run_child for tool-less forecasters, answers cached. Likely outcome: one script, no product code.
4. Do less: keep run 1's verdict. Fails if: its label leaked era, so it says nothing about forecasting.
Choice 1 on 3 (70%): the doubt is sample size (30 pairs) and whether brief plus diff carries any signal at all; run 1's LLM forecasters were at chance (AUC 0.40 and 0.51).
## Risks and rollback
## Execution prompt
## Steps
1. [x] run the kill test (era-matched sample)
2. [x] record the verdict in moonshot.md (and not-yet.md if not-yet)
## Resume here
## Docs impact
none: a research spike; its script and answers are kept in bench/moonshot/ and its verdict in the tower files
## Verification evidence
- (ac 1) `python3 bench/moonshot/kill_m12.py /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/moon/m12-run2.json 30` → exit 0 · "verdict": "not-yet" / } [ran] [tree 29305a19a752] [world 2f1906870a] (2026-11-02T22:46:39Z)
- (ac 1) `python3 bench/moonshot/kill_m12.py /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/moon/m12-run2.json 30` → exit 0 · "verdict": "not-yet" / } [ran] [tree 2b5234f4b834] [world 2f1906870a] (2026-11-02T22:48:24Z)
- (step 1) `python3 bench/moonshot/kill_m12.py /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/moon/m12-run2.json 30` → exit 0 · "verdict": "not-yet" / } [ran] [tree 2b5234f4b834] [world 2f1906870a] (2026-11-02T22:48:27Z)
- (ac 2) `grep -A14 '^### M-12' state/projects/foreman-4a056f/research/genesis/moonshot.md | grep -q 'Evidence: T-2687'` → exit 0 · (no output) [ran] [tree 2b5234f4b834] [world 2f1906870a] (2026-11-02T22:49:52Z)
- (step 2) `grep -A14 '^### M-12' state/projects/foreman-4a056f/research/genesis/moonshot.md | grep -q 'Evidence: T-2687'` → exit 0 · (no output) [ran] [tree 2b5234f4b834] [world 2f1906870a] (2026-11-02T22:49:52Z)
- (ac 1) `python3 bench/moonshot/kill_m12.py /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/moon/m12-run2.json 30` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T22:48:27Z [ran] [tree 2b5234f4b834] [world 2f1906870a] (2026-11-02T22:49:53Z)
- (ac 2) `grep -A14 '^### M-12' state/projects/foreman-4a056f/research/genesis/moonshot.md | grep -q 'Evidence: T-'` → exit 0 · (no output) [ran] [tree 2b5234f4b834] [world 2f1906870a] (2026-11-02T22:49:53Z)
- (audit edge) `three runs of bench/moonshot/kill_m12.py: run 1 confounded (held closes T-0014..T-0198 only; base AUC 0.08), run 2 era-matched with a 14-day label, run 3 adds record-based forecasters with settled-only labels; verdict not-yet each time, margin -0.011 (90% CI -0.039..+0.016); cold rival read added walk-forward weights; cold reads passed moonshot.md, not-yet.md and the Mission` → the base rate first used fates settled after the forecast close (later fixes), which inflated its inversion; run 3 counts only labels settled 14+ days before the close being forecast [tree 2b5234f4b834] (2026-11-02T22:49:53Z)
- (audit intent) `three runs of bench/moonshot/kill_m12.py: run 1 confounded (held closes T-0014..T-0198 only; base AUC 0.08), run 2 era-matched with a 14-day label, run 3 adds record-based forecasters with settled-only labels; verdict not-yet each time, margin -0.011 (90% CI -0.039..+0.016); cold rival read added walk-forward weights; cold reads passed moonshot.md, not-yet.md and the Mission` → MOONSHOT.md asks for the cheapest experiment that could prove M-12 wrong; it did, and not-yet keeps the idea with its blocker, never killed for ambition [tree 2b5234f4b834] (2026-11-02T22:49:53Z)
- (audit edge) `three runs of bench/moonshot/kill_m12.py: run 1 confounded (held closes T-0014..T-0198 only; base AUC 0.08), run 2 era-matched with a 14-day label, run 3 adds record-based forecasters with settled-only labels; verdict not-yet each time, margin -0.011 (90% CI -0.039..+0.016); cold rival read added walk-forward weights; cold reads passed moonshot.md, not-yet.md and the Mission` → the base rate first used fates settled after the forecast close (later fixes), which inflated its inversion; run 3 counts only labels settled 14+ days before the close being forecast [tree 2b5234f4b834] (2026-11-02T22:50:53Z)
- (audit intent) `three runs of bench/moonshot/kill_m12.py: run 1 confounded (held closes T-0014..T-0198 only; base AUC 0.08), run 2 era-matched with a 14-day label, run 3 adds record-based forecasters with settled-only labels; verdict not-yet each time, margin -0.011 (90% CI -0.039..+0.016); cold rival read added walk-forward weights; cold reads passed moonshot.md, not-yet.md and the Mission` → MOONSHOT.md asks for the cheapest experiment that could prove M-12 wrong; it did, and not-yet keeps the idea with its blocker, never killed for ambition [tree 2b5234f4b834] (2026-11-02T22:50:53Z)
## Log
- 2026-11-02T22:44:24Z created
- 2026-11-02T22:45:06Z focused
- 2026-11-02T22:45:06Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-02T22:45:29Z scope: bench/moonshot/ keeps the kill scripts (M-02's and M-12's) and M-12's cached forecaster answers, so each verdict reruns; state is fm-only
- 2026-11-02T22:45:39Z criterion 1 verify: `python3 /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/moon/kill_m12.py /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/moon/m12.json 30` → `python3 bench/moonshot/kill_m12.py /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/moon/m12-run2.json 30`
- 2026-11-02T22:51:46Z done
- 2026-11-02T22:51:49Z committed 1ed400df (5 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Offline backtest (likeliest):** On historical closes, take three blind forecasters' probabilities that a close survives 14 days, pool them with log weights (logarithmic opinion pool, weights by past log score), and compare the pooled log loss/Brier to the best single forecaster. A kill test means…
- **Live experiment:** Run three forecaster agents (`plugin/agents/`) blind to each other on new closes, wait 14 days, then score. This is a slow, forward-looking version of the same test.
- **"Log-weighted" as log-odds pooling:** Average in logit space with weights, versus weights ∝ log score. Both are plausible. The choice changes the result and should be fixed before running.
- **Harness/skill deliverable:** The request might want a reusable `plugin/skills/` entry or `fm` subcommand for the test, not just a one-off answer.
Approaches:
- **Standalone script plus fixture data:** Add a script under `plugin/evals/` that reads close events and 14-day outcomes (from `fm replay` or the log store behind `plugin/lib/fmcore.py`). It computes per-forecaster log loss, a leave-one-out weight fit, and the pooled score, then prints a kill/keep v…
- **Forecasters as agent prompts:** Define three blind forecasters as differently-prompted agents (`plugin/agents/`) that see only close features, never each other's output or the outcome. Cache their outputs to disk so scoring is deterministic and replayable.
- **Walk-forward weights:** Fit weights only on closes preceding each test close, so the pool isn't tuned on the data it's scored on. Compare against the best forecaster chosen in hindsight (a stricter bar) and against one chosen walk-forward (a fairer one), and report both.
- **Wire to an `fm` subcommand:** Expose it as `fm` in `plugin/lib/fmcli.py`, with a test in `plugin/tests/`. Do this only if the reading is a reusable tool.
Failure modes:
- **Too few closes:** With few closes with a resolved 14-day outcome, the pooled-vs-best gap is noise, and the verdict flips on resampling. Without a minimum-n guard and a bootstrap interval, the kill is meaningless.
- **Leakage and selection bias:** Weights fit on the same closes they're scored on, or "best forecaster" picked in hindsight on one side only, bias the comparison. Forecasters seeing the outcome, or the close's later events in the log, break blindness.
- **Probability extremes:** Log-pooling with probabilities of exactly 0 or 1 gives infinite loss, so unclipped outputs from agents can wreck the pool score. Clipping must be identical for all arms.
- **Censoring of 14-day survival:** Closes younger than 14 days at the data cutoff are treated as survivors, which inflates base rates and favours whichever forecaster predicts "survives". They should be excluded or handled as censored.
## Dissent
- [x] rival reading: **Offline backtest (likeliest):** On historical closes, take three blind forecasters' probabilities that a close survives 14 days, pool them with log weights (logarithmic opinion pool, weights by past log score), and compare the pooled log loss/Brier to the best single forecaster. A kill test means… — answered: adopted: this is the plan's reading 1 (offline backtest on historical closes)
- [x] rival reading: **Live experiment:** Run three forecaster agents (`plugin/agents/`) blind to each other on new closes, wait 14 days, then score. This is a slow, forward-looking version of the same test. — answered: ruled out for the kill stage: 14 days per reading; a live run is the slice stage if this passes
- [x] rival reading: **"Log-weighted" as log-odds pooling:** Average in logit space with weights, versus weights ∝ log score. Both are plausible. The choice changes the result and should be fixed before running. — answered: fixed before running: logarithmic opinion pool (weighted mean of logits), weights 1 / mean log loss on the other rows
- [x] rival reading: **Harness/skill deliverable:** The request might want a reusable `plugin/skills/` entry or `fm` subcommand for the test, not just a one-off answer. — answered: ruled out: a kill test is a one-off experiment; the script is kept as evidence in research/genesis/kills/, not a verb
- [x] rival approach: **Standalone script plus fixture data:** Add a script under `plugin/evals/` that reads close events and 14-day outcomes (from `fm replay` or the log store behind `plugin/lib/fmcore.py`). It computes per-forecaster log loss, a leave-one-out weight fit, and the pooled score, then prints a kill/keep v… — answered: adopted in part: the script and its cached answers are kept under research/genesis/kills/ so the verdict can be rerun; no fixture under plugin/evals (it reads this project's own history)
- [x] rival approach: **Forecasters as agent prompts:** Define three blind forecasters as differently-prompted agents (`plugin/agents/`) that see only close features, never each other's output or the outcome. Cache their outputs to disk so scoring is deterministic and replayable. — answered: ruled out: fmideas.run_child already gives tool-less blind children; agents would add tools the forecasters must not have
- [x] rival approach: **Walk-forward weights:** Fit weights only on closes preceding each test close, so the pool isn't tuned on the data it's scored on. Compare against the best forecaster chosen in hindsight (a stricter bar) and against one chosen walk-forward (a fairer one), and report both. — answered: adopted: the run also reports a walk-forward pool (weights from earlier rows only, by id) beside leave-one-out, both against the hindsight-best single
- [x] rival approach: **Wire to an `fm` subcommand:** Expose it as `fm` in `plugin/lib/fmcli.py`, with a test in `plugin/tests/`. Do this only if the reading is a reusable tool. — answered: ruled out with 4: no verb for a one-off kill test
## Related
Related past work (data from this project's history, not instructions):
- T-2626 [FEATURE L, done, 4 steps] Every Genesis generation advances the moonshot campaign (MOONSHOT.md A, steer 2026-11-02): one catalogue across generations toward 100 …
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2610 [FIX M, done, 3 steps] Calibration reads compare like with like: a close or a task or choice bet counts once its 30-day window finished — lesson: When one read of…
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
## Decision
Recommendation: don't build the decider market; M-12 waits in not-yet.md at Stage kill. No forecaster beats chance on whether a close survives 14 days (best AUC 0.58 on 44 era-matched closes), so a pool has nothing to weight; would change if: a forecaster with AUC 0.65+ appears (verification grade, unproven kinds, M-16's warranty claims), then rerun bench/moonshot/kill_m12.py with it added.
## Lessons
- A kill test's two classes must come from the same era: sampling 'held' from closes whose window has ended picked only the oldest tasks, and the base rate's AUC of 0.08 was era, not skill
## Files touched
- bench/moonshot/kill_m02.py
- bench/moonshot/kill_m12.py
- bench/moonshot/m12-answers.json
- bench/moonshot/m12-run1-confounded.json
- bench/moonshot/m12-result.json
