---
id: T-2940
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T08:49:42Z
updated: 2026-11-04T08:51:01Z
base: 0f49df304178e31730e8a99a3a1a84b4ba738409
base_tree: 8ed4c98571262f999fae70c87de8185675b9fd56
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T08:49:43Z
plan0_scope: []
verified: strong
---
# Moons promote writes a lead's Domain as plain words ('refactors across the open-source ecosystem, from a phone'), not the raw grid cell ('refactors, at ecosystem scale, in the phone') its cold read refused
## Raw request
> Moons promote writes a lead's Domain as plain words ('refactors across the open-source ecosystem, from a phone'), not the raw grid cell ('refactors, at ecosystem scale, in the phone') its cold read refused
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a promoted block's Domain reads as a phrase for every scale and surface — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test
2. [x] phrase tables in promote
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_moons_scale.PromoteDomain` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: PromoteDomain 0s) / FAILED (1 classes: test_moons_scale.PromoteDomain) [ran] [tree 6cfa9d94ce9f] [world 2f1906870a] (2026-11-04T08:49:53Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 42 tests in 2.8s (11 classes, 16 at a time; slowest: Grow 2s, Cli 2s, Route 2s) / OK [ran] [tree c47f6b933a4b] [world 2f1906870a] (2026-11-04T08:50:07Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T08:50:07Z [ran] [tree c47f6b933a4b] [world 2f1906870a] (2026-11-04T08:50:16Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale.PromoteDomain` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: PromoteDomain 1s) / OK [ran] [tree c47f6b933a4b] [world 2f1906870a] (2026-11-04T08:50:16Z)
- (audit edge) `red test then green; test_moons_scale 42 pass, including the promote-to-catalogue test` → every scale and surface reads as a phrase; an unknown scale or surface falls back to its own word; an empty kind leaves no stray comma [tree c47f6b933a4b] (2026-11-04T08:50:16Z)
- (audit intent) `red test then green; test_moons_scale 42 pass, including the promote-to-catalogue test` → promoted leads read as plain English so the catalogue's cold read can pass them [tree c47f6b933a4b] (2026-11-04T08:50:16Z)
- (audit self) `red test then green; test_moons_scale 42 pass, including the promote-to-catalogue test` → no findings [tree c47f6b933a4b] (2026-11-04T08:50:16Z)
## Log
- 2026-11-04T08:49:42Z created
- 2026-11-04T08:49:43Z focused
- 2026-11-04T08:49:43Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T08:50:58Z done
- 2026-11-04T08:51:01Z committed 3e1f4de0 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, planned, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-fi…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- T-2868 [FEATURE M, done, 2 steps] Moonscale part 1: the candidate store (research/genesis/moons/candidates.jsonl plus an append-only funnel log), write-time rules (the '…
## Why not caught
promote's test ran with --max 0, so no block's wording was ever read
## Lessons
- text a model's reviewer reads must be written for a reader, not assembled from grid keys
## Plan gaps
- failed first: step 1 test
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/moonscale.py
