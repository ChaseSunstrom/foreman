# Cross-cutting review — gen-2

Reviewer model: fable
Missions' model: Opus 5.5
Inputs: sha256 a2c183eabc212fce3220c7448f1e450b230384b5786352b90ea3e35215578234
Drawn at: c2c0683d152bc59b1c71da1054f99660cb80db8d
Dropped (no ground in the inputs): 3

Handled is a task id, gap (the next Seed's top gaps) or dismissed: <reason>.

| # | Question | Ground | Finding | Handled |
|---|---|---|---|---|
| 1 | worse | l001 (foreman, model default): 6 scenarios; true done 0/6, checks 5/20, false done 6 | The long-horizon exam's foreman arm claims done on all six scenarios it fails, while l002 (plain) manages true done 1/6, false done 5; the harness scores below no harness on its own tier. | gap |
| 2 | worse | replay: type 259/376 (naive 256), paths 0.052 (naive 0.086) | On s11-012 the foresight file predictor is worse than the naive baseline and the type predictor beats it by 3 of 376; the predictor cleanup (T-2554) did not move it off naive. | gap |
| 3 | worse | ec276a78 | fm ship now re-picks onto a moved main and pushes up to 3 tries with no retest; the pushed commit has never had the suite run on it, and ad98d29a already shipped the same re-pick a second way. | T-2572 |
| 4 | worse | failed tool calls 0.6 → 0.7 · drive stops 0 → 0.2 | Both friction trends moved the wrong way this window while guard blocks fell by 0.1. | dismissed: one window's 0.1 moves in two friction trends with no named cause; fm friction keeps watching and files a trend that holds |
| 5 | worse | s31-006 (foreman, model haiku: a smoke signal): 9 scenarios; found 15/18, 4 false alarms | The only multi-scenario foreman run fully closed 4 of 9 with 4 false alarms; the generation adds no fix for it. | dismissed: a Haiku smoke line never decides (the user's steer); the production held-out exam runs at the end of the run |
| 6 | unearned | plugin/lib/fmgenesis.py | 729 ++++++++++++++++++++- / The tower's own machinery is the largest growth of the generation, with no exam kind, no foreman score and no held-out line measuring it, while T-2503's lean check judges only the Missions' growth. | gap |
| 7 | unearned | plugin/lib/fmmodels.py | 174 ++++- / The model layer gained 174 lines plus test_models 203 and seven CHANGELOG bullets while the exam records model 0/0 on dedupe, intake-tier and intake-type; nothing it decides has been measured once. | dismissed: the same finding as #13 (the model arm scores 0/0), handled by T-2582 |
| 8 | unearned | 85 files changed, 4595 insertions(+), 196 deletions(-) | A 23:1 add-to-cut ratio in the generation that added a "lean check measures substance" sweep; the sweep did not bite on its own generation. | dismissed: the same finding as #6 (the lean check skips the tower's own growth), handled as a gap there |
| 9 | unearned | plugin/lib/fmanergy.py | 99 +++ / The reflex-prompt timer shipped with a doctor row and a digest row although its own lesson (T-2563) says bypass mode shows no prompts and the real-data check was deferred. | dismissed: the same finding as #19 (anergy surfaces ahead of data), handled by T-2588 |
| 10 | unearned | plugin/tests/test_ci_matrix.py | 22 ++ / A test that pins a 3-shard macOS layout turns the next suite-size overrun into a test edit plus a workflow edit; it measures nothing about growth, only freezes today's cure. | T-2579 |
| 11 | mismeasured | s21-013 (oracle): 306 scenarios; found 261/261, 0 false alarms, fixed 414/414, 0 exam defects | The 306-scenario and 249-scenario lines are oracle arms scoring 100%; the only foreman lines are a 3-scenario smoke (s32-015) and a haiku run, so the scorecard measures the answer key, not the harness. | dismissed: the scorecard counts only foreman held-out lines and reads 0/13 saying so; oracle lines exist to validate the keys |
| 12 | mismeasured | overlap 0.118 against 0.113 | The CHANGELOG compares the cleaned history to the old history and omits the exam's own naive 0.116; against the baseline the gain is 0.002 on one decimal of noise. | dismissed: folded into #22 (T-2591): CHANGELOG numbers carry their counts and baselines |
| 13 | mismeasured | model dedupe: rule 1/2, model 0/0; model intake-tier: rule 24/36, model 0/0 | The model-versus-rule exam has a rule side and no model side; an exam that can report 0/0 on the arm it exists to score is not scoring that arm. | T-2582 |
| 14 | mismeasured | f95fac52 | A review finding now needs a number of 3+ digits, so the 57% landing rate, the 4% survival loss and the 0/6 long-horizon score can ground nothing; the rule excludes the numbers a reviewer most needs. | T-2583 |
| 15 | mismeasured | Survival (30 days): of 1699 closes, 66 lost (4%), 91 survived the window, 1542 settling | Only 157 closes are decided, yet "held" in the track record (546 of 568) counts the 1542 unsettled as held and the 4% is taken over all 1699. | T-2584 |
| 16 | unproven | briefs up to 8k characters landed 96–98% of the time and briefs of 8–16k landed 57% | Two CHANGELOG bullets quote the same landing rates with no counts, from briefs sized after the fact from files that may no longer exist. | dismissed: folded into #22 (T-2591): CHANGELOG numbers carry their counts and baselines |
| 17 | unproven | 56b90b65 | T-2505 seals a prediction of the user's next three steers and promises a scored hit rate; neither the exam lines nor outcomes carry a single scored steer. | gap |
| 18 | unproven | plugin/lib/fmrecall.py | 72 +- / The MASTER-clause backtest caught 4 of 46 against 31 of 400 false flags and shipped anyway as a "yardstick" for a matcher that does not exist. | T-2587 |
| 19 | unproven | 5c549eeb | The doctor names allow rules such as `Bash(git status *)` from timings whose source, the permission dialog, is invisible in the mode the user runs; the row can only ever read "none" until that is shown otherwise. | T-2588 |
| 20 | complaint | SessionStart: foreman project foreman- a f — 1×, 1,985 chars | Every session opens with a note over the project's own 1,500-character trim rule (T-2109) and the friction report has flagged it again. | T-2589 |
| 21 | complaint | l002 (foreman, model default): 6 scenarios; true done 0/6, checks 4/20, false done 6 | A user handing the harness a long task gets six confident false completions; no entry in the 67-line CHANGELOG addresses it. | dismissed: the same finding as #1 (long-tier false dones), handled as a gap there |
| 22 | complaint | CHANGELOG.md | 67 ++ / Sixty-plus Unreleased bullets, half about Genesis internals and the model layer's shadow mode, bury the three user-facing fixes a reader would want. | T-2591 |
