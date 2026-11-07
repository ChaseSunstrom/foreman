# T-2878 failure taxonomy of the local models on Sampo's work (2026-11-06, step 1)

Louhi's smith arm, `sampo exam run RUN --agent smith --model PROFILE --split all --limit 44`, on seeded exam runs of the
same 44 scenarios per model (11 kinds x 6 languages, a quarter held out): s28-020 and s29-024 (jarvis-nothink),
s28-021 (gpu-gemma12-32k), s28-022 (gpu-mimo9). Deterministic, no model judge: the per-scenario outcome is the grader's
(`sampo exam grade RUN --agent smith --json`, its closed lists: every keyed defect found, fixed and said, no false
alarm), the end class is Sampo's (`sampo exam taxonomy RUN --json`, louhi._ENDS) with its "other" split by the end
event, and the per-turn parse rate is read from the event logs (scratch reader t2878_parse.py: an act turn is a
`tokens` event inside a step, fix round or refused early done; Smith's do() emits one `action` event per action run).

## Models and outcome

| model (profile) | scenarios | passed | failed (train/held out) | fixed | found | false alarms | act-turn parse rate | Smith bench |
|---|---|---|---|---|---|---|---|---|
| qwen3.8-27b (jarvis-nothink) | 88 | 4 | **84** (62/22) | 12/96 | 23/96 | 40 | **89.1%** (84.2%, 94.8%) | 5/5 |
| gemma4:12b 32k (gpu-gemma12-32k) | 44 | 0 | **44** (33/11) | 2/48 | 7/48 | 30 | **98.5%** | 4/5 (guard-clause: 40-turn loop) |
| mimo-v2.6:9b (gpu-mimo9) | 44 | 1 | **43** (32/11) | 7/48 | 0/48 | 3 | **87.5%** | 5/5 |
| qwen3.6-35b (jarvis35-nothink) | not measured | | | | | | | |

qwen3.6-35b: unreachable for a fair run. jarvis serves both qwen models through llama-swap, and the running
`sampo moons grow --keep 10000` (11 h in, never stopped) keeps qwen3.8-27b loaded; a 35b call has to swap the model,
which takes longer than the profile's 120 s call timeout (two probes: `TimeoutError('The read operation timed out')`
at 121 s each), and each grow call swaps it back. Measure it when the grow ends (run s28-023 is generated and waiting).

The five easy bench seeds pass 4 or 5 of 5 on every model while the exam passes 0 to 5%: the bench no longer separates them.

**Gate (tool calls parse on 95% of act turns): gemma passes; qwen3.8-27b and mimo fail.** Turns with no runnable call:

| model | turns | prose, no call | empty reply | JSON that didn't parse | malformed args | unknown tool |
|---|---|---|---|---|---|---|
| qwen3.8-27b | 1112 | 73 (6.6%) | 32 (2.9%) | 16 (1.4%) | 0 | 0 |
| gemma4:12b | 1075 | 2 | 2 | 11 (1.0%) | 1 | 0 |
| mimo-v2.6:9b | 536 | 16 (3.0%) | 1 | 5 | 42 (7.8%) | 3 |

- prose: the model narrates the next move ("Let me read the benchmark file:", "Step 2 done: ...") and sends no action.
- JSON that didn't parse: 6 of qwen's 16 hold an invalid `\'` escape inside a valid `{"action": "done", ...}`
  (code like `name.replace('\'', ...)` in the summary); models.extract_json drops the whole action and Smith answers
  "No action found", 5 turns running in one scenario. Captured as T-3530. The rest are cut at the log's 1000-char say limit.
- mimo's malformed args: `write needs file as str` 28, `write needs content` 8, `edit needs file` 4: calls with no
  file argument at all.

## Failure classes: one end per failed scenario (171 failed: 84 + 44 + 43)

| end class | qwen3.8-27b | gemma4:12b | mimo-v2.6:9b | pooled |
|---|---|---|---|---|
| hollow_close: closed, the grader doesn't credit it | 40 (48%) | 17 (39%) | 4 (9%) | **61 (36%)** |
| answered: a read-only answer, nothing changed | 30 (36%) | 8 (18%) | 2 (5%) | **40 (23%)** |
| loop: all 40 turns used | 10 (12%) | 11 (25%) | 10 (23%) | **31 (18%)** |
| no_plan: no valid plan after 2 repairs | 0 | 0 | 23 (53%) | **23 (13%)** |
| finish_refused | 3 | 3 | 0 | 6 (4%) |
| fix_rounds: the verify still failed after 3 fix rounds | 1 | 3 | 1 | 5 (3%) |
| timeout / budget / plan_refused | 0 | 2 / 0 / 0 | 0 / 2 / 1 | 5 (3%) |

What the hollow closes are (from the same records): qwen's 40 closes, 29 had every criterion's verify **green before
any change** and 22 made **no edit at all**: it plans a check that already passes and closes on it. gemma's 17: 13
went red before and green after, yet the hidden check still fails: its own criterion was satisfiable without fixing
the planted defect. Test-first is near absent: 2/48 (qwen), 0/24 (gemma), 0/24 (mimo).
Answered: qwen answers read-only on change kinds too (slow 4, vuln 4, flaky 3, dep 2, bug 1, vague 2), not only on
docs and untested.

Contributing classes (share of all scenarios, `sampo exam taxonomy`): qwen loop 42%, refused 28%, false_done 5%;
gemma loop 77%, false_done 43%, refused 36%; mimo no_plan 52%, loop 34%, malformed 27%, refused 14%, wrong_tool 9%.
mimo's 23 no-plans: type outside the enum ("PERF", None) 10, tier not S or M 6, M plan without readings 4.

Findings call (the separate tool-less answer the grade reads): false alarms 40 (qwen) and 30 (gemma) against 23 and 7
found; mimo returns none (0 found, 3 false).

## Where step 2 (control) points, in order
1. Hollow close (36% of failures, qwen 48%): a red-first gate in the act loop: a FIX or change plan whose verify is
   green before any change is sent back for a criterion that fails now, and `done` with no edit on a change request
   is refused once with that reason. Measure: hollow_close rate and fixed/fixable.
2. Answered without a change (23%): route change kinds (bug, vuln, slow, flaky, dep) to the change path; an answer
   on them counts as a failed step, not an end.
3. Loop (18% of ends; contributing in 77% of gemma's scenarios): the loop breaker hands the step to the planner or
   ends the step after N repeats, instead of 40 turns.
4. Plan schema for small models (mimo 53%): constrained plan output, or enum aliases (PERF -> PERFORMANCE) and
   defaulted tiers before the plan gate.
5. Parse gate (qwen 89%, mimo 88%): T-3530's escape repair, a native or grammar-constrained tool call instead of text
   JSON for qwen's prose turns, and argument aliases (path/file) for mimo.

First cut (2026-11-04, 15 runs) for comparison: out of steps 40%, plan refused 20%, answered 13%, closed 13%,
reasoning ate the budget 7%, endpoint timeout 7%. Since then thinking is off and the plan ladder landed, so budget and
plan refusals dropped; hollow closes were not visible then (the grader's credit wasn't split from the run's close).

Runs still going (same scenarios, seed 29, for the step-2 baseline): s29-025 (gemma), s29-026 (mimo).
Reproduce: `sampo exam taxonomy RUN --json`, `sampo exam grade RUN --agent smith --json`, and the scratch readers
t2878_parse.py (parse rate) and t2878_fail.py (end per failed scenario).
