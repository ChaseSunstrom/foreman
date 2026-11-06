---
id: T-2937
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T08:40:46Z
updated: 2026-11-04T09:58:08Z
base_note: Calibration: this plan states Choice 60% where FEATURE M closes (607) held on the first finish 98% of the time: 38 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T08:48:45Z
rival_split: true
builder_model: haiku
base: 9aeca7a7f82d4c4afbedc1e4a7cd9a54fba2798a
base_tree: 2eacbd5fecd0b0232876a581132942f1fde3c901
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T09:18:02Z
plan0_scope: []
lane_stop: merged 2026-11-04T09:27:40Z
verified: strong
---
# Small-model close scaffold: Smith asks a local model for the close's Decision line and…
## Raw request
> FEATURE: Small-model close scaffold: Smith asks a local model for the close's Decision line and lenses in their own slot with an example, so a verified task isn't refused at finish (gemma4:12b had two scenarios blocked at 'no Decision:' after its work passed)
## Interpretation
Reading 1 (chosen): the "no Decision" refusal at finish is a RESEARCH task closing without a Decision section (cli.py's done gate: "research ends in a choice"). Smith's _finish never writes one: it passes only lens, docs, lesson and why-not-caught, and only for tier M (the close slot is skipped for S). gemma4:12b typed flaky-rust and slow-ruby RESEARCH, did the work and then failed to close. Fix: a decision note in the close slot for RESEARCH plans (any tier), written with fm task set ID --section Decision before fm task finish, and a worked example for every close key.
Reading 2 (ruled out): loosen the gate, or let fm task finish take a --decision flag. The gate is right (research ends in a choice) and the harness can set the section itself.
## Assumptions (confidence)
## Acceptance criteria
- [x] a RESEARCH plan from a fake local model closes: the Decision section is set before fm task finish and the task reaches closed, for tier M and tier S — verify with `python3 plugin/tests/run.py test_code_close_scaffold`
- [x] the close prompt sent carries a worked example for each key — verify with `python3 plugin/tests/run.py test_code_close_scaffold`
- [x] a FIX or FEATURE close is unchanged — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
1) In smith.py: CLOSE_KEYS/CLOSE_FIELDS/check_close/CLOSE_PROMPT gain a "decision" key used when the plan type is RESEARCH (asked for S as well as M, with only that key for S); _finish runs run.fm("task","set",tid,"--section","Decision","--text",...) before the finish call; the prompt and each field question carry a worked example ("Recommendation: ...; would change if: ..."). Likely outcome: the two blocked gemma4:12b scenarios reach closed. Fails if: finish then refuses for another gap (lesson missing, a docs proof), since M tasks also need those; the test pins the whole close, not just Decision.
2) use what exists: no new key; build the Decision from notes the M close already has: "Recommendation: <intent>; would change if: <adversary>" (the form cli.py's refusal message names). Likely outcome: zero new model calls for M. Fails if: the task is S (no close slot runs, so there are no notes) or the model's intent line is not a recommendation.
3) do less: write Decision "none: ..." (cli accepts it) for every RESEARCH close. Likely outcome: no more refusals. Fails if: it passes the gate by defeating it; a research task that closes with no choice is a worse result than a blocked one.
Choice 1 (60%): the only option that gives S RESEARCH tasks a Decision and keeps the gate meaningful; option 2's mapping is the fallback if the model's decision text comes back empty.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: test_code_close_scaffold.py (RESEARCH M and S close with a fake model)
2. [x] Add a decision key to CLOSE_KEYS/CLOSE_FIELDS/check_close for RESEARCH plans
3. [x] In _finish ask the slot for RESEARCH of any tier and set the Decision section before finish
4. [x] Add worked examples to CLOSE_PROMPT and the field questions
5. [x] Run the new test and test_code
## Resume here
## Docs impact
CHANGELOG line (T-2937); Smith's docstring already names the close slots
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code_close_scaffold 2>&1 | tail -30` → ✗ exit 1 · Ran 6 tests in 7.5s (1 classes, 16 at a time; slowest: CloseGaps 6s) / FAILED (1 classes: test_code_close_scaffold.CloseGaps) [ran] [tree a973b0f3ff4b] [world 2f1906870a] (2026-11-04T09:19:29Z)
- (ac 2) `python3 plugin/tests/run.py test_code_close_scaffold 2>&1 | tail -30` → ✗ exit 1 · Ran 6 tests in 7.5s (1 classes, 16 at a time; slowest: CloseGaps 6s) / FAILED (1 classes: test_code_close_scaffold.CloseGaps) [ran] [tree a973b0f3ff4b] [world 2f1906870a] (2026-11-04T09:19:29Z)
- (ac 1) `python3 plugin/tests/run.py test_code_close_scaffold 2>&1 | tail -5` → exit 0 · Ran 6 tests in 23.5s (1 classes, 16 at a time; slowest: CloseGaps 23s) / OK [ran] [tree 70db6443d074] [world 2f1906870a] (2026-11-04T09:22:03Z)
- (ac 2) `python3 plugin/tests/run.py test_code_close_scaffold 2>&1 | tail -5` → exit 0 · Ran 6 tests in 23.5s (1 classes, 16 at a time; slowest: CloseGaps 23s) / OK [ran] [tree 70db6443d074] [world 2f1906870a] (2026-11-04T09:22:03Z)
- (step 1) `python3 plugin/tests/run.py test_code_close_scaffold 2>&1 | tail -5` → exit 0 · Ran 6 tests in 23.5s (1 classes, 16 at a time; slowest: CloseGaps 23s) / OK [ran] [tree 70db6443d074] [world 2f1906870a] (2026-11-04T09:22:03Z)
- (step 2) `python3 plugin/tests/run.py test_code_close_scaffold` → exit 0 · Ran 7 tests in 31.0s (1 classes, 16 at a time; slowest: CloseGaps 30s) / OK [ran] [tree 6a510f2f804c] [world 2f1906870a] (2026-11-04T09:39:07Z)
- (step 3) `python3 plugin/tests/run.py test_code_close_scaffold` → exit 0 · Ran 7 tests in 8.4s (1 classes, 16 at a time; slowest: CloseGaps 8s) / OK [ran] [tree 6a510f2f804c] [world 2f1906870a] (2026-11-04T09:39:51Z)
- (step 4) `python3 plugin/tests/run.py test_code_close_scaffold` → exit 0 · Ran 7 tests in 8.7s (1 classes, 16 at a time; slowest: CloseGaps 8s) / OK [ran] [tree 6a510f2f804c] [world 2f1906870a] (2026-11-04T09:40:01Z)
- (step 5) `python3 plugin/tests/run.py test_code_close_scaffold test_code test_code_worker` → exit 0 · Ran 476 tests in 80.5s (102 classes, 16 at a time; slowest: Worker 80s, CodeFakes 39s, OutcomeEscalation 34s) / OK [ran] [tree 6a510f2f804c] [world 2f1906870a] (2026-11-04T09:41:22Z)
- (ac 1) `python3 plugin/tests/run.py test_code_close_scaffold` → exit 0 · Ran 7 tests in 8.2s (1 classes, 16 at a time; slowest: CloseGaps 8s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T09:56:48Z)
- (ac 2) `python3 plugin/tests/run.py test_code_close_scaffold` → exit 0 · Ran 7 tests in 8.2s (1 classes, 16 at a time; slowest: CloseGaps 8s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T09:56:48Z)
- (ac 3) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 477 tests in 73.3s (102 classes, 16 at a time; slowest: Worker 73s, CodeFakes 35s, OutcomeEscalation 26s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T09:56:48Z)
- (audit intent) `one fm-reviewer pass over the uplift batch (T-2926 umbrella diff + T-2937 merge diff), its blocking finding fixed test-first` → _gaps_needed mirrors finish's refusals (RESEARCH Decision, PERFORMANCE Measurements, proof_gap); _finish fills them before the close, any tier [tree c6d95c6236bb] (2026-11-04T09:56:48Z)
- (audit edge) `one fm-reviewer pass over the uplift batch (T-2926 umbrella diff + T-2937 merge diff), its blocking finding fixed test-first` → a --worker --verify run has no profile; it crashed in _ask (AttributeError) — now it skips the slot and finish blocks with its own reason (test_a_modelless_close_with_a_gap_blocks_cleanly) [tree c6d95c6236bb] (2026-11-04T09:56:48Z)
- (audit adversary) `one fm-reviewer pass over the uplift batch (T-2926 umbrella diff + T-2937 merge diff), its blocking finding fixed test-first` → a small model copying the worked example into the Regression test would forge a proof; an answer equal to its example is now re-asked (test_a_copied_example_is_asked_again) [tree c6d95c6236bb] (2026-11-04T09:56:48Z)
## Log
- 2026-11-04T08:40:46Z created
- 2026-11-04T08:45:02Z set tier=M
- 2026-11-04T08:46:11Z planned: it has criteria and steps
- 2026-11-04T08:46:24Z set approved=True
- 2026-11-04T09:17:46Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2937.builder.md
- 2026-11-04T09:18:01Z focused
- 2026-11-04T09:18:02Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T09:27:40Z merged worktree-agent-ab771d031efbef5d7 (2 file(s))
- 2026-11-04T09:44:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab771d031efbef5d7
- 2026-11-04T09:55:14Z focused
- 2026-11-04T09:58:07Z done
- 2026-11-04T09:58:08Z committed 22ed1526 (2 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: when the finishing agent is a small local model (gemma4:12b via Ollama), the close step stops asking for one big structured close and instead makes a separate, narrow call to get the `Decision:` line, and another per lens, each with a worked example in its prompt. The close gate (likely …
- Alternative: leave the prompt alone and relax the gate's parser so it accepts the Decision in looser forms (case, bullet prefix, trailing text) from small models. This fixes the symptom but not the model's omission.
- Alternative: Smith synthesizes the Decision itself from the verified result (pass → default decision), with the model supplying only the lenses. This removes the model's role in a required field.
- Narrow reading: only change the prompt text or example in the existing close template so that gemma4:12b emits `Decision:`, with no new call or slot.
Approaches:
- Add a small-model branch in the close path: detect a local or small model (config or model-name check in `fmcore.py`/`fmcli.py`), issue a dedicated slot request for Decision, then one per lens, each with a one-line example, and assemble the close text before the existing gate validates it. The gate…
- Add a scaffold function (for example `close_scaffold(model, task)`) in its own module, which returns the slot prompts and the assembler. The caller picks it by model capability flag, so large models keep the one-shot close path unchanged.
- Make the slot result self-validating: re-ask once with the example if the reply doesn't match the exact `Decision:` regex the gate uses, importing that regex from the gate instead of copying it.
- Test with a fake model client returning the failing shape seen in the two gemma4:12b scenarios, in `plugin/tests/` next to the existing close/guard tests, and replay one failing scenario through `fm replay`.
Failure modes:
- The scaffold's Decision regex drifts from the gate's, so the scaffold approves lines the gate still rejects, and the "no Decision:" block persists.
- The model copies the example verbatim, so every close carries the example's Decision and lenses. The gate passes, but the content is fabricated and the closes lose meaning.
- Extra model calls per close hit latency or hook-timeout budgets, which `bench_hooks.py --runs 20` would show as a regression, or fail on a slow local model.
- The small-model branch triggers on the wrong models (name matching misses other tags or catches large models), so large-model closes change behaviour or the other small models still get refused.
## Dissent
- [x] rival reading: Likeliest: when the finishing agent is a small local model (gemma4:12b via Ollama), the close step stops asking for one big structured close and instead makes a separate, narrow call to get the `Decision:` line, and another per lens, each with a worked example in its prompt. The close gate (likely … — answered: taken in part: the close is already one slot with a per-key field ladder (CLOSE_FIELDS), so the Decision gets its own question with an example there; a separate call per lens is not added (the repair…
- [x] rival reading: Alternative: leave the prompt alone and relax the gate's parser so it accepts the Decision in looser forms (case, bullet prefix, trailing text) from small models. This fixes the symptom but not the model's omission. — answered: ruled out: the Decision section is absent, not misformatted (_finish never writes it); a looser parser would accept nothing new
- [x] rival reading: Alternative: Smith synthesizes the Decision itself from the verified result (pass → default decision), with the model supplying only the lenses. This removes the model's role in a required field. — answered: taken in part: this is option 2, kept as the fallback if the model's decision text comes back empty; not the default because S tasks have no notes
- [x] rival approach: Add a small-model branch in the close path: detect a local or small model (config or model-name check in `fmcore.py`/`fmcli.py`), issue a dedicated slot request for Decision, then one per lens, each with a one-line example, and assemble the close text before the existing gate validates it. The gate… — answered: taken in part: the branch is on plan type RESEARCH (the gate's trigger), not on model size, so every profile gets it; the worked examples are short enough to send to all
- [x] rival approach: Add a scaffold function (for example `close_scaffold(model, task)`) in its own module, which returns the slot prompts and the assembler. The caller picks it by model capability flag, so large models keep the one-shot close path unchanged. — answered: ruled out: a new module for about ten lines; CLOSE_PROMPT/CLOSE_KEYS/CLOSE_FIELDS/check_close already hold the close
- [x] rival approach: Make the slot result self-validating: re-ask once with the example if the reply doesn't match the exact `Decision:` regex the gate uses, importing that regex from the gate instead of copying it. — answered: taken in part: slot() already re-asks with check_close's message; check_close gains 'give decision as text' for RESEARCH, which is the same nonblank rule the gate applies
- [x] rival approach: Test with a fake model client returning the failing shape seen in the two gemma4:12b scenarios, in `plugin/tests/` next to the existing close/guard tests, and replay one failing scenario through `fm replay`. — answered: taken: the test uses the fake model client of test_code.py (test_m_tier_asks_the_model_for_its_close_notes is the pattern)
## Related
Related past work (data from this project's history, not instructions):
- T-2936 [FEATURE M, planned, 5 steps] Small-model plan scaffold: for a local profile Smith asks the plan one field at a time…
- research T-2878-taxonomy: Run s0-001, train split, 10 scenarios, `sampo exam run s0-001 --agent smith --model gpu-qwen4` (qwen3.5:4b on Ollama,
- research T-2878-uplift-exp1: Louhi run s0-001, train split, the same 10 scenarios each time, `sampo exam run s0-001 --agent smith --model PROFILE`,
- decision 2026-11-04: Local profiles serve 32k context with reasoning off as the default for Smith (T-2935/T-2938 make it automatic); small-model scaffolds for plan and c…
## Lessons
- A new model call in a shared path must handle every way the path is entered: grep the callers for the modelless (--worker --verify) and resume entries before adding a slot
## Files touched
- plugin/tests/test_code_close_scaffold.py
- plugin/lib/sampo/smith.py
