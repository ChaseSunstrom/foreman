---
id: T-2855
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T22:30:15Z
updated: 2026-11-03T22:41:51Z
base: f228f2c9cf89512c03d7587d1ba743979def8e89
base_tree: 4d989dd254ba13b64eef1b07b033e0c9de5ee66e
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T22:30:16Z
plan0_scope: []
verified: ok
unproven: [typed]
---
# Two tests red after today's renames: test_claims expects 'fm lease take' in a lane brief (T-2778 taught sampo spellings) and test_unattended expects the Next-followed key 'fm task step' (T-2845 keyed it by the bare words)
## Raw request
> Two tests red after today's renames: test_claims expects 'fm lease take' in a lane brief (T-2778 taught sampo spellings) and test_unattended expects the Next-followed key 'fm task step' (T-2845 keyed it by the bare words)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_claims and test_unattended pass; the Next-followed key keeps the spelling the Next line used — verify with `python3 plugin/tests/run.py test_claims test_unattended test_cost`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test_claims accepts the sampo spelling the builder contract now teaches
2. [x] cost.py keys Next-followed by the Next's own spelling, matching on the words after either program
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_claims test_unattended` → red: 'fm lease take' not in the brief; {'task step': 1} != {'fm task step': 1} [tree 4d989dd254ba] (2026-11-03T22:30:24Z)
- (step 2) `python3 plugin/tests/run.py test_claims test_unattended test_cost` → exit 0 · Ran 54 tests in 11.3s (14 classes, 16 at a time; slowest: Unattended 11s, Claims 9s, TaskCostCap 8s) / OK [ran] [tree 8136bffa2548] [world 2f1906870a] (2026-11-03T22:31:10Z)
- (ac 1) `python3 plugin/tests/run.py test_claims test_unattended test_cost` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T22:31:10Z [ran] [tree 8136bffa2548] [world 2f1906870a] (2026-11-03T22:31:11Z)
- (audit intent) `self: cost.py's Next-followed counter is keyed by the Next's own spelling (fm task step) and still matched on the words after either program; test_claims accepts either spelling of lease take, as the contract teaches sampo now; markers tie each test to the file it depends on` → the suite is green again after T-2778 and T-2845 [tree 8136bffa2548] (2026-11-03T22:31:11Z)
- (audit edge) `self: cost.py's Next-followed counter is keyed by the Next's own spelling (fm task step) and still matched on the words after either program; test_claims accepts either spelling of lease take, as the contract teaches sampo now; markers tie each test to the file it depends on` → a sampo-spelled Next is counted under 'sampo …', an fm one under 'fm …'; a run in either spelling follows either [tree 8136bffa2548] (2026-11-03T22:31:11Z)
- (audit adversary) `self: cost.py's Next-followed counter is keyed by the Next's own spelling (fm task step) and still matched on the words after either program; test_claims accepts either spelling of lease take, as the contract teaches sampo now; markers tie each test to the file it depends on` → test and analytics only [tree 8136bffa2548] (2026-11-03T22:31:11Z)
- (audit self) `self: cost.py's Next-followed counter is keyed by the Next's own spelling (fm task step) and still matched on the words after either program; test_claims accepts either spelling of lease take, as the contract teaches sampo now; markers tie each test to the file it depends on` → no findings [tree 8136bffa2548] (2026-11-03T22:31:11Z)
## Log
- 2026-11-03T22:30:15Z created
- 2026-11-03T22:30:15Z focused
- 2026-11-03T22:30:16Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T22:31:35Z done
- 2026-11-03T22:31:36Z committed 363b6c3f (3 files)
- 2026-11-03T22:41:51Z includes T-2854: Baseline red: `python3 plugin/tests/run.py` fails…
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2845 [FEATURE M, done, 2 steps] Every parser that reads typed commands or goals accepts sampo as well as fm (cost, repeats, friction, bench, long, smithtui, smith, man…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
## Regression test
none separate: the two failing tests are the regression tests; red recorded at step 1, green at step 2; map-links markers now tie them to cost.py and the builder contract so --affected runs them
## Why not caught
neither test was linked to the file it depends on (cost.py, plugin/agents/fm-builder.md), so the closes' --affected runs skipped them
## Lessons
- A behaviour test that reads a file's output or text through another verb names that file on a map-links line
## Files touched
- plugin/lib/sampo/cost.py
- plugin/tests/test_claims.py
- plugin/tests/test_unattended.py
