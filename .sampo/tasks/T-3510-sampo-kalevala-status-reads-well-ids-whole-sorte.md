---
id: T-3510
type: FIX
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:06:04Z
updated: 2026-11-06T19:10:13Z
lane: ~/.claude/foreman.lanes/T-3510
lane_branch: foreman/T-3510
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T19:09:19Z
plan0_scope: []
---
# sampo kalevala status reads well: ids whole, sorted by number, sealed shown once as a count
## Raw request
> sampo kalevala status reads well: ids whole, sorted by number, sealed shown once as a count
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo kalevala status prints whole ids sorted numerically (1, 2, 10) and one sealed count instead of a '(sealed: True)' per row — verify with `python3 plugin/tests/run.py test_kalevala`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] status layout, test-first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 75 tests in 10.8s (9 jobs, 16 at a time; slowest: KalevalaStep 10s, KalevalaWatch 4s, Kalevala 2s) / OK [ran] [tree 5226c8fb81ff] [world 2f1906870a] (2026-11-06T19:10:13Z)
## Log
- 2026-11-06T19:06:04Z created
- 2026-11-06T19:06:20Z lane: ~/.claude/foreman.lanes/T-3510 on foreman/T-3510
- 2026-11-06T19:09:18Z focused
- 2026-11-06T19:09:19Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3081 [FEATURE M, done, 4 steps] Kalevala part 2: the towers per aspect, seeded and sealed, run at once as jobs; Kalevala's own generations and the capability registry …
- T-3266 [FEATURE M, done, 3 steps] Remake the Rune page (site/genesis) in the Sampo look with Kalevala: every tower, the meta-generations and Väinämöinen's acts — lesson:…
- T-3321 [FEATURE M, active, 3 steps] Fleet part 1: claims on git refs: take, renew, release and list claims under refs/sampo/<slug>/claim/<key> by atomic compare-and-swap…
- decision 2026-11-05: Kalevala (T-3050): namespaced Rune towers per aspect run at once, Väinämöinen oversees against the user's intent, Kalevala's own generations evolve …
