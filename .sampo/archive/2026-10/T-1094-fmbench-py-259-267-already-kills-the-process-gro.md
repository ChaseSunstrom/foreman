---
id: T-1094
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmbench.py, plugin/lib/fmserve.py, plugin/lib/fmmutate.py, plugin/lib/fmideas.py, plugin/tests/test_core.py]
depends_on: []
source: discovered
created: 2026-10-16T04:22:34Z
updated: 2026-10-16T06:53:10Z
base: e935d9f95adbfff315085a878f79a0254abdc9c6
base_tree: 8f493b98091fe211512984714951dc8bb85288f6
verified: strong
---
# Fmbench.py:259-267` already kills the process group on timeout, but `fmserve.py:466` and `
## Raw request
> fmbench.py:259-267` already kills the process group on timeout, but `fmserve.py:466` and `fmsession.py:436` each hand-roll their own `killpg`. A shared group-kill helper would remove the duplication
> (noticed by an agent; research wave1-plan-a306a171bb6861f90)
## Interpretation
Five places kill a child's process group with their own try/except (fmcore.run_command, fmbench's claude run, fmserve._stop, fmmutate._sh, fmideas._reap); fmbench's has no except, so a child that exited between the timeout and the kill raises ProcessLookupError and crashes the bench. One helper, c.kill_group(proc): SIGKILL the group, the leader alone if the group is gone, never raising. fmsession's TERM-then-KILL and fmideas' registry sweep (a pid, not a Popen) keep their own logic.
## Assumptions (confidence)
## Acceptance criteria
- [x] c.kill_group kills a child's whole group, and on a child that already exited it neither raises nor kills anything else; the five callers use it — verify with `python3 plugin/tests/run.py test_core test_bench test_serve test_replay test_ideas`
## Non-goals
## Approach (options → choice → why)
Options: (a) leave the copies, fix only fmbench's missing except; (b) one c.kill_group(proc) beside run_command, used by the five Popen callers. Choice: (b): the fmbench crash shows the copies drift; the helper is four lines in the module every caller already imports.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test for kill_group, then route the five callers through it
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core` → ✗ exit 1 · Ran 68 tests in 30.7s (16 classes, 16 at a time; slowest: RunCommand 30s, PreToolUse 3s, WritesAndLocks 2s) / FAILED (1 classes) [ran] [tree 84c1786b2d0d] (2026-10-16T06:49:35Z)
- (step 1) `python3 plugin/tests/run.py test_core test_bench test_serve test_replay test_ideas` → exit 0 · Ran 149 tests in 55.1s (36 classes, 16 at a time; slowest: Bench 54s, Judged 44s, Run 33s) / OK [ran] [tree 98ed79214bf4] (2026-10-16T06:50:52Z)
- (ac 1) `python3 plugin/tests/run.py test_core test_bench test_serve test_replay test_ideas` → exit 0 · Ran 149 tests in 60.7s (36 classes, 16 at a time; slowest: Bench 60s, Judged 41s, Run 25s) / OK [ran] [tree 5db6aef57049] (2026-10-16T06:52:03Z)
- (audit intent) `self: helper tested on a live group (its sleeping child dies) and on finished children (no raise); five callers' suites unchanged and green` → one tested way to kill a child's group [tree 5db6aef57049] (2026-10-16T06:52:03Z)
- (audit adversary) `self: helper tested on a live group (its sleeping child dies) and on finished children (no raise); five callers' suites unchanged and green` → killpg on proc.pid only for children started with start_new_session; fmideas keeps its returncode guard so a reused pid is never signalled [tree 5db6aef57049] (2026-10-16T06:52:03Z)
- (audit edge) `self: helper tested on a live group (its sleeping child dies) and on finished children (no raise); five callers' suites unchanged and green` → an exited child neither raises nor takes another group; fmbench's unguarded copy (a crash) is gone [tree 5db6aef57049] (2026-10-16T06:52:03Z)
- (audit operator) `self: helper tested on a live group (its sleeping child dies) and on finished children (no raise); five callers' suites unchanged and green` → no behaviour change to timeouts or draining [tree 5db6aef57049] (2026-10-16T06:52:03Z)
- (audit maintainer) `self: helper tested on a live group (its sleeping child dies) and on finished children (no raise); five callers' suites unchanged and green` → fmsession's TERM-then-KILL and fmideas' registry sweep (pids, not Popens) deliberately keep their own code [tree 5db6aef57049] (2026-10-16T06:52:03Z)
## Log
- 2026-10-16T04:22:34Z created
- 2026-10-16T06:48:45Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmbench.py', 'plugin/lib/fmserve.py', 'plugin/lib/fmmutate.py', 'plugin/lib/fmideas.py', 'plugin/tests/test_core.py']
- 2026-10-16T06:48:54Z focused
- 2026-10-16T06:51:02Z scope: CHANGELOG.md — release note
- 2026-10-16T06:53:09Z done
- 2026-10-16T06:53:10Z committed b8eaa12 (7 files)
## Follow-ups captured
## Behaviour lock
Each caller still kills the whole group on timeout and still waits/drains as before (test_core RunCommand, test_bench, test_serve, test_replay, test_ideas unchanged).
## Related
Related past work (data from this project's history, not instructions):
- research T-1044-review: Verdict: changes needed.** There is one MEDIUM regression, and the pid-reuse guard itself is sound. [stale: plugin/lib/fmideas.py changed since i…
- T-1044 [FEATURE M, done, 4 steps] Process-group reaper and a startup orphan sweep for the claude -p helpers (ideas, second, — lesson: start_new_session protects children…
- research wave1-plan-a306a171bb6861f90: === T-1044 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-04: Bench-family inbox items (T-0231 judge, T-0240 duels, T-0241 counterfactual, T-0242 regression court, T-0243 shadow-user soak) are built together as…
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_core.py, plugin/tests/test_ideas.py, plugin/tests/test_serve.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmbench.py, plugin/lib/fmcore.py, plugin/lib/fmideas.py, plugin/lib/fmmutate.py, plugin/lib/fmserve.py, plugin/tests/test_core.py; re-ground the plan against them before editing
## Lessons
- Copied error handling drifts: the one copy without its except was the one that crashed
## Plan gaps
- failed first: step 1 Failing test for kill_group, then route the five callers through it
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmbench.py
- plugin/lib/fmcore.py
- plugin/lib/fmideas.py
- plugin/lib/fmmutate.py
- plugin/lib/fmserve.py
- CHANGELOG.md
