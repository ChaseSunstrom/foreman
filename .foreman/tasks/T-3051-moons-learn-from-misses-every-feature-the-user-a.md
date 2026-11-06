---
id: T-3051
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/moonscale.py, plugin/tests/test_moons_scale.py]
depends_on: []
source: user
created: 2026-11-05T00:18:06Z
updated: 2026-11-06T03:52:37Z
inferred_deps: [T-3050]
inferred_why: T-3050: named in its request
group: 10000 moons target
---
# Moons learn from misses: every feature the user asks for that no moon predicted…
## Raw request
> Moons learn from misses: every feature the user asks for that no moon predicted (T-3050's Kalevala, an orchestrator of towers; T-3034's network view; T-3044's progress view) becomes a blind-spot question in the generator's prompt and a Sampo-grid cell, and a miss count is tracked per generation (the user: 'how come ideas like that were never come up with during the moons? for features/capabilities?'). Root causes found: the generator prompt says payoffs never land 'on the harness's own parts', the write rule rejects payoffs naming tower/generation/harness/sampo, the grid has no Sampo-architecture cells, and the one-day kill judge killed 70 of 127 orchestration-like moons as 'needs a tool nobody has built'
## Interpretation
Reading 1 (taken): moons learn from their misses: every feature the user asks for that no moon predicted becomes data for the generator: a blind-spot question in the prompts of the cells it belongs to, a new Sampo-grid cell when it names an area the grid lacks, and a miss count per generation (moons that predicted a later user ask / user asks no moon predicted). Reading 2 (ruled out): a hand-written list of the missed ideas added to the prompt: the user's rule is to learn gaps from data, never hardcoded lists.
## Assumptions (confidence)
## Acceptance criteria
- [ ] Every user feature ask since the moons began is matched against the kept moons; asks no moon predicted are listed as misses with the nearest moon and its similarity — verify with `python3 plugin/tests/run.py test_moons_scale`
- [ ] Each miss becomes a blind-spot question in the prompts of the cells it belongs to, and a new Sampo-grid area when its subject has none — verify with `python3 plugin/tests/run.py test_moons_scale`
- [ ] A miss rate per generation (asks predicted by a kept moon / all asks) is shown in sampo genesis moonshot --status and recorded each generation — verify with `python3 plugin/tests/run.py test_moons_scale`
- [ ] The known misses are caught: T-3050's Kalevala (an orchestrator of towers), T-3034's network view and T-3044's progress view each show as a miss with its nearest moon, or as predicted with the moon that predicted it — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
1) use what exists: the user's FEATURE requests are in the ledger (source user, type FEATURE); match each against the kept moons with the embed or shingle similarity moonscale already has; an ask with no kept moon above BAR['novel'] is a miss; misses feed _hints per cell and, through their nouns, new Sampo-grid areas: likely outcome: the generator sees what it missed, measured each generation. 2) the brainstorm's blind-spots lens alone: fails if: moons never read it. 3) a model judge deciding misses: fails if: costly and unverifiable; similarity first, a judge only for borderline pairs. 4) do less: count misses only: fails if: nothing changes the generator. Choice 1 (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] match asks to kept moons, list misses (tests first)  <- CURRENT
2. [ ] misses into prompts and grid areas (tests first)
3. [ ] the miss rate per generation (tests first)
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T00:18:06Z created
- 2026-11-05T00:39:38Z set depends_on=['T-3045'], scope=['plugin/lib/sampo/moonscale.py', 'plugin/tests/test_moons_scale.py']
- 2026-11-05T00:39:40Z planned: it has criteria and steps
- 2026-11-05T00:39:40Z set approved=True
- 2026-11-05T02:03:02Z set depends_on=[]
- 2026-11-05T02:03:12Z blocked: planned and briefable; waits for a builder slot (6 of 6 out: T-3055, T-3083, T-3093 and the cli guards' one branch counted as T-3087, T-3088, T-3089) until the merge chain lands them
- 2026-11-06T03:52:37Z unblocked
## Follow-ups captured
