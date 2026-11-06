---
id: T-0154
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmfriction.py, plugin/tests/test_friction.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-03T06:58:14Z
updated: 2026-10-03T06:59:22Z
base: 8dd13a711bdab26d82adbec1342b058b1129d8f7
base_tree: 5bfc12de3f1a50a6e623b4779a77bcef90567242
verified: strong
---
# Self-improvement pass waits at least 2 h after the last one, so it has friction to read
## Raw request
> Self-improvement pass waits at least 2 h after the last one, so it has friction to read
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] N closed tasks right after a pass aren't due; the same N with the last pass 2 h back are — verify with `python3 plugin/tests/run.py -p test_friction.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then fix
## Resume here
## Docs impact
CHANGELOG; MASTER loop paragraph
## Verification evidence
- `python3 plugin/tests/run.py -p test_friction.py` → ✗ exit 1 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Friction 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ab5bc1c78fc2] (2026-10-03T06:58:23Z)
- `python3 plugin/tests/run.py -p test_friction.py` → ✗ exit 1 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: Friction 1s) / FAILED (1 classes) [ran] [tree ab5bc1c78fc2] (2026-10-03T06:58:23Z)
- `python3 plugin/tests/run.py -p test_friction.py` → ✗ exit 1 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Friction 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 92260cf71fd2] (2026-10-03T06:58:33Z)
- `python3 plugin/tests/run.py -p test_friction.py` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Friction 1s) / OK [ran] [tree 92260cf71fd2] (2026-10-03T06:58:33Z)
- (ac 1) `python3 plugin/tests/run.py -p test_friction.py` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Friction 1s) / OK [ran] [tree d0f549a2acfd] (2026-10-03T06:59:22Z)
- (step 1) `python3 plugin/tests/run.py -p test_friction.py` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Friction 1s) / OK [ran] [tree d0f549a2acfd] (2026-10-03T06:59:22Z)
- (audit self) `self: one more condition in due(); a never-run project (no rsi_at) is unaffected; the trigger tests still pass; decision recorded` → no findings [tree d0f549a2acfd] (2026-10-03T06:59:22Z)
## Log
- 2026-10-03T06:58:14Z created
- 2026-10-03T06:58:14Z focused
- 2026-10-03T06:59:22Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- T-0152 [CLEAN S, done, 1 steps] drive_wait is logged once per wait, not on every Stop
- T-0018 [FEATURE L, done, 6 steps] Recursive Foreman self-improvement: 10 rounds, each a slate implemented test-first, audited and committed
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- similar finished tasks took 1–6 steps
- likely tests for the scope: plugin/tests/test_friction.py
## Files touched
- plugin/tests/test_friction.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmfriction.py
