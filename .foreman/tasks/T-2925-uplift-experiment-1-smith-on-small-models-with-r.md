---
id: T-2925
type: RESEARCH
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T07:47:46Z
updated: 2026-11-04T09:03:11Z
base: 044e0c58dd6a617a74eb7dd27a75a68caf2c9899
base_tree: d4d5851c8d7f48faf47ea50260933639e83fb567
plan0_at: 2026-11-04T07:47:47Z
plan0_scope: []
verified: ok
unproven: [research-uncited, typed]
---
# Uplift experiment 1: Smith on small models with reasoning off, measured on Louhi's s0-001 train split against the same models with reasoning on (6 of 10 qwen3.5:4b scenarios died with reasoning eating its 8192-token budget)
## Raw request
> Uplift experiment 1: Smith on small models with reasoning off, measured on Louhi's s0-001 train split against the same models with reasoning on (6 of 10 qwen3.5:4b scenarios died with reasoning eating its 8192-token budget)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the reasoning-off runs are graded and their taxonomy filed beside the reasoning-on run — verify with `sampo research show T-2878-uplift-exp1`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] nothink profiles; run, grade, taxonomy
2. [x] file the comparison
## Resume here
## Docs impact
## Verification evidence
- (step 1) `five exam runs on s0-001 train (qwen4 and gemma12; reasoning on/off; 4096 vs 32768 context)` → gemma4:12b with 32k context and reasoning off: 3/8 fixed, 4 closed with commits; every earlier variant 0-1/8 [tree 50be6491b62b] (2026-11-04T09:03:02Z)
- (step 2) `sampo research show T-2878-uplift-exp1` → exit 0 · about 9B, a different strategy (plan by the bigger model, act by the small one) is the next experiment. / Next run: the same scenarios after T-2936 and T-2937, then the held-out split, beside the agen [ran] [tree 50be6491b62b] [world 2f1906870a] (2026-11-04T09:03:02Z)
- (ac 1) `sampo research show T-2878-uplift-exp1` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T09:03:02Z [ran] [tree 50be6491b62b] [world 2f1906870a] (2026-11-04T09:03:03Z)
- (audit intent) `five live exam runs on the same ten train scenarios, graded; filed as research T-2878-uplift-exp1` → measured what lifts a small local model on Sampo's real scenarios: 32k context plus reasoning off takes gemma4:12b from 0 to 3 of 8 fixed [tree 50be6491b62b] (2026-11-04T09:03:03Z)
- (audit edge) `five live exam runs on the same ten train scenarios, graded; filed as research T-2878-uplift-exp1` → train split only (the held-out split stays clean); 'found' is unscored for the smith arm (T-2931); ten scenarios is a small sample [tree 50be6491b62b] (2026-11-04T09:03:03Z)
- (audit self) `five live exam runs on the same ten train scenarios, graded; filed as research T-2878-uplift-exp1` → no findings [tree 50be6491b62b] (2026-11-04T09:03:03Z)
- (audit intent) `five live exam runs on the same ten train scenarios, graded; filed as research T-2878-uplift-exp1` → measured what lifts a small local model on Sampo's real scenarios: 32k context plus reasoning off takes gemma4:12b from 0 to 3 of 8 fixed [tree 50be6491b62b] (2026-11-04T09:03:10Z)
- (audit edge) `five live exam runs on the same ten train scenarios, graded; filed as research T-2878-uplift-exp1` → train split only (the held-out split stays clean); 'found' is unscored for the smith arm (T-2931); ten scenarios is a small sample [tree 50be6491b62b] (2026-11-04T09:03:10Z)
- (audit self) `five live exam runs on the same ten train scenarios, graded; filed as research T-2878-uplift-exp1` → no findings [tree 50be6491b62b] (2026-11-04T09:03:10Z)
## Log
- 2026-11-04T07:47:46Z created
- 2026-11-04T07:47:47Z focused
- 2026-11-04T07:48:02Z paused: focus moved to T-2908
- 2026-11-04T08:22:44Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T08:22:44Z focused
- 2026-11-04T08:40:36Z focused
- 2026-11-04T08:49:42Z paused: focus moved to T-2940
- 2026-11-04T09:03:01Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T09:03:01Z focused
- 2026-11-04T09:03:11Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2878-smithbench-gpu: `fm code bench --model PROFILE --seed-timeout 600` on an RTX 5070 Ti (16 GB) through Ollama 0.40.11, one model at a time,
- T-2908 [FEATURE M, planned, 4 steps] Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded…
- T-2878 [FEATURE L, planned, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- decision 2026-11-02: [costly] The steer expander keeps one Rule section; the Rule/Proposals split (T-2632) is reverted
## Decision
Local profiles serve 32k context with reasoning off as the default for Smith (T-2935/T-2938 make it automatic); small-model scaffolds for plan and close (T-2936, T-2937) come next; below ~9B, plan with the bigger model and act with the small one (next experiment). Evidence: research T-2878-uplift-exp1.
## Lessons
- measure the serving setup before the model: the default context and an ignored reasoning switch hid what the model could do
## Files touched
- models.json
