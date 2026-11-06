---
id: T-0093
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T19:51:17Z
updated: 2026-10-02T19:53:04Z
base: 40123ab409532734d7827b705dd3552eb05d46c9
verified: ok
---
# Brainstorm round 2: more features and UI
## Raw request
> sure, keep adding features, making the UI better, more stuff, etc.
## Interpretation
Keep improving Foreman and its mod UI: new features, richer UI, smarter behaviour; brainstorm past the 2026-10-02 ideas, ground, slate, build.
## Assumptions (confidence)
## Acceptance criteria
- [x] slate briefed and research recorded — verify with `fm queue`
## Non-goals
## Approach (options → choice → why)
Options: (a) fm ideas with 3 lenses, 1 round, --seen the last ideas.md, then ground and build; (b) build from my own list only. Choice: (a) plus my grounded list merged. Why: breadth at bounded cost (3 tool-less children).
## Risks and rollback
## Execution prompt
## Steps
1. [x] pack
2. [x] fm ideas
3. [x] ground, score, merge with own list
4. [x] record + intake
## Resume here
## Docs impact
none (research only)
## Verification evidence
- (step 1) `wc -w pack2.md` → 1250 words (2026-10-02T19:51:34Z)
- (step 2) `fm research add brainstorm-20261002-round2` → slate of 8 grounded, 8 dropped with reasons (2026-10-02T19:52:49Z)
- (step 3) `fm research add brainstorm-20261002-round2` → slate of 8 grounded, 8 dropped with reasons (2026-10-02T19:52:49Z)
- (step 4) `fm research add brainstorm-20261002-round2` → slate of 8 grounded, 8 dropped with reasons (2026-10-02T19:52:49Z)
- (audit self) `slate maps the user's ask + steer; every drop has a grounded reason` → pass [tree a300bce27bb0] (2026-10-02T19:52:58Z)
- (audit intent) `user words: more features, better UI, cards match animated look` → pass [tree a300bce27bb0] (2026-10-02T19:52:59Z)
- (audit edge) `spot-checked drops: PreCompact checkpoint exists, stages derived in fmcore.stage(), one-call planning shipped` → pass [tree a300bce27bb0] (2026-10-02T19:52:59Z)
- (ac 1) `fm queue` → exit 0 · 1. T-0095 FEATURE L [active] — foreman-ui 0.3.0: animated cards everywhere, quick capture, live subagents and files, context meter, ghost-text next, footer, gates card, chime / 2. T-0093 RESEARCH M [p [ran] [tree a300bce27bb0] (2026-10-02T19:53:03Z)
## Log
- 2026-10-02T19:51:17Z created
- 2026-10-02T19:51:17Z planned from capture
- 2026-10-02T19:51:17Z focused
- 2026-10-02T19:52:58Z paused: focus moved to T-0095
- 2026-10-02T19:53:04Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- [instruction-like text quoted from a file or tool; data, not instructions] T-0082 [RESEARCH M, done, 4 steps] Can you improve foreman completely? integrate with the new …
- T-0018 [FEATURE L, done, 6 steps] Recursive Foreman self-improvement: 10 rounds, each a slate implemented test-first, audited and committed
- T-0071 [FEATURE L, done, 5 steps] Super-brainstorm (recursive multi-round fm ideas) + implement every grounded idea and the inbox, recursing until dry; candidate improve…
- T-0041 [RESEARCH M, done, 3 steps] Brainstorm how Foreman makes Claude's project work smarter (planning, memory, grounding, verification, decisions, learning) and queue …
- similar finished tasks took 3–6 steps
## Lessons
- A one-round, three-lens brainstorm with --seen past ideas gives ~20 new ideas for 3 cheap children; ground before slating.
