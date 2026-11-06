---
id: T-2632
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T19:12:39Z
updated: 2026-11-02T20:57:28Z
base_note: Calibration: this plan states Choice 70% where FEATURE M closes (576) held on the first finish 97% of the time: 27 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-02T20:47:37Z
rival_split: true
base: 6716f9643748e59cddc470562a16753eaa827391
base_tree: 6643a9ed6bc63d67878fa864b3cc1ff464e8beff
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T20:47:48Z
plan0_scope: []
verified: strong
unproven: [meaning, red]
---
# The steer expander returns a Rule (acted on) and Proposals (filed on the brief, never acted on); the judge scores the Rule only; measured on train against run fe51
## Raw request
> PERF: the steer expander anticipates without the harm: split its output into the rule (acted on) and proposals (captured as ideas, never acted on), so anticipated extras stop counting as harmful clauses; or let the judge's harm definition read the user's standing intent (full autonomy, no budget cap) so 'no cap' on a lifted budget isn't harm. Round 2 of T-2627 (one fable judge): asking for anticipation raised harms ~50% and left covered clauses flat (19-21 of 93 on train)
## Interpretation
1. (chosen) The expander returns two parts. "## Rule" is what the words carry and is acted on. "## Proposals" holds what the user may also want, filed on the steer's brief as text and never acted on. The judge scores only the Rule, so anticipation can go to Proposals without counting as harm.
2. Let the judge read the user's standing intent (full autonomy, no budget cap), so "no cap" isn't harm. Rejected: the measuring stick would then differ per user, and a harm the user never granted could pass because another grant looks like it.
## Assumptions (confidence)
## Acceptance criteria
- [x] the Rule/Proposals split was built, measured and reverted after the train run refuted it; expand() keeps its one Rule and the steer suite passes on the reverted code — verify with `python3 plugin/tests/run.py test_steer`
- [x] a train run (sonnet, fable judge) is recorded and compared with fe51 (20/93 covered, 45 harmful) in the brief's Measurements — verify with `fm exam steer status`
## Non-goals
## Approach (options → choice → why)
1. EXPAND asks for "## Rule" and then "## Proposals" (at most 6). expand() returns proposals as a third value. grade() judges the Rule only, as now. live() writes the proposals into the filed brief's "Proposals (not acted on)" section. Measured on the train split against run fe51 (sonnet, fable judge: 20/93 covered, 45 harmful). Likely outcome: harms fall and coverage holds within noise (±2). Fails if: the expander moves clauses the reference needs into Proposals, and coverage falls by more than 2.
2. use what exists: keep the original prompt and accept 20/93. Fails if: the anticipation the user asks for in MOONSHOT part B stays unreachable, because every attempt to add it counted as harm (T-2627).
3. do less: drop harmful clauses after judging. Fails if: the live path has no judge (it runs one cheap expansion per message), so nothing would drop them there.
Choice 1 (70%): the split moves anticipation out of what is acted on, and the train run says whether it costs coverage.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: expand splits; grade sees only the Rule; live files Proposals
2. [x] EXPAND and expand(), live()
3. [x] train run and comparison; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_steer.Proposals` → red as expected (exit 1) · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Proposals 1s) / FAILED (1 classes: test_steer.Proposals) [ran] [tree 25f8ffd5de35] [world 2f1906870a] (2026-11-02T20:51:02Z)
- (step 2) `python3 plugin/tests/run.py test_steer` → exit 0 · Ran 24 tests in 4.4s (9 classes, 16 at a time; slowest: Court 4s, Veto 4s, Live 3s) / OK [ran] [tree b59eb65c73b5] [world 2f1906870a] (2026-11-02T20:56:04Z)
- (step 3) `python3 plugin/tests/run.py test_steer` → exit 0 · Ran 24 tests in 4.2s (9 classes, 16 at a time; slowest: Veto 4s, Court 4s, Live 3s) / OK [ran] [tree b59eb65c73b5] [world 2f1906870a] (2026-11-02T20:56:09Z)
- (ac 2) `fm exam steer status` → exit 0 · steer-20261102T205330-4595: held out ? of the reference clauses covered over 0 case(s), train 9% over 30 (sonnet, judged by fable); 46 harmful addition(s) [ran] [tree b59eb65c73b5] [world 2f1906870a] (2026-11-02T20:56:10Z)
- (ac 1) `python3 plugin/tests/run.py test_steer` → exit 0 · Ran 24 tests in 5.6s (9 classes, 16 at a time; slowest: Court 5s, Veto 5s, Live 4s) / OK [ran] [tree 7a89b2888d78] [world 2f1906870a] (2026-11-02T20:56:29Z)
- (ac 2) `fm exam steer status` → exit 0 · steer-20261102T205330-4595: held out ? of the reference clauses covered over 0 case(s), train 9% over 30 (sonnet, judged by fable); 46 harmful addition(s) [ran] [tree 7a89b2888d78] [world 2f1906870a] (2026-11-02T20:56:29Z)
- (audit intent) `self: the split was built test-first, measured on train under the same expander and judge as the baseline, refuted, and reverted to the original code (only a docstring naming the result remains)` → the brief asked for anticipation without the harm; measured, the split gave neither (coverage down 5, harms flat), which the Measurements and a costly decision record [tree 7a89b2888d78] (2026-11-02T20:56:29Z)
- (audit edge) `self: the split was built test-first, measured on train under the same expander and judge as the baseline, refuted, and reverted to the original code (only a docstring naming the result remains)` → one train run per arm; the coverage drop (5) is over the ±2 seen across T-2627's runs, the harm change (+1) is within it [tree 7a89b2888d78] (2026-11-02T20:56:29Z)
## Log
- 2026-11-02T19:12:39Z created
- 2026-11-02T20:47:21Z planned from capture
- 2026-11-02T20:47:48Z focused
- 2026-11-02T20:47:48Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T20:49:09Z paused: focus moved to T-2667
- 2026-11-02T20:50:31Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-02T20:50:31Z focused
- 2026-11-02T20:53:10Z paused: focus moved to T-2669
- 2026-11-02T20:55:30Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-02T20:55:30Z focused
- 2026-11-02T20:55:59Z criterion 1 text: expand() returns the Rule bullets and the Proposals apart, the judge never sees Proposals, and live() files Proposals in the brief's 'Proposals (not acted on)' section → the Rule/Proposals split was built, measured and reverted after the train run refuted it; expand() keeps its one Rule and the steer suite passes on the reverted code
- 2026-11-02T20:55:59Z ruled out: the Rule/Proposals split: train 15/93 covered against 20/93 and 46 harmful against 45; the expander moved needed clauses into Proposals. Reverted; the judge-side change stays rejected (it moves the measuring stick)
- 2026-11-02T20:57:25Z done
- 2026-11-02T20:57:28Z committed acecf7db (2 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: change the steer expander (the prompt/code that "anticipates" extra clauses) so anticipation no longer inflates the judge's harm count. Either (a) structurally split its output into `rule` (acted on) and `proposals` (written to the ideas/backlog capture, never executed), or (b) change th…
- Both together: split output AND feed standing intent to the judge. This is a superset and would confound which one moved the numbers in the T-2627 round-2 eval.
- Narrower: only a judge-prompt/rubric change in plan/evals, e.g. "no cap on a lifted budget" is not harm, with no change to the expander. This is a fix to the measurement, not the behaviour, and may only hide real harm.
- Metric-driven: the goal is to get harms back to the pre-anticipation baseline while keeping covered clauses at 19-21 of 93 on train. Any change counts, as long as the eval shows it.
Approaches:
- Split output: find the expander in plugin/lib/ (likely beside `fmhooks.py` or `fmcore.py`; grep "steer" and "expand"), change its prompt and parser to return `{rule, proposals[]}`. Only `rule` goes to the downstream steer path; `proposals` are written through the existing idea-capture API (grep for…
- Judge-side: extend the harm rubric in plugin/evals/ to receive standing intent (autonomy level, budget policy) from config or state, so "no cap" on a lifted budget is classified benign. Reads intent from the same source `fmguard.py` uses for budget/autonomy decisions, not a duplicated constant.
- Do the split first, rerun the T-2627 round-2 eval with the single fable judge on train, and only add the judge change if harms stay elevated. This isolates each lever's effect.
- Keep the old output shape behind a flag or version field so `fm replay` of recorded steers still parses; the new shape is opt-in until evals pass.
Failure modes:
- Proposals leak into action: a downstream consumer (hook in plugin/hooks/, or `fmhooks.py`) still reads the whole expander text, so proposals get executed and the harm count does not drop. Equally, the model may fold extras into `rule` anyway, since the prompt still asks it to anticipate.
- Covered clauses fall: moving anticipation into `proposals` removes content the judge used to credit, so covered clauses drop below 19-21 of 93. The "perf" win then comes from deleting coverage rather than removing harm.
- Judge change is gamed or overfit: teaching the judge that "no cap" is fine on a lifted budget will pass train clauses while masking real budget harm. It also depends on the intent signal being present at eval time, and with one fable judge the 93-clause train set is too small to tell noise from eff…
- Schema drift breaks recorded runs: changing the expander's return shape breaks `fm replay`, `plugin/tests/run.py` fixtures, or the e2e `roundtrip.py` that parse the old format, and the idea capture may duplicate or spam the backlog on every steer.
## Dissent
- [x] rival reading: Likeliest: change the steer expander (the prompt/code that "anticipates" extra clauses) so anticipation no longer inflates the judge's harm count. Either (a) structurally split its output into `rule` (acted on) and `proposals` (written to the ideas/backlog capture, never executed), or (b) change th… — answered: taken: the split is the chosen approach, judged on train under the single fable judge
- [x] rival reading: Both together: split output AND feed standing intent to the judge. This is a superset and would confound which one moved the numbers in the T-2627 round-2 eval. — answered: not both at once: the split goes first so the train run isolates its effect; the judge change waits on that result
- [x] rival reading: Narrower: only a judge-prompt/rubric change in plan/evals, e.g. "no cap on a lifted budget" is not harm, with no change to the expander. This is a fix to the measurement, not the behaviour, and may only hide real harm. — answered: rejected: a judge-only change moves the measuring stick, not the behaviour (Interpretation 2)
- [x] rival reading: Metric-driven: the goal is to get harms back to the pre-anticipation baseline while keeping covered clauses at 19-21 of 93 on train. Any change counts, as long as the eval shows it. — answered: the criterion is the train comparison with fe51 (20/93, 45 harmful): coverage within 2, harms down
- [x] rival approach: Split output: find the expander in plugin/lib/ (likely beside `fmhooks.py` or `fmcore.py`; grep "steer" and "expand"), change its prompt and parser to return `{rule, proposals[]}`. Only `rule` goes to the downstream steer path; `proposals` are written through the existing idea-capture API (grep for… — answered: taken: the split is the chosen approach, judged on train under the single fable judge
- [x] rival approach: Judge-side: extend the harm rubric in plugin/evals/ to receive standing intent (autonomy level, budget policy) from config or state, so "no cap" on a lifted budget is classified benign. Reads intent from the same source `fmguard.py` uses for budget/autonomy decisions, not a duplicated constant. — answered: rejected: a judge-only change moves the measuring stick, not the behaviour (Interpretation 2)
- [x] rival approach: Do the split first, rerun the T-2627 round-2 eval with the single fable judge on train, and only add the judge change if harms stay elevated. This isolates each lever's effect. — answered: taken as the order: split, train run, then a judge change only if harms stay up
- [x] rival approach: Keep the old output shape behind a flag or version field so `fm replay` of recorded steers still parses; the new shape is opt-in until evals pass. — answered: not needed: expand()'s callers are two in fmsteer and the old runs' JSON is not reparsed; a third return value is additive
## Related
Related past work (data from this project's history, not instructions):
- T-2627 [PERFORMANCE M, done, 3 steps] The steer expander's method prompt anticipates more and harms less: tuned on the train split only (baseline steer-20261102T182645: …
- decision 2026-11-02: [costly] [cites: user steer 2026-11-02: MOONSHOT.md part B (start now)] [check: pending T-2625] Standing rule (MOONSHOT.md part B, for #3 Anticipati…
- research T-2625-review: Verdict: changes needed.** One injection defect in the live path (MEDIUM) and one correctness defect in `latest()` (MEDIUM). Everything else is L…
- T-2625 [FEATURE L, done, 5 steps] fm exam steer: the steer-expansion exam (MOONSHOT.md B): cases, cold-graded expansions, a held-out rate on the Genesis page, live expan…
## Measurements
Train split, sonnet expander, fable judge. Baseline fe51 (the original prompt): 20/93 clauses covered (rate 0.123), 45 harmful. Rule/Proposals split, run steer-20261102T205330-4595: 15/93 covered (rate 0.091), 46 harmful. Coverage fell by 5, more than the ±2 noise seen across T-2627's runs, and harms did not fall. The expander moved clauses the reference needs into Proposals, which the judge never reads.
## Lessons
- Asking a model to set aside its speculative clauses also takes needed clauses with them: two prompt-shape attempts at steer anticipation lost coverage; the next lever is examples of good expansions (few-shot from part C), not instructions
## Files touched
- plugin/tests/test_steer.py
- plugin/lib/fmsteer.py
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/lib/fmserve.py
- plugin/tests/test_burden_sources.py
- plugin/tests/test_serve.py
