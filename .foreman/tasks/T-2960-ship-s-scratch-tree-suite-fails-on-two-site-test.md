---
id: T-2960
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T12:19:38Z
updated: 2026-11-04T12:22:43Z
base: 726d9eedafd701d58f42d44856b8c18549e12b8c
base_tree: b4fa2d896f4d46873cfd33a92bff2b9c5774ed9c
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T12:19:39Z
plan0_scope: []
verified: strong
---
# Ship's scratch-tree suite fails on two site tests: the Code page doesn't name fm code's new --planner (test_site.CodePageCoversFmCode), and the tower probe's longReason check reads every text on the page, so the live tower's newer data with 'ahead' or 'behind' anywhere fails it (test_site_build.GenesisScorecard)
## Raw request
> Ship's scratch-tree suite fails on two site tests: the Code page doesn't name fm code's new --planner (test_site.CodePageCoversFmCode), and the tower probe's longReason check reads every text on the page, so the live tower's newer data with 'ahead' or 'behind' anywhere fails it (test_site_build.GenesisScorecard)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the Code page names --planner and the tower probe checks only the long-run row's own sentence; both pass with main's tower data — verify with `python3 plugin/tests/run.py test_site test_site_build`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] probe: check the long row's 'Sampo is ahead of/level with/behind plain' sentence, not any text; Code page: --planner beside --escalate
## Resume here
## Docs impact
the Code page (site/pages.py) names --planner
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site test_site_build test_genesis` → exit 0 · Ran 292 tests in 34.7s (50 classes, 16 at a time; slowest: GenesisRead 32s, GenerationReview 32s, GenesisCheck 27s) / OK [ran] [tree 4a1a13e91619] [world 2f1906870a] (2026-11-04T12:21:29Z)
- (ac 1) `python3 plugin/tests/run.py test_site test_site_build` → exit 0 · Ran 76 tests in 10.0s (27 classes, 16 at a time; slowest: Built 10s, Landing 5s, Header 5s) / OK [ran] [tree 4a1a13e91619] [world 2f1906870a] (2026-11-04T12:21:46Z)
- (audit intent) `self: both failures read from the ship's scratch-tree log; the probe reproduced on main's genesis.json before and after` → the tower probe now checks the long row's own sentence, so the page's other text can say ahead or behind; the Code page names --planner [tree 4a1a13e91619] (2026-11-04T12:21:46Z)
- (audit edge) `self: both failures read from the ship's scratch-tree log; the probe reproduced on main's genesis.json before and after` → the probe still fails if the row prints its ahead/level/behind sentence for a no-common-goals state, which is the bug it guards [tree 4a1a13e91619] (2026-11-04T12:21:46Z)
- (audit self) `self: both failures read from the ship's scratch-tree log; the probe reproduced on main's genesis.json before and after` → no findings [tree 4a1a13e91619] (2026-11-04T12:21:46Z)
## Log
- 2026-11-04T12:19:38Z created
- 2026-11-04T12:19:38Z focused
- 2026-11-04T12:19:39Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T12:21:30Z the probe on main's genesis.json (live tower data) printed longReason false before the change and true after; the Code page test listed --planner as missing before and passes after
- 2026-11-04T12:22:41Z done
- 2026-11-04T12:22:43Z committed d93ac9f8 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2080 [FEATURE M, done, 4 steps] Genesis on the site: fm genesis export + a live interactive tower graph page, shipped to main — lesson: An export that feeds a public p…
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: [cites: user steer 2026-10-30: have your stuff automatically update the site] [check: python3 plugin/tests/run.py test_genesis.GenesisLive] Standing…
## Regression test
none new: the red needs main's live tower data, which the repo's fixture doesn't carry; test_site.CodePageCoversFmCode and test_site_build.GenesisScorecard are the tests, run red in the ship's scratch tree (ship-3) and green here, and the probe's before/after on main's data is in the task log
## Why not caught
the probe ran only on the repo's tower data; main's live data first reached it in ship's scratch tree
## Lessons
- A page probe that searches every text on the page breaks on the data a live job publishes: anchor it on the element's own sentence
## Files touched
- plugin/tests/genesis_page.js
- site/pages.py
