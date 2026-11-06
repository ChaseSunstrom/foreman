---
id: T-2936
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T08:40:46Z
updated: 2026-11-04T10:01:51Z
base_note: Calibration: this plan states Choice 65% where FEATURE M closes (607) held on the first finish 98% of the time: 33 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T08:48:04Z
rival_split: true
builder_model: haiku
base: fd52a0f157949bae8fd5eba92bbd83596104db51
base_tree: c5d5cd49aa9b8626737175f911b2798bb558fc0a
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T09:03:34Z
plan0_scope: []
lane_stop: merged 2026-11-04T09:15:22Z
verified: strong
---
# Small-model plan scaffold: for a local profile Smith asks the plan one field at a time…
## Raw request
> FEATURE: Small-model plan scaffold: for a local profile Smith asks the plan one field at a time with a worked example per field, and fills an M plan's readings and options from a template the model completes, so a 4B passes Sampo's plan bar (qwen3.5:4b failed 'an M plan needs readings/options' and 'type must be one of' on 6 of 10 exam scenarios)
## Interpretation
Reading 1 (chosen): when the plan's JSON slot fails (two repairs) the field-by-field ladder runs, and for a local profile that ladder cannot succeed on an M plan: PLAN_FIELDS (smith.py) asks only type, tier, title, criteria and steps, while check_plan ends in _m_gaps, which needs readings, options and a choice. The first exam run ended "an M plan needs readings/options" and "type must be one of" on 4 of 10 scenarios even after the ladder (exam-nothink-v2.log, gpu-qwen4-nothink). So extend the ladder: M-only fields asked when the tier answer is M, and a worked example in every question.
Reading 2 (ruled out): a separate small-model planner (own prompt, own checker). The checker's bar is Sampo's real plan bar, which a task must meet anyway; the ladder is the part that cannot reach it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a model that never writes valid plan JSON still gets an M plan through the field-by-field ladder, with readings, three or more options (one exists, one less), choice and confidence, and it passes check_plan — verify with `python3 plugin/tests/run.py test_code_plan_scaffold`
- [x] every ladder question carries a worked example and the type question lists the six types — verify with `python3 plugin/tests/run.py test_code_plan_scaffold`
- [x] an S answer asks no M fields; the existing ladder test and the plan tests pass — verify with `python3 plugin/tests/run.py test_code_plan_scaffold && python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
1) Extend the ladder in smith.py: PLAN_FIELDS entries gain an optional condition (asked only when the tier answered so far is M) and new fields readings (two lines), options (three or more lines written "kind | approach | fails if", kinds build, exists, less), choice (a number) and confidence (a number), assembled into the keys check_plan reads (readings, options, choice, confidence, why). Every question, the existing type/tier/title/criteria/steps included, carries a one-line worked example, and the type question lists the six TYPES. slot() builds v from the answers, so the change is a condition in its loop and new parsers beside _items/_word/_criteria. Likely outcome: a 4B that cannot write the JSON object still passes check_plan and _m_gaps, so the plan stage stops being the end of 4 of 10 scenarios. Fails if: the model writes the fields but options of the wrong kinds (no "exists"/"less"), which _m_gaps then quotes back, and the ladder has no repair turn per field, so one bad field ends the run.
2) use what exists: no new code path; add a worked example plan to PLAN_PROMPT (via the variant_note() slot _plan already prepends) for local profiles only. Likely outcome: the JSON slot succeeds more often, at no cost to cloud models. Fails if: a 4B still cannot hold a 600-token nested JSON object (the exam's "no valid plan after 2 repairs" ends), because the ladder it falls to still has no M fields.
3) do less: a local profile's ladder fixes tier to S and skips the M gate. Likely outcome: removes the readings/options failures at once. Fails if: a real M task is planned as S, which only hides the failure and plans less carefully than the work needs; it is a tier lie, not a scaffold.
Choice 1 (65%): only the ladder has no way to meet the M bar, and option 2 cannot help a model that cannot write the object at all; the examples from option 2 go into the ladder's questions.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: test_code_plan_scaffold.py with a fake model that answers JSON badly, then the ladder's questions one by one
2. [x] Give slot()'s field tuples an optional condition on the answers so far
3. [x] Add readings, options, choice, confidence fields and parsers beside _items/_word/_criteria
4. [x] Add a worked example to each PLAN_FIELDS question
5. [x] Run the new test and test_code
## Resume here
<!-- auto -->
- 2026-11-04T09:47:35Z steps 5/5 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/sampo/smith.py, plugin/tests/test_code_close_scaffold.py, plugin/tests/test_code_plan_scaffold.py, plugin/tests/test_code_worker.py
## Docs impact
CHANGELOG line (T-2936); Smith's docstring names the ladder
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code_plan_scaffold 2>&1 | tail -15` → ✗ exit 1 · Ran 3 tests in 3.2s (1 classes, 16 at a time; slowest: Ladder 1s) / FAILED (1 classes: test_code_plan_scaffold.Ladder) [ran] [tree 6cc102d9d501] [world 2f1906870a] (2026-11-04T09:04:24Z)
- (ac 2) `python3 plugin/tests/run.py test_code_plan_scaffold 2>&1 | tail -15` → ✗ exit 1 · Ran 3 tests in 3.2s (1 classes, 16 at a time; slowest: Ladder 1s) / FAILED (1 classes: test_code_plan_scaffold.Ladder) [ran] [tree 6cc102d9d501] [world 2f1906870a] (2026-11-04T09:04:24Z)
- (ac 1) `python3 plugin/tests/run.py test_code_plan_scaffold 2>&1 | tail -15` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: Ladder 1s) / OK [ran] [tree e10800ecca48] [world 2f1906870a] (2026-11-04T09:04:46Z)
- (ac 2) `python3 plugin/tests/run.py test_code_plan_scaffold 2>&1 | tail -15` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: Ladder 1s) / OK [ran] [tree e10800ecca48] [world 2f1906870a] (2026-11-04T09:04:46Z)
- (step 1) `python3 plugin/tests/run.py test_code_plan_scaffold 2>&1 | tail -15` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: Ladder 1s) / OK [ran] [tree e10800ecca48] [world 2f1906870a] (2026-11-04T09:04:46Z)
- (step 5) `python3 plugin/tests/run.py test_code_plan_scaffold` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: Ladder 1s) / OK [ran] [tree e10800ecca48] [world 2f1906870a] (2026-11-04T09:11:51Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_code_hardening test_code_plan_scaffold test_code_worker && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.03s] [ran] [tree e10800ecca48] [world 2f1906870a] (2026-11-04T09:15:30Z)
- (step 2) `python3 plugin/tests/run.py test_code_plan_scaffold` → exit 0 · Ran 4 tests in 1.2s (1 classes, 16 at a time; slowest: Ladder 1s) / OK [ran] [tree 26b3652ceb8c] [world 2f1906870a] (2026-11-04T09:43:49Z)
- (step 3) `python3 plugin/tests/run.py test_code_plan_scaffold` → exit 0 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: Ladder 1s) / OK [ran] [tree 26b3652ceb8c] [world 2f1906870a] (2026-11-04T09:43:52Z)
- (step 4) `python3 plugin/tests/run.py test_code_plan_scaffold` → exit 0 · Ran 4 tests in 1.5s (1 classes, 16 at a time; slowest: Ladder 1s) / OK [ran] [tree 26b3652ceb8c] [world 2f1906870a] (2026-11-04T09:43:54Z)
- (ac 1) `python3 plugin/tests/run.py test_code_plan_scaffold` → exit 0 · Ran 4 tests in 0.6s (1 classes, 16 at a time; slowest: Ladder 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T09:59:38Z)
- (ac 2) `python3 plugin/tests/run.py test_code_plan_scaffold` → exit 0 · Ran 4 tests in 0.6s (1 classes, 16 at a time; slowest: Ladder 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T09:59:38Z)
- (ac 3) `python3 plugin/tests/run.py test_code_plan_scaffold && python3 plugin/tests/run.py test_code` → exit 0 · Ran 477 tests in 79.6s (102 classes, 16 at a time; slowest: Worker 79s, CodeFakes 35s, OutcomeEscalation 27s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T09:59:38Z)
- (audit intent) `one fm-reviewer pass over the uplift batch; its edge finding (the first word 'THE' read as the type) fixed test-first` → PLAN_FIELDS asks one field at a time with a worked example; M-only fields wait on _is_m and an S answer skips them [tree c6d95c6236bb] (2026-11-04T09:59:38Z)
- (audit edge) `one fm-reviewer pass over the uplift batch; its edge finding (the first word 'THE' read as the type) fixed test-first` → 'The task is a FIX' gave type THE and failed check_plan; _word now takes the first type or tier word (test_a_sentence_answer_still_gives_the_type_and_tier) [tree c6d95c6236bb] (2026-11-04T09:59:38Z)
- (audit operator) `one fm-reviewer pass over the uplift batch; its edge finding (the first word 'THE' read as the type) fixed test-first` → an M plan costs at most 10 field calls, only after 3 failed JSON tries, each under check_cap [tree c6d95c6236bb] (2026-11-04T09:59:38Z)
## Log
- 2026-11-04T08:40:46Z created
- 2026-11-04T08:45:01Z set tier=M
- 2026-11-04T08:46:03Z planned: it has criteria and steps
- 2026-11-04T08:46:23Z set approved=True
- 2026-11-04T09:03:20Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2936.builder.md
- 2026-11-04T09:03:33Z focused
- 2026-11-04T09:03:34Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T09:15:22Z merged worktree-agent-a5c7c3284249f22f2 (2 file(s))
- 2026-11-04T09:17:44Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5c7c3284249f22f2
- 2026-11-04T09:41:34Z focused
- 2026-11-04T09:55:14Z paused: focus moved to T-2937
- 2026-11-04T09:58:15Z focused
- 2026-11-04T10:01:46Z done
- 2026-11-04T10:01:51Z committed 2c84199e (2 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a new "scaffold" mode in the plan-authoring path (Smith agent, likely `plugin/lib/sampo/agents.py` / `fmagents.py`, plus the plan validator behind the 'an M plan needs readings/options' and 'type must be one of' errors). When the profile is local, Smith prompts for one plan field per mod…
- Prompt-only reading: change only the prompts, with a per-field loop and examples, and keep the existing validator and plan schema unchanged. Template filling is just text in the prompt.
- Structural reading: the scaffold is code-driven. Python assembles the plan JSON from a template, and the model returns only the missing slots (strings or enum choices), so the model never emits plan structure or the `type` enum.
- Narrow reading: the goal is only to make the 4B pass the 6 failing exam scenarios, so the change is tuned to those cases in `plugin/evals/` and the Sampo plan-bar exam rather than being a general mechanism.
Approaches:
- Per-field loop in the Smith plan step. Keyed on a "local" profile flag, iterate over the plan schema's fields in order. Each call carries one field's instruction plus a worked example kept next to the field definition, so the examples can't drift from the validator. Assemble the answers into the pl…
- Template-completion for M plans. Ship a skeleton under `plugin/templates/` with readings/options slots already shaped (ids, `type` already set from the allowed list). The model fills only the text slots and picks `type` from a short numbered list, which the code maps back to the enum. This removes …
- Reuse the validator's field and enum definitions as the source for both the scaffold prompts and the validation, rather than duplicating them. Add a retry that re-asks only the field that failed, with the validator's message quoted.
- Gate on the profile (local vs hosted) in one place, so hosted models keep the current single-shot path with no behaviour change. Verify with the exam scenarios through `fm replay` or the evals runner, using qwen3.5:4b.
Failure modes:
- The scaffold's field list or enum drifts from the validator. The scaffold then passes its own check but fails the real plan bar, or the 'type must be one of' error persists. Single-sourcing the schema is the mitigation.
- A template that is too prescriptive yields plans where readings/options are filler. These pass the structural bar but score badly on content, or the model copies the worked example verbatim into every plan, so examples have to be clearly marked and varied.
- Per-field calls multiply latency and token use on a 4B. A cross-field inconsistency (an option that doesn't match any reading) appears because each field was written without seeing the others, so later fields need earlier answers in context.
- The profile detection misfires: a hosted profile gets the scaffold, or a local one doesn't. Non-M plans (S/L) hit the M-only template path and get readings/options they shouldn't have, so the size check has to run before template selection.
## Dissent
- [x] rival reading: Likeliest: a new "scaffold" mode in the plan-authoring path (Smith agent, likely `plugin/lib/sampo/agents.py` / `fmagents.py`, plus the plan validator behind the 'an M plan needs readings/options' and 'type must be one of' errors). When the profile is local, Smith prompts for one plan field per mod… — answered: taken in part: the change is in smith.py's slot() and PLAN_FIELDS, the existing ladder, not a new mode; the plan validator stays check_plan/_m_gaps
- [x] rival reading: Prompt-only reading: change only the prompts, with a per-field loop and examples, and keep the existing validator and plan schema unchanged. Template filling is just text in the prompt. — answered: ruled out: prompt-only is option 2 and cannot help a model that cannot write the nested object
- [x] rival reading: Structural reading: the scaffold is code-driven. Python assembles the plan JSON from a template, and the model returns only the missing slots (strings or enum choices), so the model never emits plan structure or the `type` enum. — answered: taken in part: the code already assembles the plan from per-field answers; the model returns text per field; a numbered list for type is left out because _word already takes one word and the question…
- [x] rival reading: Narrow reading: the goal is only to make the 4B pass the 6 failing exam scenarios, so the change is tuned to those cases in `plugin/evals/` and the Sampo plan-bar exam rather than being a general mechanism. — answered: ruled out: the scaffold is a general mechanism tested with a fake model; the exam is the measurement afterwards, not the spec
- [x] rival approach: Per-field loop in the Smith plan step. Keyed on a "local" profile flag, iterate over the plan schema's fields in order. Each call carries one field's instruction plus a worked example kept next to the field definition, so the examples can't drift from the validator. Assemble the answers into the pl… — answered: taken: this is option 1; each example sits in the field tuple beside its question
- [x] rival approach: Template-completion for M plans. Ship a skeleton under `plugin/templates/` with readings/options slots already shaped (ids, `type` already set from the allowed list). The model fills only the text slots and picks `type` from a short numbered list, which the code maps back to the enum. This removes … — answered: ruled out: a skeleton file is a second copy of the plan schema that can drift from check_plan; the field tuples are the one place
- [x] rival approach: Reuse the validator's field and enum definitions as the source for both the scaffold prompts and the validation, rather than duplicating them. Add a retry that re-asks only the field that failed, with the validator's message quoted. — answered: taken in part: check_plan stays the only validator and the examples sit beside the field definitions; a per-field repair turn is not added (it is the failure named in option 1) and is captured as a f…
- [x] rival approach: Gate on the profile (local vs hosted) in one place, so hosted models keep the current single-shot path with no behaviour change. Verify with the exam scenarios through `fm replay` or the evals runner, using qwen3.5:4b. — answered: ruled out: the ladder only runs after the JSON slot has failed, so a model that writes the JSON object is unchanged; a profile test is not needed
## Related
Related past work (data from this project's history, not instructions):
- research T-2878-uplift-exp1: Louhi run s0-001, train split, the same 10 scenarios each time, `sampo exam run s0-001 --agent smith --model PROFILE`,
- research T-2878-taxonomy: Run s0-001, train split, 10 scenarios, `sampo exam run s0-001 --agent smith --model gpu-qwen4` (qwen3.5:4b on Ollama,
- T-2935 [FEATURE M, active, 4 steps] Local models get the context their prompts need: Sampo reads an Ollama model's served…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Lessons
- A small model answers a one-word question with a sentence: parse for the allowed word anywhere in it, never position 0
## Files touched
- plugin/tests/test_code_plan_scaffold.py
- plugin/lib/sampo/smith.py
- CHANGELOG.md
