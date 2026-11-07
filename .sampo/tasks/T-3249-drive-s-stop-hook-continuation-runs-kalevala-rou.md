---
id: T-3249
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/lib/sampo/kalevala.py, plugin/tests/test_hooks.py, plugin/tests/test_kalevala.py, CHANGELOG.md]
depends_on: [T-3163, T-3265]
source: followup
created: 2026-11-05T21:26:45Z
updated: 2026-11-06T02:25:09Z
inferred_deps: [T-3082]
inferred_why: T-3082: named in its request
---
# Drive's Stop-hook continuation runs Kalevala rounds too (T-3082 criterion 3's drive…
## Raw request
> Drive's Stop-hook continuation runs Kalevala rounds too (T-3082 criterion 3's drive half: hooks.py _drive, after T-3163 merges since it edits test_hooks.py); and check night's Kalevala loop has a wall-clock cap, not only spend
## Interpretation
Reading 1 (chosen): Kalevala's towers move forward while other work goes on (T-2902: genesis and moons run alongside the main task). Each tower's next step is either a job (spec, seed 2+, select: kalevala.step runs them) or session work (gen-1's seed, each Mission's doc, briefs and critique: rune.step names the command). The drive's Stop-hook continuation names one tower's next session action as a lane-sized item beside the queue's work, and starts a background round when a tower's next stage is a job. Reading 2 (ruled out): the drive only calls kalevala.loop. Ruled out because on 2026-11-06 all 26 towers sat at gen 0: after spec, every tower's gen-1 seed is session work, so job rounds alone never move them.
## Assumptions (confidence)
## Acceptance criteria
- [ ] With towers open and Kalevala not paused, the drive's continuation names one tower's next session action (its rune.step command with --tower) beside the queue's work, a different tower each time, and nothing when Kalevala is paused or the drive is off — verify with `python3 plugin/tests/run.py test_hooks`
- [ ] When a tower's next stage is a job, the drive starts one background kalevala step at idle CPU priority, never two rounds at once and at most one per 15 minutes — verify with `python3 plugin/tests/run.py test_hooks test_kalevala`
## Non-goals
## Approach (options → choice → why)
1. Drive names tower session actions and starts job rounds in the background. Likely outcome: towers advance every drive cycle; one more line in the continuation.
2. Night only (night._kalevala_rounds plus T-3265). Likely outcome: one job round a night and no session work; fails if towers need gen-1 seeds, which they do.
3. Capture each tower step into the queue as its own task. Likely outcome: 26 towers flood the queue; fails if user tasks get buried behind tower steps.
4. Do less: the drive calls kalevala.loop only. Likely outcome: same stall as today after spec.

Choice 1 (85%): it is the only option that moves session-work stages, and it keeps the queue clean. Captured: none.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] drive line: next tower session action, rotated  <- CURRENT
2. [ ] background job round from the drive: idle class, single-flight, 15-minute floor
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T21:26:45Z created
- 2026-11-06T02:25:07Z set tier=M, depends_on=['T-3163', 'T-3265'], scope=['plugin/lib/sampo/hooks.py', 'plugin/lib/sampo/kalevala.py', 'plugin/tests/test_hooks.py', 'plugin/tests/test_kalevala.py', 'CHANGELOG.md']
- 2026-11-06T02:25:09Z planned: it has criteria and steps
## Follow-ups captured
