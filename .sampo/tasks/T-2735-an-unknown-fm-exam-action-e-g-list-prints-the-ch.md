---
id: T-2735
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-03T00:20:06Z
updated: 2026-11-03T00:34:11Z
base: ee300ad78647f71b2195c8f6c79bbee86edff47d
base_tree: 2afdc5b2d3e36dd63ac8262a2c59114bf638b30b
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-03T00:32:21Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# an unknown action that means 'list' (list, ls) points at the parser's listing action (fm exam list → did you mean runs?), since difflib alone finds nothing that close
## Raw request
> an unknown fm exam action (e.g. 'list') prints the choices but no nearest match; name the closest one (runs or status) as the CLI does for verbs
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam list ends with 'did you mean runs?' — verify with `python3 plugin/tests/run.py test_gate_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the synonym step
## Resume here
## Docs impact
none: an error hint
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 12 tests in 2.3s (2 classes, 16 at a time; slowest: Typos 2s, Flakes 1s) / OK [ran] [tree 275e5580cca9] [world 2f1906870a] (2026-11-03T00:32:56Z)
- (step 2) `python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 12 tests in 2.3s (2 classes, 16 at a time; slowest: Typos 2s, Flakes 1s) / OK [ran] [tree 275e5580cca9] [world 2f1906870a] (2026-11-03T00:32:59Z)
- `python3 plugin/tests/run.py test_gate_friction` → ✗ exit 1 · Ran 12 tests in 3.4s (2 classes, 16 at a time; slowest: Typos 2s, Flakes 1s) / FAILED (1 classes: test_gate_friction.Typos) (start tree + this task's tests) [ran] [tree 275e5580cca9] [world 2f1906870a] (2026-11-03T00:33:07Z)
- `python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 12 tests in 3.7s (2 classes, 16 at a time; slowest: Typos 3s, Flakes 3s) / OK [ran] [tree 275e5580cca9] [world 2f1906870a] (2026-11-03T00:33:07Z)
- (ac 1) `python3 plugin/tests/run.py test_gate_friction` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:33:07Z [ran] [tree 275e5580cca9] [world 2f1906870a] (2026-11-03T00:33:33Z)
- `python3 plugin/tests/run.py test_gate_friction test_cli` → exit 0 · Ran 157 tests in 23.9s (46 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 12s, StateViews 12s) / OK [ran] [tree 275e5580cca9] [world 2f1906870a] (2026-11-03T00:33:33Z)
- (audit edge) `an invalid 'list' or 'ls' with no spelling match now names the first of list, runs, status, show that the parser offers; fm exam list ends with 'did you mean runs?'; difflib and FOLDED still come first` → a parser offering none of the four says nothing new; 'list' typed where a real 'list' choice exists never errors at all [tree 275e5580cca9] (2026-11-03T00:33:33Z)
- (audit self) `an invalid 'list' or 'ls' with no spelling match now names the first of list, runs, status, show that the parser offers; fm exam list ends with 'did you mean runs?'; difflib and FOLDED still come first` → no findings [tree 275e5580cca9] (2026-11-03T00:33:33Z)
## Log
- 2026-11-03T00:20:06Z created
- 2026-11-03T00:32:20Z planned from capture
- 2026-11-03T00:32:20Z focused
- 2026-11-03T00:32:21Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-03T00:32:53Z scope: plugin/tests/test_gate_friction.py
- 2026-11-03T00:34:09Z done
- 2026-11-03T00:34:11Z committed fc60bb35 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1170 [FIX S, done, 2 steps] An unknown fm command prints argparse's full list of 170 choices (and a poor 'did you mean
- playbook CLI errors and argument shape (fm playbooks show fix/cli-errors)
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: pending T-2184] Standing rule: every capability Genesis builds must…
- similar finished tasks took 1–2 steps
- start here (files T-1170 touched): plugin/tests/test_gate_friction.py, plugin/lib/fmcli.py, CHANGELOG.md
## Files touched
- plugin/tests/test_gate_friction.py
- plugin/lib/fmcli.py
