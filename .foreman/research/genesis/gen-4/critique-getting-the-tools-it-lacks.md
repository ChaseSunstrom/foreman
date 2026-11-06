# Critique — Mission 7, getting the tools it lacks (gen 4, #5)

Tasks: T-2917 (done, merged 2026-11-04 08:38Z). T-2932 (captured, the live batch and bench rows; depends on T-2949). T-2949 (captured, a FIX for the audit's findings). T-2878 step 4 (planned). Mission: gen-4/mission-getting-the-tools-it-lacks.md.

## Closed vs planned
- Brief 1 (T-2917) is closed as code. `sampo playbooks eval NAME --real --model PROFILE` answers each brief through an own or loopback profile, never `claude -p`, and books the profile in playbook-evals.jsonl. `sampo playbooks small NAME --model PROFILE` drafts a variant on the local writer and drafts held-out briefs from the original when it has none. It keeps the variant only when its lift is at least the original's. `playbooks show NAME --model PROFILE` serves the kept variant, the coverage line counts variants, and Smith's phase prompt for a local profile carries the variant routed for the task's type, cut to the profile's context. It reuses `sampo.smallcards` (T-2909) and the existing eval. No second store.
- Criteria 1 to 3 and 5 are ticked on tests (test_playbook_evals, test_code). Two live criteria were cut away at 08:23Z and moved to T-2932: criterion 4 (a first batch on the 27B and one small GPU model, with a lift table) and the bench rows for `sampo code bench` with and without a variant. The reason in the log: the endpoint grows moons and the GPU runs the exam. T-2932 is captured and now depends on T-2949.
- Review found a real defect and the task did not fix it. T-2949 says `smallcards._variant_prompt` hands the writer the exact "has" phrases the eval briefs check, then scores the variant on those briefs. A variant can pass by containing the phrases. The task's own lesson says "never score a generated artefact on checks its writer was shown: hold the eval briefs out of the writer's prompt". The lesson exists and the code in the merge still breaks it, so the keep rule is partly circular. The Mission's Risks section promised "briefs drafted from the original before the variant, held by a test". The order is held; the leakage of check phrases is not.

## Measures (first readings and due dates)
- Lift table per playbook and profile (kept, refused, mean lift gained). First reading: none. `state/playbook-evals.jsonl` still has 2 rows, both from 2026-10-22 on the scripted "literal" model. There is no research note small-playbooks. Not one real model has been measured against one playbook. Due: T-2932, after T-2949; no date set.
- Corpus size. Zero kept variants on this machine, as far as the ledger and eval file show. The user's standing ask is "thousands of skills and playbooks written for smaller models". The tooling for that now exists and the count is 0.
- Smith bench with and without a variant. First reading: none. `state/code-bench.jsonl` has 13 rows; none is a with-variant row.
- Taxonomy, from the same T-2878 work, since small models are the target. On 15 local runs, 40% ended out of steps, 20% had a plan refused by the plan gate (T-3016 now returns the refusal to the planner once; T-3016 is planned, not merged), 7% hit the reasoning budget, 7% timed out. `sampo exam taxonomy s5-019` for gemma 12B reads one scenario ending on budget. T-3006's reasoning arms on s5-019 with gemma 12B read off 0/3 fixed, state 1/3 fixed. That is a smoke signal, n of 3. The 27B arms need an API key this session does not store. These say where small models fail: running out of steps and plan refusal, not following a playbook's wording. A variant that lifts brief-following will not touch the top failure.
- Friction lead from the Mission: sessions reached for `fm models`, `fm andon` and `fm shot` by name. No alias or capture is recorded as made; I did not check further.

## What failed
- The Mission is the one most about measured help, and its measured part is the part that did not run. The tool for lift exists; no lift exists.
- The keep rule is circular as merged (T-2949). Until it is fixed, any batch run would produce lifts that overstate the variants. Running T-2932 first would waste the endpoint's slot.
- The grounding said small models "can do the work" (4B and e4b closed 4 of 5 seeds; the 27B closed 1 of 5, its misses endpoint errors). That is a seed count of 5, a smoke signal, and the Mission built on it as fact.
- Nothing in this Mission finds or installs a plugin or server. The capability name is "getting the tools it lacks", and the brief narrowed it to one tool, small-model instructions. That was a fair cut. But gen-0 #5's other half (find, build, test and use a tool; queue install grants) has no brief at all in gen-4.

## What the next Seed should change
- Run T-2949 before T-2932, in that order, and put the order in T-2932's criteria. Score variants on briefs the writer never saw.
- Pick the playbooks by the failure taxonomy. Cards for "stay within the step budget" and "revise the plan after a refusal" go first. The 40% and 20% buckets are where a card could change a close.
- Set a date for the first lift table and run it on a free slot, with the GPU profile as the one that is free by default.
- Add the second half of #5 as its own brief: an unknown verb a session reaches twice becomes an alias or a capture (`sampo friction` already has the data), with a count of how many it made.
