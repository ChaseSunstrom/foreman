---
id: T-0843
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T13:38:24Z
updated: 2026-10-15T14:11:57Z
base: c596d3e0094e2de932fe332f4ca80e357e543948
base_tree: aff92f04e40793d59720599d1a0fd64b78726292
paused_tree: c43a546d55356ae901d3c8195d67cb09b33f4993
verified: strong
---
# Make Foreman THE plugin: round 4 brainstorm from new evidence (rival plugins, a fresh install as a new user, real usage data), then build every grounded idea in rounds
## Raw request
> can you keep going? super super improve? recursively? genuinely, make it THE plugin, everything, etc.
## Interpretation
The user wants the recursive loop to continue ('make it THE plugin, everything'). Rounds 2-3 went dry because they re-asked the same question about Foreman's internals with the same evidence. A new round needs new inputs: what other Claude Code workflow plugins do that Foreman doesn't, what a brand-new user hits installing and first using it, and what the usage data (fm repeats: 52 repeated procedures; outcomes; never-used verbs) says.
## Assumptions (confidence)
## Acceptance criteria
- [x] a round-4 catalogue grounded in the code and the three evidence sources is recorded, and its slate is briefed — verify with `fm research show brainstorm-round4-20261015`
## Non-goals
## Approach (options → choice → why)
Options: (a) rerun fm ideas with the old pack (dry last time); (b) gather three new evidence sources first, put them in the pack, then super mode; (c) skip brainstorming and build the deferred clusters. Chose (b): new evidence is what makes new grounded ideas possible; (c) builds things whose own reactivation evidence hasn't arrived.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Gather new evidence: rival plugins survey, fresh-install walkthrough, usage data
2. [x] Context pack + fm ideas super mode past every earlier run
3. [x] Cluster, ground, score, record, intake
## Resume here
<!-- auto -->
- 2026-10-15T14:04:46Z step 2/3: Context pack + fm ideas super mode past every earlier run
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: plugin/tests/test_doctor.py
## Docs impact
none: research record
## Verification evidence
- (step 1) `test -s /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/pack-round4.md` → exit 0 · (no output) [ran] [tree b2ab4ebce449] (2026-10-15T13:43:37Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/brainstorm-20261015-084445/ideas.md` → exit 0 · (no output) [ran] [tree 28ac020d939b] (2026-10-15T14:09:23Z)
- (step 3) `fm research show brainstorm-round4-20261015` → exit 0 · - Expose verify-as-a-service over A2A and MCP (Round 4) / - Add a thin editor sidebar for VS Code, Cursor and Windsurf (Round 4) [ran] [tree 28ac020d939b] (2026-10-15T14:11:57Z)
- (ac 1) `fm research show brainstorm-round4-20261015` → exit 0 · - Expose verify-as-a-service over A2A and MCP (Round 4) / - Add a thin editor sidebar for VS Code, Cursor and Windsurf (Round 4) [ran] [tree 28ac020d939b] (2026-10-15T14:11:57Z)
- (audit intent) `self: new evidence gathered (clean-HOME install, rival survey, usage data, bloat audit), 437 ideas clustered (script-verified), all 31 clusters grounded by recon with file:line; marks reviewed (newcomer-gates to later: suite never ran without claude; bypass-earned folded into install consent; gate-packs and shell hygiene marked done from today's T-0855)` → the user asked to keep going recursively and make it THE plugin; this round looked outward (newcomers, rivals) where rounds 2-3 looked inward and went dry, and it produced 6 builds plus 14 fixes already shipped [tree 28ac020d939b] (2026-10-15T14:11:57Z)
- (audit maintainer) `self: new evidence gathered (clean-HOME install, rival survey, usage data, bloat audit), 437 ideas clustered (script-verified), all 31 clusters grounded by recon with file:line; marks reviewed (newcomer-gates to later: suite never ran without claude; bypass-earned folded into install consent; gate-packs and shell hygiene marked done from today's T-0855)` → catalogue at research brainstorm-round4-20261015; 9 later clusters deferred to 2026-10-29 with the evidence each waits for [tree 28ac020d939b] (2026-10-15T14:11:57Z)
## Log
- 2026-10-15T13:38:24Z created
- 2026-10-15T13:38:31Z planned from capture
- 2026-10-15T13:38:31Z focused
- 2026-10-15T13:45:58Z paused: focus moved to T-0855
- 2026-10-15T14:04:26Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T14:04:26Z focused
- 2026-10-15T14:05:01Z paused: focus moved to T-0857
- 2026-10-15T14:11:57Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0588 [RESEARCH L, done, 3 steps] And maybe a knowledge graph if we dont have it already, and also, better intuition/reasoni — lesson: grounding brainstormers in today'…
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- research mission-20261014-130857: Request: recursively improve: review what round 1 shipped today and brainstorm improvements on top of it — super improve foreman, integ…
- decision 2026-10-14: Round 2 slate: 437 ideas in 29 clusters grounded → 3 build (compact spill cap T-0824, closed-pipe verb sweep T-0825, verb-usage evidence attached to…
## Lessons
- When a recursive loop goes dry, change the evidence, not the prompt: a clean-HOME walkthrough and a rival survey yielded more than two more inward rounds
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmrepeats.py
- plugin/tests/test_repeats.py
