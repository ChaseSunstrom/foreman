# Uplift experiment 2: the scaffolds and the planner split (2026-11-04)

Louhi run s0-001, train split, the same 10 scenarios as experiment 1 (`sampo exam run s0-001 --agent smith --split train --limit 10 --model PROFILE [--planner PROFILE]`), Ollama on the RTX 5070 Ti, both profiles served 32k context with reasoning off. New since exp 1: the plan ladder (T-2936), the close-note slots (T-2937), prompt fitting (T-2939), the smith arm's findings (T-2931), `--planner` (T-2945).

| arm | fixed | closed | found | false alarms | ends |
|---|---|---|---|---|---|
| exp 1: gemma4:12b solo | 3/8 | 4 | (not asked) | – | finish refused 2, plan refused 2 |
| **exp 2: gemma4:12b solo** | **1/8** | **5** | 0/8 | 4 | closed 5, loop 4, other 1 |
| exp 1: qwen3.5:4b solo | 0/8 | 0 | (not asked) | – | loop 4, no plan 3 |
| **exp 2: qwen3.5:4b acting, gemma4:12b planning** | **1/8** | **2** | 1/8 | 1 | loop 4, plan refused 2, closed 2, other 2 |

Findings:
1. The close scaffold did its job: no run ended refused at finish (exp 1: 2), and gemma closed 5 of 10. But it fixed 1, not 3: 4 of its closes were false_done (a close the grade doesn't credit). With n = 8, 3 → 1 is inside the noise; the close slots make a model that thinks it is done able to close, so a close no longer means a fix.
2. The planner split lifted the 4B model from nothing to something: 0 → 1 fixed, 0 → 2 closed, and it named the 1 missing tool. Plans still get refused twice (plan_refused: the planner's plan failed Sampo's plan gaps), and the 4B actor still loops in 6 of 10 scenarios.
3. Loops are now the main end on both arms (4 of 10 each). The next lever is the act loop, not the plan: a loop detector that hands the step back to the planner, or a step budget per plan step.
4. The findings call works end to end but is noisy on gemma (4 false alarms, 0 found): its answer names files it touched, not the planted defect.

Next: a loop breaker in the act phase (hand a looping step to the planner once), rerun with 3 seeds per arm to get past n = 8 noise, and the held-out split.
