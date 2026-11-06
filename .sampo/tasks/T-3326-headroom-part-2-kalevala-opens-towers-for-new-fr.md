---
id: T-3326
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/kalevala.py, plugin/tests/test_kalevala.py, plugin/lib/sampo/moonscale.py]
depends_on: []
source: followup
created: 2026-11-06T04:31:23Z
updated: 2026-11-06T04:31:24Z
---
# Headroom part 2: Kalevala opens towers for new Frame areas, at most 2 a generation, each an act with an undo
## Raw request
> Headroom part 2: Kalevala opens towers for new Frame areas, at most 2 a generation, each an act with an undo
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] aspects() includes the root Frame's grown areas and capabilities (rune.grow, T-2188); gen() opens a tower for each aspect with none, at most BIRTHS_MAX=2 per generation, each logged as a 'birth' act with undo 'sampo kalevala pause NAME'; moonscale.SAMPO_AREAS reads kalevala.FIXED instead of a copy — verify with `python3 plugin/tests/run.py test_kalevala`
## Non-goals
## Approach (options → choice → why)
1) births through the Frame (rune.grow): evidence and a cold read already exist. 2) births straight from headroom proposals: skips the Frame's checks. 3) a manual kalevala add verb only: still needs a person. Choice 1; the headroom pass (T-3316 part 3) feeds rune.grow.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] test: a Frame area added after start opens one tower at the next gen, with its act and undo; a third birth waits a generation  <- CURRENT
2. [ ] move start's open loop into _open and call it from gen()
3. [ ] fold SAMPO_AREAS into FIXED
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:31:23Z created
## Follow-ups captured
