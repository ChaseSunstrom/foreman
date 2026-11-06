---
id: T-2283
type: FIX
tier: S
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T06:31:14Z
updated: 2026-10-31T06:39:58Z
baseline: true
base: 541838aabccdfdc300ada21962a988b127c83b2c
base_tree: 0933508bbd81d2da1f620ad6cb9f730290e7cde7
plan0_at: 2026-10-31T06:36:53Z
plan0_scope: []
verified: strong
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_genesis.GenesisCheck.test_a_verb_whose_module_a_reached_verbs_module_imports_is_reached. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
test_genesis.GenesisCheck pins the live import graph: it expects fm adopt unreached after a session runs fm find, but T-2239 made fmfind import fmeco (the capability-miss capture), and fm adopt lives in fmeco, so fm find now reaches it. The reach rule is right; the test's example verb is stale.
## Assumptions (confidence)
## Acceptance criteria
- [x] test_genesis.GenesisCheck passes with an example verb fm find's import closure doesn't reach — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) swap the example verb for one whose module fm find's import closure doesn't hold (fm serve, in fmserve); 2) mock the import graph — rejected: the test's point is the real modules' imports; 3) drop the assertion — rejected: it guards T-2186. Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] swap fm adopt for fm serve in the reach test
## Resume here
## Docs impact
none: a test fixture
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisCheck` → exit 0 · Ran 12 tests in 5.516s / OK (start tree + this task's tests) [ran] [tree a31ffacaa442] (2026-10-31T06:39:07Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisCheck` → exit 0 · Ran 12 tests in 5.385s / OK [ran] [tree a31ffacaa442] (2026-10-31T06:39:07Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 154 tests in 7.7s (17 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree a31ffacaa442] (2026-10-31T06:39:15Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 154 tests in 7.6s (17 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 6s, GenesisDrift 6s) / OK [ran] [tree a31ffacaa442] (2026-10-31T06:39:35Z)
- (audit intent) `self: the reach rule is right (fm find now imports fmeco, so fm adopt is reached); the test's example verb was stale; swapped for fm which, a leaf module only fmcli imports and the rules name` → keeps T-2186's guard (a verb reached through a reached module's imports counts) on a stable example [tree a31ffacaa442] (2026-10-31T06:39:35Z)
- (audit edge) `self: the reach rule is right (fm find now imports fmeco, so fm adopt is reached); the test's example verb was stale; swapped for fm which, a leaf module only fmcli imports and the rules name` → the example picked from the data (modules no other module imports), not guessed [tree a31ffacaa442] (2026-10-31T06:39:35Z)
- (audit self) `self: the reach rule is right (fm find now imports fmeco, so fm adopt is reached); the test's example verb was stale; swapped for fm which, a leaf module only fmcli imports and the rules name` → no findings [tree a31ffacaa442] (2026-10-31T06:39:35Z)
## Log
- 2026-10-31T06:31:14Z created
- 2026-10-31T06:36:52Z set tier=S
- 2026-10-31T06:36:52Z planned: it has criteria and steps
- 2026-10-31T06:36:53Z focused
- 2026-10-31T06:39:15Z scope: plugin/tests/test_genesis.py
- 2026-10-31T06:39:56Z done
- 2026-10-31T06:39:58Z committed 4816eb6f (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2186 [FIX M, done, 3 steps] Wire the four verbs gen-1's missions name that no session path calls (fm genesis check's… — lesson: A reach check that reads words fails bo…
- T-2080 [FEATURE M, done, 4 steps] Genesis on the site: fm genesis export + a live interactive tower graph page, shipped to main — lesson: An export that feeds a public p…
- T-2147 [FIX M, done, 1 steps] Baseline red: `python3 plugin/tests/run.py` fails… — lesson: a new MASTER note bumps its group's map-table count; run test_docs after any M…
- decision 2026-10-30: [revisited: every capability genesis builds must be called] [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: python3…
## Regression test
none: the fix is to the test itself (a stale fixture verb); its red runs are fm check's (this task's capture) and ship67's scratch run (T-2286)
## Why not caught
T-2239's lane ran test_find and test_prove, not test_genesis, whose reach check reads fmfind's imports
## Lessons
- A test that pins the live import graph should pick its example from a leaf module, or every new import elsewhere breaks it
## Files touched
- plugin/tests/test_genesis.py
