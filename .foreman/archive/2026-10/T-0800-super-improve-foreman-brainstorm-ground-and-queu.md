---
id: T-0800
type: RESEARCH
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T15:57:05Z
updated: 2026-10-14T16:01:39Z
base: 4aecea1df413a2029cc510b5ccb8c28445c997b7
base_tree: 9fbf7df9dd3f3f007b3ac68a2b68b13199490a6d
paused_tree: 9fbf7df9dd3f3f007b3ac68a2b68b13199490a6d
---
# Super-improve Foreman: brainstorm, ground and queue (CC-feature integration)
## Raw request
> Super-improve Foreman: brainstorm, ground and queue (CC-feature integration)
## Interpretation
Recreates T-0760. Super-mode brainstorm on Foreman weighted to unused Claude Code features plus the user's inbox asks; ground every cluster; queue the build marks.
## Assumptions (confidence)
## Acceptance criteria
- [ ] catalogue recorded and slate queued — verify with `test -s state/projects/foreman-4a056f/research/brainstorm-20261014.md && fm queue | grep -q T-0775`
## Non-goals
## Approach (options → choice → why)
Options: lens-only brainstorm; grounded CC inventory then fm ideas super mode; hand-pick. Chose the inventory + super mode: the brainstormers can't see the harness.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Inventory, fan out, cluster, ground, score
2. [ ] Record catalogue, intake slate, publish the picks page  <- CURRENT
## Resume here
<!-- auto -->
- 2026-10-14T15:58:22Z step 2/2: Record catalogue, intake slate, publish the picks page
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/brainstorm-20261014-103619/ideas.md && grep -c '^## \[' state/projects/foreman-4a056f/research/brainstorm-20261014.md` → exit 0 · 30 [ran] [tree 9fbf7df9dd3f] (2026-10-14T15:57:12Z)
- (step 2) `fm queue | grep -cE 'T-07(7[5-9]|8[0-6])'` → ✗ exit 1 · 0 [ran] [tree 9fbf7df9dd3f] (2026-10-14T15:57:12Z)
- (ac 1) `test -s state/projects/foreman-4a056f/research/brainstorm-20261014.md && fm queue | grep -q T-0775` → ✗ exit 1 · (no output) [ran] [tree 9fbf7df9dd3f] (2026-10-14T15:57:13Z)
## Log
- 2026-10-14T15:57:05Z created
- 2026-10-14T15:57:05Z focused
- 2026-10-14T15:58:22Z paused: focus moved to T-0775
- 2026-10-14T16:00:26Z steer: user — 'recursively improve' means finish the tasks, then look at what was done and brainstorm improvements on top of it, repeatedly (not a one-time pass): after round 1 ships, review it, run fm ideas --seen on the improved project, build round 2, until a round comes back dry
- 2026-10-14T16:01:39Z dropped: its check grepped the queue for T-0775, which left the queue when it was done; recreated with a durable check
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0760 [RESEARCH M, dropped, 3 steps] Super-improve Foreman: brainstorm, ground and queue (CC-feature integration)
- T-0588 [RESEARCH L, done, 3 steps] And maybe a knowledge graph if we dont have it already, and also, better intuition/reasoni — lesson: grounding brainstormers in today'…
- decision 2026-10-14: [revisit: after 2026-10-15] Round 1 of the T-0760 brainstorm: build 12 briefs (T-0775..T-0786) plus the 5 discovered fixes (T-0759, T-0765, T-0767, …
- research mission-20261014-103352: Request: super improve foreman, integrate better with new CC features, super improve, smarter, faster, better, more capable, etc. etc. …
- similar past tasks were L: consider --tier L
- the similar finished task took 3 steps
