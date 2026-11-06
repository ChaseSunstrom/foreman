---
id: T-0857
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T14:05:01Z
updated: 2026-10-15T14:08:21Z
base: 381720db5585e72c8e15de0996b1d0e7713e712c
base_tree: c43a546d55356ae901d3c8195d67cb09b33f4993
verified: strong
---
# fm repeats never suggests a narrowed test run (one file, -k, -p) as a gate for every task
## Raw request
> fm repeats never suggests a narrowed test run (one file, -k, -p) as a gate for every task
## Interpretation
fm repeats on this repo suggested fm check add 'python3 -m unittest … -p test_diff_gates.py -k dirty' and single test modules as gates for every task: advice that would slow every close and test the wrong thing.
## Assumptions (confidence)
## Acceptance criteria
- [x] a repeated narrowed run is reported as part of an existing gate or as a script, never as fm check add; a repeated whole-suite run still is — verify with `python3 plugin/tests/run.py test_repeats`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then the narrowing check in suggest
## Resume here
## Docs impact
none
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_repeats` → exit 0 · Ran 10 tests in 10.3s (3 classes, 16 at a time; slowest: Repeats 10s, Bench 1s, Playbook 1s) / OK [ran] [tree 28ac020d939b] (2026-10-15T14:05:58Z)
- `python3 plugin/tests/run.py test_repeats` → ✗ exit 1 · Ran 10 tests in 10.4s (3 classes, 16 at a time; slowest: Repeats 10s, Bench 1s, Playbook 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 28ac020d939b] (2026-10-15T14:06:19Z)
- `python3 plugin/tests/run.py test_repeats` → exit 0 · Ran 10 tests in 10.3s (3 classes, 16 at a time; slowest: Repeats 10s, Bench 1s, Playbook 1s) / OK [ran] [tree 28ac020d939b] (2026-10-15T14:06:19Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmrepeats.py — commit it through a task, or git checkout it back / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.8    38.8     150  [0] / SessionEnd                  30.2    32.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/forema [ran] [tree 28ac020d939b] (2026-10-15T14:08:02Z)
- (ac 1) `python3 plugin/tests/run.py test_repeats` → exit 0 · Ran 10 tests in 10.2s (3 classes, 16 at a time; slowest: Repeats 10s, Bench 1s, Playbook 1s) / OK [ran] [tree 28ac020d939b] (2026-10-15T14:08:20Z)
- (audit edge) `self: narrowed runs (one test file/module, -k/-p/-t filters, ::) never become 'fm check add'; when a habit holds both kinds, the whole-suite run is the example; live: this repo's repeats now offer 'python3 -m unittest discover -s plugin/tests -q', not a -k filter` → a whole-suite command whose path contains test_ (e.g. tests/test_all.sh) counts as narrow and is offered as a script instead — conservative, never a wrong gate [tree 28ac020d939b] (2026-10-15T14:08:20Z)
- (audit self) `self: narrowed runs (one test file/module, -k/-p/-t filters, ::) never become 'fm check add'; when a habit holds both kinds, the whole-suite run is the example; live: this repo's repeats now offer 'python3 -m unittest discover -s plugin/tests -q', not a -k filter` → no findings [tree 28ac020d939b] (2026-10-15T14:08:20Z)
## Log
- 2026-10-15T14:05:01Z created
- 2026-10-15T14:05:01Z focused
- 2026-10-15T14:08:21Z done
- 2026-10-15T14:08:21Z committed 011ff34 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261009-091631.pack: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just sim…
- research t0023-grounding: Ledger events (this project, ~700 events): step_done 66, step_add 64, task_set 61, ac_check 58, audit 37, subagent 35,
- research mission-20261009-091631: Request: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just…
- decision 2026-10-09: T-0672 L self-approved: every member only adds checks or logging; replay at close proves nothing is newly allowed
## Why not caught
none: found reading fm repeats' output during round 4
## Lessons
- Advice a tool gives must be checked against the real data it runs on, not only the fixtures
## Files touched
- plugin/tests/test_repeats.py
- plugin/lib/fmrepeats.py
