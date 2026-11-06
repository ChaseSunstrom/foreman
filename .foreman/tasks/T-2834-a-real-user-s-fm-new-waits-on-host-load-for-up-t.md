---
id: T-2834
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T19:26:14Z
updated: 2026-11-03T20:13:26Z
base: 50cfca437ef88cc4a205203323644b5af5e74e5e
base_tree: 9963cd4d79ca5629338e8b288ff84cfa5b4ba5c3
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T20:12:19Z
plan0_scope: []
verified: ok
unproven: [meaning, typed]
---
# A real user's fm new waits on host load for up to 600 s: its born step runs fm check,…
## Raw request
> FIX: a real user's fm new waits on host load for up to 600 s: its born step runs fm check, which calls wait_for_load (cli.py:4949, new.py:194 born), so scaffolding a project on a loaded machine stalls for minutes; the scaffold's first check should not wait (found by T-2822's builder)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] born's fm check runs with the load gate off (FOREMAN_LOAD_GATE=0), the rest of the env kept — verify with `python3 plugin/tests/run.py test_scaffold`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: born's fm check env carries FOREMAN_LOAD_GATE=0
2. [x] fix: born passes that env to its steps
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scaffold` → red: TypeError 'NoneType' not subscriptable, born passes no env so its fm check inherits the load gate [tree 33849e292d5f] (2026-11-03T20:12:43Z)
- (step 2) `python3 plugin/tests/run.py test_scaffold` → exit 0 · Ran 14 tests in 2.2s (4 classes, 16 at a time; slowest: BuildWhatIsMissing 2s, Born 0s, Codemod 0s) / OK [ran] [tree d2a16415edc5] [world 2f1906870a] (2026-11-03T20:12:56Z)
- `python3 plugin/tests/run.py test_scaffold` → ✗ exit 1 · Ran 14 tests in 3.3s (4 classes, 16 at a time; slowest: BuildWhatIsMissing 2s, Born 0s, Dev 0s) / FAILED (1 classes: test_scaffold.Born) (start tree + this task's tests) [ran] [tree d2a16415edc5] [world 2f1906870a] (2026-11-03T20:13:04Z)
- `python3 plugin/tests/run.py test_scaffold` → exit 0 · Ran 14 tests in 2.2s (4 classes, 16 at a time; slowest: BuildWhatIsMissing 2s, Born 0s, Codemod 0s) / OK [ran] [tree d2a16415edc5] [world 2f1906870a] (2026-11-03T20:13:04Z)
- (ac 1) `python3 plugin/tests/run.py test_scaffold` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:13:04Z [ran] [tree d2a16415edc5] [world 2f1906870a] (2026-11-03T20:13:10Z)
- (audit intent) `self: read born end to end; the env only adds FOREMAN_LOAD_GATE=0 to the inherited environment, so git identity, PATH and FOREMAN_* still reach the steps; wait_for_load and host_strain's load hold honour it, the memory hold stays` → fm new on a loaded machine scaffolds without the 300-600 s load wait; the project is still born green [tree d2a16415edc5] (2026-11-03T20:13:10Z)
- (audit edge) `self: read born end to end; the env only adds FOREMAN_LOAD_GATE=0 to the inherited environment, so git identity, PATH and FOREMAN_* still reach the steps; wait_for_load and host_strain's load hold honour it, the memory hold stays` → FOREMAN_LOAD_GATE already set by a sandbox caller is overwritten to 0, which is the same value; git init/commit ignore the var [tree d2a16415edc5] (2026-11-03T20:13:10Z)
- (audit adversary) `self: read born end to end; the env only adds FOREMAN_LOAD_GATE=0 to the inherited environment, so git identity, PATH and FOREMAN_* still reach the steps; wait_for_load and host_strain's load hold honour it, the memory hold stays` → no new exec or input; the env is the user's own plus one flag that only skips a wait [tree d2a16415edc5] (2026-11-03T20:13:10Z)
- (audit self) `self: read born end to end; the env only adds FOREMAN_LOAD_GATE=0 to the inherited environment, so git identity, PATH and FOREMAN_* still reach the steps; wait_for_load and host_strain's load hold honour it, the memory hold stays` → no findings [tree d2a16415edc5] (2026-11-03T20:13:10Z)
## Log
- 2026-11-03T19:26:14Z created
- 2026-11-03T20:12:18Z planned: it has criteria and steps
- 2026-11-03T20:12:18Z set tier=S
- 2026-11-03T20:12:18Z focused
- 2026-11-03T20:12:19Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T20:12:29Z criterion 1 verify: `python3 -m unittest -q plugin.tests.test_scaffold` → `python3 plugin/tests/run.py test_scaffold`
- 2026-11-03T20:13:25Z done
- 2026-11-03T20:13:26Z committed 643a52e8 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-1554 [FEATURE M, done, 6 steps] Round 3 (T-1520): Scaffolding and dev loop: fm new for projects born proven, fm dev as a w — lesson: Make a scaffold prove itself at bi…
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- decision 2026-10-31: [reverses: a later Mission's lane waits only for earlier-Mission lanes launched before it] Mission-order merging, revised: lanes that are ready merg…
## Why not caught
the born test runs on an unloaded test env; T-2822's sandbox audit covered sandboxes, not the user's own scaffold
## Lessons
- A user-facing command that runs fm check as a fixed self-test (born, demo) is not a gate competing for the machine: pass FOREMAN_LOAD_GATE=0 to it
## Files touched
- plugin/tests/test_scaffold.py
- plugin/lib/sampo/new.py
