---
id: T-2733
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-03T00:20:05Z
updated: 2026-11-03T00:31:53Z
base: 8170d5d31ca2b860ba101f195c72c7ace03281f0
base_tree: 9e6b321042eb5bfe1ce98b66a9aa0dd76fc1e40d
plan0_at: 2026-11-03T00:29:41Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# fm friction splits failed Bash calls by program and leaves out a leading grep, test or diff whose exit 1 only means 'no', so real failures (fm 33, python3 26) aren't buried in one 'Exit code 1' bucket
## Raw request
> fm friction groups failed Bash calls by the first 90 chars of the error (fmfriction.py:175), so every exit 1 (mostly a grep that found nothing) is one bucket that outranks real friction; key Bash failures by the command's first word too
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] failed Bash calls group as 'Bash fm', 'Bash python3' and so on, and a grep's exit 1 is not listed — verify with `python3 plugin/tests/run.py test_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the per-program key
## Resume here
## Docs impact
none: the friction digest's own grouping
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_friction test_ideas test_night` → exit 0 · Ran 91 tests in 12.8s (22 classes, 16 at a time; slowest: Ideas 12s, Friction 12s, Night 11s) / OK [ran] [tree 2afdc5b2d3e3] [world 2f1906870a] (2026-11-03T00:30:54Z)
- (step 2) `python3 plugin/tests/run.py test_friction test_ideas test_night` → exit 0 · Ran 91 tests in 15.8s (22 classes, 16 at a time; slowest: Friction 15s, Ideas 15s, Night 14s) / OK [ran] [tree 2afdc5b2d3e3] [world 2f1906870a] (2026-11-03T00:31:10Z)
- (ac 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 21 tests in 12.5s (5 classes, 16 at a time; slowest: Friction 12s, UserPromptSubmit 1s, BoardIdeas 0s) / OK [ran] [tree 2afdc5b2d3e3] [world 2f1906870a] (2026-11-03T00:31:25Z)
- `python3 plugin/tests/run.py test_friction test_ideas test_night` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:31:10Z [ran] [tree 2afdc5b2d3e3] [world 2f1906870a] (2026-11-03T00:31:25Z)
- (audit edge) `failed Bash calls key on 'Bash <program>' past leading cd and VAR= words; a leading grep, rg, test, [, diff or cmp whose error is 'Exit code 1' is left out; on this machine's events that splits 33 fm and 26 python3 exit-1s from 14 grep no-matches` → a grep piped into another program exits with the last program's code, so only a leading grep's own exit 1 is dropped; any other grep exit (2: an error) still counts [tree 2afdc5b2d3e3] (2026-11-03T00:31:25Z)
- (audit self) `failed Bash calls key on 'Bash <program>' past leading cd and VAR= words; a leading grep, rg, test, [, diff or cmp whose error is 'Exit code 1' is left out; on this machine's events that splits 33 fm and 26 python3 exit-1s from 14 grep no-matches` → no findings [tree 2afdc5b2d3e3] (2026-11-03T00:31:25Z)
## Log
- 2026-11-03T00:20:05Z created
- 2026-11-03T00:29:39Z planned from capture
- 2026-11-03T00:29:40Z focused
- 2026-11-03T00:30:40Z scope: plugin/tests/test_friction.py
- 2026-11-03T00:31:51Z done
- 2026-11-03T00:31:53Z committed ee300ad7 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Shell script errors (bash -n, ShellCheck, bats) (fm playbooks show build/shell-build)
- T-2613 [FEATURE M, done, 4 steps] fm exam long grade splits false dones into misses on names the goal never states and real misses — lesson: When an automatic rule repla…
- research T-2125-review: Verdict:** approve with nits. I found no HIGH issues. There are three MEDIUM design gaps worth fixing or capturing, plus some LOW nits. I did not…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
## Behaviour lock
test_friction's existing cases (Read failures grouped by cause, background waits, downstream labels) pass unchanged; only Bash keys gain the program
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/fmfriction.py
