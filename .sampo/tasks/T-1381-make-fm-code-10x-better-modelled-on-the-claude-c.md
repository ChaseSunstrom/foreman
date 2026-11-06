---
id: T-1381
type: RESEARCH
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T16:48:44Z
updated: 2026-10-21T16:51:36Z
base: a3a5b47a75619feb96fac19e34cfdd881dc15d4f
base_tree: 06949f07bede6866bef3b0f03eb488a0cbd01812
plan0_at: 2026-10-21T16:48:56Z
plan0_scope: []
paused_tree: 06949f07bede6866bef3b0f03eb488a0cbd01812
---
# Capability map: what Claude Code does (from its public GitHub repo) against fm code today, every gap grounded and scored, the slate briefed
## Raw request
> make fm code 10x better, modelled on the Claude Code GitHub repo (anthropics/claude-code: its README, CHANGELOG and plugins as the map of what a coding agent CLI does), working with anything (any CLI, any model) and full management from the app (verbatim: 'can you take off the claude code github repo. and make fm code 10x better, work with anything, etc. full management')
## Interpretation
The user wants fm code 10x better, modelled on Claude Code's public GitHub repo, working with any CLI or model, with full management from the app. Map every user-facing capability Claude Code's repo documents (README, CHANGELOG, plugins, examples) against fm code and the earlier catalogue (research/brainstorm-fm-code-catalogue.md), ground each gap in fm code's code, score it, and brief the build slate.
## Assumptions (confidence)
## Acceptance criteria
- [ ] research/claude-code-capability-map.md lists every capability with its source, fm code's status (have/partial/missing, with the code that shows it) and a mark — verify with `test -s state/projects/foreman-4a056f/research/claude-code-capability-map.md`
- [ ] every 'build' mark is a planned brief or an existing slate task named in the map — verify with `fm queue`
## Non-goals
## Approach (options → choice → why)
One fm-recon agent reads the repo (public files only: README, CHANGELOG, plugins/, examples/; no leaked or decompiled source) and returns a capability list with citations; I ground each against plugin/lib/fmcode*.py and the 29 slate briefs, mark have/partial/missing, score value and effort, and brief the missing ones that fit fm code's model (the harness drives, a runner works). Alternatives: a full 10-lens brainstorm (a 522-idea round already ran; economy mode), or building the open slate as is (misses what Claude Code users expect).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Recon: Claude Code's capabilities from its public repo, cited  <- CURRENT
2. [ ] Ground against fm code and the slate; score and mark; write the map
3. [ ] Brief the build marks; order the queue
## Resume here
<!-- auto -->
- 2026-10-21T16:49:14Z step 1/3: Recon: Claude Code's capabilities from its public repo, cited
- git: foreman/build; 1 uncommitted: CHANGELOG.md
## Docs impact
## Verification evidence
## Log
- 2026-10-21T16:48:44Z created
- 2026-10-21T16:48:54Z planned from capture
- 2026-10-21T16:48:56Z focused
- 2026-10-21T16:49:14Z paused: focus moved to T-1343
- 2026-10-21T16:51:36Z dropped: folded into T-1382: the Claude Code capability map is that brainstorm's first input (research/claude-code-capabilities.md)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261020-222446: Request: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage AN…
- research mission-20261020-222446.pack: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage ANY CL…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- decision 2026-10-16: Recommendation: build the slate T-1042..T-1053 plus T-1028 widened (recorded in research brainstorm-20261016-catalogue); the user then asked for eve…
