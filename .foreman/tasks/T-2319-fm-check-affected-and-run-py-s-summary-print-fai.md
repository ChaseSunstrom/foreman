---
id: T-2319
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T11:07:33Z
updated: 2026-10-31T11:15:28Z
base: a1897c9f532e55a2377a33065bd4348ee8869519
base_tree: 8f3c67fda29cc507563b90b49809fab8a9a18368
plan0_at: 2026-10-31T11:13:18Z
plan0_scope: []
verified: strong
---
# run.py's summary line names the failing classes, so a red run says what failed in its last line
## Raw request
> fm check --affected (and run.py's summary) print 'FAILED (1 classes)' without naming the failing class or test, so a load-induced failure costs a full re-run to diagnose (T-2316's builder): name each failing class and its first failing test in the summary line
## Interpretation
run.py ends with 'FAILED (N classes)'; the class names sit in earlier ==== blocks that fm check's and evidence's tails cut, so a load-induced failure cost a full re-run to diagnose (T-2316's builder).
## Assumptions (confidence)
## Acceptance criteria
- [x] A red run's last line reads 'FAILED (N classes: mod.Class, ...)' naming up to 5 failing classes, then '+M more' — verify with `python3 plugin/tests/run.py test_run`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: a class asked to fail by an env var makes the summary name it; then name the failing classes in run.py's summary line
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_run -k last_line_names` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: UnknownNames 1s) / FAILED (1 classes) [ran] [tree d3bdba30bc64] (2026-10-31T11:13:28Z)
- `python3 plugin/tests/run.py test_run -k last_line_names` → ✗ exit 1 · Ran 1 tests in 3.5s (1 classes, 16 at a time; slowest: UnknownNames 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 0c5d4624a34a] (2026-10-31T11:13:42Z)
- `python3 plugin/tests/run.py test_run -k last_line_names` → exit 0 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: UnknownNames 1s) / OK [ran] [tree 0c5d4624a34a] (2026-10-31T11:13:42Z)
- (step 1) `python3 plugin/tests/run.py test_run test_bookkeeping test_bench test_recall` → exit 0 · Ran 154 tests in 55.0s (69 classes, 16 at a time; slowest: Bench 54s, Recall 34s, Judged 32s) / OK [ran] [tree 0c5d4624a34a] (2026-10-31T11:14:38Z)
- (ac 1) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 64 tests in 5.3s (36 classes, 16 at a time; slowest: Ship 5s, Ambient 5s, Hang 5s) / OK [ran] [tree a6ac7800886f] (2026-10-31T11:14:55Z)
- (audit intent) `self-review: the summary line keeps its 'FAILED (N classes' prefix (parsers matching FAILED ( still read it: test_bookkeeping, test_bench, test_recall pass) and adds up to five class ids, then +N more; the demo class fails only under its env var and skips otherwise` → the one line every tail keeps now says which classes failed [tree a6ac7800886f] (2026-10-31T11:14:55Z)
- (audit edge) `self-review: the summary line keeps its 'FAILED (N classes' prefix (parsers matching FAILED ( still read it: test_bookkeeping, test_bench, test_recall pass) and adds up to five class ids, then +N more; the demo class fails only under its env var and skips otherwise` → more than five failures read '+N more'; a not-started class (deadline) is named like any failure, as the ==== block lists it [tree a6ac7800886f] (2026-10-31T11:14:55Z)
- (audit self) `self-review: the summary line keeps its 'FAILED (N classes' prefix (parsers matching FAILED ( still read it: test_bookkeeping, test_bench, test_recall pass) and adds up to five class ids, then +N more; the demo class fails only under its env var and skips otherwise` → no findings [tree a6ac7800886f] (2026-10-31T11:14:55Z)
## Log
- 2026-10-31T11:07:33Z created
- 2026-10-31T11:13:16Z planned from capture
- 2026-10-31T11:13:17Z focused
- 2026-10-31T11:14:48Z scope: plugin/tests/run.py (summary line), plugin/tests/test_run.py, CHANGELOG.md
- 2026-10-31T11:15:25Z done
- 2026-10-31T11:15:28Z committed 022091b3 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1825 [FEATURE M, done, 3 steps] FEATURE: fm run (headless) skips a model call when the tree and the failing check's output — lesson: count list items by line start, no…
- T-1809 [FIX M, done, 4 steps] CI's macOS job names what makes it time out: run.py --deadline stops below each job's cap, killing and naming running classes; slowest clas…
- T-1769 [FIX S, done, 1 steps] A test runner's tally became the failure signature, so red-first runs read as a recurring obstacle
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (second): standing rule] Every user steer becomes a standing rule plus an automatic check in the same task, so t…
- similar finished tasks took 1–4 steps
## Lessons
- The last line of a tool's output is the only one guaranteed to be read: put the fact you'd act on there
## Plan gaps
- failed first: step 1 Red test: a class asked to fail by an env var makes the summary name it; then name the failing clas…
## Files touched
- plugin/tests/test_run.py
- plugin/tests/run.py
- CHANGELOG.md
