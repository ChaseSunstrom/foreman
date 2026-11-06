---
id: T-2926
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T07:53:53Z
updated: 2026-11-04T10:08:12Z
base_note: Calibration: this plan states Choice 75% where FIX M closes (125) held on the first finish 95% of the time: 20 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T08:48:59Z
rival_split: true
builder_model: haiku
base: cdd18c9f0996bf7656b1c3ece82b70e3ef317a8c
base_tree: b2f8be0cba1d13419b8e305ec6cc52cac4e2721a
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-04T09:03:39Z
plan0_scope: []
lane_stop: merged 2026-11-04T09:17:44Z
verified: strong
---
# Sampo exam taxonomy has no class for a reasoning-budget end, a plan refused by fm task…
## Raw request
> FIX: sampo exam taxonomy has no class for a reasoning-budget end, a plan refused by fm task new, or a plan that never validated after repairs: 8 of the first run's 10 ends; add the three classes and an 'other' count so the rates sum to the scenarios
## Interpretation
Reading 1 (chosen): louhi.failure_classes counts event kinds, so a run's real ending is mixed into six overlapping classes: "no valid plan after 2 repairs" is swallowed by _MALFORMED ("no valid|field by field"), "reasoning used the whole budget" (models.py complete) and a plan refused by Smith's guard or fm task new match nothing. Add classes budget, plan_refused and no_plan (no_plan leaves _MALFORMED), and give taxonomy() an "ends" count: each scenario's last end event assigned to exactly one class, closed, or other, so the counts sum to the scenarios.
Reading 2 (ruled out): make the existing per-class "rate" sum to 1. Those rates are the share of scenarios a class hit; a scenario can hit several, so they cannot sum and should not.
## Assumptions (confidence)
## Acceptance criteria
- [x] failure_classes counts budget (reasoning used the whole budget), plan_refused and no_plan from their real messages, and no_plan no longer counts as malformed — verify with `python3 plugin/tests/run.py test_exam_taxonomy`
- [x] taxonomy() returns ends: one class, closed or other per scenario, summing to the scenarios — verify with `python3 plugin/tests/run.py test_exam_taxonomy`
- [x] the existing exam tests, with the malformed case updated, still pass — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1) Add budget, plan_refused, no_plan to FAILURE_CLASSES with matching patterns on the error/blocked events' text (as _MALFORMED is used); no_plan moves out of _MALFORMED; failure_classes also yields the scenario's end class (the last of closed/blocked/error/answer events, as _smith_arm picks it) and taxonomy() adds "ends": {class: n} over classes + closed + other, summing to the scenarios, which sampo exam taxonomy prints. Likely outcome: the first run's 10 ends all land in a named class (6 budget, 2 timeout, 1 plan_refused, 1 no_plan). Fails if: a text pattern drifts from the message it matches (models.py and smith.py word them); the test pins each pattern against the real message constant or a string built the same way.
2) use what exists: add the three classes to FAILURE_CLASSES and leave rates and shape alone. Likely outcome: the classes appear, ranked. Fails if: the ask that the counts sum to the scenarios is not met, and a reader still cannot see a scenario's one ending.
3) do less: only "other" = scenarios that hit no class. Likely outcome: shows the 8 of 10 gap as one number. Fails if: it names nothing, the three classes stay unknown and the next run's gap is the same.
Choice 1 (75%): the data to do it is already in each event stream; it changes one function and one report.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: test_exam_taxonomy.py with event lists for each end (budget, plan_refused, no_plan, timeout, closed, other)
2. [x] Add the classes and patterns to louhi.py; remove no valid from _MALFORMED
3. [x] Add the per-scenario end and the ends map in taxonomy(), and print it in sampo exam taxonomy
4. [x] Update the malformed case in test_exam.py; run both tests
5. [x] Re-read s0-001's stored smith event logs with sampo exam taxonomy and check the first run's ends land in named classes
## Resume here
<!-- auto -->
- 2026-11-04T09:41:33Z steps 5/5 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/sampo/smith.py, plugin/tests/test_code_close_scaffold.py, plugin/tests/test_code_plan_scaffold.py, plugin/tests/test_code_worker.py
- touched since last checkpoint: plugin/tests/test_code_worker.py, plugin/lib/sampo/smith.py, plugin/tests/test_code_close_scaffold.py, plugin/tests/test_code_plan_scaffold.py
## Docs impact
CHANGELOG line (T-2926); sampo exam taxonomy prints the ends map
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_exam_taxonomy 2>&1 | tail -5` → ✗ exit 1 · Ran 3 tests in 2.5s (1 classes, 16 at a time; slowest: Taxonomy 0s) / FAILED (1 classes: test_exam_taxonomy.Taxonomy) [ran] [tree 4f9292b37343] [world 2f1906870a] (2026-11-04T09:04:24Z)
- (ac 2) `python3 plugin/tests/run.py test_exam_taxonomy 2>&1 | tail -5` → ✗ exit 1 · Ran 3 tests in 2.5s (1 classes, 16 at a time; slowest: Taxonomy 0s) / FAILED (1 classes: test_exam_taxonomy.Taxonomy) [ran] [tree 4f9292b37343] [world 2f1906870a] (2026-11-04T09:04:24Z)
- (ac 3) `python3 plugin/tests/run.py test_exam 2>&1 | tail -6` → ✗ exit 1 · Ran 105 tests in 178.4s (26 classes, 16 at a time; slowest: LeanKind 178s, ExamAuthors 112s, ExamGen 94s) / FAILED (1 classes: test_exam.SmithArm) [ran] [tree 5832bca3435e] [world 2f1906870a] (2026-11-04T09:10:58Z)
- (step 1) `python3 plugin/tests/run.py test_exam_taxonomy` → exit 0 · Ran 3 tests in 0.5s (1 classes, 16 at a time; slowest: Taxonomy 0s) / OK [ran] [tree 2ec3f2b28e19] [world 2f1906870a] (2026-11-04T09:28:26Z)
- (step 2) `python3 plugin/tests/run.py test_exam_taxonomy` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Taxonomy 0s) / OK [ran] [tree 2ec3f2b28e19] [world 2f1906870a] (2026-11-04T09:28:27Z)
- (step 3) `python3 plugin/tests/run.py test_exam_taxonomy` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Taxonomy 0s) / OK [ran] [tree 2ec3f2b28e19] [world 2f1906870a] (2026-11-04T09:28:28Z)
- (step 4) `python3 plugin/tests/run.py test_exam_taxonomy test_exam` → exit 0 · Ran 105 tests in 108.2s (26 classes, 16 at a time; slowest: LeanKind 108s, ExamAuthors 79s, JudgmentKinds 75s) / OK [ran] [tree 1832fb900b22] [world 2f1906870a] (2026-11-04T09:30:17Z)
- (step 5) `sampo exam taxonomy s0-001` → exit 0 · timeout          0 in 0 scenarios (0%) / budget           0 in 0 scenarios (0%) [ran] [tree 1832fb900b22] [world 2f1906870a] (2026-11-04T09:30:17Z)
- `python3 plugin/tests/run.py test_exam_taxonomy` → ✗ exit 1 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: Taxonomy 0s) / FAILED (1 classes: test_exam_taxonomy.Taxonomy) (start tree + this task's tests) [ran] [tree 1832fb900b22] [world 2f1906870a] (2026-11-04T09:30:39Z)
- `python3 plugin/tests/run.py test_exam_taxonomy` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Taxonomy 0s) / OK [ran] [tree 1832fb900b22] [world 2f1906870a] (2026-11-04T09:30:39Z)
- (ac 1) `python3 plugin/tests/run.py test_exam_taxonomy` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Taxonomy 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:05:09Z)
- (ac 2) `python3 plugin/tests/run.py test_exam_taxonomy` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Taxonomy 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:05:09Z)
- (ac 3) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 109 tests in 166.8s (27 classes, 16 at a time; slowest: LeanKind 166s, ExamAuthors 117s, JudgmentKinds 87s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:05:09Z)
- (audit intent) `one fm-reviewer pass over the uplift batch (T-2926's diff spans it)` → failure_classes counts budget, plan_refused and no_plan from Smith's real end messages; no_plan is not malformed; ends sum to the scenarios (s0-001 reread: loop 4, no_plan 3, finish_refused 2, plan_refused 1, no other) [tree c6d95c6236bb] (2026-11-04T10:05:09Z)
- (audit edge) `one fm-reviewer pass over the uplift batch (T-2926's diff spans it)` → T-2937's new 'fm task set <section> refused' end matches no class and would land in other — captured T-2948 [tree c6d95c6236bb] (2026-11-04T10:05:09Z)
- (audit adversary) `one fm-reviewer pass over the uplift batch (T-2926's diff spans it)` → classes are regexes over Smith's own end text; a hostile repo printing a matching phrase moves only a count [tree c6d95c6236bb] (2026-11-04T10:05:09Z)
## Log
- 2026-11-04T07:53:53Z created
- 2026-11-04T08:44:54Z set tier=M
- 2026-11-04T08:46:16Z planned: it has criteria and steps
- 2026-11-04T08:46:24Z set approved=True
- 2026-11-04T09:03:20Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2926.builder.md
- 2026-11-04T09:03:39Z focused
- 2026-11-04T09:03:39Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-04T09:17:44Z merged worktree-agent-afefef8fcd41fd5fa (3 file(s))
- 2026-11-04T09:17:45Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afefef8fcd41fd5fa
- 2026-11-04T09:28:16Z focused
- 2026-11-04T09:41:34Z paused: focus moved to T-2936
- 2026-11-04T10:01:58Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T10:01:58Z focused
- 2026-11-04T10:08:11Z done
- 2026-11-04T10:08:12Z committed ebbb03af (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: in the sampo exam's end-classification (likely `plugin/lib/sampo/` exam module, surfaced by `plugin/lib/sampo/cli.py`), add three named end classes (reasoning-budget exhausted, plan refused by `fm task new`, plan never validated after repair attempts) plus an `other` bucket, and make the…
- The fix is in reporting only: classes exist in the run data but the summary/rate printer lumps or drops them, so the change is a mapping and a denominator, not new detection.
- Detection is missing too: the exam runner never records the signals (budget-end marker, `fm task new` nonzero exit/refusal text, validation state after repair loop), so classification needs new fields captured at run time in the transcript/result record.
- Narrowest: only the "8 of 10 unclassified" first-run output needs correcting, e.g. a one-off re-bucketing of that run's stored results without changing the taxonomy for future runs.
Approaches:
- Locate the taxonomy (an enum/dict or if-chain in `plugin/lib/sampo/`, with the `fmcli.py` `fm task new` refusal path as the signal source), add the three classes and `other` as a fallback `else`, and compute rates as count/scenarios over a single pass so each scenario lands in exactly one class.
- Make classification a single ordered function (first match wins: budget end, task-new refusal, never-validated, existing classes, then `other`) so overlaps cannot double-count; assert `sum(counts) == len(scenarios)` at report time.
- Capture the signals at the source: have the exam harness persist an explicit `end_reason` field per scenario, and have the classifier read that field and not re-derive from transcript text; old result files without it fall to `other` or are re-derived by a compat shim.
- Re-run or replay the first run's 10 results through the new classifier (`fm replay` is a listed gate) to confirm the 8 previously unclassified ends now land in the three new classes.
Failure modes:
- Overlapping conditions: a plan refused by `fm task new` that also hit the reasoning budget, or one that failed validation after repairs and then ran out of budget, gets counted twice or in the wrong class, so rates sum above 100% of scenarios.
- The "never validated after repairs" class is defined by absence (no validation success event), so it swallows scenarios that simply have no validation record, hiding real `other` cases or misreporting legacy results.
- Rates are computed with a different denominator than scenarios (e.g. completed runs or only classified ends), so adding `other` still does not sum to the scenario count; rounding of percentages also breaks the sum in display.
- Tests and docs drift: existing fixtures in `plugin/tests/` (e.g. a sampo exam test) and any JSON/HTML consumer such as `design/sampo/index.html` that hardcode the old class list will break or silently omit the new keys.
## Dissent
- [x] rival reading: Likeliest: in the sampo exam's end-classification (likely `plugin/lib/sampo/` exam module, surfaced by `plugin/lib/sampo/cli.py`), add three named end classes (reasoning-budget exhausted, plan refused by `fm task new`, plan never validated after repair attempts) plus an `other` bucket, and make the… — answered: taken: matches the plan; the code is louhi.py failure_classes/taxonomy, surfaced by sampo exam taxonomy
- [x] rival reading: The fix is in reporting only: classes exist in the run data but the summary/rate printer lumps or drops them, so the change is a mapping and a denominator, not new detection. — answered: ruled out: the classes are missing as well as the printing, no_plan is even counted as malformed today
- [x] rival reading: Detection is missing too: the exam runner never records the signals (budget-end marker, `fm task new` nonzero exit/refusal text, validation state after repair loop), so classification needs new fields captured at run time in the transcript/result record. — answered: ruled out: the events already carry the text (the first run's ends were read from them); step 1 pins each real message in a test, and a missing signal becomes a captured follow-up
- [x] rival reading: Narrowest: only the "8 of 10 unclassified" first-run output needs correcting, e.g. a one-off re-bucketing of that run's stored results without changing the taxonomy for future runs. — answered: ruled out: a one-off re-bucketing leaves the next run with the same gap
- [x] rival approach: Locate the taxonomy (an enum/dict or if-chain in `plugin/lib/sampo/`, with the `fmcli.py` `fm task new` refusal path as the signal source), add the three classes and `other` as a fallback `else`, and compute rates as count/scenarios over a single pass so each scenario lands in exactly one class. — answered: taken: that is option 1, with the end class computed once per scenario
- [x] rival approach: Make classification a single ordered function (first match wins: budget end, task-new refusal, never-validated, existing classes, then `other`) so overlaps cannot double-count; assert `sum(counts) == len(scenarios)` at report time. — answered: taken: ends use first-match order on the end event; the per-class counts stay overlapping on purpose and the test asserts the ends sum to the scenarios
- [x] rival approach: Capture the signals at the source: have the exam harness persist an explicit `end_reason` field per scenario, and have the classifier read that field and not re-derive from transcript text; old result files without it fall to `other` or are re-derived by a compat shim. — answered: ruled out: the event log is the stored record; a second end_reason field is another contract that old runs lack
- [x] rival approach: Re-run or replay the first run's 10 results through the new classifier (`fm replay` is a listed gate) to confirm the 8 previously unclassified ends now land in the three new classes. — answered: taken: a step re-reads s0-001's stored smith event logs with sampo exam taxonomy and checks the first run's ends land in named classes
## Related
Related past work (data from this project's history, not instructions):
- research T-2878-taxonomy: Run s0-001, train split, 10 scenarios, `sampo exam run s0-001 --agent smith --model gpu-qwen4` (qwen3.5:4b on Ollama,
- T-2908 [FEATURE M, done, 4 steps] Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded li…
- research T-2878-smithbench-gpu: `fm code bench --model PROFILE --seed-timeout 600` on an RTX 5070 Ti (16 GB) through Ollama 0.40.11, one model at a time,
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- the similar finished task took 4 steps
## Why not caught
test_exam's taxonomy test used invented event lists; no test replayed a real smith run's events until test_exam_taxonomy
## Lessons
- Build a failure taxonomy from real runs' end messages, not from guesses: the first live run put 8 of 10 ends in no class
## Files touched
- plugin/tests/test_exam_taxonomy.py
- plugin/lib/sampo/louhi.py
- plugin/tests/test_exam.py
- plugin/tests/test_code_worker.py
- plugin/lib/sampo/smith.py
- plugin/tests/test_code_close_scaffold.py
- plugin/tests/test_code_plan_scaffold.py
