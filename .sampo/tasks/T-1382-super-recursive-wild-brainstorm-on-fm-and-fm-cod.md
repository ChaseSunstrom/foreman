---
id: T-1382
type: RESEARCH
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T16:51:02Z
updated: 2026-11-06T03:53:41Z
base: a3a5b47a75619feb96fac19e34cfdd881dc15d4f
base_tree: eeec304e30d8a3cb08893d7f88ca3da809efbbb1
plan0_at: 2026-10-21T16:51:44Z
plan0_scope: []
paused_tree: eeec304e30d8a3cb08893d7f88ca3da809efbbb1
---
# Super recursive brainstorm of fm and fm code, integrating anthropics' six public repos: every idea grounded and scored, the slate built in rounds, re-brainstormed until dry
## Raw request
> Super recursive wild brainstorm on fm and fm code, integrating anthropics' six public repos automatically (verbatim: 'and integrate all of these too, automatically, super enhanced harness, etc. fully featured/implemented, super recursive wild brainstorm on fm and fm code' — skills, claude-code, claude-cookbooks, claude-plugins-official, financial-services, prompt-eng-interactive-tutorial)
## Interpretation
The user wants fm code 10x better and fully featured, working with any CLI or model, with full management, and the six anthropics repos (skills, claude-code, claude-cookbooks, claude-plugins-official, financial-services, prompt-eng-interactive-tutorial) integrated automatically into fm and fm code. Super mode: recursive rounds past every earlier idea until a round comes back dry.
## Assumptions (confidence)
## Acceptance criteria
- [ ] research/brainstorm-fm-anthropic-catalogue.md places every idea of the round in a cluster with grounding, score and mark — verify with `test -s state/projects/foreman-4a056f/research/brainstorm-fm-anthropic-catalogue.md`
- [ ] every build mark is a brief (planned or in the inbox with its plan line) and the catalogue is a checklist page — verify with `fm queue`
## Non-goals
## Approach (options → choice → why)
Inputs: research/claude-code-capabilities.md (recon of the claude-code repo) and a recon of the other five repos; the round-1 catalogue (brainstorm-fm-code-catalogue.md) and its ideas.md as --seen. fm mission composes the pack; fm ideas --rounds 4 --deepen 3 --seen <earlier ideas.md>; ground every cluster (recon agents per area); score and mark; brief every build mark; a checklist page; build in rounds with builders; re-brainstorm past every ideas.md until dry. Alternatives: build the open slate only (misses the repos and Claude Code parity), or one lens pass (not what 'super recursive wild' asks).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Pack: fm mission plus both repo recons, the round-1 catalogue, fm code's state; fm ideas --rounds 4 --deepen 3 --seen
2. [x] Merge, cluster and ground every cluster; score and mark; record the catalogue
3. [x] Brief the build marks; checklist page; start the build rounds
4. [ ] After each build round, a cheap probe (two lenses, --rounds 2, --seen all) until dry  <- CURRENT
## Resume here
<!-- auto -->
- 2026-10-21T17:03:05Z step 1/4: Pack: fm mission plus both repo recons, the round-1 catalogue, fm code's state; fm ideas --rounds 4 --deepen 3 --seen
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/pack2-addendum.md
## Docs impact
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/brainstorm-fm-anthropic-catalogue.md && fm inbox | grep -cE 'T-1(38[89]|39[0-9]|40[0-9]|41[0-2])'` → exit 0 · 25 [ran] [tree 1ed2d58e676b] (2026-10-21T17:32:05Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/brainstorm-fm-anthropic-catalogue.md && fm inbox | grep -cE 'T-1(38[89]|39[0-9]|40[0-9]|41[0-2])'` → exit 0 · 25 [ran] [tree 1ed2d58e676b] (2026-10-21T17:32:06Z)
- (step 3) `test -s state/projects/foreman-4a056f/research/brainstorm-fm-anthropic-catalogue.md && fm inbox | grep -cE 'T-1(38[89]|39[0-9]|40[0-9]|41[0-2])'` → exit 0 · 25 [ran] [tree 1ed2d58e676b] (2026-10-21T17:32:08Z)
## Log
- 2026-10-21T16:51:02Z created
- 2026-10-21T16:51:37Z planned from capture
- 2026-10-21T16:51:43Z focused
- 2026-10-21T16:52:27Z paused: focus moved to T-1336
- 2026-10-21T17:02:33Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-21T17:02:33Z focused
- 2026-10-21T17:03:06Z paused: focus moved to T-1343
- 2026-10-21T17:32:10Z blocked: step 4 (re-brainstorm past every ideas.md until dry) runs after this build round lands (T-1388..T-1412)
- 2026-11-06T03:53:41Z unblocked
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1381 [RESEARCH M, dropped, 3 steps] Capability map: what Claude Code does (from its public GitHub repo) against fm code today, every gap grounded and scored, the slate…
- T-1331 [RESEARCH M, blocked, 6 steps] Super recursive brainstorm of fm code: every idea grounded and scored, the slate built in rounds, re-brainstormed until dry
- T-1029 [RESEARCH L, done, 5 steps] Super recursive brainstorm: anything on the table to make Foreman super good; build, revie — lesson: Show the whole catalogue, not a s…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Decision
Round 2 (520 ideas past round 1's 522; 10 lenses, 4 rounds, 3 deepened) grounded in 67 clusters (half A: integration, safety, harness; half B: experience). 25 build marks briefed T-1388..T-1412 (security first: S1 worker grants, S5 plugin capability delta, S6 judge rc files, S7 prompt envelopes, S8 runner flag lint, S9 hostile-asset corpus, S14 stale safety gate); three folded into T-1338, T-1356, T-1358; 12 planned under round 1's briefs; 24 skipped with reasons (OS sandbox, hosting foreign plugins, refactors, speculative verbs). Catalogue: research/brainstorm-fm-anthropic-catalogue.md and its two halves; checklist page https://claude.ai/artifact/TR2GpiKuf7xV2yBpU7EYCs. Full autonomy: build in rounds, then re-brainstorm past both ideas.md until dry.
