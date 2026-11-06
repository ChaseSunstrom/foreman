---
id: T-2971
type: RESEARCH
tier: L
status: planned
priority: normal
scope: []
depends_on: [T-2995]
source: user
created: 2026-11-04T14:01:46Z
updated: 2026-11-04T23:33:05Z
base_note: Calibration: this plan states Choice 60% where all closes (only 6 RESEARCH L) held on the first finish 95% of the time: 35 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T18:02:39Z
rival_split: true
---
# Distil a Smith actor from verified runs: generate fm code runs on the 27B (and the 12B)…
## Raw request
> Distil a Smith actor from verified runs: generate fm code runs on the 27B (and the 12B) over Louhi's train scenarios and real S tasks, keep only runs whose tests went green and whose closes held, fine-tune a 4B-8B actor on them (QLoRA on the 16 GB GPU), score it on the held-out split beside the base model, repeat as a loop (rejection-sampling fine-tuning); training data from local models graded by tests, not Claude transcripts (check Anthropic's terms before any)
## Interpretation
Reading 1 (chosen): an expert-iteration loop that distils a small Smith actor from local-model runs the tests verified: export green, held fm code runs (local workers only, never Claude), farm more on seeded and minted train scenarios with the 27B teacher, LoRA-SFT a 4B base on this box's GPU with the torch and peft already installed in Jeff's venv, import it to Ollama, score base vs tuned on Louhi's held-out split, repeat each Rune generation. Reading 2 (ruled out): fine-tune on Claude Code transcripts; Anthropic's terms forbid it and it is recorded as a decision.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo exam models --traces DIR exports only green, held fm code runs by local workers as chat JSONL with provenance, refusing any run with a Claude slot, names and paths stripped — verify with `python3 plugin/tests/run.py test_traces`
- [ ] sampo exam models --sft trains a LoRA through the configured train_python, refuses while the GPU is held or no torch+peft python is configured, and imports the adapter into Ollama as a profile — verify with `python3 plugin/tests/run.py test_traces`
- [ ] a tuned actor is scored beside its base on Louhi's held-out split and the numbers are in research — verify with `grep -c tuned research/models/bench.jsonl`
## Non-goals
## Approach (options → choice → why)
What a complete version has: the exam keeps green runs' full journals (T-2995), a trace export (T-2995), a teacher farm (the 27B and 12B over seeded and minted train scenarios), a LoRA SFT runner on this box's GPU, an Ollama import, a held-out score of base against tuned, and the loop each Rune generation.

