---
id: T-2958
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T11:57:24Z
updated: 2026-11-04T12:00:51Z
base: bdd2e914a138b419de66487126bf3964962a0c12
base_tree: 919931ebd5d28eb28d93115c55d3bd76ab579c1d
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T11:57:25Z
plan0_scope: []
verified: strong
---
# The site build crashes on an unrated moon: build.py's moons_html compares r['wild'] >= 4 and the live tower now publishes M-59..M-61 with wild null (not yet rated), so main's genesis.json fails the build and the ship's scratch-tree tests
## Raw request
> The site build crashes on an unrated moon: build.py's moons_html compares r['wild'] >= 4 and the live tower now publishes M-59..M-61 with wild null (not yet rated), so main's genesis.json fails the build and the ship's scratch-tree tests
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an unrated moon (wild null) is left out of the wild list and still counted in the totals; the build exits 0 — verify with `python3 plugin/tests/run.py test_site_landing test_site_build`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test first: a fixture row with wild null, then the guard in moons_html and the real-catalogue test
## Resume here
## Docs impact
CHANGELOG line (T-2958)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site_landing test_site_build` → exit 0 · Ran 24 tests in 5.4s (9 classes, 16 at a time; slowest: Landing 5s, Landing 2s, Reproducible 1s) / OK [ran] [tree b04841f06f63] [world 2f1906870a] (2026-11-04T11:58:00Z)
- `python3 plugin/tests/run.py test_site_landing` → ✗ exit 1 · Ran 10 tests in 7.2s (1 classes, 16 at a time; slowest: Landing 6s) / FAILED (1 classes: test_site_landing.Landing) (start tree + this task's tests) [ran] [tree b04841f06f63] [world 2f1906870a] (2026-11-04T11:58:16Z)
- `python3 plugin/tests/run.py test_site_landing` → exit 0 · Ran 10 tests in 7.3s (1 classes, 16 at a time; slowest: Landing 7s) / OK [ran] [tree b04841f06f63] [world 2f1906870a] (2026-11-04T11:58:16Z)
- (ac 1) `python3 plugin/tests/run.py test_site_landing test_site_build` → exit 0 · Ran 24 tests in 12.6s (9 classes, 16 at a time; slowest: Landing 12s, Landing 6s, Reproducible 3s) / OK [ran] [tree fdcd3b8030cf] [world 2f1906870a] (2026-11-04T11:58:39Z)
- (audit intent) `self: the failing ship's traceback pinned site/build.py:342; grep found the only other reader of wild (genesis.js wildOf) already tolerates a non-number` → an unrated moon is left out of the wild 4-5 list and still counted in the totals; the build exits 0 on main's real data (61 moons, 3 unrated) [tree fdcd3b8030cf] (2026-11-04T11:58:39Z)
- (audit edge) `self: the failing ship's traceback pinned site/build.py:342; grep found the only other reader of wild (genesis.js wildOf) already tolerates a non-number` → the real-catalogue test compared None >= 4 too; it now reads an unrated moon as 0, as genesis.js does [tree fdcd3b8030cf] (2026-11-04T11:58:39Z)
- (audit self) `self: the failing ship's traceback pinned site/build.py:342; grep found the only other reader of wild (genesis.js wildOf) already tolerates a non-number` → no findings [tree fdcd3b8030cf] (2026-11-04T11:58:39Z)
## Log
- 2026-11-04T11:57:24Z created
- 2026-11-04T11:57:24Z focused
- 2026-11-04T11:57:25Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T12:00:48Z done
- 2026-11-04T12:00:51Z committed e6c9d8cd (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2080 [FEATURE M, done, 4 steps] Genesis on the site: fm genesis export + a live interactive tower graph page, shipped to main — lesson: An export that feeds a public p…
- T-2767 [FEATURE M, done, 3 steps] Louhi, Moons and Underworld pages from the tower's real records (T-2742 step 7c-1): Louhi's scorecard from exam.jsonl, the Moons catalo…
- T-2955 [FIX M, done, 2 steps] fm ship can't ship a branch that touched a file fm genesis live keeps publishing to main: the tower's commits make the replay fall back to …
- decision 2026-10-30: [cites: user steer 2026-10-30: have your stuff automatically update the site] [check: python3 plugin/tests/run.py test_genesis.GenesisLive] Standing…
## Why not caught
the landing fixture's moons were all rated; it now carries one with wild null
## Lessons
- Data a live job publishes can hold states the build's fixtures never did (a moon not yet rated): fixtures should carry each optional field's empty form
## Files touched
- plugin/tests/test_site_landing.py
- site/build.py
- CHANGELOG.md
