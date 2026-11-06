---
id: T-1029
type: RESEARCH
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T02:12:18Z
updated: 2026-10-16T05:00:35Z
base: fc9c6af91ad056b43bb9587f687fda59a255cb7d
base_tree: 4c27ddbdf9cfbc3cc1dac898896bbfa12545e261
verified: strong
---
# Super recursive brainstorm: anything on the table to make Foreman super good; build, revie
## Raw request
> Super recursive brainstorm: anything on the table to make Foreman super good; build, review, brainstorm on top, repeat until dry
## Interpretation
A deep, repeated brainstorm on making Foreman the best plugin for any project, not one pass: every lens, several rounds that each go past the last, every idea grounded in the real code and shown, the best built in rounds, then brainstorm again on top of what shipped until a run comes back dry (the user's recursive-improvement standard). Anything is on the table: self-improvement that needs no asking, cross-project and team learning through git, speed and token cost, small-model reliability, the UI.
## Assumptions (confidence)
## Acceptance criteria
- [x] A super-mode brainstorm ran (≥ 3 rounds) and its full catalogue, every cluster grounded and marked build or skip, is recorded with fm research add — verify with `fm research list`
- [x] The build-marked clusters are briefs in the queue, in order — verify with `fm queue`
## Non-goals
## Approach (options → choice → why)
Options: (a) one fm ideas run with the default lenses: shallow, the user asked for recursive; (b) super mode: fm ideas --rounds 4 --deepen 3 over a fresh mission pack, ground every cluster with fm-recon, slate in rounds, re-brainstorm with --seen after each build round until dry; (c) a human-style audit of the codebase only: misses the bold bets. Choice (b).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Mission pack (fm mission) with the user's recent asks, the state of the code and the queue
2. [x] fm ideas --rounds 4 --deepen 3 (super mode), read ideas.md
3. [x] Cluster, ground every cluster (fm-recon in parallel), score and mark
4. [x] Record the catalogue, intake the slate, show the catalogue page
5. [x] Community wants: what people ask of Claude Code workflow plugins (anthropics/claude-code feature requests, popular plugin repos' issues and discussions), grounded against Foreman, into the pack
## Resume here
## Docs impact
none: research only
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/mission-20261015-215750.pack.md` → exit 0 · (no output) [ran] [tree 66d68c1277d3] (2026-10-16T03:25:17Z)
- (step 2) `test $(grep -c '^## Round' state/projects/foreman-4a056f/research/brainstorm-20261015-221834/ideas.md) -ge 3` → exit 0 · (no output) [ran] [tree 66d68c1277d3] (2026-10-16T03:25:18Z)
- (step 5) `test -s state/projects/foreman-4a056f/research/community-wants-20261016.md` → exit 0 · (no output) [ran] [tree 66d68c1277d3] (2026-10-16T03:25:18Z)
- (ac 1) `fm research list` → exit 0 · wave3-intent  2026-09-26  708B  Wave 3 intent audit (fm-reviewer, read-only) over wave3.diff + wave3-stages-ear… / claude-code-capabilities-2026-09-26  2026-09-26  1497B  Claude Code 2.1.280 capabilit [ran] [tree 4c27ddbdf9cf] (2026-10-16T05:00:34Z)
- (ac 2) `fm queue` → exit 0 · 1. T-1029 RESEARCH L [active] — Super recursive brainstorm: anything on the table to make Foreman super good; build, revie / 2. T-1089 FEATURE M [planned] — Ok, don't ask me any more questions or ANYT [ran] [tree 4c27ddbdf9cf] (2026-10-16T05:00:34Z)
- (step 3) `fm research list` → exit 0 · wave3-intent  2026-09-26  708B  Wave 3 intent audit (fm-reviewer, read-only) over wave3.diff + wave3-stages-ear… / claude-code-capabilities-2026-09-26  2026-09-26  1497B  Claude Code 2.1.280 capabilit [ran] [tree 4c27ddbdf9cf] (2026-10-16T05:00:34Z)
- (step 4) `fm research list` → exit 0 · wave3-intent  2026-09-26  708B  Wave 3 intent audit (fm-reviewer, read-only) over wave3.diff + wave3-stages-ear… / claude-code-capabilities-2026-09-26  2026-09-26  1497B  Claude Code 2.1.280 capabilit [ran] [tree 4c27ddbdf9cf] (2026-10-16T05:00:34Z)
- (audit intent) `self: super-mode brainstorm (3 rounds + 3 deepen, 6 lenses, past two earlier runs), community wants researched, every cluster grounded by three fm-recon passes and marked, catalogue recorded (brainstorm-20261016-catalogue) and published as a page, slate intaken as T-1042..T-1053` → every idea is on the page with a mark; the user's follow-up made every mark a build (T-1054) [tree 4c27ddbdf9cf] (2026-10-16T05:00:34Z)
- (audit operator) `self: super-mode brainstorm (3 rounds + 3 deepen, 6 lenses, past two earlier runs), community wants researched, every cluster grounded by three fm-recon passes and marked, catalogue recorded (brainstorm-20261016-catalogue) and published as a page, slate intaken as T-1042..T-1053` → the page link is in the report [tree 4c27ddbdf9cf] (2026-10-16T05:00:34Z)
- (audit adversary) `self: super-mode brainstorm (3 rounds + 3 deepen, 6 lenses, past two earlier runs), community wants researched, every cluster grounded by three fm-recon passes and marked, catalogue recorded (brainstorm-20261016-catalogue) and published as a page, slate intaken as T-1042..T-1053` → web and recon text treated as data [tree 4c27ddbdf9cf] (2026-10-16T05:00:34Z)
- (audit edge) `self: super-mode brainstorm (3 rounds + 3 deepen, 6 lenses, past two earlier runs), community wants researched, every cluster grounded by three fm-recon passes and marked, catalogue recorded (brainstorm-20261016-catalogue) and published as a page, slate intaken as T-1042..T-1053` → Reddit/HN pages didn't load; community wants came from GitHub issues and plugin repos [tree 4c27ddbdf9cf] (2026-10-16T05:00:34Z)
- (audit maintainer) `self: super-mode brainstorm (3 rounds + 3 deepen, 6 lenses, past two earlier runs), community wants researched, every cluster grounded by three fm-recon passes and marked, catalogue recorded (brainstorm-20261016-catalogue) and published as a page, slate intaken as T-1042..T-1053` → research only [tree 4c27ddbdf9cf] (2026-10-16T05:00:34Z)
## Log
- 2026-10-16T02:12:18Z created
- 2026-10-16T03:07:50Z steer: include wants from other people (issues/requests on CC and similar plugins), not only rival plugins' features (T-0964 covered those)
- 2026-10-16T03:13:23Z community wants saved: research/community-wants-20261016.md (continuity after compaction, hook-enforced rules, token cost of skills/subagents, AGENTS.md portability, MCP scoped to subagents, see which skill fired, diff review UI); feed into the mission pack
- 2026-10-16T03:23:47Z focused
- 2026-10-16T03:25:26Z paused: focus moved to T-1036
- 2026-10-16T05:00:30Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T05:00:30Z focused
- 2026-10-16T05:00:35Z done
## Follow-ups captured
## Build vs reuse
Reuses the brainstorm machinery as is: fm mission (the pack), fm ideas --rounds/--deepen/--seen (tool-less claude -p fan-out, dedupe into ideas.md), fm-recon for grounding, fm research add for the catalogue, fm intake for the slate; plus the saved research (community-wants-20261016, T-0964 rival surveys) folded into the pack. Nothing new to build for the brainstorm itself.
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261014-130857: Request: recursively improve: review what round 1 shipped today and brainstorm improvements on top of it — super improve foreman, integ…
- research mission-20261008-195201: Request: super improve foreman [stale: plugin/lib/fmagents.py, plugin/lib/fmbench.py, plugin/lib/fmbudget.py changed since it was writt…
- research mission-20261015-215750: Request: how can we make it so worktree agents can easily resumed if a session was stopped or something? etc. and super improve recursi…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
## Decision
Recommendation: build the slate T-1042..T-1053 plus T-1028 widened (recorded in research brainstorm-20261016-catalogue); the user then asked for every cluster including the skips, which T-1054 turned into briefs; would change if: grounding shows a cluster exists already.
## Lessons
- Show the whole catalogue, not a slate: the user wanted every idea built