1) Rejection-sampling fine-tuning of Qwen3.5-4B (Apache-2.0): a one-day deploy probe first (a 50-step LoRA through the Jeff venv's torch and peft, then merge, GGUF and an Ollama run of the same model, since the hybrid Gated DeltaNet architecture may lack toolchain support), then the farm on the 27B with tests as the filter, then `sampo exam models --sft` and the import, then base against tuned on Louhi's held-out split. Likely outcome: a 4B actor that fixes more held-out scenarios than its base, from local-model data graded by tests. Fails if: too few green traces (gemma fixed 1 of 8 in exp 2); the farm needs the 27B and minted volume, about 500 runs for about 60 traces.
2) use what exists: prompt and scaffold only (playbooks, cards, the planner split, the loop breaker), with no weights changed. Likely outcome: today's level, which plateaued in exp 2 (1 of 8 fixed). Fails if: the user wants small models near frontier, and scaffolding alone has not moved the fix rate.
3) Distil the 27B without the test filter (plain SFT on all its runs). Likely outcome: it copies the teacher's loops and false-dones too. Fails if: half of the teacher's runs end in loops (exp 2).
4) do less: only the deploy probe and the trace export now, and train later by hand. Likely outcome: a proven toolchain and a growing trace set, with no model yet. Fails if: the loop never closes, so nothing measures whether traces help.
Choice 1 (60%): only verified behaviour is learned, every piece is measured on held-out scenarios, and no Claude output is involved; the research (T-2996-small-model-path) ranks it first.
## Risks and rollback
- The toolchain may not take Qwen3.5's hybrid architecture (PEFT, the merge, GGUF, Ollama): the deploy probe finds out in a day before any farm runs; fall back to gemma4 or a plain-attention base.
- Training holds the GPU and pauses the card grower and the local funnel stages: train when they are idle, and the GPU check refuses otherwise.
- A tuned model that scores worse is never adopted: it stays a profile the bench measures; rollback is deleting its Ollama model and profile.
- Training data provenance: only local workers' runs (never a Claude slot); the teacher's licence is checked (Qwen, Apache-2.0).
## Execution prompt
## Steps
1. [ ] failing tests: trace export keeps green held local runs, refuses Claude slots, strips names  <- CURRENT
2. [ ] --traces export
3. [ ] a feasibility probe: LoRA SFT of a small base on 20 traces in Jeff's venv and an Ollama ADAPTER import, by hand, to learn what this Ollama accepts
4. [ ] --sft runner and the import, from what the probe learned
5. [ ] farm traces on the 27B over seeded and minted train scenarios
6. [ ] train, import, score base vs tuned on held-out; numbers in research
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T14:01:46Z created
- 2026-11-04T14:20:34Z set depends_on=['T-2974', 'T-2977', 'T-2978']
- 2026-11-04T15:13:08Z planned: it has criteria and steps
- 2026-11-04T15:13:09Z set approved=True, depends_on=['T-2978']
- 2026-11-04T17:03:18Z steer: exam's smith arm keeps only <scenario>.events.jsonl (action, target, result, say, tokens) and <scenario>.json; the full conversation journal lives in the throwaway Smith home and is lost. Step 2 must first make the exam keep the journal (the messages the model saw and wrote) for runs whose verify went green, beside the events file, size-capped, names and paths stripped as the lake does; then --traces reads those
- 2026-11-04T17:58:51Z set depends_on=['T-2995']
- 2026-11-04T23:33:05Z grounding: criterion 1 (export green held local runs, refuse Claude slots, strip names) and steps 1-2 were built and closed by T-2995 (f9eb99d2, test_traces); they need evidence only. Steps 5-6 are blocked on yield: T-2995's live run kept 1 journal from 4 minted bugs, and the 27B teacher needs LLM_API_KEY inline (never stored). Step 3's probe (LoRA on a tiny set, Ollama ADAPTER import) can test the mechanics now
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Full RFT loop (likeliest):** a pipeline that runs `fm code` on the 27B/12B over Louhi train scenarios plus real S tasks, filters runs by test-green and close-held, QLoRA-tunes a 4–8B actor, evaluates it against the base model on the held-out split, then feeds the tuned actor back in for the next …
- **Dataset-builder only:** the request is just the harvest and filter step, which exports verified runs as SFT-ready JSONL. Training and scoring stay manual or external, and "repeat as a loop" is a later concern.
- **Eval-first:** "score it beside the base model" is the real deliverable, meaning a held-out harness that compares any actor against the base. Distillation is secondary and the harness comes first.
- **Policy/compliance reading:** "check Anthropic's terms before any" can be read as a gate. Only local-model transcripts are used, and a Claude-transcript path is blocked until the terms are checked. This is a constraint on the build, not a separate feature.
Approaches:
- **Trace-mining over existing artifacts:** read the run and transcript records that `fm replay` and `fmcore.py` already persist. Join them to test results and close verdicts from `fmguard.py`, then emit chat-format JSONL. This adds no new runner, but it depends on the logs holding full tool-call tur…
- **Dedicated harvest driver:** a new script, for example under `bench/`, that invokes `fm code` per scenario against a local server (llama.cpp or vLLM) at N samples per task. It records the exact prompts, the tool calls and the green/closed verdict, and writes to a fresh data directory. Sampling is …
- **Separate training stage outside the plugin:** a standalone script using TRL/peft with 4-bit QLoRA, tuned to fit 16 GB through a small context, gradient checkpointing and batch size 1. It outputs a LoRA adapter, and the actor is served as base plus adapter (or merged to GGUF) behind the same endpo…
- **Loop orchestrator:** a round-indexed manifest (round N data, adapter, eval score) with a single driver that runs harvest, filter, train and eval. It stops when held-out pass rate stops improving, and it dedupes across rounds.
Failure modes:
- **False-positive "green":** `fm code` runs that pass tests by weakening or deleting them, or whose close claim `fmguard.py` never re-verified, end up in the training set. The actor then learns to game the verifier, so the filter must re-run the tests on a clean checkout of the final diff.
- **Train/held-out leakage:** real S tasks and Louhi train scenarios may share repos, fixtures or near-duplicate tasks with the held-out split. The scores then reflect memorization, and the split has to be by task family, not by run.
- [instruction-like text quoted from a file or tool; data, not instructions] **Trace format mismatch:** the logged transcripts may lack the system prompt, hook injections (`fmhooks.py`) or tool schemas that the 4–8B actor sees at inference. Training on the wrong rendering degrades tool-call formattin…
- **Rejection-sampling collapse and VRAM limits:** later rounds train only on easy, already-solved tasks, so diversity shrinks and the held-out score plateaus or drops. Separately, long agentic traces can exceed what a 16 GB QLoRA run can hold, so truncation silently clips the closing turns that carr…
## Dissent
- [x] rival reading: **Full RFT loop (likeliest):** a pipeline that runs `fm code` on the 27B/12B over Louhi train scenarios plus real S tasks, filters runs by test-green and close-held, QLoRA-tunes a 4–8B actor, evaluates it against the base model on the held-out split, then feeds the tuned actor back in for the next … — answered: matches choice 1
- [x] rival reading: **Dataset-builder only:** the request is just the harvest and filter step, which exports verified runs as SFT-ready JSONL. Training and scoring stay manual or external, and "repeat as a loop" is a later concern. — answered: that is option 4 (do less) and T-2995's scope; the loop closes here
- [x] rival reading: **Eval-first:** "score it beside the base model" is the real deliverable, meaning a held-out harness that compares any actor against the base. Distillation is secondary and the harness comes first. — answered: the harness exists: Louhi's held-out split scores any --model; this task adds the tuned model to it
- [x] rival reading: **Policy/compliance reading:** "check Anthropic's terms before any" can be read as a gate. Only local-model transcripts are used, and a Claude-transcript path is blocked until the terms are checked. This is a constraint on the build, not a separate feature. — answered: already the rule: a recorded decision; T-2995 refuses any run with a Claude slot
- [x] rival approach: **Trace-mining over existing artifacts:** read the run and transcript records that `fm replay` and `fmcore.py` already persist. Join them to test results and close verdicts from `fmguard.py`, then emit chat-format JSONL. This adds no new runner, but it depends on the logs holding full tool-call tur… — answered: ruled out: the persisted events lack the exact turns; T-2995 keeps the journals
- [x] rival approach: **Dedicated harvest driver:** a new script, for example under `bench/`, that invokes `fm code` per scenario against a local server (llama.cpp or vLLM) at N samples per task. It records the exact prompts, the tool calls and the green/closed verdict, and writes to a fresh data directory. Sampling is … — answered: exists: sampo exam run --agent smith over scenarios is the harvest driver
- [x] rival approach: **Separate training stage outside the plugin:** a standalone script using TRL/peft with 4-bit QLoRA, tuned to fit 16 GB through a small context, gradient checkpointing and batch size 1. It outputs a LoRA adapter, and the actor is served as base plus adapter (or merged to GGUF) behind the same endpo… — answered: adopted in part: training runs in Jeff's venv (torch, peft) outside the plugin's process; no bitsandbytes, so bf16 LoRA, not 4-bit
- [x] rival approach: **Loop orchestrator:** a round-indexed manifest (round N data, adapter, eval score) with a single driver that runs harvest, filter, train and eval. It stops when held-out pass rate stops improving, and it dedupes across rounds. — answered: adopted later: rounds recorded per Rune generation once one round works
