---
id: T-0432
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:16:25Z
updated: 2026-10-09T14:31:05Z
verified: ok
---
# Super brainstorm: Foreman capabilities and features
## Raw request
> can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just simple things either
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] every idea from a recursive multi-lens brainstorm is grounded, scored and shown to the user; build marks become briefs — verify with `test -s ~/.claude/foreman/state/projects/foreman-4a056f/research/brainstorm-foreman-20261009.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] mission + pack
2. [x] fm ideas super mode (rounds 4, deepen 3) + extra lenses
3. [x] merge, cluster, ground every cluster
4. [x] score, record catalogue, briefs/inbox, checklist page
## Resume here
## Docs impact
none: research only; the catalogue is a research note and a checklist page
## Verification evidence
- (step 1) `fm mission + extended pack` → mission-20261009-091631.md; pack extended with every fm command and the user's ambition line (scratchpad/foreman-pack.md, 2541 words) [tree 8b29094c3f16] (2026-10-09T14:17:01Z)
- (step 2) `fm ideas super mode` → 15 lenses, 4 rounds + 3 deepen rounds: 835 distinct ideas (research/brainstorm-20261009-091701/ideas.md) [tree 8b29094c3f16] (2026-10-09T14:28:27Z)
- (step 3) `ground every cluster` → 7 grounding agents covered all 103 capabilities (89 partial, 9 missing, 5 exist); 835/835 ideas assigned [tree 8b29094c3f16] (2026-10-09T14:29:57Z)
- (step 4) `score, record, brief` → 70 build / 33 skip scored; catalogue saved (research brainstorm-foreman-20261009); 70 captured T-0433..T-0502; checklist page published with a choices store (read back: empty) [tree 8b29094c3f16] (2026-10-09T14:30:57Z)
- (ac 1) `test -s ~/.claude/foreman/state/projects/foreman-4a056f/research/brainstorm-foreman-20261009.md` → exit 0 · (no output) [ran] [tree 8b29094c3f16] (2026-10-09T14:31:01Z)
- (audit intent) `self: 835/835 ideas assigned exactly once (build.py asserts), every capability grounded with evidence, skips carry reasons on the page` → the user asked for many brainstorm agents, recursive, past simple things: 15 lenses x 4 rounds + 3 deepen rounds, grounded, all shown on a checklist page [tree 8b29094c3f16] (2026-10-09T14:31:01Z)
- (audit edge) `self: 835/835 ideas assigned exactly once (build.py asserts), every capability grounded with evidence, skips carry reasons on the page` → grounding agents read docs and greps more than code (medium confidence); each brief re-grounds at plan time [tree 8b29094c3f16] (2026-10-09T14:31:01Z)
- (audit intent) `self: 835/835 ideas assigned exactly once (build.py asserts), every capability grounded with evidence, skips carry reasons on the page` → the user asked for many brainstorm agents, recursive, past simple things: 15 lenses x 4 rounds + 3 deepen rounds, grounded, all shown on a checklist page [tree 8b29094c3f16] (2026-10-09T14:31:05Z)
- (audit edge) `self: 835/835 ideas assigned exactly once (build.py asserts), every capability grounded with evidence, skips carry reasons on the page` → grounding agents read docs and greps more than code (medium confidence); each brief re-grounds at plan time [tree 8b29094c3f16] (2026-10-09T14:31:05Z)
## Log
- 2026-10-09T14:16:25Z created
- 2026-10-09T14:16:30Z planned from capture
- 2026-10-09T14:28:27Z clustered: 835/835 ideas into 103 capabilities in 13 areas (scratchpad clusters.json); grounding: 7 parallel agents, one per area group, each writing grounding/gN.json
- 2026-10-09T14:31:05Z done
## Follow-ups captured
## Lessons
- Number the ideas before clustering: coverage then becomes a one-line assertion instead of a hope.
