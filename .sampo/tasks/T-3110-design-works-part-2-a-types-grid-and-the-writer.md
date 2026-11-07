---
id: T-3110
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:08:02Z
updated: 2026-11-06T03:52:29Z
inferred_deps: [T-3104]
inferred_why: T-3104: named in its request
---
# Design works part 2: a types grid and the writer loop: best of N, critique of the render, revise, pairwise rank (T-3104)
## Raw request
> Design works part 2: a types grid and the writer loop: best of N, critique of the render, revise, pairwise rank (T-3104)
## Interpretation
Reading 1 (chosen): a works grid (type x subject x style x technique, styles drawn from the user's taste: crafted, detailed, lit, animated, never cartoonish) read thinnest first; per cell the strongest writer drafts N candidates, each is rendered and gated (part 1), a vision critique of its own render names concrete defects (advice only), the writer revises up to K rounds, and survivors are ranked pairwise; the best is kept with its render, rounds and gate numbers. Reading 2: one draft per cell; rejected, single drafts are uneven.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo works grow --grid works --target N fills thinnest cells with best-of-N, critique-and-revise rounds and a pairwise rank; each kept work records its writer, rounds, gate numbers and rank, and a cell whose candidates all fail keeps nothing — verify with `python3 plugin/tests/run.py test_design_works`
## Non-goals
## Approach (options → choice → why)
1. Reuse moons' grid-and-funnel shape and the cards' writer plumbing, with renders in the loop; likely outcome: kept works that pass gates after revision. 2. Do less: best of N without critique; fails if: fixable defects (a clipped wing, muddy contrast) are thrown away instead of fixed. 3. Critique by text only; fails if: the writer can't see what its SVG looks like. Choice 1 (75%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests with a fake writer and fake renders  <- CURRENT
2. [ ] the grid, the loop and the store
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:08:02Z created
- 2026-11-05T03:08:10Z set approved=True
- 2026-11-05T03:08:33Z blocked: approved; waits for a builder slot (lanes free as the merge queue lands)
- 2026-11-05T05:59:17Z steer: user 2026-11-05: 'I want opus to design the svg/art walk through cards and such, as it is the best model for UI and stuff, and you can use haiku for moon ideas and cards and whatever if the locals aren't cutting it' -> the design-works writer (drafts, revisions, pairwise rank) is Opus; local models join a type only after their measured lift clears the bar
- 2026-11-06T03:52:29Z unblocked
## Follow-ups captured
