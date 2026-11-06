---
id: T-2272
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T04:52:09Z
updated: 2026-10-31T05:25:49Z
base: ea94b84a3d36b79c6210eca853a6f8d4546a6455
base_tree: 5e3e10e7e98a23803decf1425907a80eb100efa1
plan0_at: 2026-10-31T04:53:30Z
plan0_scope: []
verified: strong
---
# Signal-to-fix loop (Mission 8, #7): a failure signature that recurs across 3+ tasks with no finished task that met it becomes one root-cause FIX task
## Raw request
> Signal-to-fix loop (Mission 8, #7): a failure signature that recurs across 3+ tasks with no finished task that met it becomes one root-cause FIX task
## Interpretation
Gap map #7: failures.jsonl feeds hints only (a pointer to a task that met the failure, a thrash nudge within one task). A failure that keeps biting different tasks is a defect in the project or its tooling, yet nothing turns that signal into a fix; each task works around it again.
## Assumptions (confidence)
## Acceptance criteria
- [x] note_failure captures one FIX (source discovered) when the same signature, carrying an error word and not a test runner's tally, is in failures.jsonl under 3+ distinct tasks, whether or not one closed (working around a failure isn't fixing it); never twice for one signature (keyed once ever); a tally or a word with no error ('failed (3 classes)', 'guard-publish') never captures; the note names the captured task — verify with `python3 plugin/tests/run.py test_recall`
## Non-goals
## Approach (options → choice → why)
1) in fmrecall.note_failure, after the append: count distinct non-null tasks with this signature in the kept records; at 3+, with an error word in the signature (the _ERROR_LINE pattern) and no seen_before hint, fmeco.capture_once a FIX 'Recurring failure across N tasks: <sig>' (plained, fitted, redacted) naming the tasks, so the root cause is fixed once. 2) a nightly sweep (fmnight) over failures.jsonl — rejected: a day late, and the hook already holds the record. 3) count raw occurrences — rejected: one task's red-first runs would trigger it. Choice 1.
## Risks and rollback
A noisy environment failure (a flaky network) recurring across tasks files one FIX; that's the right signal (fix or mark it flaky). The capture is once per signature, so no flood.
## Execution prompt
## Steps
1. [x] red tests: 3 tasks with one signature capture once; 2 don't; a met signature doesn't; junk signatures don't
2. [x] the capture in fmrecall.note_failure, with the signature plained and fitted
3. [x] docs: MASTER failure memory line, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T05:24:06Z step 1/3: red tests: 3 tasks with one signature capture once; 2 don't; a met signature doesn't; junk signatures don't
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmrecall.py, plugin/tests/test_recall.py
- touched since last checkpoint: plugin/lib/fmrecall.py, plugin/tests/test_recall.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_recall` → ✗ exit 1 · Ran 21 tests in 36.191s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 536de8beec45] (2026-10-31T05:23:07Z)
- `cd plugin/tests && python3 -m unittest -q test_recall` → exit 0 · Ran 21 tests in 39.136s / OK [ran] [tree 536de8beec45] (2026-10-31T05:23:07Z)
- (step 1) `python3 plugin/tests/run.py test_recall test_docs` → exit 0 · Ran 107 tests in 22.6s (32 classes, 16 at a time; slowest: Recall 22s, Fences 10s, OtherProjects 8s) / OK [ran] [tree de8837abb0e0] (2026-10-31T05:24:34Z)
- (step 2) `python3 plugin/tests/run.py test_recall test_docs` → exit 0 · Ran 107 tests in 27.8s (32 classes, 16 at a time; slowest: Recall 27s, Fences 11s, OtherProjects 9s) / OK [ran] [tree de8837abb0e0] (2026-10-31T05:25:02Z)
- (step 3) `grep -c T-2272 MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:1 [ran] [tree de8837abb0e0] (2026-10-31T05:25:03Z)
- (ac 1) `python3 plugin/tests/run.py test_recall` → exit 0 · Ran 25 tests in 15.0s (10 classes, 16 at a time; slowest: Recall 15s, OtherProjects 5s, Consolidate 3s) / OK [ran] [tree de8837abb0e0] (2026-10-31T05:25:18Z)
- (audit intent) `self + one fm-reviewer pass (3 medium, 1 low, all fixed with tests); checked against the real failures.jsonl: the six signatures spanning 3+ tasks today are tallies, Foreman's own messages or bare builtin exceptions, now all skipped` → an obstacle hitting 3+ tasks becomes one root-cause FIX, closed tasks included (test_recall red-to-green) [tree de8837abb0e0] (2026-10-31T05:25:18Z)
- (audit adversary) `self + one fm-reviewer pass (3 medium, 1 low, all fixed with tests); checked against the real failures.jsonl: the six signatures spanning 3+ tasks today are tallies, Foreman's own messages or bare builtin exceptions, now all skipped` → the signature is redacted (failure_signature), plained, fitted and defanged before it enters a task [tree de8837abb0e0] (2026-10-31T05:25:18Z)
- (audit edge) `self + one fm-reviewer pass (3 medium, 1 low, all fixed with tests); checked against the real failures.jsonl: the six signatures spanning 3+ tasks today are tallies, Foreman's own messages or bare builtin exceptions, now all skipped` → once ever per signature (key line, archive searched); a captured row in failures.jsonl spares later hooks the brief scan; a lock timeout keeps the other hints [tree de8837abb0e0] (2026-10-31T05:25:18Z)
## Log
- 2026-10-31T04:52:09Z created
- 2026-10-31T04:53:29Z focused
- 2026-10-31T04:54:40Z criterion 1 text: note_failure captures one FIX (source discovered, priority normal) when the same signature, carrying an error word, is in failures.jsonl under 3+ distinct tasks and seen_before finds no done task that met it; never twice for one signature (an open or done capture blocks it); a tally or a bare word ('0 total', 'guard-publish') never captures → note_failure captures one FIX (source discovered) when the same signature, carrying an error word and not a test runner's tally, is in failures.jsonl under 3+ distinct tasks, whether or not one closed (working around a failure isn't fixing it); never twice for one signature (keyed once ever); a tally or a word with no error ('failed (3 classes)', 'guard-publish') never captures; the note names the captured task
- 2026-10-31T04:57:49Z paused: focus moved to T-2268
- 2026-10-31T05:21:14Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T05:21:14Z focused
- 2026-10-31T05:25:03Z scope: plugin/lib/fmrecall.py (_recurring), plugin/tests/test_recall.py, MASTER.md, CHANGELOG.md
- 2026-10-31T05:25:47Z done
- 2026-10-31T05:25:49Z committed a9231d93 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2270 [FEATURE M, planned, 3 steps] Capability-miss trigger (Mission 6, #5): a missing command or module names the find-or-build path once per session, and a tool missi…
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- decision 2026-10-30: [cites: user steer 2026-10-30] Standing rule (user steer): weakness-finding uses signals Foreman didn't author — outcome survival (fm outcomes: reve…
## Lessons
- A recurrence trigger needs its noise filter tuned on the real log first: the obvious threshold alone would have filed six FIX tasks with no single cause
## Files touched
- plugin/tests/test_recall.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmmap.py
- plugin/tests/test_dirty_at_focus.py
