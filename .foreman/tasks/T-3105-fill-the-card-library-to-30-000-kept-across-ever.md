---
id: T-3105
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:06:17Z
updated: 2026-11-06T03:53:07Z
inferred_deps: [T-3100, T-3103]
inferred_why: T-3100: named in its request; T-3103: fill across every grid needs the new domains
group: card library at scale
---
# Fill the card library to 30,000 kept across every grid, local writers first, the night growing it and the live page showing progress (T-3100 part 4)
## Raw request
> Fill the card library to 30,000 kept across every grid, local writers first, the night growing it and the live page showing progress (T-3100 part 4)
## Interpretation
Reading 1 (chosen): grow --grid all --keep 30000 fills thinnest cells across all grids with local writers (Jarvis 27B and 35B, gemma 12B on this GPU) first and Haiku only as a capped fallback; it waits and retries a busy local model (as T-3096 does for moons) and shares Jarvis fairly with the moons fill; the night grows while kept cards are under 30,000; the live page shows the fill's progress (T-3083 progress rows). Reading 2: Haiku writes them all; rejected, about 3,000 paid calls per 5,000 cards when local writers are free and the admission rules decide quality.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo playbooks small grow --grid all --keep N rounds until N cards are kept, local writers first, a busy local model waited on and retried, stopping after three rounds that keep nothing; Haiku is used only within the budget cap and never on a sensitive project — verify with `python3 plugin/tests/run.py test_small_cards`
- [ ] the night grows cards while kept cards are under 30,000 and a local writer answers; the live page shows the fill's kept count, rate and ETA — verify with `python3 plugin/tests/run.py test_night test_live`
- [ ] a live fill runs to at least 30,000 kept cards across at least 8 grids — verify with `python3 plugin/tests/run.py test_small_cards`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: grow's cell loop, admit, dedupe and the night job, with --keep like moons; likely outcome: the store climbs to 30,000 over nights without paid calls. 2. Do less: one long Haiku run; fails if: the budget caps stop it far short. 3. Pretrain a card writer first; fails if: training waits on thousands of kept cards it would need. Choice 1 (80%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: --keep rounds, local first, wait and retry, the stall stop, the night job, progress rows  <- CURRENT
2. [ ] grow --keep, the night job, progress rows
3. [ ] the live fill to 30,000 (runs over nights)
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:06:17Z created
- 2026-11-05T03:08:33Z blocked: approved; waits for a builder slot (lanes free as the merge queue lands)
- 2026-11-05T05:59:18Z steer: user 2026-11-05: 'I want opus to design the svg/art walk through cards and such, as it is the best model for UI and stuff, and you can use haiku for moon ideas and cards and whatever if the locals aren't cutting it' -> local writers first, Haiku as the fallback when they fall short
- 2026-11-06T03:53:07Z unblocked
## Follow-ups captured
