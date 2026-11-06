---
id: T-0573
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:32:09Z
updated: 2026-10-09T15:20:47Z
base: f5734785abfe14500ebb59d7c6fea68ad5917215
base_tree: 48435ca99ec79fccad64fa10d83378ce20996a87
verified: ok
---
# Super brainstorm: Foreman's intelligence (planning, brainstorming, agent types, reasoning, steps, self-improvement)
## Raw request
> I like almost all of those so feel free to continue with those, and, I want genuine like capabilities/intelligence from it to, like planning/brainstorming/agent types/improvements/thought process/steps all ofit
## Interpretation
The user liked almost all of the first brainstorm's 70 build marks (continue them) and wants a second, deeper look at Foreman's intelligence: how it plans, brainstorms, reasons, decomposes into steps, chooses agent types, deliberates, judges, debugs, learns and improves its own thinking — real capabilities, not prompt tweaks.
## Assumptions (confidence)
## Acceptance criteria
- [x] a recursive multi-lens brainstorm on Foreman's intelligence, past the first one, grounded, scored and shown on the punch list; build marks become briefs — verify with `test -s ~/.claude/foreman/state/projects/foreman-4a056f/research/brainstorm-intelligence-20261009.md`
## Non-goals
## Approach (options → choice → why)
(A, chosen) the same super-brainstorm pipeline with 15 thinking-focused lenses, --seen the first brainstorm's ideas.md so it goes past them, a pack describing today's thinking machinery (skills, references, agent types, second reads, memory); cluster, ground in code, score, add to the same punch list. (B, rejected) extend the first catalogue by hand: one mind's ideas. (C, rejected) research papers only: ungrounded.
## Risks and rollback
## Execution prompt
## Steps
1. [x] mission + pack with Foreman's current thinking machinery
2. [x] fm ideas super mode, seen the first brainstorm
3. [x] cluster, ground, score, add to the punch list, brief
## Resume here
## Docs impact
none: research and briefs only
## Verification evidence
- (step 1) `mission + pack` → mission-20261009-093310 + intel-pack.md: the user's focus line and how Foreman thinks today (skills, references, agent types, second reads, memory, self-improvement) [tree 8b29094c3f16] (2026-10-09T14:33:33Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/brainstorm-20261009-093357/ideas.md && grep -c '' state/projects/foreman-4a056f/research/brainstorm-20261009-093357/ideas.md` → exit 0 · 800 [ran] [tree 48435ca99ec7] (2026-10-09T15:20:41Z)
- (step 3) `test -s state/projects/foreman-4a056f/research/brainstorm-intelligence-20261009.md && grep -c '^## I' state/projects/foreman-4a056f/research/brainstorm-intelligence-20261009.md` → exit 0 · 106 [ran] [tree 48435ca99ec7] (2026-10-09T15:20:41Z)
- (ac 1) `test -s ~/.claude/foreman/state/projects/foreman-4a056f/research/brainstorm-intelligence-20261009.md` → exit 0 · (no output) [ran] [tree 48435ca99ec7] (2026-10-09T15:20:47Z)
- (audit intent) `self: 768 ideas (15 lenses, 4 rounds, 3 deepened), all clustered into 106 capabilities with full coverage asserted by the page builder; 6 grounding agents read the code per area; 75 build marks became T-0593..T-0667 in one intake; the page shows all three brainstorms with filters` → every idea is visible to the user with a mark and reason; the user's request for genuine intelligence is answered by the catalogue and by the frontier pass T-0588 it led to [tree 48435ca99ec7] (2026-10-09T15:20:47Z)
- (audit edge) `self: 768 ideas (15 lenses, 4 rounds, 3 deepened), all clustered into 106 capabilities with full coverage asserted by the page builder; 6 grounding agents read the code per area; 75 build marks became T-0593..T-0667 in one intake; the page shows all three brainstorms with filters` → intake run once (the T-0503 duplicate lesson); the user's page adds raised to urgent; ungrounded count 0 [tree 48435ca99ec7] (2026-10-09T15:20:47Z)
## Log
- 2026-10-09T14:32:09Z created
- 2026-10-09T14:33:10Z planned from capture
- 2026-10-09T14:47:21Z focused
- 2026-10-09T14:47:53Z paused: focus moved to T-0581
- 2026-10-09T15:19:20Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-09T15:19:20Z focused
- 2026-10-09T15:20:47Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261009-093310: Request: I want genuine like capabilities/intelligence from it to, like planning/brainstorming/agent types/improvements/thought process…
- research mission-20261009-093310.pack: I want genuine like capabilities/intelligence from it to, like planning/brainstorming/agent types/improvements/thought process/ste…
- research mission-20261008-195201: Request: super improve foreman [stale: plugin/lib/fmagents.py, plugin/tests/test_agents.py changed since it was written]
- decision 2026-10-09: [costly] Build all 70 'build' capabilities from the Foreman brainstorm in value-for-effort rounds (security first); the user's ticks on the punch li…
## Lessons
- a brainstorm's cards must carry the first buildable slice and the grounding evidence, or the user can't judge them; the user judges 'groundbreaking' by step change, so a frontier pass with an explicit bar must follow an incremental catalogue
