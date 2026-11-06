---
id: T-2838
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T20:34:37Z
updated: 2026-11-03T21:04:36Z
base: 360ccb14737a437f4bd3f9f21fea567a12b2d3a8
base_tree: 3888ef3c580478f668355f66244ff2429bf113cd
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T21:02:07Z
plan0_scope: []
verified: ok
unproven: [typed]
---
# A test that counts calls in other modules (test_core.SandboxEnv reads…
## Raw request
> FIX: a test that counts calls in other modules (test_core.SandboxEnv reads demo/drill/bench/long/louhi/smithbench sources) has no map link to them, so a close editing louhi.py or long.py never runs it (T-2835 broke it unseen); let a test name the modules it guards (a string literal module name under the lib folder, or an explicit marker) so fm check --affected runs it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a test file may name the files it guards on a '# map-links: PATH …' line; fm map links it to each named tracked file, so fm check --affected runs test_core when louhi.py or long.py changes — verify with `python3 plugin/tests/run.py test_map test_affected_hubs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: a marker line links its test to the named files; an untracked name is ignored
2. [x] map reads the marker (VERSION bump); test_core's SandboxEnv names its six modules
## Resume here
## Docs impact
none: the marker is documented where the map reads it and at its first use
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_map` → red: AssertionError: None != ['src/report.py'] (a '# map-links:' line links nothing) [tree f29da2c57fba] (2026-11-03T21:02:52Z)
- (step 2) `python3 plugin/tests/run.py test_map test_affected_hubs test_core` → green: OK; fm impact plugin/lib/sampo/louhi.py names test_core.py [tree 49aa9eb40480] (2026-11-03T21:03:42Z)
- `python3 plugin/tests/run.py test_map` → ✗ exit 1 · Ran 11 tests in 7.1s (3 classes, 16 at a time; slowest: Map 5s, Cold 1s, RoundG 0s) / FAILED (1 classes: test_map.Map) (start tree + this task's tests) [ran] [tree 49aa9eb40480] [world 2f1906870a] (2026-11-03T21:03:56Z)
- `python3 plugin/tests/run.py test_map` → exit 0 · Ran 11 tests in 5.0s (3 classes, 16 at a time; slowest: Map 5s, Cold 0s, RoundG 0s) / OK [ran] [tree 49aa9eb40480] [world 2f1906870a] (2026-11-03T21:03:56Z)
- (ac 1) `python3 plugin/tests/run.py test_map test_affected_hubs` → exit 0 · Ran 15 tests in 5.1s (4 classes, 16 at a time; slowest: Map 5s, AffectedHubs 3s, Cold 1s) / OK [ran] [tree 49aa9eb40480] [world 2f1906870a] (2026-11-03T21:04:02Z)
- `python3 plugin/tests/run.py test_map` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T21:03:56Z [ran] [tree 49aa9eb40480] [world 2f1906870a] (2026-11-03T21:04:02Z)
- (audit intent) `self: map.build adds each tracked path a test names on a '# map-links:' line (untracked names dropped); VERSION 13 rebuilds old maps; the churn filter's set(files) is built once instead of per log line; test_core's SandboxEnv names its six modules` → a source-reading test runs on --affected when the files it reads change (the gap that let T-2835 break test_core unseen) [tree 49aa9eb40480] (2026-11-03T21:04:02Z)
- (audit edge) `self: map.build adds each tracked path a test names on a '# map-links:' line (untracked names dropped); VERSION 13 rebuilds old maps; the churn filter's set(files) is built once instead of per log line; test_core's SandboxEnv names its six modules` → a marker naming a missing or untracked file links nothing; several marker lines add up; a marker in a non-test file is never read (only test files are scanned) [tree 49aa9eb40480] (2026-11-03T21:04:02Z)
- (audit adversary) `self: map.build adds each tracked path a test names on a '# map-links:' line (untracked names dropped); VERSION 13 rebuilds old maps; the churn filter's set(files) is built once instead of per log line; test_core's SandboxEnv names its six modules` → reads test files the map already opens; paths are compared against git ls-files, never opened or run [tree 49aa9eb40480] (2026-11-03T21:04:02Z)
- (audit self) `self: map.build adds each tracked path a test names on a '# map-links:' line (untracked names dropped); VERSION 13 rebuilds old maps; the churn filter's set(files) is built once instead of per log line; test_core's SandboxEnv names its six modules` → no findings [tree 49aa9eb40480] (2026-11-03T21:04:02Z)
## Log
- 2026-11-03T20:34:37Z created
- 2026-11-03T21:02:06Z planned: it has criteria and steps
- 2026-11-03T21:02:06Z set tier=S
- 2026-11-03T21:02:06Z focused
- 2026-11-03T21:02:07Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T21:04:33Z done
- 2026-11-03T21:04:36Z committed 2c21833e (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
## Why not caught
map links come from names and folders only; nothing let a test declare what it reads
## Lessons
- A test that guards other files by reading them as text declares them on a '# map-links:' line
## Files touched
- plugin/tests/test_map.py
- plugin/lib/sampo/map.py
- plugin/tests/test_core.py
