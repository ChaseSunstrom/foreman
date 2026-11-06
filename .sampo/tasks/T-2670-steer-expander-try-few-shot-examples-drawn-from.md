---
id: T-2670
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-02T20:57:34Z
updated: 2026-11-02T21:26:46Z
base_note: Calibration: this plan states Choice 60% where FEATURE M closes (578) held on the first finish 97% of the time: 37 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-02T21:22:30Z
rival_split: true
base: 2e6b1eeef531c3f28389a397b44f18f60ef5e7b0
base_tree: 3b6fbbf51909554659805218634798e69982b5a0
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T21:22:39Z
plan0_scope: []
---
# The steer expander sees three worked examples (raw words → reference Rule) from train cases only, never the case it expands; measured on held-out against two baselines
## Raw request
> Steer expander: try few-shot examples drawn from the train split only (never the held-out cases), measured on holdout against 19%; two instruction-shape attempts (T-2627, T-2632) lost coverage or added harm
## Interpretation
1. (chosen) Show the expander how this user's words became rules: three worked examples, each raw words then its reference Rule, taken from train cases only (never a held-out case, never the case being expanded). Measured on the held-out split, where no example can leak, against two baseline runs.
2. Instruct more ("anticipate the pattern"). Rejected: T-2627 and T-2632 tried two instruction shapes; both lost coverage or added harm.
## Assumptions (confidence)
## Acceptance criteria
- [ ] expand() puts three train-split examples before the raw words, never a held-out case nor the case being expanded — verify with `python3 plugin/tests/run.py test_steer`
- [ ] two held-out runs with examples are compared with two baselines in the brief's Measurements, and the change is kept only if coverage beats both with harms no higher — verify with `fm exam steer status`
## Non-goals
## Approach (options → choice → why)
1. fmsteer._examples(p, skip) picks three train cases deterministically (part-C pairs with the most clauses, skip excluded) and expand() puts them before the raw words; grade and live unchanged. Held-out runs: two with examples against two baselines (7457: 5/23, and one more run on the old code). Likely outcome: coverage rises past both baselines with harms flat. Fails if: the expander copies an example's clauses into unrelated rules (harms or off-topic clauses rise), or held-out coverage stays inside the baselines' spread.
2. use what exists: keep the plain prompt at 19% held out. Fails if: part B's live use keeps reading most expansions as low-score, so the user reads them, which the steer exists to avoid.
3. do less: one example instead of three. Fails if: one example teaches its topic, not the pattern.
Choice 1 (60%): examples are the lever not yet tried, and the held-out split measures it without leakage.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: examples are train-only and skip the case itself
2. [x] _examples and expand()
3. [x] held-out runs, comparison, keep or revert; CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_steer 2>&1 | grep -E "^(FAIL|ERROR):|Error:|^OK|FAILED \(" | head -4` → exit 0 · OK [ran] [tree 4dc270e1a898] [world 2f1906870a] (2026-11-02T21:23:36Z)
- (step 1) `python3 plugin/tests/run.py test_steer 2>&1 | grep -E "^(FAIL|ERROR):|Error:|^OK|FAILED \(" | head -4` → exit 0 · OK [ran] [tree 4dc270e1a898] [world 2f1906870a] (2026-11-02T21:23:36Z)
- (step 1) `python3 plugin/tests/run.py test_steer.Examples` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: Examples 0s) / OK [ran] [tree 4dc270e1a898] [world 2f1906870a] (2026-11-02T21:23:43Z)
- (step 2) `python3 plugin/tests/run.py test_steer` → exit 0 · Ran 26 tests in 4.0s (10 classes, 16 at a time; slowest: Court 4s, Veto 4s, Live 3s) / OK [ran] [tree 4dc270e1a898] [world 2f1906870a] (2026-11-02T21:23:47Z)
- (step 3) `python3 plugin/tests/run.py test_steer` → exit 0 · Ran 24 tests in 4.4s (9 classes, 16 at a time; slowest: Veto 4s, Court 4s, Live 3s) / OK [ran] [tree 8132ce553e49] [world 2f1906870a] (2026-11-02T21:26:35Z)
- (ac 2) `fm exam steer status` → exit 0 · steer-20261102T212604-3954: held out 22% of the reference clauses covered over 13 case(s), train ? over 0 (sonnet, judged by fable); 22 harmful addition(s) [ran] [tree 8132ce553e49] [world 2f1906870a] (2026-11-02T21:26:35Z)
## Log
- 2026-11-02T20:57:34Z created
- 2026-11-02T21:22:12Z planned from capture
- 2026-11-02T21:22:38Z focused
- 2026-11-02T21:22:39Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T21:26:17Z focused
- 2026-11-02T21:26:30Z ruled out: three worked train examples: held-out 4/23 and 5/23 against 5/23 and 3/23, harms 22 and 22 against 16 and 12; reverted
- 2026-11-02T21:26:46Z dropped: measured and refuted: held-out 4/23 and 5/23 covered with 22 and 22 harmful against baselines 5/23 and 3/23 with 16 and 12; the change was reverted, so nothing lands (Measurements and decisions.md keep the numbers)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: improve the "steer expander" prompt (an LLM step that expands a short steer/instruction into a fuller one) by adding few-shot examples sampled only from the train split of the eval dataset in `plugin/evals/`, then run it on the holdout split and compare against the 19% baseline (presumab…
- The 19% could be a coverage metric, not accuracy. Prior attempts "lost coverage or added harm", so the holdout score is probably a composite (coverage up, harm down), and "beat 19%" may mean beating it without regressing the harm rate.
- The request may also want the train/holdout separation enforced, e.g. a guard that fails if any few-shot example id appears in holdout. "Never the held-out cases" would then be a checked invariant, not just a convention.
- Less likely: a general few-shot selection framework (retrieval of nearest train examples per input) rather than a fixed example set.
Approaches:
- Fixed few-shot block: pick k (3–6) train cases covering distinct steer categories, hand-curated or chosen by stratified sampling with a seed. Render them into the expander's prompt template (likely in `plugin/lib/` or `plugin/skills/`, where the expander prompt lives), then run the existing eval ru…
- Dynamic selection: for each input, retrieve the nearest train cases (by embedding or keyword overlap) as examples. This may lift the score more, but adds nondeterminism and a retrieval dependency.
- Ablate k and example choice: run several seeds and k values on train-only cross-validation, then evaluate only the winner on holdout once. This avoids tuning on holdout, which would defeat the point of the split.
- Add a split-leak check in the eval harness (`plugin/evals/`) that asserts the few-shot example ids are disjoint from holdout ids and runs before scoring.
Failure modes:
- Leakage: the split is defined by an id list or file, and train and holdout items share near-duplicates (same steer, different wording). Few-shot examples then effectively contain the holdout answers, which inflates the score without a real gain.
- Overfitting to holdout: trying many example sets and keeping the best by holdout score turns the holdout into a tuning set, so the final number is no longer a fair comparison against 19%.
- Same regression as the instruction attempts: examples can anchor the expander toward narrow patterns, so coverage drops, or it copies example content into outputs, which adds harm. A single aggregate score can hide this, so coverage and harm must be reported separately.
- Prompt size and variance: extra examples change token cost and hook latency, and nondeterministic sampling means one holdout run can't tell a real change from noise. The `bench_hooks.py` and `fm replay` gates may also shift if the expander runs on a hook path.
## Dissent
- [x] rival reading: Likeliest: improve the "steer expander" prompt (an LLM step that expands a short steer/instruction into a fuller one) by adding few-shot examples sampled only from the train split of the eval dataset in `plugin/evals/`, then run it on the holdout split and compare against the 19% baseline (presumab… — answered: taken: the expander prompt is the step changed
- [x] rival reading: The 19% could be a coverage metric, not accuracy. Prior attempts "lost coverage or added harm", so the holdout score is probably a composite (coverage up, harm down), and "beat 19%" may mean beating it without regressing the harm rate. — answered: taken: 19% is clause coverage under the judge; the criterion compares coverage and harms together
- [x] rival reading: The request may also want the train/holdout separation enforced, e.g. a guard that fails if any few-shot example id appears in holdout. "Never the held-out cases" would then be a checked invariant, not just a convention. — answered: taken: _examples draws train cases only and the red test asserts no held-out id and not the case itself
- [x] rival reading: Less likely: a general few-shot selection framework (retrieval of nearest train examples per input) rather than a fixed example set. — answered: deferred: a fixed block first; retrieval per input adds nondeterminism, tried only if the fixed block helps
- [x] rival approach: Fixed few-shot block: pick k (3–6) train cases covering distinct steer categories, hand-curated or chosen by stratified sampling with a seed. Render them into the expander's prompt template (likely in `plugin/lib/` or `plugin/skills/`, where the expander prompt lives), then run the existing eval ru… — answered: taken in part: three part-C pairs with the most clauses, chosen deterministically
- [x] rival approach: Dynamic selection: for each input, retrieve the nearest train cases (by embedding or keyword overlap) as examples. This may lift the score more, but adds nondeterminism and a retrieval dependency. — answered: deferred, as reading 4
- [x] rival approach: Ablate k and example choice: run several seeds and k values on train-only cross-validation, then evaluate only the winner on holdout once. This avoids tuning on holdout, which would defeat the point of the split. — answered: not now: one fixed choice evaluated once on holdout is the cheaper honest test; tuning k on train comes only if it helps
- [x] rival approach: Add a split-leak check in the eval harness (`plugin/evals/`) that asserts the few-shot example ids are disjoint from holdout ids and runs before scoring. — answered: taken: the red test is that check
## Related
Related past work (data from this project's history, not instructions):
- T-2632 [FEATURE M, done, 3 steps] The steer expander returns a Rule (acted on) and Proposals (filed on the brief, never acted on); the judge scores the Rule only; measur…
- T-2627 [PERFORMANCE M, done, 3 steps] The steer expander's method prompt anticipates more and harms less: tuned on the train split only (baseline steer-20261102T182645: …
- T-2625 [FEATURE L, done, 5 steps] fm exam steer: the steer-expansion exam (MOONSHOT.md B): cases, cold-graded expansions, a held-out rate on the Genesis page, live expan…
- decision 2026-11-02: [revisited: steer-expansion exam. From a user's raw words] [cites: user steer 2026-11-02: MOONSHOT.md part B (start now)] [check: python3 plugin/tes…
## Measurements
Held-out split (13 cases, 23 clauses), sonnet expander, fable judge. Baselines on the plain prompt: run 7457 5/23 covered, 16 harmful; run 6850 3/23, 12 harmful. With three worked train examples: run 3422 4/23, 22 harmful; run 3954 5/23, 22 harmful. Coverage stayed inside the baselines' spread (3-5) while harmful additions rose about 60%: the expander copied the examples' scope (spend, completeness, autonomy clauses) into unrelated rules.
