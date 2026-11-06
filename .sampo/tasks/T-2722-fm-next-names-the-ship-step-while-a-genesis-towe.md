---
id: T-2722
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T23:20:41Z
updated: 2026-11-02T23:21:40Z
base: 46a868c5d69adf506c5e27e746ad8546c53d0ec5
base_tree: cf103702454725182ff448a4de6da80a4b3ca4c1
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T23:20:42Z
plan0_scope: []
verified: strong
---
# fm next names the ship step while a Genesis tower is open too: with the task queue closed, the tower's stage is 'genesis', never 'idle', so T-2682's rule never fired here
## Raw request
> fm next names the ship step while a Genesis tower is open too: with the task queue closed, the tower's stage is 'genesis', never 'idle', so T-2682's rule never fired here
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with an open tower, the queue closed, waiting commits and the push grant, fm next leads with the ship step — verify with `python3 plugin/tests/run.py test_ship_next`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] let the rule fire at the genesis stage
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ship_next` → exit 0 · Ran 9 tests in 2.1s (1 classes, 16 at a time; slowest: ShipNext 2s) / OK [ran] [tree 767472890410] [world 2f1906870a] (2026-11-02T23:21:04Z)
- `python3 plugin/tests/run.py test_ship_next` → ✗ exit 1 · Ran 9 tests in 3.3s (1 classes, 16 at a time; slowest: ShipNext 2s) / FAILED (1 classes: test_ship_next.ShipNext) (start tree + this task's tests) [ran] [tree 767472890410] [world 2f1906870a] (2026-11-02T23:21:10Z)
- `python3 plugin/tests/run.py test_ship_next` → exit 0 · Ran 9 tests in 2.1s (1 classes, 16 at a time; slowest: ShipNext 2s) / OK [ran] [tree 767472890410] [world 2f1906870a] (2026-11-02T23:21:10Z)
- (ac 1) `python3 plugin/tests/run.py test_ship_next` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:21:10Z [ran] [tree 767472890410] [world 2f1906870a] (2026-11-02T23:21:18Z)
- (step 2) `python3 plugin/tests/run.py test_ship_next test_core` → exit 0 · Ran 147 tests in 6.3s (29 classes, 16 at a time; slowest: ConfidenceRoutes 6s, BriefIndex 2s, ShipNext 2s) / OK [ran] [tree 767472890410] [world 2f1906870a] (2026-11-02T23:21:18Z)
- (step 3) `python3 plugin/tests/run.py test_ship_next test_core` → exit 0 · Ran 147 tests in 6.3s (29 classes, 16 at a time; slowest: ConfidenceRoutes 6s, BriefIndex 2s, ShipNext 2s) / OK [ran] [tree 767472890410] [world 2f1906870a] (2026-11-02T23:21:18Z)
- (audit edge) `the ship rider's condition now admits the genesis stage; a task still silences it (b is set), as does a lane; with an open tower the ship step leads and the tower's step follows on the same line` → without the grant, the tower's line gains only the count rider; with nothing waiting, nothing changes [tree 767472890410] (2026-11-02T23:21:18Z)
- (audit operator) `the ship rider's condition now admits the genesis stage; a task still silences it (b is set), as does a lane; with an open tower the ship step leads and the tower's step follows on the same line` → found by dogfooding: the queue closed, 5 commits waited, and fm next named only the gap map [tree 767472890410] (2026-11-02T23:21:18Z)
- (audit self) `the ship rider's condition now admits the genesis stage; a task still silences it (b is set), as does a lane; with an open tower the ship step leads and the tower's step follows on the same line` → no findings [tree 767472890410] (2026-11-02T23:21:18Z)
## Log
- 2026-11-02T23:20:41Z created
- 2026-11-02T23:20:41Z focused
- 2026-11-02T23:20:42Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T23:21:01Z scope: CHANGELOG.md
- 2026-11-02T23:21:38Z done
- 2026-11-02T23:21:40Z committed 4992e2d2 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2095 [FEATURE M, done, 3 steps] fm genesis step: the tower's next action from its files, resumable after any kill — lesson: A resumable state machine over files has to…
- T-2555 [FEATURE S, done, 2 steps] fm ship retries its push when main moved between the last check and the push, through the same re-pick check, up to 3 tries — lesson: a…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
## Why not caught
test_ship_next built its repo without a Genesis tower, while this project, the one the brief measured, always has one open
## Files touched
- plugin/tests/test_ship_next.py
- plugin/lib/fmcore.py
- CHANGELOG.md
