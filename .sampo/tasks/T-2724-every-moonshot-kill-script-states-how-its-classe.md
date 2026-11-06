---
id: T-2724
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T23:25:02Z
updated: 2026-11-02T23:26:58Z
base: 4992e2d2a78993ffc29fafeaac12af32e1b618fd
base_tree: 767472890410b1bfafd1f0c8ebcc9f972e1102c7
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-02T23:25:04Z
plan0_scope: []
verified: strong
---
# every moonshot kill script states how its classes or cases are drawn (a 'Sample' line in its docstring) before it runs, held by test_moonshot_bench
## Raw request
> every moonshot kill script states how its classes or cases are drawn (a 'Sample' line in its docstring) before it runs, held by test_moonshot_bench
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_moonshot_bench fails for a kill script whose docstring names no Sample — verify with `python3 plugin/tests/run.py test_moonshot_bench`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the test and kill_m02's Sample line
## Resume here
## Docs impact
none: a repo test and a docstring
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_moonshot_bench` → exit 0 · Ran 3 tests in 0.5s (1 classes, 16 at a time; slowest: MoonshotBench 0s) / OK [ran] [tree 9e8cae51c4ca] [world 2f1906870a] (2026-11-02T23:25:21Z)
- (ac 1) `python3 plugin/tests/run.py test_moonshot_bench` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:25:21Z [ran] [tree 9e8cae51c4ca] [world 2f1906870a] (2026-11-02T23:25:23Z)
- (audit edge) `the test parses each kill script's docstring and needs a line starting 'Sample' with a colon; kill_m12 already had one (run 2 on), kill_m02 now names its fixed three modules` → a script with no docstring fails by name; the regex allows 'Sample (run 2 on):' [tree 9e8cae51c4ca] (2026-11-02T23:25:23Z)
- (audit self) `the test parses each kill script's docstring and needs a line starting 'Sample' with a colon; kill_m12 already had one (run 2 on), kill_m02 now names its fixed three modules` → no findings [tree 9e8cae51c4ca] (2026-11-02T23:25:23Z)
## Log
- 2026-11-02T23:25:02Z created
- 2026-11-02T23:25:03Z focused
- 2026-11-02T23:25:04Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-02T23:25:20Z scope: bench/moonshot/kill_m02.py (its Sample line), plugin/tests/test_moonshot_bench.py
- 2026-11-02T23:26:54Z done
- 2026-11-02T23:26:58Z committed 33a6416b (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2687 [RESEARCH M, done, 2 steps] M-12 kill test (moonshot spike, gen 3): does a log-weighted pool of three blind forecasters beat the best one on whether a close survi…
- T-2721 [FEATURE S, done, 1 steps] every kill script in bench/moonshot has its result file beside it with a verdict, held by a test
- T-2719 [FIX S, dropped, 3 steps] bench/moonshot keeps verdicts only: M-02's result beside its script, the confounded M-12 run removed
- decision 2026-11-02: [revisited: the moonshot campaign is not queued behind DONE-WHEN] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into each gen of the to…
- similar finished tasks took 1–2 steps
## Files touched
- bench/moonshot/kill_m02.py
- plugin/tests/test_moonshot_bench.py
