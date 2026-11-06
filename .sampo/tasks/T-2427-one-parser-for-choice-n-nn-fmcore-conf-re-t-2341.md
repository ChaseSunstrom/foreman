---
id: T-2427
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_second.py]
depends_on: []
source: discovered
created: 2026-10-31T16:31:12Z
updated: 2026-11-02T01:44:18Z
base: 6abadf0c6aae5c7b7916dfd225866365614b1631
base_tree: a18f9789caa5d157769aee001338c53a8ddefb55
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T01:35:32Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_second.py]
verified: strong
---
# The rival gate reads a plan's Choice percent with the one shared parser (stated_confidence), not its own _CONF_RE
## Raw request
> One parser for 'Choice N (NN%)': fmcore._CONF_RE (T-2341) and stated_confidence (T-2338) parse the same text with two regexes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] rival_gaps reads the Approach's percent through stated_confidence (the last stated percent, as the plan gate and the ledger read it); _CONF_RE is gone; a plan that states 'Choice 1 (60%)' then changes its mind to 'Choice 2 (85%)' asks no rival for confidence — verify with `python3 plugin/tests/run.py test_second`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: an M plan whose Approach ends 'Choice 2 (85%)' after an earlier '(60%)' choice gets no 'under 80%' rival gap; one ending '(70%)' still does
2. [x] fmcore.rival_gap: conf = stated_confidence(...); _CONF_RE goes (no other reader); Why not caught
## Resume here
## Docs impact
none: no visible change beyond the gate agreeing with the plan gate
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_second` → exit 0 · Ran 35 tests in 15.3s (12 classes, 16 at a time; slowest: Rival 15s, RivalSplit 4s, Session 2s) / OK [ran] [tree a18f9789caa5] [world 2f1906870a] (2026-11-02T01:35:16Z)
- (step 1) `python3 plugin/tests/run.py test_second.Rival` → ✗ exit 1 · Ran 19 tests in 15.5s (2 classes, 16 at a time; slowest: Rival 15s, RivalSplit 4s) / FAILED (1 classes: test_second.Rival) [ran] [tree 61a49afbb706] [world 2f1906870a] (2026-11-02T01:36:13Z)
- (step 1) `python3 plugin/tests/run.py test_second.Rival` → exit 0 · Ran 19 tests in 22.6s (2 classes, 16 at a time; slowest: Rival 22s, RivalSplit 5s) / OK [ran] [tree 1396a158a16f] [world 2f1906870a] (2026-11-02T01:37:14Z)
- (step 2) `python3 plugin/tests/run.py test_second test_core` → exit 0 · Ran 170 tests in 30.8s (39 classes, 16 at a time; slowest: Rival 29s, ConfidenceRoutes 21s, RivalSplit 14s) / OK [ran] [tree 1396a158a16f] [world 2f1906870a] (2026-11-02T01:37:46Z)
- `python3 plugin/tests/run.py test_second.Rival` → ✗ exit 1 · Ran 19 tests in 11.3s (2 classes, 16 at a time; slowest: Rival 10s, RivalSplit 2s) / FAILED (1 classes: test_second.Rival) (start tree + this task's tests) [ran] [tree 1396a158a16f] [world 2f1906870a] (2026-11-02T01:38:08Z)
- `python3 plugin/tests/run.py test_second.Rival` → exit 0 · Ran 19 tests in 10.1s (2 classes, 16 at a time; slowest: Rival 10s, RivalSplit 2s) / OK [ran] [tree 1396a158a16f] [world 2f1906870a] (2026-11-02T01:38:08Z)
- (ac 1) `python3 plugin/tests/run.py test_second` → exit 0 · Ran 36 tests in 10.1s (12 classes, 16 at a time; slowest: Rival 10s, RivalSplit 2s, Session 1s) / OK [ran] [tree 1396a158a16f] [world 2f1906870a] (2026-11-02T01:43:50Z)
- (audit edge) `self-review: rival_gap reads conf through stated_confidence (the last stated percent, None when none or over 100), the same parser the plan gate and the ledger use; the M under-the-race-bar branch tests conf is not None and conf < RACE_BAR; _CONF_RE had no other reader and is gone` → a changed mind (60 then 90) asks no rival; a single 60 still does; no percent at all asks none for confidence [tree 1396a158a16f] (2026-11-02T01:43:50Z)
- (audit self) `self-review: rival_gap reads conf through stated_confidence (the last stated percent, None when none or over 100), the same parser the plan gate and the ledger use; the M under-the-race-bar branch tests conf is not None and conf < RACE_BAR; _CONF_RE had no other reader and is gone` → no findings [tree 1396a158a16f] (2026-11-02T01:43:50Z)
## Log
- 2026-10-31T16:31:12Z created
- 2026-11-02T01:19:21Z planned from capture
- 2026-11-02T01:35:30Z step 2 text: fmcore.rival_gaps: conf = stated_confidence(...); delete _CONF_RE; Why not caught → fmcore.rival_gap: conf = stated_confidence(...); _CONF_RE goes (no other reader); Why not caught
- 2026-11-02T01:35:30Z focused
- 2026-11-02T01:35:32Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T01:44:15Z done
- 2026-11-02T01:44:18Z committed f73bef75 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2338-review: T-2338 review (fm-reviewer, one pass): changes needed, all fixed in b6fa01bf.
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- research T-2341-review: Verdict: changes needed.** One HIGH problem, because the tests on the branch break once T-2335's plan gate is merged in. Several MEDIUM findings …
- decision 2026-10-30: The Genesis line and the exam_scorecard MCP tool show the held-out scorecard to sessions: aggregate N/M pass on the shared line, per-capability coun…
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmcore.py; re-ground the plan against them before editing
## Why not caught
The rival gate's tests state one percent per plan, so its own first-match parser and the shared last-match one agreed; T-2341 added _CONF_RE beside T-2338's stated_confidence without a test that told them apart.
## Lessons
- One number, one parser: two regexes for the same field drift on the first case one of them never saw
## Files touched
- plugin/tests/test_second.py
- plugin/lib/fmcore.py
