---
id: T-3312
type: FEATURE
tier: L
status: planned
priority: normal
scope: []
depends_on: [T-3265, T-3249, T-3282]
source: user
created: 2026-11-06T04:11:12Z
updated: 2026-11-06T04:25:27Z
---
# Kalevala at any depth: sampo kalevala start --depth N stacks N levels of genesis, each level choosing among setups of the level below by their measured results
## Raw request
> Kalevala at any depth: sampo kalevala start --depth N stacks N levels of genesis, each level choosing among setups of the level below by their measured results
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] depth 1 is Rune (one genesis), depth 2 is today's Kalevala (towers chosen by their exams), depth N adds a level whose units are whole level-(N-1) setups; one generic level type, no per-depth code — verify with `python3 plugin/tests/run.py test_kalevala`
- [ ] a level only selects when the level below has graded results with enough samples to tell setups apart (the exam-signal floor from T-3282); below the floor it reports 'not enough signal' instead of choosing — verify with `python3 plugin/tests/run.py test_kalevala`
- [ ] each level gets a budget share and a wall-clock cap; the live Rune page shows the stack (T-3266's city view, one ring per level) — verify with `python3 plugin/tests/run.py test_kalevala test_site`
- [ ] every depth does all its work, fast and cheap per result, not by being capped: no level reruns a graded setup (one shared cache of results keyed by setup and scenario, reused by every level above), candidates are screened by local GPU models and exam subsets and only the promising few get full runs and Claude sessions (successive halving), upper levels act on lower results as they land rather than waiting for whole rounds, and idle local capacity is used first; a depth-4 dry run reports projected Claude spend, local GPU hours and wall time per level, and the Claude spend per kept improvement falls level over level — verify with `python3 plugin/tests/run.py test_kalevala`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] generic level: units, select, budget, cap  <- CURRENT
2. [ ] signal floor gate from T-3282
3. [ ] depth flag and status; page view
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:11:12Z created
- 2026-11-06T04:11:18Z set depends_on=['T-3265', 'T-3249', 'T-3282']
- 2026-11-06T04:24:25Z steer: the user: 'kalevala of kalevala' means another layer on top of Kalevala the way Kalevala sits on genesis, and each depth is one of those on the one below; it must be fast, efficient and still ambitious, or it takes forever and costs a fortune. So: total cost bounded whatever the depth (a geometric budget, each level a fraction of the one below), upper levels tick slower, reuse every lower result from a shared cache keyed by setup and scenario instead of rerunning, screen many candidates cheaply (local models, exam subsets, short horizons) and promote few to full runs (successive halving), Claude only for promoted candidates
- 2026-11-06T04:25:27Z criterion 4 text: cost and time stay bounded whatever the depth: level k's budget is a fixed fraction of level k-1's (total under 2x depth-2's), level k ticks once per several level-(k-1) rounds, every lower-level result is reused from a cache keyed by setup and scenario (no level reruns a graded setup), and candidates are screened cheaply (local models, exam subsets) before a few are promoted to full runs; a depth-4 dry run reports its projected cost and hours within that bound → every depth does all its work, fast and cheap per result, not by being capped: no level reruns a graded setup (one shared cache of results keyed by setup and scenario, reused by every level above), candidates are screened by local GPU models and exam subsets and only the promising few get full runs and Claude sessions (successive halving), upper levels act on lower results as they land rather than waiting for whole rounds, and idle local capacity is used first; a depth-4 dry run reports projected Claude spend, local GPU hours and wall time per level, and the Claude spend per kept improvement falls level over level
- 2026-11-06T04:25:27Z steer: the user: 'I don't want to just cap the cost of things to prevent the work from getting done, I want it to still get done without burning a fuck ton of money, and quick'. Budgets are a backstop, never the method: efficiency comes from reuse, cheap screening and local models, and the work still completes
## Follow-ups captured
