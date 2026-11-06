---
id: T-2034
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T19:43:00Z
updated: 2026-10-29T19:56:52Z
base: 199dcc3b0ef7df42b0a4d3c0c2bdadffadf95537
base_tree: 052aa6d4c1426be98af845973f47980c798754c3
plan0_at: 2026-10-29T19:52:37Z
plan0_scope: []
verified: strong
---
# run.py's per-class unittest children (start_new_session) outlive a killed run: a…
## Raw request
> run.py's per-class unittest children (start_new_session) outlive a killed run: a test_shade child spun a CPU core for 24 h as an orphan; kill them when run.py dies (pdeathsig / signal handler), and find what in test_shade can loop forever
## Interpretation
run.py starts each test class in its own session (so a timeout can killpg its children). When run.py itself is killed (a Bash tool timeout, TaskStop), nothing kills those classes. On 2026-10-28 a test_shade class started during T-1846's red phase (a shader loop with no step cap yet) was orphaned and spun a CPU core for 24 h, skewing later timing runs. The current fmshade has the cap, so the hang is gone; the orphaning isn't.
## Assumptions (confidence)
## Acceptance criteria
- [x] A class still running when run.py is SIGKILLed dies within seconds — verify with `python3 plugin/tests/run.py test_run -k orphan`
## Non-goals
## Approach (options → choice → why)
Options: (1) signal handlers in run.py that killpg live children - misses SIGKILL; (2) preexec_fn prctl - unsafe with run.py's thread pool; (3) start each class through a tiny -c bootstrap that sets PR_SET_PDEATHSIG=SIGKILL via ctypes, exits if run.py is already gone, then runs unittest.main like -m unittest - chosen: covers SIGKILL, no fork-time code, no-op off Linux.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: SIGKILL a process running run_one; its class process must die
2. [x] Start classes through a pdeathsig bootstrap
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_run -k orphaning` → ✗ exit 1 · Ran 1 tests in 5.6s (1 classes, 16 at a time; slowest: Hang 5s) / FAILED (1 classes) [ran] [tree 7ee78c7b8c9a] (2026-10-29T19:52:58Z)
- `python3 plugin/tests/run.py test_run -k orphaning` → ✗ exit 1 · Ran 1 tests in 6.2s (1 classes, 16 at a time; slowest: Hang 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 85c48479d346] (2026-10-29T19:53:32Z)
- `python3 plugin/tests/run.py test_run -k orphaning` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Hang 0s) / OK [ran] [tree 85c48479d346] (2026-10-29T19:53:32Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (50 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 19:51 UTC; claude plugin test mods/foreman-ui → [ran] [tree 85c48479d346] (2026-10-29T19:56:32Z)
- (ac 1) `python3 plugin/tests/run.py test_run -k orphan` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Hang 0s) / OK [ran] [tree 85c48479d346] (2026-10-29T19:56:44Z)
- (audit intent) `self-review of the diff: classes start through a -c bootstrap equal to -m unittest after a pdeathsig prctl; own session and the killpg on timeout kept` → a class dies with run.py even when run.py is SIGKILLed (tested by SIGKILLing a process mid run_one) [tree 85c48479d346] (2026-10-29T19:56:44Z)
- (audit edge) `self-review of the diff: classes start through a -c bootstrap equal to -m unittest after a pdeathsig prctl; own session and the killpg on timeout kept` → pdeathsig tracks the forking thread, and the pool thread blocks in communicate until the class ends; run.py dying between fork and prctl is caught by the getppid check; off Linux the prctl raises and is skipped; faulthandler's SIGABRT stack on timeout still works (Hang test green); suite time 156-159 s before and after [tree 85c48479d346] (2026-10-29T19:56:44Z)
- (audit self) `self-review of the diff: classes start through a -c bootstrap equal to -m unittest after a pdeathsig prctl; own session and the killpg on timeout kept` → no findings [tree 85c48479d346] (2026-10-29T19:56:44Z)
## Log
- 2026-10-29T19:43:00Z created
- 2026-10-29T19:45:17Z set type=FIX, tier=S
- 2026-10-29T19:45:17Z planned: it has criteria and steps
- 2026-10-29T19:52:37Z focused
- 2026-10-29T19:56:51Z done
- 2026-10-29T19:56:52Z committed 84c44ebd (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1809 [FIX M, done, 4 steps] CI's macOS job names what makes it time out: run.py --deadline stops below each job's cap, killing and naming running classes; slowest clas…
- research T-1044-review: Verdict: changes needed.** There is one MEDIUM regression, and the pid-reuse guard itself is sound. [stale: plugin/lib/fmideas.py changed since i…
- research T-1846-review: Verdict: changes needed.** The adversary question you asked has a clean answer. The resource-exhaustion and error-handling findings below are rea…
- decision 2026-09-26: T-0014 fm run: minimal one-shot worker (fresh claude -p per task, drive scoped to that task via FOREMAN_DRIVE_TASK, per-task timeout, stop on no pro…
## Lessons
- Children started in their own session (for killpg) need a death signal too, or a killed parent leaves them running forever
## Plan gaps
- failed first: step 1 Red test: SIGKILL a process running run_one; its class process must die
## Files touched
- plugin/tests/test_run.py
- plugin/tests/run.py
- CHANGELOG.md
