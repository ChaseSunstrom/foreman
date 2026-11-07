---
id: T-3112
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:08:04Z
updated: 2026-11-06T03:52:32Z
inferred_deps: [T-3104]
inferred_why: T-3104: named in its request
---
# Design works part 4: fill to 3,000 kept across 10+ types over nights; local models learn SVG techniques as cards and join when their measured lift clears the bar (T-3104)
## Raw request
> Design works part 4: fill to 3,000 kept across 10+ types over nights; local models learn SVG techniques as cards and join when their measured lift clears the bar (T-3104)
## Interpretation
Reading 1 (chosen): the night grows works while kept works are under 3,000, within the usage window; SVG technique cards (gradients and lighting, layering and depth, strokes and grids for icon sets, motion) are written into the card library's design grid, and a local model's drafts with those cards are measured against the gates and the user's picks; it writes a type only when it clears the bar there. Reading 2: the strongest writer for everything forever; rejected, the user wants local models scaffolded to frontier results.
## Assumptions (confidence)
## Acceptance criteria
- [ ] at least 3,000 works are kept across at least 10 types; the night job grows them while under target; a local model writes a type only after its gate-pass rate and pick rate there clear the strongest writer's by the recorded bar — verify with `python3 plugin/tests/run.py test_design_works test_night`
## Non-goals
## Approach (options → choice → why)
1. The night job plus a measured local arm per type; likely outcome: thousands kept, and local models taking the types they can. 2. Do less: a one-off long run; fails if: it stops at the budget and never compounds. 3. Train a local SVG model first; fails if: training needs the kept works this fill produces. Choice 1 (75%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: night job, local arm gating  <- CURRENT
2. [ ] the night job, technique cards, the local arm
3. [ ] the live fill to 3,000 (runs over nights)
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:08:04Z created
- 2026-11-05T03:08:10Z set approved=True
- 2026-11-05T03:08:34Z blocked: approved; waits for a builder slot (lanes free as the merge queue lands)
- 2026-11-05T05:59:18Z steer: user 2026-11-05: 'I want opus to design the svg/art walk through cards and such, as it is the best model for UI and stuff, and you can use haiku for moon ideas and cards and whatever if the locals aren't cutting it' -> the design-works writer (drafts, revisions, pairwise rank) is Opus; local models join a type only after their measured lift clears the bar
- 2026-11-06T03:52:32Z unblocked
## Follow-ups captured
