---
id: T-0994
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-15T23:48:45Z
updated: 2026-10-16T00:01:01Z
base: 07bc6b65f566308e1e85e1b4a7dc3c79b27f06a2
base_tree: bef4722dec0cc876bf14dee35f60c82441d442de
verified: strong
---
# Ambient runs close only the step whose own verify ran; unmappable files get no ambient evidence (T-0994)
## Raw request
> Ambient tests (T-0705) mark the current step done with any passing affected run: on T-0989 it closed 'look at it live' and 'docs' steps, and its command for a .tsx edit was 'python3 plugin/tests/run.py foreman-ui.test test_ui', a runner that can't test the file; ambient evidence should only verify a step whose own verify it ran, and only map files the template can run
## Interpretation
Ambient tests (T-0705) run the affected tests after each edit. Two faults seen on T-0989: a passing run was recorded as the current step's evidence, which marks the step done, so steps closed mid-work ('look at it live', 'docs'); and the selection handed a Python runner a .tsx test it can't run, so the 'pass' tested nothing. Fix both where they start.
## Assumptions (confidence)
## Acceptance criteria
- [x] an ambient pass never marks a step done; the pass-again note names the fm task evidence line for the current step — verify with `python3 plugin/tests/run.py test_ambient`
- [x] affected tests a template's runner can't run (a .tsx test under a python runner) are left out of fm check --affected and ambient runs — verify with `python3 plugin/tests/run.py test_ambient`
## Non-goals
## Approach (options → choice → why)
Options: (1) drop ambient's auto-evidence and say in the pass-again note how to record it — chosen: a pass of affected tests mid-step says nothing about whether the step is done (it closed 'look at it live' and 'docs' on T-0989); (2) auto-evidence only for steps whose text names tests — still closes a test step mid-work; (3) keep it and let the model reopen steps — silent wrong state. Runner fit: filter the affected tests by the template's runner (python → .py; npm/bun/jest/vitest/node → js/ts; go → .go; cargo → .rs; unknown → no filter), in fmcli.affected so fm check --affected and ambient agree.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Reproduce on T-0989's state: a passing affected run closes a step whose verify did not run; write the failing test first
2. [x] Limit ambient evidence to the step's own verify command; drop unmappable file-to-command mappings
3. [x] Re-run fm check and confirm T-0989's closed steps are reopened, not silently passed
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ambient` → ✗ exit 1 · Ran 3 tests in 2.8s (1 classes, 16 at a time; slowest: Ambient 3s) / FAILED (1 classes) [ran] [tree ba840114cb5a] (2026-10-15T23:59:27Z)
- (step 2) `python3 plugin/tests/run.py test_ambient` → exit 0 · Ran 3 tests in 2.7s (1 classes, 16 at a time; slowest: Ambient 3s) / OK [ran] [tree 5f8d789c01ae] (2026-10-15T23:59:51Z)
- (step 3) `python3 plugin/tests/run.py test_ambient test_suite_hygiene test_cli test_diff_gates test_lanes` → exit 0 · Ran 138 tests in 23.4s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, DiffGates 12s, Lanes 10s) / OK [ran] [tree 119087f2f4c6] (2026-10-16T00:00:56Z)
- (ac 1) `python3 plugin/tests/run.py test_ambient` → exit 0 · Ran 3 tests in 2.8s (1 classes, 16 at a time; slowest: Ambient 3s) / OK [ran] [tree 119087f2f4c6] (2026-10-16T00:01:00Z)
- (ac 2) `python3 plugin/tests/run.py test_ambient` → exit 0 · Ran 3 tests in 2.8s (1 classes, 16 at a time; slowest: Ambient 3s) / OK [ran] [tree 119087f2f4c6] (2026-10-16T00:01:00Z)
- (audit intent) `self: read fmambient._record and fmcli.affected after the change; the auto-evidence block is gone (no other caller relied on it: grep), the pass note names the evidence line unless the step wants a red run; _runnable filters by runner words, unknown runners keep every test` → a pass of affected tests never closes a step; tests a runner can't run are not handed to it [tree 119087f2f4c6] (2026-10-16T00:01:00Z)
- (audit edge) `self: read fmambient._record and fmcli.affected after the change; the auto-evidence block is gone (no other caller relied on it: grep), the pass note names the evidence line unless the step wants a red run; _runnable filters by runner words, unknown runners keep every test` → a template naming run.py (python3 plugin/tests/run.py) keeps .py tests; 'claude plugin test' matches no runner and keeps all; a step whose text asks for a red run gets no evidence hint [tree 119087f2f4c6] (2026-10-16T00:01:00Z)
## Log
- 2026-10-15T23:48:45Z created
- 2026-10-15T23:49:09Z planned from capture
- 2026-10-15T23:59:15Z criterion 1 verify: `fm check` → `python3 plugin/tests/run.py test_ambient`
- 2026-10-15T23:59:15Z criterion 1 text: An affected ambient run does not mark a step done unless that step's own verify command ran → an ambient pass never marks a step done; the pass-again note names the fm task evidence line for the current step
- 2026-10-15T23:59:15Z criterion 2 verify: `fm check` → `python3 plugin/tests/run.py test_ambient`
- 2026-10-15T23:59:15Z criterion 2 text: A file the template's runner cannot test (e.g. .tsx under the foreman-ui runner) maps to no ambient command and records no evidence → affected tests a template's runner can't run (a .tsx test under a python runner) are left out of fm check --affected and ambient runs
- 2026-10-15T23:59:15Z focused
- 2026-10-16T00:01:00Z done
- 2026-10-16T00:01:01Z committed 650fbea (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0705 [FEATURE M, done, 4 steps] Frontier 05 — Ambient verification and test intelligence — lesson: Background verification has to answer the revert case: selection by …
- research T-0978-small-models: Measured, not guessed. Sources: two recorded Sonnet demo sessions (T-0979; T-0983/T-0984 were written by them), one
- T-0901 [SECURITY M, done, 4 steps] Commands fm stores and runs later bypass the guard: a verify command (--ac "x :: CMD", fm — lesson: A guard that reads commands must a…
- decision 2026-09-26: Order after T-0016: T-0022 and T-0023 (user requests, explore items: take the recommendation after self-critique in full autonomy), then T-0018's ro…
- similar finished tasks took 4–4 steps
## Why not caught
T-0705's fixture had one Python test and steps that were all code steps; ambient was off in every real project until today, and the first real use (a TypeScript mod) showed both faults
## Lessons
- Automatic evidence must prove the thing it's attached to: a pass of whatever tests an edit touched says nothing about whether a docs or review step is done.
## Plan gaps
- failed first: step 1 Reproduce on T-0989's state: a passing affected run closes a step whose verify did not run; write t…
## Files touched
- plugin/tests/test_ambient.py
- plugin/lib/fmambient.py
- plugin/lib/fmcli.py
- CHANGELOG.md
