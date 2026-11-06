---
id: T-3006
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T19:25:22Z
updated: 2026-11-05T03:02:38Z
base_note: Calibration: this plan states Choice 65% where FEATURE M closes (630) held on the first finish 98% of the time: 33 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T19:25:38Z
rival_split: true
builder_model: haiku
base: 881e863554f21fa00e09e35fddfdf98b181d47f6
base_tree: d099e04ed02fba6ff30ce4a26c81e45043933c38
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T19:59:50Z
plan0_scope: []
lane_stop: merged 2026-11-04T21:06:46Z
door_seen: [b605e5d787cf]
verified: strong
unproven: [docs, infra, ui-unshot]
---
# Smith --reason state: a compact thought state carried between turns, thinking off by default with deliberate turns on low confidence or a failed check, a check before an edit, and an exam arm comparing it with native thinking on and off (T-3005 part 1)
## Raw request
> From T-3005 (a model-agnostic reasoning layer, better reasoning without overthinking, on any model): the first slice in Smith's phase loop, measured on Louhi held-out
## Interpretation
Reading 1 (chosen): a reasoning structure Sampo runs around any model: dense state instead of long prose thinking, compute spent where confidence is low, and checks against reality before commits; measured, not assumed. Reading 2 (ruled out): latent (neuralese) reasoning; it needs weight changes and can't apply to any model (research T-2996-small-model-path).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code --reason state carries the model's compact state as one message per call, turns thinking on only on low confidence, a failed check or a loop break, and asks for the named check before an edit; a turn without a state runs as today — verify with `python3 plugin/tests/run.py test_code_reason`
- [x] sampo exam run --reason state|off|native records each arm's fix rate and tokens per fix on the same scenarios — verify with `python3 plugin/tests/run.py test_code_reason test_exam`
- [x] models.complete applies a thinking budget with a forced close, a rumination logit bias where the backend accepts it (reported per profile when it doesn't), and a JSON schema for action turns where supported; each is a --reason arm — verify with `python3 plugin/tests/run.py test_code_reason test_models`
## Non-goals
## Approach (options → choice → why)
1) `fm code --reason state` (Smith's phase loop):
   - **State.** Each action the model sends may carry `state`: {goal, facts[], hypothesis, next_check, confidence 0..1}, capped in size. Smith keeps the latest state and puts it just before each call as one compact message. Older turns' prose stays trimmed as today, so the state carries continuity instead of long thinking.
   - **Thinking is off by default.** A turn gets deliberate mode (think on, a larger output cap) only when the state's confidence is under 0.5, the last check failed, or the loop breaker fired.
   - **A hypothesis needs a check.** When the state names a next_check, the next action must run or read it before an edit to the hypothesised file; otherwise Smith asks for the check first.
   - **Logging.** The mode is logged per turn.
   - **Measurement.** `sampo exam run ... --reason state|off|native` on the same held-out scenarios gives fix rate and tokens per fix per arm.
   Likely outcome: fewer wasted tokens and fewer blind edits on small models, and no empty overthinking turns on the 27B. Fails if: small models can't keep the state's JSON shape; it is parsed leniently, as cards are, and a missing state means the turn runs as today.
2) use what exists: the profile's think flag (on or off for every turn) and the planner split. Likely outcome: today's results (exp 2: gemma 1 of 8; the 27B's empty turns). Fails if: one switch for every turn either overthinks or underthinks.
3) do less: only adaptive thinking, with no state and no check rule. Likely outcome: fewer empty turns, but the same blind edits. Fails if: most misses today were wrong targets, not thin thinking.
Choice 1 (65%): state, adaptive budget and a check before edits, measured per arm on held-out scenarios before any default changes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests with a fake model: the state message, the deliberate trigger, the check-before-edit ask, a stateless reply unchanged, the exam arm
2. [x] the state, the budget policy, the check rule, the --reason flag on fm code and exam run
3. [x] a live arm comparison on seeded and minted held-out scenarios for gemma 12B and the 27B; numbers in research
## Resume here
<!-- auto -->
- 2026-11-04T20:33:30Z step 3/3: a live arm comparison on seeded and minted held-out scenarios for gemma 12B and the 27B; numbers in research
- git: worktree-agent-a99d1beb2cbd31fe7; 4 uncommitted: plugin/lib/sampo/models.py, plugin/lib/sampo/smith.py, plugin/tests/test_code_reason.py, plugin/tests/test_models.py
- touched since last checkpoint: plugin/lib/sampo/louhi.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/models.py, plugin/tests/test_models.py, plugin/lib/sampo/smith.py, plugin/tests/test_code_reason.py
## Docs impact
research T-3006-reason-arms (the first live arm table and reading); CHANGELOG line; --reason is in fm code's and exam run's argparse help.
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code_reason 2>&1 | tail -40` → ✗ exit 1 · Ran 11 tests in 45.5s (2 classes, 16 at a time; slowest: State 43s, Arm 1s) / FAILED (1 classes: test_code_reason.State) [ran] [tree 12ca33650801] [world 2f1906870a] (2026-11-04T20:07:30Z)
- (ac 1) `python3 plugin/tests/run.py test_code_reason 2>&1 | tail -40` → ✗ exit 1 · Ran 11 tests in 45.8s (2 classes, 16 at a time; slowest: State 44s, Arm 1s) / FAILED (1 classes: test_code_reason.State) [ran] [tree 0cce96cef9ef] [world 2f1906870a] (2026-11-04T20:08:35Z)
- (step 2) `python3 plugin/tests/run.py test_code_reason test_exam test_models` → exit 0 · Ran 204 tests in 211.0s (43 classes, 16 at a time; slowest: LeanKind 210s, ExamAuthors 86s, JudgmentKinds 79s) / OK [ran] [tree e1d3f8ef8d68] [world 2f1906870a] (2026-11-04T20:20:28Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code_close_scaffold test_code_hardening test_code_reason test_code_worker test_core test_ctx_variant test_doctor test_exam test_left_out test_louhi_models test_mint test_models test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [14.27s] [ran] [tree e1d3f8ef8d68] [world 2f1906870a] (2026-11-04T20:26:38Z)
- (step 3) `python3 plugin/tests/run.py test_code_reason test_models test_exam` → exit 0 · (no output) [ran] [tree 072c1a71759a] [world 2f1906870a] (2026-11-04T20:35:19Z)
- (step 2) `python3 plugin/tests/run.py test_code_reason test_exam test_models` → exit 0 · Ran 213 tests in 284.9s (43 classes, 16 at a time; slowest: LeanKind 284s, ExamAuthors 90s, JudgmentKinds 79s) / OK [ran] [tree b02e107d2c28] [world 2f1906870a] (2026-11-04T20:45:05Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code_close_scaffold test_code_hardening test_code_reason test_code_worker test_core test_ctx_variant test_doctor test_exam test_left_out test_louhi_models test_mint test_models test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [13.47s] [ran] [tree b02e107d2c28] [world 2f1906870a] (2026-11-04T20:55:26Z)
- (step 1) `python3 plugin/tests/run.py test_code_reason test_exam test_models` → exit 0 · Ran 217 tests in 300.1s (44 classes, 16 at a time; slowest: LeanKind 299s, ExamAuthors 97s, JudgmentKinds 81s) / OK [ran] [tree 6a413ae7f6aa] [world 2f1906870a] (2026-11-05T02:50:02Z)
- (ac 1) `python3 plugin/tests/run.py test_code_reason` → exit 0 · Ran 18 tests in 13.8s (2 classes, 16 at a time; slowest: State 13s, Arm 0s) / OK [ran] [tree 6a413ae7f6aa] [world 2f1906870a] (2026-11-05T02:53:57Z)
- (ac 2) `python3 plugin/tests/run.py test_code_reason test_exam` → exit 0 · Ran 129 tests in 197.2s (29 classes, 16 at a time; slowest: LeanKind 197s, ExamAuthors 85s, JudgmentKinds 76s) / OK [ran] [tree d1a1ef0c4759] [world 2f1906870a] (2026-11-05T02:57:15Z)
- (ac 3) `python3 plugin/tests/run.py test_code_reason test_models` → exit 0 · Ran 106 tests in 13.5s (17 classes, 16 at a time; slowest: State 13s, Bench 3s, RunRoute 1s) / OK [ran] [tree d1a1ef0c4759] [world 2f1906870a] (2026-11-05T02:57:29Z)
- (step 3) `test -f ~/.claude/foreman/state/projects/foreman-4a056f/research/T-3006-reason-arms.md` → exit 0 · (no output) [ran] [tree d1a1ef0c4759] [world 2f1906870a] (2026-11-05T02:57:30Z)
- `python3 plugin/tests/run.py test_code_reason` → ✗ exit 1 · Ran 18 tests in 2.8s (2 classes, 16 at a time; slowest: State 1s, Arm 0s) / FAILED (2 classes: test_code_reason.State, test_code_reason.Arm) (start tree + this task's tests) [ran] [tree d1a1ef0c4759] [world 2f1906870a] (2026-11-05T02:58:10Z)
- `python3 plugin/tests/run.py test_code_reason` → exit 0 · Ran 18 tests in 13.5s (2 classes, 16 at a time; slowest: State 13s, Arm 0s) / OK [ran] [tree d1a1ef0c4759] [world 2f1906870a] (2026-11-05T02:58:10Z)
- (ac 1) `python3 plugin/tests/run.py test_code_reason` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T02:58:10Z [ran] [tree d1a1ef0c4759] [world 2f1906870a] (2026-11-05T02:58:16Z)
- (ac 2) `python3 plugin/tests/run.py test_code_reason test_exam` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T02:57:15Z [ran] [tree d1a1ef0c4759] [world 2f1906870a] (2026-11-05T02:58:16Z)
- (ac 3) `python3 plugin/tests/run.py test_code_reason test_models` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T02:57:29Z [ran] [tree d1a1ef0c4759] [world 2f1906870a] (2026-11-05T02:58:16Z)
- (audit intent) `self: the merged builder diff (6 files) adds --reason off|state|native to fm code and exam run, the state message and deliberate-turn trigger in smith, the thinking budget with a forced close in models.complete, and the arm field in exam answers; tests cover each with a fake model` → the arms ran live on gemma 12B, MiMo 9B and the 27B (research T-3006-reason-arms); no arm separates at n=3, native thinking ran out of budget 6 of 6 on gemma against state's 1 of 3; the larger slice is T-2878's measurement [tree d1a1ef0c4759] (2026-11-05T02:58:16Z)
- (audit edge) `self: the merged builder diff (6 files) adds --reason off|state|native to fm code and exam run, the state message and deliberate-turn trigger in smith, the thinking budget with a forced close in models.complete, and the arm field in exam answers; tests cover each with a fake model` → a reply with no state runs as today; a backend that ignores the thinking switch (gemma over Ollama, once) is logged, not hidden; --reason off is the default [tree d1a1ef0c4759] (2026-11-05T02:58:16Z)
- (audit adversary) `self: the merged builder diff (6 files) adds --reason off|state|native to fm code and exam run, the state message and deliberate-turn trigger in smith, the thinking budget with a forced close in models.complete, and the arm field in exam answers; tests cover each with a fake model` → the state message is the model's own text carried back to the same model, capped in size, never into a gate, a commit or a label (models learn only from outcomes); no new network endpoint, only fields on the existing call [tree d1a1ef0c4759] (2026-11-05T02:58:16Z)
## Log
- 2026-11-04T19:25:22Z created
- 2026-11-04T19:25:23Z set approved=True
- 2026-11-04T19:28:11Z steer (user 2026-11-04: 'inject a reasoning layer that's really good into each model, and fast, so it doesn't do the whole maybe this, wait no, maybe this burning compute like qwen 3.8'): add decoding-level controls behind models.complete, per backend, each its own exam arm: (1) rumination suppression: logit bias against Wait, Hmm, Alternatively and their variants while thinking (NoWait, 2025: 27-51% shorter, no accuracy loss) where the backend takes logit_bias (llama.cpp server, vLLM; probe jarvis; Ollama may not, then serve the same GGUF through llama-server); (2) budget forcing: a thinking token budget per step from the difficulty, then the thinking is closed and an answer forced; (3) constrained output: a JSON schema for action turns (Ollama format) so the reply is state plus action; measured per model by fix rate, tokens per fix and wall time against native thinking
- 2026-11-04T19:59:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3006.builder.md
- 2026-11-04T19:59:49Z focused
- 2026-11-04T19:59:50Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T21:06:46Z merged worktree-agent-a99d1beb2cbd31fe7 (6 file(s))
- 2026-11-04T21:09:04Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a99d1beb2cbd31fe7
- 2026-11-04T22:40:31Z arm finding (gemma4-12b-32k, s5-019 off arm): 1 of 3 runs ended 'reasoning used the whole budget: no text in 8192 tokens' although the call sent enable_thinking false and reasoning_effort none (models.complete:996-1001): gemma 4 over Ollama's OpenAI API reasons anyway on some turns, so the off arm isn't fully off for this model; read its fix rate with that in mind. The 27B arms need LLM_API_KEY inline (never stored), so they wait for a session that has it
- 2026-11-04T23:03:22Z arms paused at gemma native (16:50) so the T-3026/T-3029 merges get a quiet machine; so far gemma12 off 0/3 fixed (ends other 2, loop 1), state 1/3 (loop 2, budget 1); native and MiMo's arms rerun after the merges
- 2026-11-05T02:55:13Z focused
- 2026-11-05T02:55:20Z scope: CHANGELOG.md (the user-visible line)
- 2026-11-05T03:02:36Z done
- 2026-11-05T03:02:38Z committed 2de15c35 (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest:** Build the first slice of a reasoning layer inside Smith's phase loop (probably under `plugin/lib/sampo/`, wired through `plugin/lib/fmhooks.py` or `fmcore.py`). The slice would be a single phase-level reasoning-budget or "stop when sufficient" controller that works on any model. "Mea…
- **Alternative:** The deliverable is mainly the measurement harness. That would be a Louhi held-out eval under `plugin/evals/` or `bench/` that scores accuracy and token cost, with the layer as a thin stub or flag.
- **Alternative:** "First slice" means a design or spec only (`design/`, `MASTER.md`, T-3005 notes), with no runtime code yet.
- **Unknown:** I can't tell what "Smith" and "Louhi" refer to in this repo. They might be a module and a dataset, or an agent persona and a benchmark name. I'd grep for both before committing to any reading.
Approaches:
- **Phase-loop wrapper:** Add a model-agnostic module (e.g. `plugin/lib/sampo/reasoning.py`) that the phase loop calls before and after each phase. It would carry prompt-level scaffolds (plan-then-verify, a cap on reasoning length) and an early-exit check on confidence or agreement. It would sit behi…
- **Eval-first:** Write the Louhi held-out runner first (`plugin/evals/` plus a `bench/` entry). It would record the baseline accuracy and tokens per model, and the layer would then be built against that number. The held-out split stays frozen and is never used for tuning.
- **Hook-based injection:** Implement the layer as a hook in `plugin/lib/fmhooks.py`, so it applies to every model without touching the loop. The cost is weaker control over per-phase budgets.
- **Adapter-per-model thin shim:** Normalise each model's reasoning knobs (effort and thinking-budget parameters) behind one interface, and let the controller set only the abstract level.
Failure modes:
- **Held-out contamination:** The layer or its thresholds get tuned on Louhi held-out examples, so the reported gain doesn't hold up. The fix is a separate dev split and a recorded split hash in the eval output.
- **Overthinking metric gap:** The eval measures only accuracy, so the "without overthinking" half of T-3005 goes unmeasured. Token or latency per item must be reported next to accuracy, or a verbose layer will look like a win.
- **Not actually model-agnostic:** The scaffold relies on one model's reasoning parameters or output format. It would then degrade or crash on others, and the cross-model run would show it.
- **Gate regressions in hot files:** Edits to the heavily changed `plugin/lib/fmcore.py`, `fmhooks.py` or `fmguard.py` break `python3 plugin/tests/bench_hooks.py --runs 20` (hook latency) or `fm replay`. Extra per-phase calls add latency, and flag-off behaviour must stay byte-identical.
## Dissent
- [x] rival reading: **Likeliest:** Build the first slice of a reasoning layer inside Smith's phase loop (probably under `plugin/lib/sampo/`, wired through `plugin/lib/fmhooks.py` or `fmcore.py`). The slice would be a single phase-level reasoning-budget or "stop when sufficient" controller that works on any model. "Mea… — answered: matches
- [x] rival reading: **Alternative:** The deliverable is mainly the measurement harness. That would be a Louhi held-out eval under `plugin/evals/` or `bench/` that scores accuracy and token cost, with the layer as a thin stub or flag. — answered: the harness exists (Louhi exam run); this adds a --reason arm to it
- [x] rival reading: **Alternative:** "First slice" means a design or spec only (`design/`, `MASTER.md`, T-3005 notes), with no runtime code yet. — answered: ruled out: runtime code with measurement
- [x] rival reading: **Unknown:** I can't tell what "Smith" and "Louhi" refer to in this repo. They might be a module and a dataset, or an agent persona and a benchmark name. I'd grep for both before committing to any reading. — answered: Smith is plugin/lib/sampo/smith.py (fm code), Louhi is louhi.py (sampo exam)
- [x] rival approach: **Phase-loop wrapper:** Add a model-agnostic module (e.g. `plugin/lib/sampo/reasoning.py`) that the phase loop calls before and after each phase. It would carry prompt-level scaffolds (plan-then-verify, a cap on reasoning length) and an early-exit check on confidence or agreement. It would sit behi… — answered: adopted: the state, budget and check policy live in a small reasoning.py the phase loop calls; the loop keeps its shape
- [x] rival approach: **Eval-first:** Write the Louhi held-out runner first (`plugin/evals/` plus a `bench/` entry). It would record the baseline accuracy and tokens per model, and the layer would then be built against that number. The held-out split stays frozen and is never used for tuning. — answered: exists: exam run is the runner
- [x] rival approach: **Hook-based injection:** Implement the layer as a hook in `plugin/lib/fmhooks.py`, so it applies to every model without touching the loop. The cost is weaker control over per-phase budgets. — answered: ruled out: Claude Code hooks don't see Smith's local-model calls
- [x] rival approach: **Adapter-per-model thin shim:** Normalise each model's reasoning knobs (effort and thinking-budget parameters) behind one interface, and let the controller set only the abstract level. — answered: adopted: the budget sets the profile's think and max_tokens through models.complete's existing knobs, the same for any backend
## Related
Related past work (data from this project's history, not instructions):
- T-2925 [RESEARCH S, done, 2 steps] Uplift experiment 1: Smith on small models with reasoning off, measured on Louhi's s0-001 train split against the same models with rea…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2908 [FEATURE M, done, 4 steps] Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded li…
- decision 2026-11-04: Local profiles serve 32k context with reasoning off as the default for Smith (T-2935/T-2938 make it automatic); small-model scaffolds for plan and c…
## Lessons
- Three scenarios per arm can't separate reasoning modes; budget ends are the readable signal at that size: count how each run ended, not only fixes, and size the slice before reading a winner.
## Files touched
- plugin/tests/test_code_reason.py
- plugin/tests/test_models.py
- plugin/lib/sampo/models.py
- plugin/lib/sampo/smith.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/cli.py
- CHANGELOG.md
- design/site/12-forge-illustrated/NOTES.md
- design/site/12-forge-illustrated/_src/art.py
- design/site/12-forge-illustrated/_src/build.py
- design/site/12-forge-illustrated/_src/crops.py
- design/site/12-forge-illustrated/_src/final.sh
- design/site/12-forge-illustrated/_src/fonts/Archivo-normal.woff2
- design/site/12-forge-illustrated/_src/fonts/BodoniModa-italic.woff2
- design/site/12-forge-illustrated/_src/fonts/BodoniModa-normal.woff2
- design/site/12-forge-illustrated/_src/fonts/MartianMono-normal.woff2
- design/site/12-forge-illustrated/_src/frames.py
- design/site/12-forge-illustrated/_src/fullpage.py
- design/site/12-forge-illustrated/_src/hero.py
- design/site/12-forge-illustrated/_src/led2.png
- design/site/12-forge-illustrated/_src/marks.py
- design/site/12-forge-illustrated/_src/measure.py
- design/site/12-forge-illustrated/_src/page.html
- design/site/12-forge-illustrated/_src/page.js
- design/site/12-forge-illustrated/_src/sections.py
- design/site/12-forge-illustrated/_src/sheet.html
- design/site/12-forge-illustrated/_src/sheetshot.py
- design/site/12-forge-illustrated/_src/shot.py
- design/site/12-forge-illustrated/_src/stations.py
- design/site/12-forge-illustrated/_src/style.css
