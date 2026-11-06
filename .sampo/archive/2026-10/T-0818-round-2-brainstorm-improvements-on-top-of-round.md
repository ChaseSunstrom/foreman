---
id: T-0818
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T18:08:48Z
updated: 2026-10-14T18:38:08Z
base: e5df8015564e111332438df79d0513fd524301b6
base_tree: ee7c0734d9be63a8b4b2c698365ccadf944ccaeb
verified: strong
---
# Round 2 brainstorm: improvements on top of round 1 (what shipped today), past every earlier idea
## Raw request
> Round 2 brainstorm: improvements on top of round 1 (what shipped today), past every earlier idea
## Interpretation
The user's recursive loop: after round 1's builds, review what shipped and brainstorm improvements on top of it, past every idea already seen, then build the grounded ones; stop when a cheap probe yields fewer than ~3 grounded ideas.
## Assumptions (confidence)
## Acceptance criteria
- [x] a round-2 catalogue is recorded and its slate is briefed or the run is recorded dry — verify with `fm research show brainstorm-round2-20261014`
## Non-goals
## Approach (options → choice → why)
Options: (a) fm ideas super mode (4 rounds, deepen 3) with --seen both 10-14 runs and the 10-09 runs; (b) a cheap probe first (2 lenses, 2 rounds); (c) re-ground only the 13 later clusters. Chose (a) seeded with round-1's shipped list and the later clusters' reasons, since round 1 changed the ground (new monitor, compact output, fm page, guard work); (b) is the stopping test for later rounds.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Context pack with round-1 results
2. [x] fm ideas super mode with --seen every earlier ideas.md
3. [x] Cluster, ground, score, record, intake
## Resume here
<!-- auto -->
- 2026-10-14T18:31:35Z step 3/3: Cluster, ground, score, record, intake
- git: foreman/build; 0 uncommitted
## Docs impact
none: research record
## Verification evidence
- (step 1) `test -s /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/pack-round2.md` → exit 0 · (no output) [ran] [tree 2a5d935940b2] (2026-10-14T18:09:33Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/brainstorm-20261014-130926/ideas.md` → exit 0 · (no output) [ran] [tree 374a0776be48] (2026-10-14T18:30:29Z)
- (step 3) `fm research show brainstorm-round2-20261014` → exit 0 · - Wild: Hand the queue to a rival harness overnight and diff the results — near T-0683 (done): Milestone: Intelligence — Agent types and roles (Round 4) / - Wild: Offer a "premortem tape" the user can [ran] [tree ee7c0734d9be] (2026-10-14T18:37:55Z)
- (ac 1) `fm research show brainstorm-round2-20261014` → exit 0 · - Wild: Hand the queue to a rival harness overnight and diff the results — near T-0683 (done): Milestone: Intelligence — Agent types and roles (Round 4) / - Wild: Offer a "premortem tape" the user can [ran] [tree ee7c0734d9be] (2026-10-14T18:38:08Z)
- (audit intent) `self: every idea clustered (script-verified 1..437, no duplicates), every cluster grounded by recon with file:line, marks reviewed by me (two changed: feature-usage → one-off evidence for T-0794 since events.jsonl already holds it; state-integrity → skip, one-call crash window, no incident)` → the user's loop asked for improvements on top of round 1; the pack carried round 1's shipped list and --seen excluded all 8 earlier runs, and the catalogue keeps every idea with its mark [tree ee7c0734d9be] (2026-10-14T18:38:08Z)
- (audit maintainer) `self: every idea clustered (script-verified 1..437, no duplicates), every cluster grounded by recon with file:line, marks reviewed by me (two changed: feature-usage → one-off evidence for T-0794 since events.jsonl already holds it; state-integrity → skip, one-call crash window, no incident)` → catalogue at research brainstorm-round2-20261014; later clusters are inbox items with their reactivation evidence in the title [tree ee7c0734d9be] (2026-10-14T18:38:08Z)
## Log
- 2026-10-14T18:08:48Z created
- 2026-10-14T18:08:54Z focused
- 2026-10-14T18:10:10Z paused: focus moved to T-0819
- 2026-10-14T18:30:25Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-14T18:30:25Z focused
- 2026-10-14T18:31:43Z paused: focus moved to T-0823
- 2026-10-14T18:34:50Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-14T18:34:50Z focused
- 2026-10-14T18:38:08Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0588 [RESEARCH L, done, 3 steps] And maybe a knowledge graph if we dont have it already, and also, better intuition/reasoni — lesson: grounding brainstormers in today'…
- T-0258 [RESEARCH L, done, 4 steps] After all of that, recursively brainstorm and improve yourself — lesson: Recursive brainstorming converges fast once each pass is grou…
- T-0219 [RESEARCH M, done, 2 steps] Super-brainstorm round 2: bold ideas past everything built, now measurable with fm bench — lesson: The near-done marker over-matches w…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
## Lessons
- Round 2 of a recursive loop mostly re-proposes what exists; ground before counting, and expect the yield curve to fall fast
