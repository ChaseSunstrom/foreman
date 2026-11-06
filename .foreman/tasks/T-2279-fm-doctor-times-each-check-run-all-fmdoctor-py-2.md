---
id: T-2279
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T05:53:58Z
updated: 2026-10-31T08:48:53Z
builder_model: sonnet
base: fc6a417ae0d2e003e63cf4abdb6c0ed254680cb3
base_tree: 8f7f82f6f8b3ba34688f15c9d8f4ad6a5a864552
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T08:21:58Z
plan0_scope: []
verified: strong
---
# fm doctor times each check: ms on Result, the three slowest under -v and in --json
## Raw request
> fm doctor times each check: run_all (fmdoctor.py:2108-2168) runs ~60 checks with no per-check time, so 'fm doctor: 26s vs 15s' can't say which grew; add ms to Result and list the three slowest under -v and in --json
## Interpretation
Make fm doctor say which checks are slow: each check's wall time in ms on its Result, the three slowest under -v and in --json, so a doctor that grew from 15 s to 26 s names the cause.
## Assumptions (confidence)
## Acceptance criteria
- [x] Each doctor Result carries ms (wall time of its check), --json includes it per result plus a slowest list of three, and -v prints the three slowest with their ms; a slow stubbed check tops the list — verify with `python3 plugin/tests/run.py test_doctor`
- [x] fm doctor's own wall time doesn't grow by more than a few ms from the timing — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
Options: 1) wrap each check call in run_all with a timing helper that stamps ms on its Result(s); 2) a decorator on every check_* function; 3) profile run_all with cProfile under -v only. Choice 1: one place, covers checks that return lists, no edits to ~60 functions; cProfile can't name checks cleanly and costs time.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: a stubbed slow check is named first in --json slowest and in -v
2. [x] Time each check in run_all (wrap each call; keep the order and the results unchanged), add ms to Result, print and emit the slowest three
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_doctor 2>&1 | tail -8` → ✗ exit 1 · Ran 80 tests in 53.5s (29 classes, 16 at a time; slowest: ViewsRepair 41s, LockProbe 21s, Timing 21s) / FAILED (1 classes) [ran] [tree 59c67f3c66d8] (2026-10-31T08:24:03Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor 2>&1 | tail -8` → ✗ exit 1 · Ran 80 tests in 53.5s (29 classes, 16 at a time; slowest: ViewsRepair 41s, LockProbe 21s, Timing 21s) / FAILED (1 classes) [ran] [tree 59c67f3c66d8] (2026-10-31T08:24:03Z)
- (step 1) `python3 plugin/tests/run.py test_doctor` → ✗ exit 1 · Ran 80 tests in 61.3s (29 classes, 16 at a time; slowest: ViewsRepair 58s, LockProbe 33s, Timing 32s) / FAILED (1 classes) [ran] [tree 59c67f3c66d8] (2026-10-31T08:25:11Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor 2>&1 | tail -12` → ✗ exit 1 · Ran 80 tests in 71.8s (29 classes, 16 at a time; slowest: ViewsRepair 66s, Timing 47s, LockProbe 31s) / FAILED (2 classes) [ran] [tree 621ed923b785] (2026-10-31T08:26:57Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor 2>&1 | tail -12` → ✗ exit 1 · Ran 80 tests in 71.8s (29 classes, 16 at a time; slowest: ViewsRepair 66s, Timing 47s, LockProbe 31s) / FAILED (2 classes) [ran] [tree 621ed923b785] (2026-10-31T08:26:57Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor 2>&1 | grep -E "^(FAIL|ERROR)"` → ✗ exit 1 · FAILED (failures=1) / FAILED (2 classes) [ran] [tree 621ed923b785] (2026-10-31T08:28:18Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor 2>&1 | grep -E "^(FAIL|ERROR)"` → ✗ exit 1 · FAILED (failures=1) / FAILED (2 classes) [ran] [tree 621ed923b785] (2026-10-31T08:28:18Z)
- (step 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 80 tests in 37.2s (29 classes, 16 at a time; slowest: ViewsRepair 35s, LockProbe 19s, Command 10s) / OK [ran] [tree 8c647f8d8369] (2026-10-31T08:35:59Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_crash_hygiene test_doctor test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [63.98s] [ran] [tree 8c647f8d8369] (2026-10-31T08:37:51Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK)"` → ✗ exit 1 · Ran 82 tests in 32.1s (29 classes, 16 at a time; slowest: ViewsRepair 29s, LockProbe 20s, Command 9s) / FAILED (1 classes) [ran] [tree ca992dc891ad] (2026-10-31T08:40:43Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK)"` → ✗ exit 1 · Ran 82 tests in 32.1s (29 classes, 16 at a time; slowest: ViewsRepair 29s, LockProbe 20s, Command 9s) / FAILED (1 classes) [ran] [tree ca992dc891ad] (2026-10-31T08:40:43Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_crash_hygiene test_doctor test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [46.68s] [ran] [tree 9ccb14bb0757] (2026-10-31T08:42:27Z)
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 82 tests in 13.4s (29 classes, 16 at a time; slowest: ViewsRepair 12s, LockProbe 7s, Command 5s) / OK [ran] [tree c9aad6408591] (2026-10-31T08:47:37Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_edit_cards` → exit 0 · Ran 103 tests in 14.7s (34 classes, 16 at a time; slowest: ImportCards 14s, ViewsRepair 11s, EditCards 11s) / OK [ran] [tree c9aad6408591] (2026-10-31T08:47:53Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 82 tests in 6.5s (29 classes, 16 at a time; slowest: ViewsRepair 6s, LockProbe 3s, Timing 2s) / OK [ran] [tree 46811fc59d51] (2026-10-31T08:48:26Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 82 tests in 6.5s (29 classes, 16 at a time; slowest: ViewsRepair 6s, LockProbe 3s, Timing 2s) / OK [ran] [tree 46811fc59d51] (2026-10-31T08:48:26Z)
- (audit intent) `one fm-reviewer pass (intent, edge, maintainer): 2 MEDIUM (hook benchmark untimed so the slowest list missed the biggest cost; briefs and views rows always 0) and LOWs (0 vs unmeasured, dead list branch, -v format untested); all fixed test-first by the builder; I read the fixed diff` → a doctor that grew names its slow checks, including the hook benchmark, briefs and views, so '26 s vs 15 s' points at a cause [tree 46811fc59d51] (2026-10-31T08:48:26Z)
- (audit edge) `one fm-reviewer pass (intent, edge, maintainer): 2 MEDIUM (hook benchmark untimed so the slowest list missed the biggest cost; briefs and views rows always 0) and LOWs (0 vs unmeasured, dead list branch, -v format untested); all fixed test-first by the builder; I read the fixed diff` → unmeasured rows are None and skipped by slowest; a nested run_all restores in stack order; not thread-safe, commented, no caller threads [tree 46811fc59d51] (2026-10-31T08:48:26Z)
- (audit maintainer) `one fm-reviewer pass (intent, edge, maintainer): 2 MEDIUM (hook benchmark untimed so the slowest list missed the biggest cost; briefs and views rows always 0) and LOWs (0 vs unmeasured, dead list branch, -v format untested); all fixed test-first by the builder; I read the fixed diff` → one swap in run_all instead of edits at ~60 call sites; functools.wraps keeps inspect.getsource working [tree 46811fc59d51] (2026-10-31T08:48:26Z)
- (audit operator) `one fm-reviewer pass (intent, edge, maintainer): 2 MEDIUM (hook benchmark untimed so the slowest list missed the biggest cost; briefs and views rows always 0) and LOWs (0 vs unmeasured, dead list branch, -v format untested); all fixed test-first by the builder; I read the fixed diff` → overhead is ~60 perf_counter pairs, negligible by reading; no new output unless -v or --json [tree 46811fc59d51] (2026-10-31T08:48:26Z)
- (audit adversary) `one fm-reviewer pass (intent, edge, maintainer): 2 MEDIUM (hook benchmark untimed so the slowest list missed the biggest cost; briefs and views rows always 0) and LOWs (0 vs unmeasured, dead list branch, -v format untested); all fixed test-first by the builder; I read the fixed diff` → no new input; ms is a number [tree 46811fc59d51] (2026-10-31T08:48:26Z)
## Log
- 2026-10-31T05:53:58Z created
- 2026-10-31T08:20:07Z planned from capture
- 2026-10-31T08:21:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2279.builder.md
- 2026-10-31T08:21:56Z focused
- 2026-10-31T08:21:58Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T08:47:21Z merged worktree-agent-a8b00c8f64a012e77 (2 file(s))
- 2026-10-31T08:47:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8b00c8f64a012e77
- 2026-10-31T08:47:22Z focused
- 2026-10-31T08:48:20Z scope: plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, MASTER.md, CHANGELOG.md
- 2026-10-31T08:48:51Z done
- 2026-10-31T08:48:53Z committed 0d750042 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1462 [PERFORMANCE S, done, 2 steps] fm task finish names its slowest run
- T-1809 [FIX M, done, 4 steps] CI's macOS job names what makes it time out: run.py --deadline stops below each job's cap, killing and naming running classes; slowest clas…
- research T-1667-review: Verdict: changes needed.** One MEDIUM and one more MEDIUM-ish lead, both small to fix. I could only read files (no shell), so I did not run the t…
- decision 2026-10-23: Cause: hooks handed Claude the exact fm command each turn, so it never loaded the skill describing the step; descriptions used Foreman jargon or use…
- similar finished tasks took 2–4 steps
## Lessons
- Timing the calls you can see misses setup run before them: charge shared setup (the hook bench) to a row, or the slowest list names the wrong thing
## Plan gaps
- failed first: step 1 Red test: a stubbed slow check is named first in --json slowest and in -v
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- .fm-scratch/probe.py
- MASTER.md
- CHANGELOG.md
