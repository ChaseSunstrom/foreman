---
id: T-0219
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:57:26Z
updated: 2026-10-04T04:59:44Z
base: 64b3600c03a657a0b680b2d649928f52a319a525
base_tree: b0c22b6f06082a803dde8057db824b4168ff74cc
verified: strong
---
# Super-brainstorm round 2: bold ideas past everything built, now measurable with fm bench
## Raw request
> Super-brainstorm round 2: bold ideas past everything built, now measurable with fm bench
## Interpretation
The user asked for recursive super-improvement with groundbreaking ideas, not small fixes. Round 1 shipped. Brainstorm again past every earlier idea, aimed at bold capabilities that fm bench can now measure.
## Assumptions (confidence)
## Acceptance criteria
- [x] round-2 ideas grounded, recorded, and the surviving slate queued (or the round recorded as dry) — verify with `ls state/projects/foreman-4a056f/research/ | grep -c round7`
## Non-goals
## Approach (options → choice → why)
A) default six lenses again: last general probe went dry. B) aimed lenses (bold bets, measured self-evolution, state-of-the-art harness gaps, unspoken needs) past every ideas.md, deepen 2. Choice: B.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Pack + fm ideas past every earlier ideas.md
2. [x] Ground, score, record, intake
## Resume here
## Docs impact
none: research only, recorded with fm research add
## Verification evidence
- (step 1) `ls state/projects/foreman-4a056f/research/ | grep -c round7` → exit 0 · 1 [ran] [tree b0c22b6f0608] (2026-10-04T04:59:44Z)
- (step 2) `ls state/projects/foreman-4a056f/research/ | grep -c round7` → exit 0 · 1 [ran] [tree b0c22b6f0608] (2026-10-04T04:59:44Z)
- (ac 1) `ls state/projects/foreman-4a056f/research/ | grep -c round7` → exit 0 · 1 [ran] [tree b0c22b6f0608] (2026-10-04T04:59:44Z)
- (audit intent) `self review of grounding` → aimed at the user's 'groundbreaking, recursive' ask: everything on the slate builds on fm bench toward a measured self-improvement loop (fm evolve) and usage savings (model routing) [tree b0c22b6f0608] (2026-10-04T04:59:44Z)
- (audit edge) `self review of grounding` → 'near T-…' marks on bench ideas were false friends (shared words with T-0212, not built) — checked each against fmbench.py; plan-critic and slice premises checked in planning.md and fm outline [tree b0c22b6f0608] (2026-10-04T04:59:44Z)
## Log
- 2026-10-04T04:57:26Z created
- 2026-10-04T04:57:30Z focused
- 2026-10-04T04:59:44Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0071 [FEATURE L, done, 5 steps] Super-brainstorm (recursive multi-round fm ideas) + implement every grounded idea and the inbox, recursing until dry; candidate improve…
- research brainstorm-20261003-round5: Quota brake (bold bets) → T-0198 economy mode: the mod reads session.usage rate limits; past 80% weekly / 90% 5-hour a prompt.compos…
- T-0184 [RESEARCH M, done, 2 steps] Super-improve Foreman: round 4 brainstorm past the 152 earlier ideas, grounded slate — lesson: Count lenses per idea: the one four len…
- T-0018 [FEATURE L, done, 6 steps] Recursive Foreman self-improvement: 10 rounds, each a slate implemented test-first, audited and committed
- similar finished tasks took 2–6 steps
## Lessons
- The near-done marker over-matches when a new idea extends a just-built feature (same nouns): treat 'near' on the newest tasks as 'builds on', and check the code
