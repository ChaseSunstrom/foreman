---
id: T-0149
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-03T06:52:17Z
updated: 2026-10-03T06:57:53Z
base: 801ed2d92943045455c1551421647c666aae8adb
base_tree: 83e42ab0502639ff18425384b92075b3a1e66fd1
verified: strong
---
# A passing criterion check run while a step is current also verifies that step
## Raw request
> Evidence nudge ignores auto-evidence: _auto_evidence tags a criterion's verify run as (ac N) (fmhooks.py:1007) but _evidence_gate asks has_evidence(step=N) (fmhooks.py:1172), so a step verified by its exact AC command still reads unverified — RSI pass 1, 32 nudges
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] after the criterion's exact verify command passes, a Stop claiming the step done is not nudged; a failing run verifies nothing — verify with `python3 plugin/tests/run.py -p test_hooks.py -k auto`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then fix
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- `python3 plugin/tests/run.py -p test_hooks.py -k AutoEvidence` → ✗ exit 1 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: AutoEvidence 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree bf92c62765bf] (2026-10-03T06:56:41Z)
- `python3 plugin/tests/run.py -p test_hooks.py -k AutoEvidence` → ✗ exit 1 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: AutoEvidence 1s) / FAILED (1 classes) [ran] [tree bf92c62765bf] (2026-10-03T06:56:41Z)
- `python3 plugin/tests/run.py -p test_hooks.py -k AutoEvidence` → ✗ exit 1 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: AutoEvidence 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 75d75df30bda] (2026-10-03T06:56:49Z)
- `python3 plugin/tests/run.py -p test_hooks.py -k AutoEvidence` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: AutoEvidence 1s) / OK [ran] [tree 75d75df30bda] (2026-10-03T06:56:49Z)
- (ac 1) `python3 plugin/tests/run.py -p test_hooks.py -k auto` → exit 0 · Ran 8 tests in 2.2s (3 classes, 16 at a time; slowest: Stop 2s, SessionStart 1s, AutonomyWords 0s) / OK [ran] [tree 5bfc12de3f1a] (2026-10-03T06:57:53Z)
- (step 1) `python3 plugin/tests/run.py -p test_hooks.py -k AutoEvidence` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: AutoEvidence 1s) / OK [ran] [tree 5bfc12de3f1a] (2026-10-03T06:57:53Z)
- (audit self) `self: only a passing run, only the current step, only when it has no evidence yet; the criterion tagging and failure path are unchanged; fm task step done still re-checks for a newer failed run` → no findings [tree 5bfc12de3f1a] (2026-10-03T06:57:53Z)
## Log
- 2026-10-03T06:52:17Z created
- 2026-10-03T06:56:29Z planned from capture
- 2026-10-03T06:56:29Z focused
- 2026-10-03T06:57:53Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research t0018-r1-adversary: ck add \"true\"` (a trivially-passing later gate), then `fm check --evidence T-1 --step N`. `fm check`'s own exit code is 1 (line 640, corre…
- research t0018-final-operator: Not directly related. I have sufficient evidence now. Let me finalize.
- T-0152 [CLEAN S, done, 1 steps] drive_wait is logged once per wait, not on every Stop
- the similar finished task took 1 steps
- start here (files T-0152 touched): CHANGELOG.md, plugin/lib/fmhooks.py, plugin/tests/test_hooks.py
- likely tests for the scope: plugin/tests/test_hooks.py
## Lessons
- Evidence is per step and per criterion; a check that proves both must be recorded for both
## Files touched
- plugin/tests/test_hooks.py
- CHANGELOG.md
- plugin/lib/fmhooks.py
