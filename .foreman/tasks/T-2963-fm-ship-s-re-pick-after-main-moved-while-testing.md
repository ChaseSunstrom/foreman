---
id: T-2963
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T13:04:11Z
updated: 2026-11-04T13:09:47Z
base: 8cf677ca5c88cc792d863673a788707a25f5c0e7
base_tree: 7a830a18faa21908b05bd3adea30154ae009b00d
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T13:04:12Z
plan0_scope: []
verified: strong
---
# fm ship's re-pick after main moved while testing has no tower rule: the live tower pushed genesis.json mid-test and re-picking the branch's steps onto it conflicted (ship 4); the pick that keeps main's copy of the tower's files must serve both the first pick and the re-pick
## Raw request
> fm ship's re-pick after main moved while testing has no tower rule: the live tower pushed genesis.json mid-test and re-picking the branch's steps onto it conflicted (ship 4); the pick that keeps main's copy of the tower's files must serve both the first pick and the re-pick
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a tower update pushed to main while ship's test runs is re-picked over: main ends with the tower's newest copy and the branch's other files — verify with `python3 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test first: the ship's --test pushes a tower commit; then one _pick helper for both loops
## Resume here
## Docs impact
CHANGELOG line (T-2963, beside T-2955)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ship test_release` → exit 0 · Ran 92 tests in 32.7s (11 classes, 16 at a time; slowest: Ship 32s, Release 11s, BoardVerbs 3s) / OK [ran] [tree 0c2aaeae6b9b] [world 2f1906870a] (2026-11-04T13:07:12Z)
- `python3 plugin/tests/run.py test_ship` → ✗ exit 1 · Ran 48 tests in 33.7s (2 classes, 16 at a time; slowest: Ship 32s, ShipNext 2s) / FAILED (1 classes: test_ship.Ship) (start tree + this task's tests) [ran] [tree 0c2aaeae6b9b] [world 2f1906870a] (2026-11-04T13:08:19Z)
- `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 48 tests in 32.5s (2 classes, 16 at a time; slowest: Ship 32s, ShipNext 2s) / OK [ran] [tree 0c2aaeae6b9b] [world 2f1906870a] (2026-11-04T13:08:19Z)
- (ac 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 48 tests in 32.4s (2 classes, 16 at a time; slowest: Ship 32s, ShipNext 2s) / OK [ran] [tree e2c89936e82d] [world 2f1906870a] (2026-11-04T13:09:00Z)
- (audit intent) `self: the red test reproduced ship 4's exact message; one _pick helper now serves both loops, so the tower rule can't drift between them` → a tower publish that lands on main while ship tests is re-picked over: main keeps the tower's newest copy and gets the branch's other files [tree e2c89936e82d] (2026-11-04T13:09:00Z)
- (audit adversary) `self: the red test reproduced ship 4's exact message; one _pick helper now serves both loops, so the tower rule can't drift between them` → the re-pick's tower set is recomputed from the newest main (moves inside site/genesis and the stats file only); any other conflicted path still aborts and pushes nothing; the CI-ignored check (T-2572) still refuses a move in files CI tests [tree e2c89936e82d] (2026-11-04T13:09:00Z)
- (audit edge) `self: the red test reproduced ship 4's exact message; one _pick helper now serves both loops, so the tower rule can't drift between them` → when the ship has no last-ship ref the first pick's tower set (empty) is reused, so every conflict refuses as before [tree e2c89936e82d] (2026-11-04T13:09:00Z)
- (audit self) `self: the red test reproduced ship 4's exact message; one _pick helper now serves both loops, so the tower rule can't drift between them` → no findings [tree e2c89936e82d] (2026-11-04T13:09:00Z)
## Log
- 2026-11-04T13:04:11Z created
- 2026-11-04T13:04:12Z focused
- 2026-11-04T13:04:12Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T13:05:09Z hypothesis: the re-pick loop cherry-picks without T-2955's tower resolve, so the tower's mid-test genesis.json push conflicts; the red test reproduces ship 4's exact message, ruling out a CI-glob cause
- 2026-11-04T13:09:45Z done
- 2026-11-04T13:09:47Z committed 565a4418 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2555 [FEATURE S, done, 2 steps] fm ship retries its push when main moved between the last check and the push, through the same re-pick check, up to 3 tries — lesson: a…
- T-2080 [FEATURE M, done, 4 steps] Genesis on the site: fm genesis export + a live interactive tower graph page, shipped to main — lesson: An export that feeds a public p…
- T-2955 [FIX M, done, 2 steps] fm ship can't ship a branch that touched a file fm genesis live keeps publishing to main: the tower's commits make the replay fall back to …
- decision 2026-11-02: [costly] Release 1.2.51: its push step conflicted because fm ship cherry-picks left foreman/build and main with diverged histories (merge base 2026-…
## Why not caught
T-2955's test moved main before the ship, not during its test; the re-pick path had no tower case
## Lessons
- Two code paths doing the same pick must share one helper, or a fix lands in one and the other keeps the bug
## Files touched
- plugin/tests/test_ship.py
- plugin/lib/sampo/release.py
- CHANGELOG.md
