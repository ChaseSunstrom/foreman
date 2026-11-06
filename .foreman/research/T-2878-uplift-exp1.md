# Uplift experiment 1: what it takes for a small local model to drive Sampo's loop (2026-11-04)

Louhi run s0-001, train split, the same 10 scenarios each time, `sampo exam run s0-001 --agent smith --model PROFILE`,
Ollama 0.40.11 on an RTX 5070 Ti. "fixed" is graded from the tree Smith leaves (the smith arm writes no findings yet,
T-2931, so "found" is always 0).

| profile | reasoning | context served | fixed | closed with a commit | main ends |
|---|---|---|---|---|---|
| gpu-qwen4 (qwen3.5:4b) | on (default) | 4096 (Ollama default) | 0/8 | 0 | reasoning ate the 8192-token budget (6), timeouts (2) |
| gpu-qwen4-nothink | off, but not reaching Ollama | 4096 | 1/8 | 0 | budget (4), no valid plan (6) |
| gpu-gemma12-nothink (gemma4:12b) | off, not reaching Ollama | 4096 | 0/8 | 2 | budget (2), prompt truncated at 564 tokens, closes refused |
| gpu-qwen4-32k | off (T-2928: reasoning_effort none) | 32768 | 0/8 | 0 | 40-turn loops (4), no valid plan (3), plan gaps |
| **gpu-gemma12-32k** | **off** | **32768** | **3/8** | **4** | finish refused for missing numbers (2), plan refused for an unchecked request clause (2) |

Findings:
1. Ollama ignores chat_template_kwargs and think on its OpenAI API; only reasoning_effort none turns reasoning off
   (fixed in T-2928).
2. Ollama serves every model at 4096 tokens by default while Smith's prompts run 17k to 44k tokens; a num_ctx 32768
   variant (ollama create, no root) is the single largest lever. T-2935, T-2938 and T-2939 make Sampo handle it.
3. With both levers, gemma4:12b goes from 0 to 3 of 8 fixed and closes 4 scenarios with commits. Its remaining ends are
   Sampo's own bars: a perf close needs --numbers, and T-2914's new plan gap refuses a plan with an unchecked request
   clause. The scaffolds T-2936 (plan) and T-2937 (close) target these.
4. qwen3.5:4b is too weak for M plans even with both levers: it loops or never produces readings and options. Below
   about 9B, a different strategy (plan by the bigger model, act by the small one) is the next experiment.

Next run: the same scenarios after T-2936 and T-2937, then the held-out split, beside the agent arm's score.
