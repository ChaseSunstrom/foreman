---
id: T-0213
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:17:48Z
updated: 2026-10-04T04:21:22Z
base: 22bb0d130d769bd73cc172a38af2651df4dc3965
base_tree: f4d9a3e7e8e6030309a66e6e45b4ad5b58e7547f
verified: strong
---
# Research other great plugins and what people want agent harnesses to do; add the best to F
## Raw request
> research other great plugins and what people want agent harnesses to do; add the best to Foreman; keep recursively improving
## Interpretation
Survey what developers want from agent harnesses and the best-loved plugin features; ground each against Foreman; queue the real gaps.
## Assumptions (confidence)
## Acceptance criteria
- [x] landscape research saved and its grounded gaps queued — verify with `test -s state/projects/foreman-4a056f/research/harness-landscape-20261003.md`
## Non-goals
## Approach (options → choice → why)
One fm-recon web pass with quote-anchored citations (chosen over several parallel recons: usage), two claims re-fetched, gaps grounded against fm run/map/secrets/prove.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Recon, spot-check, ground, intake
## Resume here
## Docs impact
none: research only, recorded with fm research add
## Verification evidence
- (step 1) `grep -c 'github.com\|kiro.dev\|aider.chat' state/projects/foreman-4a056f/research/harness-landscape-20261003.md` → exit 0 · 10 [ran] [tree f4d9a3e7e8e6] (2026-10-04T04:21:17Z)
- (ac 1) `test -s state/projects/foreman-4a056f/research/harness-landscape-20261003.md` → exit 0 · (no output) [ran] [tree f4d9a3e7e8e6] (2026-10-04T04:21:22Z)
- (audit intent) `self review of grounding` → the ask was 'research other great plugins and what people want harnesses to do, add them'; 12 gaps + 5 pain points surveyed, each checked against Foreman: 4 already present (waves via fm run --parallel, per-tier models, fm secrets, red→green prove), 2 covered natively (/rewind, briefs as specs), 4 queued (T-0214–T-0217) [tree f4d9a3e7e8e6] (2026-10-04T04:21:22Z)
- (audit edge) `self review of grounding` → two citations re-fetched and confirmed verbatim (claudekit README: 6 parallel review agents, test-changed hooks; kiro.dev/docs/specs: waves); spexcode/HN themes medium confidence, not used to justify a brief alone [tree f4d9a3e7e8e6] (2026-10-04T04:21:22Z)
## Log
- 2026-10-04T04:17:48Z created
- 2026-10-04T04:21:17Z focused
- 2026-10-04T04:21:22Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0071 [FEATURE L, done, 5 steps] Super-brainstorm (recursive multi-round fm ideas) + implement every grounded idea and the inbox, recursing until dry; candidate improve…
- T-0018 [FEATURE L, done, 6 steps] Recursive Foreman self-improvement: 10 rounds, each a slate implemented test-first, audited and committed
- T-0041 [RESEARCH M, done, 3 steps] Brainstorm how Foreman makes Claude's project work smarter (planning, memory, grounding, verification, decisions, learning) and queue …
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- similar finished tasks took 3–6 steps
## Lessons
- Landscape research is cheapest as one quote-anchored recon pass plus two re-fetches; most 'missing' features already existed under another name (fm run --parallel = waves), so grounding against fm --help first saves building duplicates
