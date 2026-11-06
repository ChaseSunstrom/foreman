---
id: T-3103
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:05:54Z
updated: 2026-11-06T03:53:31Z
inferred_deps: [T-3100]
inferred_why: T-3100: named in its request
group: card library at scale
---
# Card grids as data, with new domains: more languages, ops and infra, data and ML, security, writing and research, design, product and planning, and Sampo's own skills (T-3100 part 3)
## Raw request
> Card grids as data, with new domains: more languages, ops and infra, data and ML, security, writing and research, design, product and planning, and Sampo's own skills (T-3100 part 3)
## Interpretation
Reading 1 (chosen): grids move from constants in smallcards.py into one data file (name, its fields and their values, a target), the general and UI grids unchanged in it (same cell keys, so no card moves); new grids for the domains the user named as 'all sorts of things', each 1,000 to 4,000 cells; a grid's thinnest cells are read first, and new values come from data (coverage misses, the user's requests and steers, repeated friction), proposed and recorded, never silently added. Reading 2: widen the general grid's tuples in code; rejected, every new domain would be a code change and the general grid's cells would shift.
## Assumptions (confidence)
## Acceptance criteria
- [ ] grids load from one data file; the general and UI grids give the same cells and counts as before; a malformed grid entry is refused naming the file and field — verify with `python3 plugin/tests/run.py test_small_cards`
- [ ] at least 8 grids exist, the new ones covering more languages, ops and infra, data and ML, security, writing and research, design, product and planning, and Sampo's own problem solving, memory and efficiency; sampo playbooks small coverage shows each — verify with `python3 plugin/tests/run.py test_small_cards`
- [ ] sampo playbooks small grids propose lists new cell values read from coverage misses, the user's requests and friction, each with its source; adding one is recorded — verify with `python3 plugin/tests/run.py test_small_cards`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: _grid, _key, admit and the coverage reader, generalised to read grid definitions from data; likely outcome: adding a domain is a data edit and grow --grid all spreads across every grid. 2. Do less: add one more hardcoded grid; fails if: tens of thousands on all sorts of things needs eight or more. 3. Free-form topics with no grid; fails if: coverage, dedupe and thinnest-first all need cells. Choice 1 (80%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: the data file loads, today's two grids unchanged, a bad entry refused, grow --grid all reads thinnest first across grids, propose cites sources  <- CURRENT
2. [ ] the grid file and loader, the new grids, coverage per grid, propose
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:05:54Z created
- 2026-11-05T03:06:17Z set approved=True
- 2026-11-05T03:08:32Z blocked: approved; waits for a builder slot (lanes free as the merge queue lands)
- 2026-11-06T03:53:31Z unblocked
## Follow-ups captured
