---
id: T-1252
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-20T13:45:23Z
updated: 2026-10-20T14:19:36Z
base: 8e943c4cb8a017aa7da88b7171b83cebd22215fd
base_tree: 3fea8d053ada0489e52606a7717831b7dfff926a
plan0_at: 2026-10-20T13:45:30Z
plan0_scope: []
paused_tree: 3fea8d053ada0489e52606a7717831b7dfff926a
verified: strong
---
# Super-improve Foreman, adapted to Claude Code 2.1.304
## Raw request
> continue, super improve foreman, and with latest claude code
## Interpretation
Brainstorm improvements in super mode, adapted to Claude Code 2.1.304, then build them in rounds
## Assumptions (confidence)
## Acceptance criteria
- [x] every brainstorm idea grounded, scored and recorded; the slate briefed — verify with `fm research list | grep -c brainstorm`
## Non-goals
## Approach (options → choice → why)
fm ideas super mode → ground every cluster → build in rounds; chosen as the brainstorm skill's super path; alternatives: only adapt to 2.1.304 (too narrow for 'super improve'), hand-picked list (drops ideas)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Context pack and fan-out (super mode)
2. [x] Ground, score, record, brief the slate
## Resume here
<!-- auto -->
- 2026-10-20T13:52:36Z step 1/2: Context pack and fan-out (super mode)
- git: foreman/build; 0 uncommitted
## Docs impact
none: research and decisions only; the page is an artifact
## Verification evidence
- (audit self) `checked the catalogue against ideas.md: all 368 ideas sit in one of 17 clusters, each cluster grounded with a read or grep, scored and marked; the slate is briefed (T-1254 to T-1258) and the rest captured (T-1259 to T-1268); page published` → pass: no idea dropped silently; the router-skill skip and the two skipped clusters carry their reasons [tree ff00e8c49bd6] (2026-10-20T14:18:17Z)
- (ac 1) `fm research list | grep -c brainstorm` → exit 0 · 76 [ran] [tree ff00e8c49bd6] (2026-10-20T14:18:27Z)
- (step 1) `test -s state/projects/foreman-4a056f/research/brainstorm-20261020.md && grep -c '^## C' state/projects/foreman-4a056f/research/brainstorm-20261020.md` → exit 0 · 17 [ran] [tree ff00e8c49bd6] (2026-10-20T14:18:27Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/brainstorm-20261020.md && grep -c '^## C' state/projects/foreman-4a056f/research/brainstorm-20261020.md` → exit 0 · 17 [ran] [tree ff00e8c49bd6] (2026-10-20T14:18:27Z)
- (audit intent) `self audit of the catalogue against ideas.md` → the user asked to super-improve Foreman on the latest Claude Code; the slate targets where Foreman trails plain Claude Code (cost, context tax, bookkeeping calls) and stamps results with the Claude Code version [tree ff00e8c49bd6] (2026-10-20T14:18:27Z)
- (audit edge) `self audit of the catalogue against ideas.md` → ideas that were already built (theme flash, figures from data) are marked done, not re-briefed; the router skill is skipped for routing risk [tree ff00e8c49bd6] (2026-10-20T14:18:27Z)
## Log
- 2026-10-20T13:45:23Z created
- 2026-10-20T13:45:29Z planned from capture
- 2026-10-20T13:45:30Z focused
- 2026-10-20T13:46:53Z paused: focus moved to T-1253
- 2026-10-20T13:51:59Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-20T13:51:59Z focused
- 2026-10-20T13:52:37Z paused: focus moved to T-1246
- 2026-10-20T14:19:36Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0801 [RESEARCH M, done, 2 steps] Super-improve Foreman round 1: brainstorm, ground and queue (CC-feature integration) — lesson: a criterion's verify must check somethi…
- T-0800 [RESEARCH M, dropped, 2 steps] Super-improve Foreman: brainstorm, ground and queue (CC-feature integration)
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- decision 2026-10-09: [costly] Build all 70 'build' capabilities from the Foreman brainstorm in value-for-effort rounds (security first); the user's ticks on the punch li…
- similar finished tasks took 2–5 steps
## Decision
Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped test runs count as evidence when the output shows the runner's summary; T-1257 Foreman's own share of the context in fm cost; T-1258 a context-tax ratchet with one-line notes said once. Round 2: T-1249 macOS CI. Later (captured T-1259 to T-1268): version tracking, benchmark rigor, compaction strategy, site, decider person, guard hardening, simplicity, unattended economy, adaptive ceremony, onboarding. Skipped: hook performance (no felt cost), integrations (not asked for), a router skill (routing risk). Why: cost and context tax are where Foreman trails plain Claude Code. Catalogue: research brainstorm-20261020; page https://claude.ai/artifact/WEbsNWhTdGDGhPkzurrHSS
## Lessons
- Brief a captured slate item's criteria when it's taken up, not at capture: the five round-1 items were captured title-only and needed criteria before work
## Files touched
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- plugin/tests/test_code_worker.py
- plugin/tests/test_docs.py
- site/build.py
- site/data/stats.json
- site/pages.py
- site/stats.py
